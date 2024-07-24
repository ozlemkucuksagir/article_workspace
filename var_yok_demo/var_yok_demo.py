import pandas as pd

# CSV dosyasını oku
df = pd.read_csv("duzenlenmis_otel_veritabani_DB4.csv")

# İlk 5 satırı al
first_five_rows = df.head()

# İlk 5 satırı tam olarak yazdır
print("İlk 5 Satır:")
print(first_five_rows.to_string())
