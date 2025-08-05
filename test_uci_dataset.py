import pandas as pd
from ucimlrepo import fetch_ucirepo

def test_uci_dataset():
    """Test the UCI drug reviews dataset"""
    print("="*60)
    print("TESTING UCI DRUG REVIEWS DATASET (ID: 461)")
    print("="*60)
    
    try:
        # fetch dataset 
        print("Fetching dataset from UCI repository...")
        drug_reviews_druglib_com = fetch_ucirepo(id=461) 
        
        # data (as pandas dataframes) 
        X = drug_reviews_druglib_com.data.features 
        y = drug_reviews_druglib_com.data.targets 
        
        print(f"\n✅ Dataset loaded successfully!")
        print(f"📊 Features shape: {X.shape}")
        print(f"📊 Targets shape: {y.shape}")
        
        # Show sample data
        print(f"\n📋 Sample features:")
        print(X.head())
        print(f"\n📋 Sample targets:")
        print(y.head())
        
        # Combine features and targets
        df = pd.concat([X, y], axis=1)
        print(f"\n📊 Combined dataset shape: {df.shape}")
        print(f"📋 Combined dataset columns: {list(df.columns)}")
        
        # Show sample reviews
        print(f"\n📝 Sample reviews:")
        if 'review' in df.columns:
            for i, review in enumerate(df['review'].head(3), 1):
                print(f"{i}. {review[:100]}...")
        
        # Show sentiment distribution
        if 'sentiment' in df.columns:
            print(f"\n📈 Sentiment distribution:")
            print(df['sentiment'].value_counts())
        
        # metadata 
        print(f"\n📋 Metadata:")
        print(drug_reviews_druglib_com.metadata)
        
        # variable information 
        print(f"\n📋 Variable information:")
        print(drug_reviews_druglib_com.variables)
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading drug reviews data: {e}")
        return None

def test_combined_datasets():
    """Test combining healthcare and drug reviews"""
    print("\n" + "="*60)
    print("TESTING COMBINED DATASETS")
    print("="*60)
    
    try:
        # Load healthcare data
        print("Loading healthcare reviews...")
        healthcare_df = pd.read_csv('healthcare_reviews_processed.csv')
        print(f"✅ Healthcare reviews: {healthcare_df.shape}")
        
        # Load drug reviews
        print("Loading drug reviews...")
        drug_df = test_uci_dataset()
        
        if drug_df is not None:
            # Combine datasets
            combined_df = pd.concat([healthcare_df, drug_df], ignore_index=True)
            print(f"\n✅ Combined dataset: {combined_df.shape}")
            print(f"📊 Total samples: {len(combined_df)}")
            
            # Show sentiment distribution
            if 'sentiment' in combined_df.columns:
                print(f"\n📈 Combined sentiment distribution:")
                print(combined_df['sentiment'].value_counts())
            
            return combined_df
        else:
            print("❌ Could not load drug reviews")
            return healthcare_df
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("Testing UCI Drug Reviews Dataset Integration...")
    combined_data = test_combined_datasets()
    
    if combined_data is not None:
        print(f"\n🎉 Success! Ready to train with {len(combined_data)} samples")
        print("Run: python train_sentiment_model.py")
    else:
        print("\n❌ Failed to load datasets") 