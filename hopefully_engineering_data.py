import pandas as pd

df = pd.read_csv('veriseti.csv')

rows_number = df.shape[0]
columns_number = df.shape[1]

for i in range(rows_number):

    if pd.isna(df.iloc[i,6]) == True: # Fun Fact: I forgot that function existed, and I
        df.iloc[i,5] = 0 #              was deprieved of sleep in an earlier hackathon,
    else: #                             yet I still forget.
        df.iloc[i,5] = 1

print(df.columns)

column_names = ['kanser_turu', 'cinsiyet', 'doğum tarihi', 'department',
       'oluşturma tarihi', 'ölüm durumu', 'ölüm tarihi', 'hba1c',
       'eşlikedentanılar', 'epikriz', 'eşlikedentanılar tarihi', 'üre',
       'kreatinin', 'bun', 'alt', 'alp', 'ast', 'ggt', 'bilirubin', 'potasyum',
       'kalsiyum', 'magnezyum', 'klor', 'albumin', 'crp', 'ldh', 'sodyum',
       'ilac', 'reçete tarihi', 'atc kod', 'hba1c tarihi', 'üre tarihi',
       'kreatinin tarihi', 'bun tarihi', 'alt tarihi', 'alp tarihi',
       'ast tarihi', 'ggt tarihi', 'bilirubin tarihi', 'potasyum tarihi',
       'kalsiyum tarihi', 'magnezyum tarihi', 'klor tarihi', 'albumin tarihi',
       'crp tarihi', 'ldh tarihi', 'sodyum tarihi', 'icd10', 'işlem adı',
       'işlem tipi', 'işlem tarihi', 'eşlikedentanı', 'eşlikedentanı tarihi',
       'oluşturma tarihi.1']

'''
I will choose the columns to go into the operations:

No Change: [0, 1, 2, 3, 5, 9]

Time: [7, 30], [8, 10], ([11, 31], [12, 32], [13, 33], ... [27, 47]), [28, 29], ,[48, 49], [48, 50], [51, 52] 
atc kod ?


'''

print('liste uzunluğu: ', len(column_names))
print(column_names[7], column_names[30])