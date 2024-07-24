import pandas as pd

# CSV dosyasını yükleyin
df = pd.read_csv('D:/Projects/Github/article_workspace/dbEdit/duzenlenmis_otel_202405072236.csv')

# Sütun adlarını değiştirin
df.rename(columns={'Hava Alanına Uzaklığı': 'hava_alanina_uzakligi', 'Denize Uzaklığı': 'denize_uzakligi'}, inplace=True)

# Değişiklikleri içeren yeni CSV dosyasını kaydedin
df.to_csv('yeni_duzenlenmis_otel_202405072236.csv', index=False)

print("Sütun adları başarıyla değiştirildi.")
