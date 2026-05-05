import pandas as pd

# (Eren) Here we go again. I will start by importing the document.
 
df = pd.read_csv('veriseti.csv')
columns_list = [col.strip() for col in df.columns]

# I will apply the same proccess as before to fill 'ölüm durumu' column.

rows_number = df.shape[0]
columns_number = df.shape[1]

for i in range(rows_number):

    if pd.isna(df.iloc[i,6]) == True: # Fun Fact: I forgot that function existed, and I
        df.iloc[i,5] = 0 #              was deprieved of sleep in an earlier hackathon,
    else: #                             yet I still forget.
        df.iloc[i,5] = 1

# Now I will create a set for columns to be deleted.

cols_to_delete = []

# I will divide my approach from here: Floats, and dates.

def parse_float_list(cell: str) -> list:
    
    if pd.isna(cell) or str(cell).strip() in ['', '[]']: return [] # Remove boundarty cases, and empty lists.
    text = str(cell).replace('[', '').replace(']', '').replace("'", '') # We remove the parts to make it float.
    return [float(x.strip()) for x in text.split(',') if x.strip()] # We finally convert to float, and assign to a list.

def parse_date_list(cell: str) -> list:

    if pd.isna(cell) or str(cell).strip() in ['', '[]']: return []
    text = str(cell).replace('[', '').replace(']', '').replace("'", '') # We remove the parts to make it date.
    dates = []
    for item in [x.strip() for x in text.split(',') if x.strip()]:
        try: # I am not sure if it will work, so I will put down a try-except block in advance.
            dates.append(pd.to_datetime(item).strftime('%Y-%m-%d %H:%M:%S'))
        except: pass
    return dates

def parse_string_list(cell: str) -> list:

    if pd.isna(cell) or str(cell).strip() in ['', '[]']: return []
    text = str(cell).replace('[', '').replace(']', '').replace("'", '') # We remove the parts to make it string.
    return [x.strip() for x in text.split(',') if x.strip()] # We finally convert to string, and assign to a list.


# Now I will note the columns I will exclude before I apply these functions to the dataframe.

excluded_columns = ['kanser_turu', 'cinsiyet', 'doğum tarihi', 'department', 'ölüm durumu', 'ölüm tarihi', 'ilac', 'işlem adı', 'eşlikedentanı', 'eşlikedentanılar']

for col in columns_list:
    if (col not in excluded_columns) and ('tarihi' not in col) and ('_list' not in col): # I remove the columns I won't use.
        possible_date_columns = [f'{col} tarihi', f'{col}_tarihi'] # For ambiguous cases.
        date_column = next((c for c in possible_date_columns if c in columns_list), None)

        if date_column:
            
            values = df[col].apply(parse_float_list)
            dates = df[date_column].apply(parse_date_list)

            df[f'{col}_list'] = [list(zip(t, v)) for t, v in zip(dates, values)] # I create [t_n, v_n] pairs.

            cols_to_delete.extend([col, date_column]) # I add the original columns to the deletion list.

# There are some columns that have special names like 'ilaç' and 'reçete tarihi' that are related.

special_pairs = {
    'ilac': 'reçete tarihi',
    'işlem adı': 'işlem tarihi',
    'eşlikedentanı': 'eşlikedentanı tarihi',
    'eşlikedentanılar': 'eşlikedentanılar tarihi'
}

for col, date_col in special_pairs.items():
    if col in columns_list and date_col in columns_list:
        values = df[col].apply(parse_string_list)
        dates = df[date_col].apply(parse_date_list)

        df[f'{col}_list'.replace(' ', '_')] = [list(zip(t, v)) for t, v in zip(dates, values)] # I create [t_n, v_n] pairs.

        cols_to_delete.extend([col, date_col]) # I add the original columns to the deletion list.

# Some columns are left to delete.
cols_to_delete.extend(['icd10', 'atc_kod', 'işlem_tipi', 'oluşturma tarihi.1'])

# Finally, I combine those sets, and delete the columns.

final_cols_to_delete = list(set(column for column in cols_to_delete if column in columns_list)) # I make sure that the columns to be deleted are actually in the dataframe.
df.drop(columns=final_cols_to_delete, inplace=True)

# (Eren) FINALLY, after that work, I will save my file.
df.to_csv('list_ordered_veriseti.csv', index=False) # I save the new dataframe to a new csv file.