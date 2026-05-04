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

# (Eren) Our next task is to group values with their relative timestamps.

# For that, I will count the number of unique timestamps, and then I will squish the
# data of time and value columns together on one column.
# I need to create one new column, and remove the old ones afterwards.

# print(cols)

transform_dict = {column: column + ' tarihi' for column in cols if ((' tarihi' not in column) and (not (column == 'kanser_turu' or column == 'cinsiyet' or column == 'doğum tarihi'
                  or column == 'department' or column == 'oluşturma tarihi' or column == 'ölüm durumu' or column == 'ölüm tarihi' or column == 'epikriz' or column == 'ilac' or column == 'icd10' or column == 'işlem adı'
                  or column == 'işlem tipi' or column == 'işlem tarihi' or column == 'oluşturma tarihi.1')))}

# (Eren) After losing a decent ammount of my sanity on this problem manually, I achieved to get a dictionart to work with.
# But I still wonder if that was worth it.

'''
I will list the columns here to modify.
'kanser_turu', 'cinsiyet', 'doğum tarihi', 'department',
'oluşturma tarihi', 'ölüm durumu', 'ölüm tarihi', 'epikriz',
'ilac', 'icd10', 'işlem adı',
'işlem tipi', 'işlem tarihi'
'oluşturma tarihi.1'

'''

# Now I will use this dictionary to modify those columns, and count the number of unique timestamps.

cols_list = list(cols)

print('transform_dict: ', transform_dict, '\n') # I will print the dictionary to see if it is correct.

# transform_list = [cols_list.index(value) for value in transform_dict.values()]

transform_list = [cols_list.index(value) for value in transform_dict.values() if value in cols_list]

# print('transform_list: ', transform_list, '\n') # I will print the list to see if it is correct.

list_of_number_of_timestamps = []

'''
for key in transform_dict.keys():

    pos = cols_list.index(key)

    for _ in range(1, 100):

        if df.iloc[_, pos] is not float:
            
            #print(df.iloc[_, pos])
            list_of_number_of_timestamps.append(df[key].astype(str).str.len())

        else:

            list_of_number_of_timestamps.append(1)

'''
# (Eren) I will print the list to see if it is correct.

# print('list_of_number_of_timestamps: ', list_of_number_of_timestamps)
# print('Number of 1s: ', list_of_number_of_timestamps.count(1))

# (Eren) Now, we learned that except it is 'oluşturma tarihi' and 'oluşturma tarihi.1', all the columns have 500 timestamps.
# Now, we use that information and continue with our mission. Also, don't forget to save this one.

# TIMESTAMP_COUNT = 500


# I give up on this, I will manually count one of them.


# print([df.iloc[:, elem] for elem in transform_list])

print(list_of_number_of_timestamps)

for elem in transform_list:

    list_of_number_of_timestamps.append(df.iloc[0, elem].count('['))

print('list_of_number_of_timestamps: ', list_of_number_of_timestamps)