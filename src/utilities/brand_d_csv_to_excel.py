import pandas as pd

df = pd.read_csv("brand_d_ROBERTA.csv")

cols = df.columns.tolist()
cols.insert(0, cols.pop(cols.index("Index No")))
df = df[cols]

df.to_excel("brand_d_ROBERTA.xlsx", index=False)

print("Excel file saved successfully")