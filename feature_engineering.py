import pandas as pd

# (Eren) Now, we are going to start reshaping the data.

# First, we will import the document.

df = pd.read_csv('veriseti.csv')

# Larp starts from here.

# Now, I will work to group the features under timestamps.
# For this, I will define two functions, and then apply them to the relevant columns.
# It must also be considered that I get output as string, 
# so I will need to convert it to list of floats or list of datetimes.

# Now, we start.

# We start by defining the first function for parsing the bracketed lists of values.
def parse_bracketed_list(cell):
    """Turn '[val1, val2, val3]' string → Python list of floats."""
    if pd.isna(cell):
        return []
    # Remove surrounding brackets, split on '], ['
    text = str(cell).strip("[]")
    items = [x.strip() for x in text.split(",")]
    results = []
    for item in items:
        try:
            results.append(float(item))
        except ValueError:
            pass  # skip non-numeric entries
    return results

# Here goes the second function for date parsing.
def parse_date_list(cell):
    """Turn date string column → list of datetime objects."""
    if pd.isna(cell):
        return []
    text = str(cell).strip("[]")
    items = [x.strip() for x in text.split("],")]
    dates = []
    for item in items:
        item = item.strip("[] ")
        try:
            dates.append(pd.to_datetime(item))
        except Exception:
            pass
    return dates

# Apply to each lab column
LAB_COLS = ['kanser_turu', 'cinsiyet', 'doğum tarihi', 
            'department', 'oluşturma tarihi', 'ölüm durumu', 
            'ölüm tarihi', 'hba1c', 'eşlikedentanılar', 
            'epikriz', 'eşlikedentanılar tarihi', 'üre', 
            'kreatinin', 'bun', 'alt', 'alp', 'ast', 'ggt', 
            'bilirubin', 'potasyum', 'kalsiyum', 'magnezyum', 
            'klor', 'albumin', 'crp', 'ldh', 'sodyum', 'ilac', 
            'reçete tarihi', 'atc kod', 'hba1c tarihi', 'üre tarihi', 
            'kreatinin tarihi', 'bun tarihi', 'alt tarihi', 'alp tarihi', 
            'ast tarihi', 'ggt tarihi', 'bilirubin tarihi', 'potasyum tarihi', 
            'kalsiyum tarihi', 'magnezyum tarihi', 'klor tarihi', 'albumin tarihi', 
            'crp tarihi', 'ldh tarihi', 'sodyum tarihi', 'icd10', 'işlem adı', 
            'işlem tipi', 'işlem tarihi', 'eşlikedentanı', 'eşlikedentanı tarihi', 'oluşturma tarihi.1']
DATE_COLS = [c + "_dates" for c in LAB_COLS]

for col in LAB_COLS:
    df[col + "_vals"] = df[col].apply(parse_bracketed_list)
for col1 in DATE_COLS:
    for col in LAB_COLS:
        df[col1] = df[col].apply(parse_date_list)

print(df)

# End of larp.