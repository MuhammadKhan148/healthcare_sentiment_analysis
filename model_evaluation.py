import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB

# Assumes y_test, X_test_tfidf from data_preparation.py

nb_model = joblib.load('sentiment_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

y_pred = nb_model.predict(X_test_tfidf)
y_pred_proba = nb_model.predict_proba(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)

target_names = ['Negative', 'Positive', 'Neutral']
class_report = classification_report(y_test, y_pred, target_names=target_names, digits=4)

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=['Negative', 'Positive', 'Neutral'],
            yticklabels=['Negative', 'Positive', 'Neutral'],
            cbar_kws={'label': 'Count'})

plt.title('Confusion Matrix - Healthcare Reviews Sentiment Analysis', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Predicted Sentiment', fontsize=14, fontweight='bold')
plt.ylabel('True Sentiment', fontsize=14, fontweight='bold')

total_samples = np.sum(cm)
for i in range(len(cm)):
    for j in range(len(cm[i])):
        percentage = (cm[i][j] / total_samples) * 100
        plt.text(j + 0.5, i + 0.7, f'({percentage:.1f}%)', 
                ha='center', va='center', fontsize=10, color='red')

plt.tight_layout()
plt.show()

from sklearn.metrics import precision_recall_fscore_support

precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred, average=None)

param_grid = {
    'alpha': [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
}

grid_search = GridSearchCV(
    MultinomialNB(), 
    param_grid, 
    cv=5, 
    scoring='accuracy',
    n_jobs=-1
)

grid_search.fit(X_train_tfidf, y_train)

best_model = grid_search.best_estimator_
y_pred_optimized = best_model.predict(X_test_tfidf)
optimized_accuracy = accuracy_score(y_test, y_pred_optimized)

if optimized_accuracy > accuracy:
    joblib.dump(best_model, 'sentiment_model_optimized.pkl')