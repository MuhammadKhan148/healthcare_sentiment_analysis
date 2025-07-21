from sklearn.naive_bayes import MultinomialNB
import joblib
import numpy as np

# Assumes X_train_tfidf, X_test_tfidf, y_train from data_preparation.py

nb_model = MultinomialNB(alpha=1.0)

nb_model.fit(X_train_tfidf, y_train)

joblib.dump(nb_model, 'sentiment_model.pkl')

joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

test_reviews = [
    "The doctor was very caring and the treatment was excellent. Highly recommend!",
    "Terrible experience. Long wait times and rude staff. Very disappointed.",
    "The hospital was clean and well-organized. Average service overall.",
    "Outstanding medical care! The nurses were professional and kind.",
    "Not satisfied with the consultation. Doctor seemed rushed and inattentive."
]

test_reviews_vec = vectorizer.transform(test_reviews)

predictions = nb_model.predict(test_reviews_vec)
prediction_probabilities = nb_model.predict_proba(test_reviews_vec)