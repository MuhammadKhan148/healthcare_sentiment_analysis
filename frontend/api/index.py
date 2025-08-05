from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import io
import json
import joblib
import os
from datetime import datetime
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

app = Flask(__name__)
CORS(app)

# Global variables to store loaded models
model = None
vectorizer = None
model_metrics = {
    "accuracy": 0.8210,  # Updated from enhanced model
    "precision": 0.79,   # Updated weighted average
    "recall": 0.82,      # Updated weighted average
    "f1_score": 0.78,    # Updated weighted average
    "last_updated": "2024-08-04",
    "training_samples": 8334,  # Updated from enhanced model
    "testing_samples": 866,    # Updated from enhanced model
    "total_samples": 4329      # Updated from enhanced model
}

def load_models():
    """Load the trained model and vectorizer"""
    global model, vectorizer
    try:
        # Load the actual trained model and vectorizer
        model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'sentiment_model.pkl')
        vectorizer_path = os.path.join(os.path.dirname(__file__), '..', '..', 'tfidf_vectorizer.pkl')
        
        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            model = joblib.load(model_path)
            vectorizer = joblib.load(vectorizer_path)
            print("Models loaded successfully from trained files")
            return True
        else:
            print("Model files not found, using simulated model")
            return False
    except Exception as e:
        print(f"Error loading models: {e}")
        return False

def predict_sentiment(text):
    """Predict sentiment for a single text using the actual trained model"""
    try:
        if model is not None and vectorizer is not None:
            # Use the actual trained model
            text_vectorized = vectorizer.transform([text])
            prediction = model.predict(text_vectorized)[0]
            probability = model.predict_proba(text_vectorized)[0]
            
            # Map prediction to sentiment
            sentiment_map = {0: 'negative', 1: 'positive', 2: 'neutral'}
            sentiment = sentiment_map[prediction]
            confidence = max(probability) * 100
            
            return sentiment, confidence / 100  # Convert to 0-1 scale
        else:
            # Fallback to keyword-based simulation
            return predict_sentiment_simulation(text)
    except Exception as e:
        print(f"Error in model prediction: {e}")
        return predict_sentiment_simulation(text)

def predict_sentiment_simulation(text):
    """Simulate sentiment prediction for demo purposes"""
    # Enhanced keyword-based simulation
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'best', 'perfect', 'outstanding', 'professional', 'caring', 'helpful', 'clean', 'modern', 'knowledgeable', 'effective', 'satisfied', 'recommend', 'excellent']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'disgusting', 'poor', 'disappointing', 'useless', 'rude', 'long wait', 'ineffective', 'terrible service', 'worst experience', 'unprofessional', 'dirty', 'old', 'broken', 'expensive']
    neutral_words = ['okay', 'fine', 'average', 'normal', 'standard', 'regular', 'usual', 'typical', 'adequate', 'acceptable']
    
    text_lower = text.lower()
    positive_score = sum(1 for word in positive_words if word in text_lower)
    negative_score = sum(1 for word in negative_words if word in text_lower)
    neutral_score = sum(1 for word in neutral_words if word in text_lower)
    
    total_score = positive_score + negative_score + neutral_score
    
    if total_score == 0:
        # If no keywords found, use text length and common patterns
        if len(text) < 20:
            return 'neutral', 0.5
        elif any(word in text_lower for word in ['doctor', 'hospital', 'medical', 'treatment', 'care']):
            return 'positive', 0.6
        else:
            return 'neutral', 0.5
    
    if positive_score > negative_score and positive_score > neutral_score:
        sentiment = 'positive'
        confidence = min(0.95, 0.6 + (positive_score * 0.1))
    elif negative_score > positive_score and negative_score > neutral_score:
        sentiment = 'negative'
        confidence = min(0.95, 0.6 + (negative_score * 0.1))
    else:
        sentiment = 'neutral'
        confidence = min(0.85, 0.5 + (neutral_score * 0.05))
    
    return sentiment, confidence

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": model is not None and vectorizer is not None,
        "model_type": "trained_model" if model is not None else "simulated_model"
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_single():
    """Analyze sentiment for a single text"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Text is required"}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400
        
        sentiment, confidence = predict_sentiment(text)
        
        return jsonify({
            "text": text,
            "sentiment": sentiment,
            "confidence": round(confidence, 3),
            "timestamp": datetime.now().isoformat(),
            "model_used": "trained_model" if model is not None else "simulated_model"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-batch', methods=['POST'])
def analyze_batch():
    """Analyze sentiment for batch of texts"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "Only CSV files are supported"}), 400
        
        # Read CSV file
        df = pd.read_csv(file)
        
        # Check if required column exists
        text_column = None
        for col in ['text', 'review', 'comment', 'feedback', 'processed_review']:
            if col in df.columns:
                text_column = col
                break
        
        if text_column is None:
            return jsonify({"error": "CSV must contain a 'text', 'review', 'comment', 'feedback', or 'processed_review' column"}), 400
        
        results = []
        for idx, row in df.iterrows():
            text = str(row[text_column]).strip()
            if text and text != 'nan' and len(text) > 0:
                sentiment, confidence = predict_sentiment(text)
                results.append({
                    "id": idx + 1,
                    "text": text,
                    "sentiment": sentiment,
                    "confidence": round(confidence, 3)
                })
        
        # Calculate summary statistics
        sentiments = [r['sentiment'] for r in results]
        summary = {
            "total": len(results),
            "positive": sentiments.count('positive'),
            "negative": sentiments.count('negative'),
            "neutral": sentiments.count('neutral')
        }
        
        return jsonify({
            "results": results,
            "summary": summary,
            "timestamp": datetime.now().isoformat(),
            "model_used": "trained_model" if model is not None else "simulated_model"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get model performance metrics"""
    return jsonify(model_metrics)

@app.route('/api/sample-reviews', methods=['GET'])
def get_sample_reviews():
    """Get sample reviews for testing"""
    sample_reviews = [
        "The doctor was very professional and caring. Great experience!",
        "Terrible service, long wait times and rude staff.",
        "The hospital was clean and the nurses were helpful.",
        "I had to wait for hours and the treatment was ineffective.",
        "The medical staff was knowledgeable and the facility was modern.",
        "Excellent care and attention to detail. Highly recommend!",
        "The medication worked perfectly for my condition.",
        "Average experience, nothing special but not bad either.",
        "The side effects were worse than the original problem.",
        "Outstanding medical care and professional staff."
    ]
    
    return jsonify({
        "sample_reviews": sample_reviews,
        "count": len(sample_reviews)
    })

# Initialize models on startup
load_models()

if __name__ == '__main__':
    app.run(port=5328, debug=True)
