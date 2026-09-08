import pandas as pd

df = pd.read_csv("brand_c_roberta_final.csv")

cols = df.columns.tolist()
cols.insert(0, cols.pop(cols.index("Index No")))
df = df[cols]

df.to_excel("brand_c_ROBERTA.xlsx", index=False)

print("Excel file saved successfully")