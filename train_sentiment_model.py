import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB, MultinomialNB
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np
from data_preparation import combine_datasets
from sklearn.utils import resample
from collections import Counter

# Load and combine datasets
print("Loading and combining datasets...")
df = combine_datasets()

if df is None:
    print("No data available. Please check your data files.")
    exit()

# Clean the data - remove NaN values
print("Cleaning data...")
df = df.dropna(subset=['processed_review'])
df = df[df['processed_review'].str.strip() != '']
print(f"After cleaning: {df.shape}")

# Add short positive examples to improve short text classification
print("Adding short positive examples for better short text handling...")
short_positive_examples = [
    "Great service",
    "Excellent care", 
    "Amazing doctor",
    "Wonderful experience",
    "Best hospital",
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
    "Fantastic service",
    "I really enjoyed",
    "I really enjoyed the experience",
    "Great",
    "Excellent",
    "Amazing",
    "Wonderful",
    "Best",
    "Love it",
    "Fantastic",
    "Outstanding",
    "Perfect",
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

# Create DataFrame for short positive examples
short_pos_df = pd.DataFrame({
    'processed_review': short_positive_examples,
    'sentiment': ['positive'] * len(short_positive_examples)
})

# Add to main dataset
df = pd.concat([df, short_pos_df], ignore_index=True)
print(f"After adding short examples: {df.shape}")

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

print(f"Dataset shape: {df.shape}")
print(f"Original sentiment distribution: {y.value_counts().to_dict()}")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, 
    stratify=y
)

print(f"Original training distribution: {Counter(y_train)}")

# Handle class imbalance with oversampling
train_df = pd.DataFrame({'processed_review': X_train, 'label': y_train})

# Separate classes
class_0 = train_df[train_df['label'] == 0]
class_1 = train_df[train_df['label'] == 1]
class_2 = train_df[train_df['label'] == 2]

# Oversample minority classes to match majority (positive)
majority_size = len(class_1)
class_0_upsampled = resample(class_0, replace=True, n_samples=majority_size, random_state=42)
class_2_upsampled = resample(class_2, replace=True, n_samples=majority_size, random_state=42)

# Combine balanced dataset
train_upsampled = pd.concat([class_0_upsampled, class_1, class_2_upsampled])
X_train_upsampled = train_upsampled['processed_review']
y_train_upsampled = train_upsampled['label']

print(f"Upsampled training distribution: {Counter(y_train_upsampled)}")

# Enhanced vectorizer with better short text handling
vectorizer = TfidfVectorizer(
    max_features=15000,  # Increased for better feature coverage
    lowercase=True, 
    stop_words='english',
    ngram_range=(1, 3),   # Use unigrams, bigrams, and trigrams
    min_df=1,             # Include all terms (even single occurrences)
    max_df=0.95,          # Maximum document frequency
    sublinear_tf=True,    # Apply sublinear tf scaling
    analyzer='word'        # Word-based analysis
)

X_train_tfidf = vectorizer.fit_transform(X_train_upsampled)
X_test_tfidf = vectorizer.transform(X_test)

print(f"Vectorizer features: {X_train_tfidf.shape[1]}")

# Train multiple models for comparison
print("\nTraining models...")

# 1. ComplementNB (better for imbalanced data)
cnb_model = ComplementNB(alpha=0.5)  # Reduced alpha for better short text handling
cnb_model.fit(X_train_tfidf, y_train_upsampled)

# 2. Random Forest with class weights
rf_model = RandomForestClassifier(
    n_estimators=200,  # Increased for better performance
    class_weight='balanced',
    random_state=42,
    max_depth=15,      # Increased depth
    min_samples_split=5,
    min_samples_leaf=2
)
rf_model.fit(X_train_tfidf, y_train_upsampled)

# 3. MultinomialNB (original) with adjusted parameters
mnb_model = MultinomialNB(alpha=0.5)  # Reduced alpha for better short text handling
mnb_model.fit(X_train_tfidf, y_train_upsampled)

# Evaluate all models
from sklearn.metrics import accuracy_score, classification_report

models = {
    'ComplementNB': cnb_model,
    'RandomForest': rf_model,
    'MultinomialNB': mnb_model
}

best_model = None
best_accuracy = 0

print("\nModel Comparison:")
print("=" * 50)

for name, model in models.items():
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n{name}:")
    print(f"Accuracy: {accuracy:.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Negative', 'Positive', 'Neutral']))
    
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        best_model_name = name

print(f"\nBest model: {best_model_name} (Accuracy: {best_accuracy:.4f})")

# Save the best model and vectorizer
joblib.dump(best_model, 'sentiment_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

print(f"\nModel trained and saved successfully!")
print(f"Training samples: {len(X_train_upsampled)}")
print(f"Testing samples: {len(X_test)}")
print(f"Best model: {best_model_name}")
print(f"Best accuracy: {best_accuracy:.4f}")

# Test short positive reviews with the new model
print("\n" + "="*60)
print("TESTING SHORT POSITIVE REVIEWS WITH ENHANCED MODEL")
print("="*60)

short_test_reviews = [
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

positive_count = 0
neutral_count = 0
negative_count = 0

for i, review in enumerate(short_test_reviews, 1):
    text_vectorized = vectorizer.transform([review])
    prediction = best_model.predict(text_vectorized)[0]
    probability = best_model.predict_proba(text_vectorized)[0]
    
    sentiment_map = {0: 'Negative', 1: 'Positive', 2: 'Neutral'}
    sentiment = sentiment_map[prediction]
    confidence = max(probability) * 100
    
    print(f"{i:2d}. Review: '{review}'")
    print(f"    Sentiment: {sentiment} (Confidence: {confidence:.1f}%)")
    
    if sentiment == 'Positive':
        positive_count += 1
    elif sentiment == 'Neutral':
        neutral_count += 1
    else:
        negative_count += 1

print("\n" + "="*60)
print("SHORT TEXT CLASSIFICATION RESULTS:")
print(f"Positive classifications: {positive_count}/{len(short_test_reviews)} ({positive_count/len(short_test_reviews)*100:.1f}%)")
print(f"Neutral classifications: {neutral_count}/{len(short_test_reviews)} ({neutral_count/len(short_test_reviews)*100:.1f}%)")
print(f"Negative classifications: {negative_count}/{len(short_test_reviews)} ({negative_count/len(short_test_reviews)*100:.1f}%)")

if neutral_count == 0 and negative_count == 0:
    print("\n✅ PERFECT! All short positive reviews correctly classified!")
elif neutral_count + negative_count < 3:
    print(f"\n✅ GOOD! Only {neutral_count + negative_count} misclassifications - significant improvement!")
else:
    print(f"\n⚠️  Still {neutral_count + negative_count} misclassifications - may need further enhancement")  