import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import numpy as np

# Load the processed data (ensure 'healthcare_reviews_processed.csv' exists in the same directory)
df = pd.read_csv('healthcare_reviews_processed.csv')

# Map sentiments to labels
sentiment_mapping = {
    'positive': 1,
    'negative': 0,
    'neutral': 2
}
df['label'] = df['sentiment'].map(sentiment_mapping)

# Prepare features and labels
X = df['processed_review']
y = df['label']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, 
    stratify=y
)

# Vectorize
vectorizer = TfidfVectorizer(
    max_features=5000, 
    lowercase=True, 
    stop_words=None
)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train the model
nb_model = MultinomialNB(alpha=1.0)
nb_model.fit(X_train_tfidf, y_train)

# Save the model and vectorizer
joblib.dump(nb_model, 'sentiment_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

print("Model trained and saved successfully!")  # Optional: Confirmation message