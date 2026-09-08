import pandas as pd

df = pd.read_excel("brand_d_VADER.xlsx")

df.to_csv("brand_d_VADER.csv", index=False)
