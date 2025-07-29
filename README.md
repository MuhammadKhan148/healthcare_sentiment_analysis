# Healthcare Sentiment Analysis

A simple sentiment analysis model for healthcare reviews using NLP and machine learning.

## What it does
- Analyzes healthcare reviews and classifies them as positive, negative, or neutral
- Uses TF-IDF features and Naive Bayes classifier
- Includes data preprocessing and model evaluation

## Quick start
```bash
pip install -r requirements.txt
python train_sentiment_model.py
```

## Files
- `train_sentiment_model.py` - Main training script
- `model_evaluation.py` - Evaluate model performance  
- `data_generation.py` - Generate sample data
- `text_preprocessing.py` - Clean and process text
- `data_preparation.py` - Prepare data for training

## Model
- Algorithm: Multinomial Naive Bayes
- Features: TF-IDF vectorization
- Classes: Positive (1), Negative (0), Neutral (2)

The trained model and vectorizer are saved as `.pkl` files for reuse. 