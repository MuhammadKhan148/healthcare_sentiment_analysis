import pandas as pd
import re

df = pd.read_csv('healthcare_reviews.csv')

stopwords = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
    'to', 'was', 'will', 'with', 'i', 'me', 'my', 'we', 'you', 'your'
}

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    tokens = re.findall(r'\b[a-zA-Z]+\b', text)
    tokens = [token for token in tokens if token not in stopwords]
    stemmed_tokens = []
    for token in tokens:
        if len(token) > 4:
            if token.endswith('ing'):
                token = token[:-3]
            elif token.endswith('ed'):
                token = token[:-2]
            elif token.endswith('er'):
                token = token[:-2]
            elif token.endswith('ly'):
                token = token[:-2]
        stemmed_tokens.append(token)
    processed_text = ' '.join(stemmed_tokens)
    return processed_text

df['processed_review'] = df['review'].apply(preprocess_text)

df = df[df['processed_review'] != ''].reset_index(drop=True)

final_df = df[['review', 'processed_review', 'sentiment']].copy()
final_df.to_csv('healthcare_reviews_processed.csv', index=False)