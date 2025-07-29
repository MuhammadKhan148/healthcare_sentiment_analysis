import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer  # For recomputing vectorization

# Load the trained model and vectorizer
nb_model = joblib.load('sentiment_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Recompute the test data for consistency (matches training)
df = pd.read_csv('healthcare_reviews_processed.csv')
sentiment_mapping = {'positive': 1, 'negative': 0, 'neutral': 2}
df['label'] = df['sentiment'].map(sentiment_mapping)
X = df['processed_review']
y = df['label']

# Resplit to get the exact same test set (using same random_state)
_, X_test, _, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, 
    stratify=y
)

# Revectorize the test set
X_test_tfidf = vectorizer.transform(X_test)

# Predict on the test set
y_pred = nb_model.predict(X_test_tfidf)
y_pred_proba = nb_model.predict_proba(X_test_tfidf)  # Optional, if you need probabilities

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.4f}")

# Classification report
target_names = ['Negative', 'Positive', 'Neutral']
class_report = classification_report(y_test, y_pred, target_names=target_names, digits=4)
print("\nClassification Report:\n", class_report)

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

plt.title('Confusion Matrix - Healthcare Reviews Sentiment Analysis', 
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
plt.show()  # This will display the plot; save it with plt.savefig('confusion_matrix.png') if needed

# Optional: Precision, Recall, F1 per class
from sklearn.metrics import precision_recall_fscore_support
precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred, average=None)
print("\nPer-Class Metrics:")
for i, name in enumerate(target_names):
    print(f"{name}: Precision={precision[i]:.4f}, Recall={recall[i]:.4f}, F1={f1[i]:.4f}, Support={support[i]}")