import pandas as pd
import os

# Create sample CSV data for testing
sample_data = [
    "The doctor was very professional and took time to explain my condition. The staff was friendly and the facility was clean.",
    "Long wait times and the receptionist was rude. The doctor seemed rushed and didn't answer my questions properly.",
    "The appointment was okay. The doctor was competent but not particularly warm. The facility is average.",
    "Excellent care! The nursing staff went above and beyond to make me comfortable. The doctor was knowledgeable and compassionate.",
    "Terrible experience. Had to wait 3 hours past my appointment time. The doctor was dismissive and didn't seem to care.",
    "The medical treatment was effective and the doctor was professional. The billing process was straightforward.",
    "Outstanding service from start to finish. The entire team was helpful and the treatment was successful.",
    "Poor communication and outdated facilities. The wait was unreasonable and the staff seemed overwhelmed.",
    "Standard healthcare experience. Nothing exceptional but the basic needs were met adequately.",
    "Amazing doctor who really listened to my concerns. The follow-up care was excellent and very thorough."
]

# Create DataFrame
df = pd.DataFrame({'text': sample_data})

# Create public directory if it doesn't exist
os.makedirs('public', exist_ok=True)

# Save to CSV
df.to_csv('public/sample_reviews.csv', index=False)

print("Sample CSV file created at public/sample_reviews.csv")
print(f"Created {len(sample_data)} sample reviews for testing")
