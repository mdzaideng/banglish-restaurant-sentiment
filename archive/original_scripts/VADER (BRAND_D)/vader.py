import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot')

import nltk


df = pd.read_csv("brand_d_cleaned_VADER.csv")

#print(df.shape)

ax = df['stars'].value_counts().sort_index().plot(kind = 'bar',
                                             title = 'Count of Reviews by Stars fo Brand D',
                                             figsize=(10, 5))

ax.set_xlabel("Review Stars")
ax.set_ylabel("Number of Consumer")



#NLTK
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
from tqdm import tqdm

sia = SentimentIntensityAnalyzer()

if 'Index No' not in df.columns:
    df['Index No'] = range(1, len(df) + 1)
res = {}
for i, row in tqdm(df.iterrows(), total=len(df)):
    text = str(row['reviews'])
    myid = row['Index No']
    res[myid] = sia.polarity_scores(text)


vaders = pd.DataFrame(res).T
vaders = vaders.reset_index()
vaders = vaders.rename(columns={'index': 'Index No'})

final_df = df.merge(vaders, on='Index No', how='left')
print(final_df)



#Validating VADER with Stars

plt.figure(figsize=(10,5))

sns.barplot(data=final_df, x='stars', y='compound')

plt.title('Compound Score VS Stars')
plt.xlabel('Review Stars')
plt.ylabel('Compound Sentiment Score')

plt.show()

#final_df.to_excel("brand_d_VADER.xlsx", index=False)
final_df.to_csv("final_sentiment_output.csv", index=False)