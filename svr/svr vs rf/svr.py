import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

# Veri temizleme fonksiyonu
def clean_data(df):
    df.fillna(df.mode().iloc[0], inplace=True)
    return df

# Modeli eğitme fonksiyonu
def train_model(X_train, y_train):
    model = SVR(kernel='linear')
    model.fit(X_train, y_train)
    return model

# Grafik oluşturma fonksiyonu
def plot_coefficients(coefficients, features, filename):
    colors = ['orange' if abs(c) > np.percentile(abs(coefficients), 90) else 'turquoise' for c in coefficients]
    plt.figure(figsize=(12, 8))
    plt.bar(range(len(coefficients)), coefficients, color=colors)
    plt.xlabel('Feature Index')
    plt.ylabel('Support Vector Coefficients')
    plt.title('Feature Contributions to Support Vectors')
    plt.xticks(range(len(features)), range(1, len(features) + 1), rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

# Özellik etiketlerini kaydetme fonksiyonu
def save_feature_labels(features, filename):
    feature_names = {
    "score": "Score",
    "hava_alanina_uzakligi": "Distance to Airport",
    "denize_uzakligi": "Distance to Sea",
    "plaj": "Beach",
    "iskele": "Pier",
    "a_la_carte_restoran": "A La Carte Restaurant",
    "asansor": "Elevator",
    "acik_restoran": "Open Restaurant",
    "kapali_restoran": "Indoor Restaurant",
    "acik_havuz": "Outdoor Pool",
    "kapali_havuz": "Indoor Pool",
    "bedensel_engelli_odasi": "Disabled Room",
    "bar": "Bar",
    "su_kaydiragi": "Water Slide",
    "balo_salonu": "Ballroom",
    "kuafor": "Hairdresser",
    "otopark": "Parking",
    "market": "Market",
    "sauna": "Sauna",
    "doktor": "Doctor",
    "beach_voley": "Beach Volleyball",
    "fitness": "Fitness",
    "canli_eglence": "Live Entertainment",
    "wireless_internet": "WiFi",
    "animasyon": "Animation",
    "sorf": "Surf",
    "parasut": "Parachute",
    "arac_kiralama": "Car Rental",
    "kano": "Canoe",
    "spa": "Spa",
    "masaj": "Massage",
    "masa_tenisi": "Table Tennis",
    "cocuk_havuzu": "Kids Pool",
    "cocuk_parki": "Kids Park"
}
    features_numbered = [f"{i+1}. {feature_names.get(f, f)}" for i, f in enumerate(features)]
    fig, ax = plt.subplots(figsize=(4, len(features) * 0.4))
    ax.axis("off")
    for i, feature in enumerate(features_numbered):
        ax.text(0, 1 - (i / len(features)), feature, fontsize=10, verticalalignment='center', fontfamily='monospace')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

# Veriyi oku ve temizle
df = pd.read_csv("D:/Projects/Github/article_workspace/svr/oteller.csv")
df = clean_data(df)

# Bağımsız ve bağımlı değişkenleri ayır
X = df.drop(['otel_ad', 'fiyat', 'imageurl', 'bolge', 'id'], axis=1)
y = df['fiyat']

# Eğitim ve test setlerini oluştur
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeli eğit ve tahmin yap
model = train_model(X_train, y_train)
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Hata metriklerini hesapla
train_rmse = mean_squared_error(y_train, y_train_pred, squared=False)
test_rmse = mean_squared_error(y_test, y_test_pred, squared=False)
print("Eğitim seti RMSE:", train_rmse)
print("Test seti RMSE:", test_rmse)

# Özelliklerin katsayılarını al
coefficients = model.coef_[0]
features = X.columns

# Grafik oluştur
plot_coefficients(coefficients, features, "D:/Projects/article_workspace/svr/img/feature_importance_SVR.png")

# Özellik etiketlerini kaydet
save_feature_labels(features, "D:/Projects/article_workspace/svr/img/feature_labels_SVR.png")

# Fiyat tahminlerini yap
predicted_prices = model.predict(X)

# Yuvarlanmış fiyatları hesapla
predicted_prices_rounded = [round(abs(price), 1) * (-1 if price < 0 else 1) for price in predicted_prices]

# Fiyat karşılaştırması ve sonuçları birleştirme
price_comparison = pd.DataFrame({
    'otel_ad': df['otel_ad'], 
    'fiyat': y, 
    'Predicted Price': predicted_prices_rounded
})

# Fiyat farkını hesapla
price_comparison['Price Difference'] = price_comparison['fiyat'] - price_comparison['Predicted Price']
price_comparison['Price Difference'] = [round(abs(diff), 1) * (-1 if diff < 0 else 1) for diff in price_comparison['Price Difference']]

# Yüzdelik hesaplamalar
price_comparison['Fair Price Percentage'] = abs(price_comparison['Price Difference'] / price_comparison['fiyat'] * 100)
price_comparison['Fair Price Percentage'] = price_comparison['Fair Price Percentage'].round(2)

# Fiyat aralığını belirleme
price_comparison['Fair Price Range'] = ''
price_comparison.loc[price_comparison['Fair Price Percentage'] <= 5, 'Fair Price Range'] = 'Fair'
price_comparison.loc[price_comparison['Fair Price Percentage'] > 5, 'Fair Price Range'] = 'Slight Overpriced'
price_comparison.loc[price_comparison['Fair Price Percentage'] > 10, 'Fair Price Range'] = 'Overpriced'
price_comparison.loc[price_comparison['Fair Price Percentage'] > 20, 'Fair Price Range'] = 'Significantly Overpriced'

# Veritabanına kaydet
conn = sqlite3.connect('otel_veritabani_DB4.db')
df.to_sql('otel_veritabani_DB4', conn, if_exists='replace', index=False)
conn.close()

print("Grafikler başarıyla kaydedildi: feature_importance.png ve feature_labels.png")
print(price_comparison)
