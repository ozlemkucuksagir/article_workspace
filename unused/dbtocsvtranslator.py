import pandas as pd
from googletrans import Translator

# Çevirmen nesnesini oluşturma
translator = Translator()

# Türkçe metni İngilizceye çeviren fonksiyon
def translate_to_english(text):
    try:
        translation = translator.translate(text, src='tr', dest='en')
        return translation.text
    except Exception as e:
        print(f"Çeviri hatası: {e}")
        return text

# PostgreSQL veritabanına bağlanma
import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

# SQL sorgusunu çalıştırma ve verileri DataFrame'e çekme
query = 'SELECT id, yorum FROM otel_yorumlar'
df = pd.read_sql_query(query, conn)

# Türkçe metni İngilizceye çevirme
df['yorum_english'] = df['yorum'].apply(translate_to_english)

# DataFrame'i CSV dosyasına yazma (UTF-8 kodlaması ile)
df.to_csv('otel_yorumlar_translated.csv', index=False)

# Veritabanı bağlantısını kapatma
conn.close()
