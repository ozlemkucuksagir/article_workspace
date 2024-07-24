import psycopg2

# PostgreSQL veritabanına bağlanma
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432",
)
cursor = conn.cursor()

# hotels_data tablosundaki id sütununu birincil anahtar olarak tanımlama
try:
    cursor.execute('''
        ALTER TABLE hotels_data
        ADD CONSTRAINT hotels_data_pkey PRIMARY KEY (id);
    ''')
    print("Birincil anahtar başarıyla eklendi.")
except psycopg2.Error as e:
    print(f"Birincil anahtar eklenirken hata oluştu: {e}")
finally:
    # Değişiklikleri kaydetme
    conn.commit()

    # Bağlantıyı kapatma
    cursor.close()
    conn.close()
