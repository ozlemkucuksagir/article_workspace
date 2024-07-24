import pandas as pd

# Veritabanını oku
df = pd.read_csv("addColumn_otel1_202407241121.csv")

# Fiyat sütununu düzelt
df['fiyat'] = df['fiyat'].apply(lambda x: float(x.replace('.', '').replace(',', '.')[:-4]))

# Bolge sütunundaki gereksiz karakterleri kaldır
df['bolge'] = df['bolge'].str.replace(r'\W+', ' ', regex=True)

# Score sütunundaki virgülleri kaldır, 10'a bölerek yuvarla
df['score'] = df['score'].str.replace(',', '').astype(float) / 10



# def process_hava_alanina_uzakligi(deger):
#     if pd.isna(deger) or deger == 'No Info':
#         return None  # NaN veya "No Info" içeriyorsa None döndür
#     elif isinstance(deger, str):  # Eğer deger bir string ise
#         deger = deger.split(' ')[0]  # İlk kelimeyi al
#         if deger.isdigit():  # Eğer alınan değer bir sayı ise
#             return int(deger)  # Sayıyı integer'a dönüştür ve döndür
#     return None  # Yukarıdaki koşullar sağlanmazsa None döndür

# # Hava Alanına Uzaklık sütununu düzenleme
# df['hava_alanina_uzakligi'] = df['hava_alanina_uzakligi'].apply(process_hava_alanina_uzakligi)





# Denize Uzaklık sütununu düzenle
def process_denize_uzaklik(deger):
    if isinstance(deger, float):
        return deger  # Eğer float ise işlem yapma, direkt olarak döndür
    elif deger == 'Denize Sıfır':
        return 0
    elif 'Arası' in deger:
        return int(deger.split()[0])  # Arası ifadesinin başındaki sayıyı al
    elif 've Üzeri' in deger:
        return int(deger.split()[0])  # "ve Üzeri" ifadesinin başındaki sayıyı al
    elif deger.isdigit():
        return int(deger)
    else:
        return None


# Denize Uzaklık sütununu düzenle
df['denize_uzakligi'] = df['denize_uzakligi'].apply(process_denize_uzaklik)

# Plaj sütununu düzenle
def process_plaj_turu(deger):
    if isinstance(deger, float):
        return None  # or any default value you prefer
    elif 'Özel Plaj' in deger:
        return 2
    elif 'Halk Plajı' in deger:
        return -1
    else:
        return None


df['plaj'] = df['plaj'].apply(process_plaj_turu)


# Direkt kaldırılacak column'lar
df = df.drop(['fiyat_araligi','hava_alanina_uzakligi'], axis=1)

print(df.head())

df.to_csv("duzenlenmis_otel_veritabani_DB4.csv", index=False)
