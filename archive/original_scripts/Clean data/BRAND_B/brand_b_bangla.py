import pandas as pd
import unicodedata

df = pd.read_csv('brand_b_google_map_reviews.csv')

def is_bangla(text):
    if pd.isna(text):
        return False
    normalized = unicodedata.normalize('NFKC', str(text))
    return any('\u0980' <= char <= '\u09FF' for char in normalized)

bangla_reviews = df[df['text'].apply(is_bangla)]

filtered_df = bangla_reviews[['name', 'stars', 'text']]
filtered_df.to_csv('brand_b_bangla_reviews.csv', index=False, encoding='utf-8')

print(f"Original dataset: {len(df)} rows")
print(f"Bangla reviews filtered: {len(filtered_df)} rows")
print("\nFirst 5 rows of filtered data:")
print(filtered_df.head())
