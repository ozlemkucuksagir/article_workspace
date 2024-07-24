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

# SQL sorgusunu tanımlayın
sql_query = """
DELETE FROM hotels_data
WHERE ctid NOT IN (
  SELECT min_ctid
  FROM (
    SELECT MIN(ctid) AS min_ctid
    FROM hotels_data
    GROUP BY id
    HAVING COUNT(*) > 1
  ) subquery
);
"""

# SQL sorgusunu çalıştırın
cursor.execute(sql_query)

# Değişiklikleri kaydedin
conn.commit()

# Bağlantıyı kapatın
conn.close()
