import pandas as pd
import re
from langdetect import detect


df = pd.read_csv("brand_d_google_map_reviews.csv")

df = df[['name', 'stars', 'reviews']]

df = df.dropna(subset=['reviews'])

def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False

df = df[df['reviews'].apply(is_english)]

def clean_text(text):
    text = text.lower()                         # lowercase
    text = re.sub(r"http\S+|www\S+", "", text)  # remove URLs
    text = re.sub(r"@\w+|\#\w+", "", text)      # remove mentions & hashtags
    text = re.sub(r"[^\w\s!?']", "", text)      # keep ! ? '
    text = re.sub(r"\d+", "", text)             # remove numbers
    text = re.sub(r"\s+", " ", text).strip()    # remove extra spaces
    return text

df['reviews'] = df['reviews'].apply(clean_text)

df = df.reset_index(drop=True)

#df.to_csv("brand_d_cleaned_VADER", index=False)

print("File saved successfully.")
print("Final shape:", df.shape)