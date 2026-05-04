import pandas as pd
import re, json
df = pd.read_csv('veriseti.csv')

rows_number = df.shape[0]

for i in range(rows_number):

    if pd.isna(df.iloc[i,6]) == True: # Fun Fact: I forgot that function existed, and I
        df.iloc[i,5] = 0 #              was deprieved of sleep in an earlier hackathon,
    else: #                             yet I still forget.
        df.iloc[i,5] = 1

# print(df.iloc[:,5:7]) # Some manual checks.

timestamp_count = {}


print(df.iloc[0, 10])
print(df.iloc[0, 10].count('['))
print(list(df.iloc[0, 10].split(',')))

# Internet search yields, result = ast.literal_eval(f"[{data_str}]")


