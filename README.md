# Healthcare Sentiment Analysis

This project implements a machine learning-based sentiment analysis system for healthcare reviews. The system can classify healthcare reviews into positive, negative, or neutral sentiments using Natural Language Processing (NLP) techniques.

## Features

- **Text Preprocessing**: Comprehensive text cleaning and normalization
- **TF-IDF Vectorization**: Feature extraction from text data
- **Naive Bayes Classification**: Multi-class sentiment classification
- **Model Evaluation**: Performance metrics and analysis
- **Data Generation**: Synthetic healthcare review data generation

## Project Structure

```
healthcare_sentiment_analysis/
├── data_generation.py          # Generate synthetic healthcare reviews
├── data_preparation.py         # Data loading and preprocessing
├── text_preprocessing.py       # Text cleaning and normalization
├── model_training.py          # Model training pipeline
├── train_sentiment_model.py   # Main training script
├── model_evaluation.py        # Model performance evaluation
├── README.md                  # Project documentation
└── .gitignore                # Git ignore rules
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd healthcare_sentiment_analysis
```

2. Install required dependencies:
```bash
pip install pandas scikit-learn numpy joblib
```

## Usage

### 1. Generate Data (Optional)
If you don't have healthcare review data, you can generate synthetic data:
```bash
python data_generation.py
```

### 2. Prepare Data
Process and prepare the data for training:
```bash
python data_preparation.py
```

### 3. Train the Model
Train the sentiment analysis model:
```bash
python train_sentiment_model.py
```

### 4. Evaluate the Model
Evaluate model performance:
```bash
python model_evaluation.py
```

## Model Details

- **Algorithm**: Multinomial Naive Bayes
- **Feature Extraction**: TF-IDF Vectorization
- **Classes**: Positive (1), Negative (0), Neutral (2)
- **Performance**: Accuracy, Precision, Recall, F1-Score

## Data Format

The system expects healthcare reviews in CSV format with the following columns:
- `review`: Raw text reviews
- `sentiment`: Sentiment labels (positive/negative/neutral)

## Output Files

- `sentiment_model.pkl`: Trained model file
- `tfidf_vectorizer.pkl`: TF-IDF vectorizer
- `healthcare_reviews_processed.csv`: Processed dataset

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue on GitHub. 