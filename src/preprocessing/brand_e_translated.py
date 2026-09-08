import pandas as pd
import time
from deep_translator import GoogleTranslator

df = pd.read_csv('brand_e_bangla_reviews.csv')

def translate_to_english(text):
    if pd.isna(text):
        return ""

    try:
        time.sleep(0.3)
        return GoogleTranslator(source='bn', target='en').translate(str(text))

    except Exception as e:
        print("Translation error:", e)
        return str(text)

print("Translating Bangla reviews to English...")

df['reviews_en'] = df['reviews'].apply(translate_to_english)

df[['name','stars','reviews_en']].to_csv(
    'brand_e_translated.csv',
    index=False,
    encoding='utf-8'
)

print("Translation completed!")