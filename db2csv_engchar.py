import pandas as pd
import psycopg2

# Türkçe karakterleri İngilizce karakterlere dönüştüren fonksiyon
def turkish_to_english(text):
    translation_table = str.maketrans(
    'ÇĞİÖŞÜçğıöşü',
    'CGIOSUcgiosu'
)

    return text.translate(translation_table)

# PostgreSQL veritabanına bağlanma
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

# SQL sorgusunu çalıştırma ve verileri DataFrame'e çekme
query = 'SELECT id, otel_id, otel_ad, yorum FROM otel_yorumlar'
df = pd.read_sql_query(query, conn)

# Türkçe karakterleri İngilizce karakterlere dönüştürme
df['yorum'] = df['yorum'].apply(turkish_to_english)
df['otel_ad'] = df['otel_ad'].apply(turkish_to_english)

# DataFrame'i CSV dosyasına yazma (UTF-8 kodlaması ile)
df.to_csv('otel_yorumlar.csv', index=False)

# Veritabanı bağlantısını kapatma
conn.close()
