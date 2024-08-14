import psycopg2

# PostgreSQL veritabanına bağlanma
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Her bir sütun için sırayla RENAME COLUMN ifadelerini çalıştırma
# 'ALTER TABLE oteller RENAME COLUMN "Fiyat Aralığı" TO fiyat_araligi',
rename_queries = [
    
    'ALTER TABLE oteller RENAME COLUMN "Bölge" TO bolge',
    'ALTER TABLE oteller RENAME COLUMN "Hava Alanına Uzaklığı" TO hava_alanina_uzakligi',
    'ALTER TABLE oteller RENAME COLUMN "Denize Uzaklığı" TO denize_uzakligi',
    'ALTER TABLE oteller RENAME COLUMN "Plaj" TO plaj',
    'ALTER TABLE oteller RENAME COLUMN "İskele" TO iskele',
    'ALTER TABLE oteller RENAME COLUMN "A la Carte Restoran" TO a_la_carte_restoran',
    'ALTER TABLE oteller RENAME COLUMN "Asansör" TO asansor',
    'ALTER TABLE oteller RENAME COLUMN "Açık Restoran" TO acik_restoran',
    'ALTER TABLE oteller RENAME COLUMN "Kapalı Restoran" TO kapali_restoran',
    'ALTER TABLE oteller RENAME COLUMN "Açık Havuz" TO acik_havuz',
    'ALTER TABLE oteller RENAME COLUMN "Kapalı Havuz" TO kapali_havuz',
    'ALTER TABLE oteller RENAME COLUMN "Bedensel Engelli Odası" TO bedensel_engelli_odasi',
    'ALTER TABLE oteller RENAME COLUMN "Bar" TO bar',
    'ALTER TABLE oteller RENAME COLUMN "Su Kaydırağı" TO su_kaydiragi',
    'ALTER TABLE oteller RENAME COLUMN "Balo Salonu" TO balo_salonu',
    'ALTER TABLE oteller RENAME COLUMN "Kuaför" TO kuafor',
    'ALTER TABLE oteller RENAME COLUMN "Otopark" TO otopark',
    'ALTER TABLE oteller RENAME COLUMN "Market" TO market',
    'ALTER TABLE oteller RENAME COLUMN "Sauna" TO sauna',
    'ALTER TABLE oteller RENAME COLUMN "Doktor" TO doktor',
    'ALTER TABLE oteller RENAME COLUMN "Beach Voley" TO beach_voley',
    'ALTER TABLE oteller RENAME COLUMN "Fitness" TO fitness',
    'ALTER TABLE oteller RENAME COLUMN "Canlı Eğlence" TO canli_eglence',
    'ALTER TABLE oteller RENAME COLUMN "Wireless Internet" TO wireless_internet',
    'ALTER TABLE oteller RENAME COLUMN "Animasyon" TO animasyon',
    'ALTER TABLE oteller RENAME COLUMN "Sörf" TO sorf',
    'ALTER TABLE oteller RENAME COLUMN "Paraşüt" TO parasut',
    'ALTER TABLE oteller RENAME COLUMN "Araç Kiralama" TO arac_kiralama',
    'ALTER TABLE oteller RENAME COLUMN "Kano" TO kano',
    'ALTER TABLE oteller RENAME COLUMN "SPA" TO spa',
    'ALTER TABLE oteller RENAME COLUMN "Masaj" TO masaj',
    'ALTER TABLE oteller RENAME COLUMN "Masa Tenisi" TO masa_tenisi',
    'ALTER TABLE oteller RENAME COLUMN "Çocuk Havuzu" TO cocuk_havuzu',
    'ALTER TABLE oteller RENAME COLUMN "Çocuk Parkı" TO cocuk_parki'
]

# Her bir sorguyu çalıştırma
for query in rename_queries:
    cursor.execute(query)

# Değişiklikleri kaydetme
conn.commit()

# Veritabanı bağlantısını ve imleci kapatma
cursor.close()
conn.close()
