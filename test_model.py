import joblib
import pandas as pd

def load_model():
    """Load the trained model and vectorizer"""
    try:
        model = joblib.load('sentiment_model.pkl')
        vectorizer = joblib.load('tfidf_vectorizer.pkl')
        return model, vectorizer
    except FileNotFoundError:
        print("Model files not found. Please run train_sentiment_model.py first.")
        return None, None

def predict_sentiment(text, model, vectorizer):
    """Predict sentiment for a single text"""
    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)[0]
    probability = model.predict_proba(text_vectorized)[0]
    sentiment_map = {0: 'Negative', 1: 'Positive', 2: 'Neutral'}
    sentiment = sentiment_map[prediction]
    confidence = max(probability) * 100
    return sentiment, confidence

def main():
    print("Loading model...")
    model, vectorizer = load_model()
    if model is None: return
    print("Model loaded successfully!")
    print("\n" + "="*50)
    print("HEALTHCARE SENTIMENT ANALYSIS")
    print("="*50)
    
    # Test regular reviews
    test_reviews = [
        "The doctor was very professional and caring. Great experience!",
        "Terrible service, long wait times and rude staff.",
        "The hospital was clean and the nurses were helpful.",
        "I had to wait for hours and the treatment was ineffective.",
        "The medical staff was knowledgeable and the facility was modern."
    ]
    
    print("\nTesting regular reviews:")
    print("-" * 50)
    for i, review in enumerate(test_reviews, 1):
        sentiment, confidence = predict_sentiment(review, model, vectorizer)
        print(f"{i}. Review: {review}")
        print(f"   Sentiment: {sentiment} (Confidence: {confidence:.1f}%)")
        print()
    
    # Test short positive reviews (the problematic ones)
    short_positive_reviews = [
        "I really enjoyed",
        "I really enjoyed the experience",
        "Great service",
        "Excellent care",
        "Amazing doctor",
        "Wonderful experience",
        "Best hospital ever",
        "Love this place",
        "Fantastic treatment",
        "Outstanding care",
        "Perfect experience",
        "Highly recommend",
        "Very satisfied",
        "Great experience",
        "Excellent service",
        "Amazing staff",
        "Wonderful care",
        "Best experience",
        "Love the staff",
        "Fantastic service"
    ]
    
    print("\nTesting short positive reviews (previously problematic):")
    print("-" * 50)
    
    positive_count = 0
    neutral_count = 0
    negative_count = 0
    
    for i, review in enumerate(short_positive_reviews, 1):
        sentiment, confidence = predict_sentiment(review, model, vectorizer)
        print(f"{i:2d}. Review: '{review}'")
        print(f"    Sentiment: {sentiment} (Confidence: {confidence:.1f}%)")
        
        if sentiment == 'Positive':
            positive_count += 1
        elif sentiment == 'Neutral':
            neutral_count += 1
        else:
            negative_count += 1
    
    print("\n" + "="*50)
    print("SHORT POSITIVE REVIEWS SUMMARY:")
    print(f"✅ Correctly classified as Positive: {positive_count}/{len(short_positive_reviews)} ({positive_count/len(short_positive_reviews)*100:.1f}%)")
    print(f"⚠️  Misclassified as Neutral: {neutral_count}/{len(short_positive_reviews)} ({neutral_count/len(short_positive_reviews)*100:.1f}%)")
    print(f"❌ Misclassified as Negative: {negative_count}/{len(short_positive_reviews)} ({negative_count/len(short_positive_reviews)*100:.1f}%)")
    
    if neutral_count == 0 and negative_count == 0:
        print("\n🎉 PERFECT! All short positive reviews correctly classified!")
    elif neutral_count + negative_count <= 2:
        print(f"\n✅ EXCELLENT! Only {neutral_count + negative_count} misclassifications - major improvement!")
    elif neutral_count + negative_count <= 5:
        print(f"\n👍 GOOD! {neutral_count + negative_count} misclassifications - significant improvement!")
    else:
        print(f"\n⚠️  Still {neutral_count + negative_count} misclassifications - needs more work")
    
    print("\n" + "="*50)
    print("You can now use this enhanced model for your sentiment analysis!")

if __name__ == "__main__":
    main() 