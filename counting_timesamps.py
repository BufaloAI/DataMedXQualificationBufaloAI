import pandas as pd

df = pd.read_csv('veriseti.csv')

rows_number = df.shape[0]
columns_number = df.shape[1]

for i in range(rows_number):

    if pd.isna(df.iloc[i,6]) == True: # Fun Fact: I forgot that function existed, and I
        df.iloc[i,5] = 0 #              was deprieved of sleep in an earlier hackathon,
    else: #                             yet I still forget.
        df.iloc[i,5] = 1


def count_timestamps(column_index: int) -> list:

    timestamp_length = []

    for i in range(columns_number):

        specific_row = df.iloc[column_index, i]
        if type(specific_row) == str:
            number_of_timestamps = specific_row.count('[')
            timestamp_length.append(number_of_timestamps)
        else:
            timestamp_length.append(0)

    return timestamp_length

print('Timestamp lengths for column 0:', count_timestamps(0), '\nTimestamp lengths for column 6:', count_timestamps(6))