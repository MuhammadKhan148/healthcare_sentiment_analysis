import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the trained model and vectorizer
try:
    nb_model = joblib.load('sentiment_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    print("✅ Model and vectorizer loaded successfully")
except FileNotFoundError:
    print("❌ Model files not found. Please run train_sentiment_model.py first.")
    exit()

# Load the combined dataset for comprehensive evaluation
try:
    df = pd.read_csv('combined_healthcare_reviews.csv')
    print(f"✅ Loaded combined dataset: {df.shape}")
except FileNotFoundError:
    print("❌ Combined dataset not found. Using healthcare reviews only.")
    df = pd.read_csv('healthcare_reviews_processed.csv')

# Map sentiments to labels
sentiment_mapping = {'positive': 1, 'negative': 0, 'neutral': 2}
df['label'] = df['sentiment'].map(sentiment_mapping)

# Clean the data
df = df.dropna(subset=['processed_review'])
df = df[df['processed_review'].str.strip() != '']

X = df['processed_review']
y = df['label']

print(f"Dataset shape: {df.shape}")
print(f"Sentiment distribution: {y.value_counts().to_dict()}")

# Resplit to get the exact same test set (using same random_state)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, 
    stratify=y
)

# Revectorize the test set
X_test_tfidf = vectorizer.transform(X_test)

# Predict on the test set
y_pred = nb_model.predict(X_test_tfidf)
y_pred_proba = nb_model.predict_proba(X_test_tfidf)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\n📊 Test Accuracy: {accuracy:.4f}")

# Classification report
target_names = ['Negative', 'Positive', 'Neutral']
class_report = classification_report(y_test, y_pred, target_names=target_names, digits=4)
print(f"\n📋 Classification Report:\n{class_report}")

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=target_names,
            yticklabels=target_names,
            cbar_kws={'label': 'Count'})

plt.title('Confusion Matrix - Healthcare Sentiment Analysis', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Predicted Sentiment', fontsize=14, fontweight='bold')
plt.ylabel('True Sentiment', fontsize=14, fontweight='bold')

# Add percentages to cells
total_samples = np.sum(cm)
for i in range(len(cm)):
    for j in range(len(cm[i])):
        percentage = (cm[i][j] / total_samples) * 100
        plt.text(j + 0.5, i + 0.7, f'({percentage:.1f}%)', 
                 ha='center', va='center', fontsize=10, color='red')

plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
print("📈 Confusion matrix saved as 'confusion_matrix.png'")

# Per-class metrics
from sklearn.metrics import precision_recall_fscore_support
precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred, average=None)
print(f"\n📊 Per-Class Metrics:")
for i, name in enumerate(target_names):
    print(f"{name}: Precision={precision[i]:.4f}, Recall={recall[i]:.4f}, F1={f1[i]:.4f}, Support={support[i]}")

# Model information
print(f"\n🔍 Model Information:")
print(f"Model type: {type(nb_model).__name__}")
print(f"Vectorizer features: {X_test_tfidf.shape[1]}")
print(f"Test samples: {len(X_test)}")
print(f"Training samples: {len(X_train)}")

# Sample predictions with confidence
print(f"\n🧪 Sample Predictions:")
sample_texts = [
    "The doctor was very professional and caring. Great experience!",
    "Terrible service, long wait times and rude staff.",
    "The hospital was clean and the nurses were helpful.",
    "I had to wait for hours and the treatment was ineffective.",
    "The medical staff was knowledgeable and the facility was modern."
]

for i, text in enumerate(sample_texts, 1):
    # Preprocess the text (simplified)
    text_lower = text.lower()
    text_clean = ' '.join([word for word in text_lower.split() if len(word) > 2])
    
    # Vectorize and predict
    text_vectorized = vectorizer.transform([text_clean])
    prediction = nb_model.predict(text_vectorized)[0]
    probability = nb_model.predict_proba(text_vectorized)[0]
    
    # Map prediction to sentiment
    sentiment_map = {0: 'Negative', 1: 'Positive', 2: 'Neutral'}
    sentiment = sentiment_map[prediction]
    confidence = max(probability) * 100
    
    print(f"{i}. Text: {text}")
    print(f"   Prediction: {sentiment} (Confidence: {confidence:.1f}%)")
    print()