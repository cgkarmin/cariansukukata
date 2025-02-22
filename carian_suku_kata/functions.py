import pandas as pd

# Fungsi untuk mencari pantun berdasarkan suku kata dan kategori
def cari_suku_kata(suku_kata, kategori):
    df = pd.read_csv("database.csv")

    if kategori not in df.columns:
        return []

    df_filtered = df[df[kategori].astype(str).str.contains(suku_kata, na=False, case=False)]
    hasil = []
    for _, row in df_filtered.iterrows():
        perkataan_dijumpai = [word for word in row["PANTUN"].split() if suku_kata in word]
        hasil.append({
            "kategori": row[kategori],
            "perkataan": ", ".join(perkataan_dijumpai) if perkataan_dijumpai else "-",
            "pantun": row["PANTUN"]
        })
    return hasil
