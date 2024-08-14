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

# Sütun adlarını güncelleme
# ALTER TABLE oteller RENAME COLUMN fiyat_araligi TO "Fiyat Aralığı";
cursor.execute('''
    
    ALTER TABLE oteller RENAME COLUMN bolge TO "Bölge";
    ALTER TABLE oteller RENAME COLUMN hava_alanina_uzakligi TO "Hava Alanına Uzaklığı";
    ALTER TABLE oteller RENAME COLUMN denize_uzakligi TO "Denize Uzaklığı";
    ALTER TABLE oteller RENAME COLUMN plaj TO "Plaj";
    ALTER TABLE oteller RENAME COLUMN iskele TO "İskele";
    ALTER TABLE oteller RENAME COLUMN a_la_carte_restoran TO "A la Carte Restoran";
    ALTER TABLE oteller RENAME COLUMN asansor TO "Asansör";
    ALTER TABLE oteller RENAME COLUMN acik_restoran TO "Açık Restoran";
    ALTER TABLE oteller RENAME COLUMN kapali_restoran TO "Kapalı Restoran";
    ALTER TABLE oteller RENAME COLUMN acik_havuz TO "Açık Havuz";
    ALTER TABLE oteller RENAME COLUMN kapali_havuz TO "Kapalı Havuz";
    ALTER TABLE oteller RENAME COLUMN bedensel_engelli_odasi TO "Bedensel Engelli Odası";
    ALTER TABLE oteller RENAME COLUMN bar TO "Bar";
    ALTER TABLE oteller RENAME COLUMN su_kaydiragi TO "Su Kaydırağı";
    ALTER TABLE oteller RENAME COLUMN balo_salonu TO "Balo Salonu";
    ALTER TABLE oteller RENAME COLUMN kuafor TO "Kuaför";
    ALTER TABLE oteller RENAME COLUMN otopark TO "Otopark";
    ALTER TABLE oteller RENAME COLUMN market TO "Market";
    ALTER TABLE oteller RENAME COLUMN sauna TO "Sauna";
    ALTER TABLE oteller RENAME COLUMN doktor TO "Doktor";
    ALTER TABLE oteller RENAME COLUMN beach_voley TO "Beach Voley";
    ALTER TABLE oteller RENAME COLUMN fitness TO "Fitness";
    ALTER TABLE oteller RENAME COLUMN canli_eglence TO "Canlı Eğlence";
    ALTER TABLE oteller RENAME COLUMN wireless_internet TO "Wireless Internet";
    ALTER TABLE oteller RENAME COLUMN animasyon TO "Animasyon";
    ALTER TABLE oteller RENAME COLUMN sorf TO "Sörf";
    ALTER TABLE oteller RENAME COLUMN parasut TO "Paraşüt";
    ALTER TABLE oteller RENAME COLUMN arac_kiralama TO "Araç Kiralama";
    ALTER TABLE oteller RENAME COLUMN kano TO "Kano";
    ALTER TABLE oteller RENAME COLUMN spa TO "SPA";
    ALTER TABLE oteller RENAME COLUMN masaj TO "Masaj";
    ALTER TABLE oteller RENAME COLUMN masa_tenisi TO "Masa Tenisi";
    ALTER TABLE oteller RENAME COLUMN cocuk_havuzu TO "Çocuk Havuzu";
    ALTER TABLE oteller RENAME COLUMN cocuk_parki TO "Çocuk Parkı";
''')

# Değişiklikleri veritabanına yansıtma ve bağlantıyı kapatma
conn.commit()
cursor.close()
conn.close()
