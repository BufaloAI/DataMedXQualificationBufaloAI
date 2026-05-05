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

specific_row = df.iloc[0, 20]
number_of_timestamps = specific_row.count('[')
row_splitted = specific_row.split(',')
row_list = list(row_splitted)
for i in range(len(row_list)):
    row_list[i] = row_list[i].replace(']', '')
    row_list[i] = row_list[i].replace('[', '')
    row_list[i] = float(row_list[i])

# (Eren) Turns out the logic I used above was really the solution to the specific rows.

# df['potasyum'] = df['potasyum'].astype(list) Does not work.

print(row_list)

# Internet search yields, result = ast.literal_eval(f"[{data_str}]")

# I will maybe come back to this file later, but I certainly earn some intutition.
# Now, I will try to use numpy for this.