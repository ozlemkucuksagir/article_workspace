import pandas as pd

# CSV dosyasını yükle
df = pd.read_csv('duzenlenmis_otel_veritabani.csv')

# Türkçe karakterleri İngilizce karakterlere çevirmek için bir fonksiyon
def replace_turkish_chars(text):
    replacements = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return text.translate(replacements)

# Tüm dataframe'deki string verileri dönüştürmek için applymap fonksiyonunu kullanın
df = df.applymap(lambda x: replace_turkish_chars(x) if isinstance(x, str) else x)

# Dönüştürülmüş veriyi yeni bir CSV dosyasına kaydedin
df.to_csv('duzenlenmis_otel_veritabani.csv',index=False)