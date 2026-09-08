import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

plt.style.use('ggplot')

from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

df = pd.read_csv("brand_c_cleaned_ROBERTA.csv")

if 'Index No' not in df.columns:
    df['Index No'] = range(1, len(df) + 1)

def polarity_scores_roberta(text):

    text = str(text)

    encoded_text = tokenizer(
        text,
        return_tensors='pt',
        truncation=True,
        padding=True,
        max_length=512
    )

    output = model(**encoded_text)

    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    return {
        'roberta_neg': scores[0],
        'roberta_neu': scores[1],
        'roberta_pos': scores[2]
    }

res = {}

for _, row in tqdm(df.iterrows(), total=len(df)):
    try:
        myid = row['Index No']
        text = row['reviews']

        res[myid] = polarity_scores_roberta(text)

    except RuntimeError:
        print(f"Broke for ID {row['Index No']}")
        continue

roberta_df = pd.DataFrame(res).T
roberta_df = roberta_df.reset_index().rename(columns={'index': 'Index No'})


print("Processing Completed")

final_df = df.merge(roberta_df, on='Index No', how='left')
print(final_df.head())

final_df['roberta_compound'] = final_df['roberta_pos'] - final_df['roberta_neg']

plt.figure(figsize=(10,5))
sns.barplot(data=final_df, x='stars', y='roberta_compound')

plt.title("Stars vs RoBERTa Sentiment Relationship")
plt.xlabel("Review Stars")
plt.ylabel("Composite RoBERTa Sentiment Score")
plt.show()

final_df.to_csv("brand_c_roberta_final.csv", index=False)