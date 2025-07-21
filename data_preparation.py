import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv('healthcare_reviews_processed.csv')

sentiment_mapping = {
    'positive': 1,
    'negative': 0,
    'neutral': 2
}

df['label'] = df['sentiment'].map(sentiment_mapping)

X = df['processed_review']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, 
    stratify=y
)

vectorizer = TfidfVectorizer(
    max_features=5000, 
    lowercase=True, 
    stop_words=None
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)