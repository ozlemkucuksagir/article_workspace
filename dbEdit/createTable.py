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

# Tabloyu oluşturma SQL sorgusu
create_table_query = '''
CREATE TABLE IF NOT EXISTS public.oteller (
    id SERIAL PRIMARY KEY,
    otel_ad VARCHAR(255),
    fiyat NUMERIC,
    imageurl VARCHAR(255),
    score NUMERIC,
    bolge VARCHAR(255),
    hava_alanina_uzakligi NUMERIC,
    denize_uzakligi NUMERIC,
    plaj NUMERIC,
    iskele NUMERIC,
    a_la_carte_restoran NUMERIC,
    asansor NUMERIC,
    acik_restoran NUMERIC,
    kapali_restoran NUMERIC,
    acik_havuz NUMERIC,
    kapali_havuz NUMERIC,
    bedensel_engelli_odasi NUMERIC,
    bar NUMERIC,
    su_kaydiragi NUMERIC,
    balo_salonu NUMERIC,
    kuafor NUMERIC,
    otopark NUMERIC,
    market NUMERIC,
    sauna NUMERIC,
    doktor NUMERIC,
    beach_voley NUMERIC,
    fitness NUMERIC,
    canli_eglence NUMERIC,
    wireless_internet NUMERIC,
    animasyon NUMERIC,
    sorf NUMERIC,
    parasut NUMERIC,
    arac_kiralama NUMERIC,
    kano NUMERIC,
    spa NUMERIC,
    masaj NUMERIC,
    masa_tenisi NUMERIC,
    cocuk_havuzu NUMERIC,
    cocuk_parki NUMERIC
);
'''

# Tablo oluşturma sorgusunu çalıştırma
cursor.execute(create_table_query)

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
cursor.close()
conn.close()

print("Tablo başarıyla oluşturuldu.")
