import pandas as pd
from ucimlrepo import fetch_ucirepo

def load_healthcare_data():
    """Load the original healthcare reviews data"""
    try:
        df = pd.read_csv('healthcare_reviews_processed.csv')
        return df
    except FileNotFoundError:
        print("Healthcare reviews data not found. Please run data_generation.py first.")
        return None

def load_drug_reviews_data():
    """Load drug reviews dataset from UCI"""
    try:
        # fetch dataset 
        drug_reviews_druglib_com = fetch_ucirepo(id=461) 
        
        # data (as pandas dataframes) 
        X = drug_reviews_druglib_com.data.features 
        y = drug_reviews_druglib_com.data.targets 
        
        print(f"UCI Dataset loaded - Features: {X.shape}")
        print(f"Feature columns: {list(X.columns)}")
        
        # Since targets is None, we'll use the rating column for sentiment
        df = X.copy()
        
        # Use commentsReview as the review text
        if 'commentsReview' in df.columns:
            df = df.rename(columns={'commentsReview': 'processed_review'})
        else:
            # If no commentsReview, use the first text-like column
            text_columns = [col for col in df.columns if df[col].dtype == 'object']
            if text_columns:
                df = df.rename(columns={text_columns[0]: 'processed_review'})
            else:
                print("No suitable review column found in UCI dataset")
                return None
        
        # Convert rating to sentiment
        if 'rating' in df.columns:
            # Convert numeric rating to sentiment
            def rating_to_sentiment(rating):
                if pd.isna(rating):
                    return 'neutral'
                rating = float(rating)
                if rating >= 4.0:
                    return 'positive'
                elif rating <= 2.0:
                    return 'negative'
                else:
                    return 'neutral'
            
            df['sentiment'] = df['rating'].apply(rating_to_sentiment)
        else:
            # If no rating column, create neutral sentiment
            df['sentiment'] = 'neutral'
        
        # Keep only the columns we need
        if 'processed_review' in df.columns and 'sentiment' in df.columns:
            df = df[['processed_review', 'sentiment']]
            print(f"Processed UCI dataset: {df.shape}")
            print(f"Sentiment distribution: {df['sentiment'].value_counts().to_dict()}")
            return df
        else:
            print("Required columns not found in UCI dataset")
            return None
            
    except Exception as e:
        print(f"Error loading drug reviews data: {e}")
        return None

def combine_datasets():
    """Combine healthcare and drug reviews datasets"""
    healthcare_df = load_healthcare_data()
    drug_df = load_drug_reviews_data()
    
    if healthcare_df is not None and drug_df is not None:
        # Combine datasets
        combined_df = pd.concat([healthcare_df, drug_df], ignore_index=True)
        combined_df.to_csv('combined_healthcare_reviews.csv', index=False)
        print(f"Combined dataset created with {len(combined_df)} samples")
        return combined_df
    elif healthcare_df is not None:
        print("Using only healthcare reviews data")
        return healthcare_df
    elif drug_df is not None:
        print("Using only drug reviews data")
        drug_df.to_csv('drug_reviews_processed.csv', index=False)
        return drug_df
    else:
        print("No data available")
        return None

if __name__ == "__main__":
    combined_data = combine_datasets()
    if combined_data is not None:
        print("Data preparation completed!")