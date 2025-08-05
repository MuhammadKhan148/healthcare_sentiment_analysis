# Healthcare Sentiment Analysis

A sentiment analysis model for healthcare and drug reviews using NLP and machine learning with a full-stack web application.

## What it does
- Analyzes healthcare and drug reviews and classifies them as positive, negative, or neutral
- Uses TF-IDF features and Naive Bayes classifier
- Combines multiple datasets for better training
- Includes data preprocessing and model evaluation
- Full-stack web application with React frontend and Flask API

## Project Structure
```
healthcare_sentiment_analysis/
├── sentiment_model.pkl              # Trained model
├── tfidf_vectorizer.pkl            # TF-IDF vectorizer
├── combined_healthcare_reviews.csv # Combined dataset
├── train_sentiment_model.py        # Model training script
├── data_preparation.py             # Data loading and preprocessing
├── model_evaluation.py             # Model performance evaluation
├── test_model.py                   # Model testing script
├── frontend/                       # React Next.js frontend
│   ├── app/                       # Next.js app directory
│   ├── components/                 # React components
│   └── api/                       # Flask API backend
└── requirements.txt                # Python dependencies
```

## Quick Setup

### Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Train the model (if not already trained)
python train_sentiment_model.py

# Start the Flask API
cd frontend/api
python index.py
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

## API Endpoints

### Health Check
- **GET** `/api/health` - Check API status and model loading

### Single Analysis
- **POST** `/api/analyze` - Analyze single text review
- **Body**: `{"text": "your review text"}`

### Batch Analysis
- **POST** `/api/analyze-batch` - Analyze CSV file with reviews
- **File**: CSV with 'text', 'review', 'comment', or 'feedback' column

### Model Metrics
- **GET** `/api/metrics` - Get model performance metrics

### Sample Reviews
- **GET** `/api/sample-reviews` - Get sample reviews for testing

## Model Details
- **Algorithm**: Multinomial Naive Bayes
- **Features**: TF-IDF vectorization
- **Classes**: Positive (1), Negative (0), Neutral (2)
- **Datasets**: Healthcare reviews + Drug reviews from UCI
- **Training Samples**: 3,432
- **Testing Samples**: 859
- **Accuracy**: 69.70%

## Usage Examples

### Single Review Analysis
```bash
curl -X POST http://localhost:5328/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "The doctor was very professional and caring. Great experience!"}'
```

### Batch Analysis
Upload a CSV file with reviews to analyze multiple reviews at once.

## Development

### Backend Development
- **API Server**: Flask with CORS enabled
- **Model**: Trained sentiment analysis model
- **Port**: 5328 (default)

### Frontend Development
- **Framework**: Next.js 15 with React 19
- **Styling**: Tailwind CSS with shadcn/ui components
- **Port**: 3000 (default)

## Files
- `train_sentiment_model.py` - Main training script
- `model_evaluation.py` - Evaluate model performance  
- `data_generation.py` - Generate sample data
- `data_preparation.py` - Load and combine datasets
- `text_preprocessing.py` - Clean and process text
- `frontend/api/index.py` - Flask API backend
- `frontend/app/page.tsx` - Main React page

