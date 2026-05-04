import pandas as pd

# (Eren) After the serious failure on last attempt, I will rearrange the code.

# I will start by reading the document again.

df = pd.read_csv('veriseti.csv')

# (Eren)

# Now, I will work to group the features under timestamps.
# I assume I could work with strings, since they will be
# converted automatically, but let's try.

# Print out the second row of the dataframe to see what it looks like before diving in.

# print(f'\ndf.iloc[1]: {df.iloc[1]}\n')

# Now, since we saw the structure, we can do it clearly.

# (Eren) My aim is to add death values first. They lack value, but they have timesamps.

cols_number = len(df.columns)
rows_number = df.shape[0]

# rows = df.iloc[:, 0] Not exactly what I want, but I got a pretty good intuition.
cols = df.columns

# print(f'\ncolumns: {cols}\n') 5 is 'ölüm durumu' and 6 is 'ölüm tarihi'.

# (Eren) After carefull research, I decided to use iloc and make a loop for that.

for i in range(rows_number):

    if pd.isna(df.iloc[i,6]) == True: # Fun Fact: I forgot that function existed, and I
        df.iloc[i,5] = 0 #              was deprieved of sleep in an earlier hackathon,
    else: #                             yet I still forget.
        df.iloc[i,5] = 1

# (Eren) I will move on and print that to confirm.

# print(f'New df: {df.iloc[:,5:7]}') Some manual checks.
# print(type(df.iloc[498,6])) I did some debugging.

# (Eren) Task 1 is done. I now have values for Y as the death status.

