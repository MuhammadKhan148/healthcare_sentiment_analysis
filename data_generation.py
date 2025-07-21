import pandas as pd
import random

random.seed(42)

positive_reviews = [
    "The doctor was very professional and caring during my visit",
    "Excellent service and quick appointment scheduling",
    "Staff was friendly and the facility was clean and modern",
    "Doctor took time to explain everything clearly",
    "Great experience with minimal wait time",
    "The treatment was effective and I felt much better",
    "Nurse was very gentle and understanding",
    "Outstanding medical care and follow-up",
    "Highly recommend this healthcare provider",
    "Professional staff and comfortable environment",
    "Doctor listened carefully to my concerns",
    "Efficient service with great results",
    "Clean facilities and modern equipment",
    "Caring medical team that goes above and beyond",
    "Quick diagnosis and effective treatment plan"
]

negative_reviews = [
    "Long wait times and poor communication from staff",
    "Doctor seemed rushed and didn't listen to my concerns",
    "Facility was outdated and not very clean",
    "Billing issues and unclear pricing information",
    "Rude receptionist and unprofessional behavior",
    "Appointment was cancelled at the last minute",
    "Doctor was dismissive of my symptoms",
    "Poor follow-up care and lack of communication",
    "Overpriced services with mediocre results",
    "Uncomfortable waiting room and long delays",
    "Staff seemed unorganized and confused",
    "Treatment didn't help and no alternative options given",
    "Difficulty getting appointments when needed",
    "Insurance problems not handled properly",
    "Felt like just another number, not a patient"
]

neutral_reviews = [
    "Average experience, nothing particularly good or bad",
    "Standard medical care, met basic expectations",
    "Typical healthcare visit with routine procedures",
    "Service was okay, could be better or worse",
    "Normal appointment with expected results",
    "Standard facility with adequate services",
    "Regular check-up went as expected",
    "Basic care provided without any issues",
    "Acceptable service for the price paid",
    "Routine visit with no surprises",
    "Average wait time and standard procedures",
    "Typical medical office environment",
    "Standard appointment scheduling process",
    "Basic medical consultation provided",
    "Regular healthcare service delivery"
]

def create_review_variations(base_reviews, num_variations=3):
    variations = []
    prefixes = ["Overall, ", "In my experience, ", "I found that ", ""]
    suffixes = [" today.", " recently.", " last week.", " during my visit.", ""]
    
    for review in base_reviews:
        variations.append(review)
        
        for i in range(num_variations):
            prefix = random.choice(prefixes)
            suffix = random.choice(suffixes)
            varied_review = prefix + review.lower() + suffix
            variations.append(varied_review)
    
    return variations

positive_varied = create_review_variations(positive_reviews)
negative_varied = create_review_variations(negative_reviews)
neutral_varied = create_review_variations(neutral_reviews)

reviews_data = []
sentiments_data = []

reviews_per_sentiment = 500 // 3
remaining_reviews = 500 % 3

for i in range(reviews_per_sentiment + (1 if remaining_reviews > 0 else 0)):
    review = random.choice(positive_varied)
    reviews_data.append(review)
    sentiments_data.append('positive')
    if remaining_reviews > 0:
        remaining_reviews -= 1

for i in range(reviews_per_sentiment + (1 if remaining_reviews > 0 else 0)):
    review = random.choice(negative_varied)
    reviews_data.append(review)
    sentiments_data.append('negative')
    if remaining_reviews > 0:
        remaining_reviews -= 1

for i in range(reviews_per_sentiment):
    review = random.choice(neutral_varied)
    reviews_data.append(review)
    sentiments_data.append('neutral')

df = pd.DataFrame({
    'review': reviews_data,
    'sentiment': sentiments_data
})

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df = df.dropna()

df = df.drop_duplicates(subset=['review'], keep='first')

df.to_csv('healthcare_reviews.csv', index=False)