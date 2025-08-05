import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    print("NLTK downloads failed, using basic preprocessing")

# Load the data
df = pd.read_csv('healthcare_reviews.csv')

# Initialize NLTK components
try:
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
except:
    # Fallback to basic stop words if NLTK fails
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his', 'hers', 'ours', 'theirs'}
    lemmatizer = None
    stemmer = None

def preprocess_text(text):
    """Enhanced text preprocessing with NLTK"""
    if pd.isna(text) or not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and numbers, keep only letters and spaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize
    try:
        tokens = word_tokenize(text)
    except:
        # Fallback to simple split
        tokens = text.split()
    
    # Remove stop words and short tokens
    tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
    
    # Lemmatization (better than stemming for meaning preservation)
    if lemmatizer:
        lemmatized = []
        for token in tokens:
            # Get part of speech for better lemmatization
            try:
                pos = nltk.pos_tag([token])[0][1]
                if pos.startswith('V'):  # Verb
                    lemma = lemmatizer.lemmatize(token, pos='v')
                elif pos.startswith('N'):  # Noun
                    lemma = lemmatizer.lemmatize(token, pos='n')
                elif pos.startswith('J'):  # Adjective
                    lemma = lemmatizer.lemmatize(token, pos='a')
                elif pos.startswith('R'):  # Adverb
                    lemma = lemmatizer.lemmatize(token, pos='r')
                else:
                    lemma = lemmatizer.lemmatize(token)
                lemmatized.append(lemma)
            except:
                lemmatized.append(token)
        tokens = lemmatized
    
    # Join tokens back into text
    processed_text = ' '.join(tokens)
    
    return processed_text

# Apply preprocessing to all reviews
print("Preprocessing reviews...")
df['processed_review'] = df['review'].apply(preprocess_text)

# Remove empty processed reviews
df = df[df['processed_review'].str.strip() != ''].reset_index(drop=True)

print(f"Original reviews: {len(df)}")
print(f"After preprocessing: {len(df)}")

# Save the processed data
final_df = df[['review', 'processed_review', 'sentiment']].copy()
final_df.to_csv('healthcare_reviews_processed.csv', index=False)

print("Preprocessing completed!")
print("Sample processed reviews:")
for i, row in df.head(3).iterrows():
    print(f"Original: {row['review']}")
    print(f"Processed: {row['processed_review']}")
    print("-" * 50)