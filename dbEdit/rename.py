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
rename_queries = [
    'ALTER TABLE otel1 RENAME COLUMN "Fiyat Aralığı" TO fiyat_araligi',
    'ALTER TABLE otel1 RENAME COLUMN "Bölge" TO bolge',
    'ALTER TABLE otel1 RENAME COLUMN "Hava Alanına Uzaklığı" TO hava_alanina_uzakligi',
    'ALTER TABLE otel1 RENAME COLUMN "Denize Uzaklığı" TO denize_uzakligi',
    'ALTER TABLE otel1 RENAME COLUMN "Plaj" TO plaj',
    'ALTER TABLE otel1 RENAME COLUMN "İskele" TO iskele',
    'ALTER TABLE otel1 RENAME COLUMN "A la Carte Restoran" TO a_la_carte_restoran',
    'ALTER TABLE otel1 RENAME COLUMN "Asansör" TO asansor',
    'ALTER TABLE otel1 RENAME COLUMN "Açık Restoran" TO acik_restoran',
    'ALTER TABLE otel1 RENAME COLUMN "Kapalı Restoran" TO kapali_restoran',
    'ALTER TABLE otel1 RENAME COLUMN "Açık Havuz" TO acik_havuz',
    'ALTER TABLE otel1 RENAME COLUMN "Kapalı Havuz" TO kapali_havuz',
    'ALTER TABLE otel1 RENAME COLUMN "Bedensel Engelli Odası" TO bedensel_engelli_odasi',
    'ALTER TABLE otel1 RENAME COLUMN "Bar" TO bar',
    'ALTER TABLE otel1 RENAME COLUMN "Su Kaydırağı" TO su_kaydiragi',
    'ALTER TABLE otel1 RENAME COLUMN "Balo Salonu" TO balo_salonu',
    'ALTER TABLE otel1 RENAME COLUMN "Kuaför" TO kuafor',
    'ALTER TABLE otel1 RENAME COLUMN "Otopark" TO otopark',
    'ALTER TABLE otel1 RENAME COLUMN "Market" TO market',
    'ALTER TABLE otel1 RENAME COLUMN "Sauna" TO sauna',
    'ALTER TABLE otel1 RENAME COLUMN "Doktor" TO doktor',
    'ALTER TABLE otel1 RENAME COLUMN "Beach Voley" TO beach_voley',
    'ALTER TABLE otel1 RENAME COLUMN "Fitness" TO fitness',
    'ALTER TABLE otel1 RENAME COLUMN "Canlı Eğlence" TO canli_eglence',
    'ALTER TABLE otel1 RENAME COLUMN "Wireless Internet" TO wireless_internet',
    'ALTER TABLE otel1 RENAME COLUMN "Animasyon" TO animasyon',
    'ALTER TABLE otel1 RENAME COLUMN "Sörf" TO sorf',
    'ALTER TABLE otel1 RENAME COLUMN "Paraşüt" TO parasut',
    'ALTER TABLE otel1 RENAME COLUMN "Araç Kiralama" TO arac_kiralama',
    'ALTER TABLE otel1 RENAME COLUMN "Kano" TO kano',
    'ALTER TABLE otel1 RENAME COLUMN "SPA" TO spa',
    'ALTER TABLE otel1 RENAME COLUMN "Masaj" TO masaj',
    'ALTER TABLE otel1 RENAME COLUMN "Masa Tenisi" TO masa_tenisi',
    'ALTER TABLE otel1 RENAME COLUMN "Çocuk Havuzu" TO cocuk_havuzu',
    'ALTER TABLE otel1 RENAME COLUMN "Çocuk Parkı" TO cocuk_parki'
]

# Her bir sorguyu çalıştırma
for query in rename_queries:
    cursor.execute(query)

# Değişiklikleri kaydetme
conn.commit()

# Veritabanı bağlantısını ve imleci kapatma
cursor.close()
conn.close()
