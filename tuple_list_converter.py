import pandas as pd

# 1. Veriyi yükle
df = pd.read_csv("veriseti.csv")
df.columns = [col.strip() for col in df.columns]

# Silinecek kolonları takip etmek için bir liste
cols_to_delete = []

def parse_bracketed_list(cell):
    if pd.isna(cell) or str(cell).strip() in ["", "[]"]: return []
    text = str(cell).replace("[", "").replace("]", "").replace("'", "")
    return [x.strip() for x in text.split(",") if x.strip()]

def parse_date_list(cell):
    if pd.isna(cell) or str(cell).strip() in ["", "[]"]: return []
    text = str(cell).replace("[", "").replace("]", "").replace("'", "")
    dates = []
    for item in [x.strip() for x in text.split(",") if x.strip()]:
        try:
            dates.append(pd.to_datetime(item).strftime('%Y-%m-%d %H:%M:%S'))
        except: pass
    return dates

# Hariç tutulacaklar
excluded_cols = ['kanser_turu', 'cinsiyet', 'doğum tarihi', 'department', 'ölüm durumu', 'ölüm tarihi']

print("--- Matris Oluşturma ve Temizlik Başlıyor ---")

# Dinamik Eşleşenler
for col in df.columns:
    if col not in excluded_cols and "tarihi" not in col and "_matrix" not in col:
        possible_date_cols = [f"{col} tarihi", f"{col}_tarihi"]
        date_col = next((c for c in possible_date_cols if c in df.columns), None)
        
        if date_col:
            vals = df[col].apply(parse_bracketed_list)
            dates = df[date_col].apply(parse_date_list)
            df[f"{col}_matrix"] = [list(zip(d, v)) for d, v in zip(dates, vals)]
            
            # Başarılıysa silinecekler listesine ekle
            cols_to_delete.extend([col, date_col])
            print(f"Dönüştürüldü: {col}")

# Özel Eşleşenler (İsimleri farklı olanlar)
special_pairs = {
    'ilac': 'reçete tarihi',
    'işlem adı': 'işlem tarihi',
    'eşlikedentanı': 'eşlikedentanı tarihi',
    'eşlikedentanılar': 'eşlikedentanılar tarihi'
}

for val_col, date_col in special_pairs.items():
    if val_col in df.columns and date_col in df.columns:
        vals = df[val_col].apply(parse_bracketed_list)
        dates = df[date_col].apply(parse_date_list)
        df[f"{val_col.replace(' ', '_')}_matrix"] = [list(zip(d, v)) for d, v in zip(dates, vals)]
        
        cols_to_delete.extend([val_col, date_col])
        print(f"Özel Dönüşüm: {val_col}")

# 6. ATLANTI mesajı veren ancak silinmesi gereken ek kolonlar (tarihi olmayan değerler vb.)
extra_cleanup = ['atc kod', 'işlem tipi', 'oluşturma tarihi.1']
cols_to_delete.extend([c for c in extra_cleanup if c in df.columns])

# --- SİLME İŞLEMİ ---
# Listedeki mükerrer isimleri temizle ve mevcut olmayanları çıkar
final_delete_list = list(set([c for c in cols_to_delete if c in df.columns]))
df.drop(columns=final_delete_list, inplace=True)

print(f"\nToplam {len(final_delete_list)} kolon temizlendi.")
print("Kalan Kolonlar:", df.columns.tolist())

# Sonucu kaydet
df.to_csv("temiz_matris_veriseti.csv", index=False)