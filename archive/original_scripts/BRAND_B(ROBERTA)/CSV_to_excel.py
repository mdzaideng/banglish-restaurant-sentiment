import pandas as pd

df = pd.read_csv("brand_b_roberta_final.csv")

cols = df.columns.tolist()
cols.insert(0, cols.pop(cols.index("Index No")))
df = df[cols]

df.to_excel("brand_b_ROBERTA_final.xlsx", index=False)

print("Excel file saved successfully")