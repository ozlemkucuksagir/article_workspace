import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

# Veri temizleme fonksiyonu
def clean_data(df):
    df.fillna(df.mode().iloc[0], inplace=True)
    return df

# SVR modelini eğitme fonksiyonu
def train_svr_model(X_train, y_train):
    svr_model = SVR(kernel='linear')
    svr_model.fit(X_train, y_train)
    return svr_model

# Random Forest modelini eğitme fonksiyonu
def train_random_forest_model(X_train, y_train):
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    return rf_model

# Grafik oluşturma fonksiyonu
def plot_comparison(svr_coefficients, rf_feature_importances, features, filename):
    plt.figure(figsize=(12, 8))

    # SVR Katsayıları
    plt.subplot(1, 2, 1)
    plt.bar(range(len(svr_coefficients)), svr_coefficients, color='orange')
    plt.xlabel('Feature Index')
    plt.ylabel('SVR Coefficients')
    plt.title('SVR Feature Coefficients')

    # Random Forest Feature Importance
    plt.subplot(1, 2, 2)
    plt.bar(range(len(rf_feature_importances)), rf_feature_importances, color='green')
    plt.xlabel('Feature Index')
    plt.ylabel('Random Forest Feature Importance')
    plt.title('Random Forest Feature Importance')

    # Ortak başlık
    plt.suptitle('SVR ve Random Forest Özellik Karşılaştırması', fontsize=14)

    # Kaydet ve göster
    plt.tight_layout()
    plt.savefig(filename, dpi=300)

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

# SVR modelini eğit ve tahmin yap
svr_model = train_svr_model(X_train, y_train)
svr_y_train_pred = svr_model.predict(X_train)
svr_y_test_pred = svr_model.predict(X_test)

# Random Forest modelini eğit ve tahmin yap
rf_model = train_random_forest_model(X_train, y_train)
rf_y_train_pred = rf_model.predict(X_train)
rf_y_test_pred = rf_model.predict(X_test)

# Hata metriklerini hesapla
svr_train_rmse = mean_squared_error(y_train, svr_y_train_pred, squared=False)
svr_test_rmse = mean_squared_error(y_test, svr_y_test_pred, squared=False)
rf_train_rmse = mean_squared_error(y_train, rf_y_train_pred, squared=False)
rf_test_rmse = mean_squared_error(y_test, rf_y_test_pred, squared=False)

print("SVR Eğitim seti RMSE:", svr_train_rmse)
print("SVR Test seti RMSE:", svr_test_rmse)
print("Random Forest Eğitim seti RMSE:", rf_train_rmse)
print("Random Forest Test seti RMSE:", rf_test_rmse)

# SVR katsayılarını al
svr_coefficients = svr_model.coef_[0]
# Random Forest feature importance
rf_feature_importances = rf_model.feature_importances_
features = X.columns

# Grafik oluştur
plot_comparison(svr_coefficients, rf_feature_importances, features, "D:/Projects/article_workspace/svr/img/model_comparison.png")

# Fiyat tahminlerini yap
svr_predicted_prices = svr_model.predict(X)
rf_predicted_prices = rf_model.predict(X)

# Yuvarlanmış fiyatları hesapla
svr_predicted_prices_rounded = [round(abs(price), 1) * (-1 if price < 0 else 1) for price in svr_predicted_prices]
rf_predicted_prices_rounded = [round(abs(price), 1) * (-1 if price < 0 else 1) for price in rf_predicted_prices]

# Fiyat karşılaştırması ve sonuçları birleştirme
price_comparison_svr = pd.DataFrame({
    'otel_ad': df['otel_ad'], 
    'fiyat': y, 
    'SVR Predicted Price': svr_predicted_prices_rounded,
    'RF Predicted Price': rf_predicted_prices_rounded
})

# Fiyat farkını hesapla
price_comparison_svr['SVR Price Difference'] = price_comparison_svr['fiyat'] - price_comparison_svr['SVR Predicted Price']
price_comparison_svr['RF Price Difference'] = price_comparison_svr['fiyat'] - price_comparison_svr['RF Predicted Price']

# Yüzdelik hesaplamalar
price_comparison_svr['SVR Fair Price Percentage'] = abs(price_comparison_svr['SVR Price Difference'] / price_comparison_svr['fiyat'] * 100)
price_comparison_svr['RF Fair Price Percentage'] = abs(price_comparison_svr['RF Price Difference'] / price_comparison_svr['fiyat'] * 100)

# Yüzde hesaplamayı yuvarla
price_comparison_svr['SVR Fair Price Percentage'] = price_comparison_svr['SVR Fair Price Percentage'].round(2)
price_comparison_svr['RF Fair Price Percentage'] = price_comparison_svr['RF Fair Price Percentage'].round(2)

# Fiyat aralığını belirleme
price_comparison_svr['SVR Fair Price Range'] = ''
price_comparison_svr['RF Fair Price Range'] = ''

price_comparison_svr.loc[price_comparison_svr['SVR Fair Price Percentage'] <= 5, 'SVR Fair Price Range'] = 'Fair'
price_comparison_svr.loc[price_comparison_svr['RF Fair Price Percentage'] <= 5, 'RF Fair Price Range'] = 'Fair'

price_comparison_svr.loc[price_comparison_svr['SVR Fair Price Percentage'] > 5, 'SVR Fair Price Range'] = 'Slight Overpriced'
price_comparison_svr.loc[price_comparison_svr['RF Fair Price Percentage'] > 5, 'RF Fair Price Range'] = 'Slight Overpriced'

price_comparison_svr.loc[price_comparison_svr['SVR Fair Price Percentage'] > 10, 'SVR Fair Price Range'] = 'Overpriced'
price_comparison_svr.loc[price_comparison_svr['RF Fair Price Percentage'] > 10, 'RF Fair Price Range'] = 'Overpriced'

price_comparison_svr.loc[price_comparison_svr['SVR Fair Price Percentage'] > 20, 'SVR Fair Price Range'] = 'Significantly Overpriced'
price_comparison_svr.loc[price_comparison_svr['RF Fair Price Percentage'] > 20, 'RF Fair Price Range'] = 'Significantly Overpriced'

# Veritabanına kaydet
conn = sqlite3.connect('otel_veritabani_DB4.db')
df.to_sql('otel_veritabani_DB4', conn, if_exists='replace', index=False)
conn.close()

# CSV olarak kaydet
price_comparison_svr.to_csv("D:/Projects/article_workspace/svr/img/price_comparison_svr.csv", index=False)

print("Grafikler başarıyla kaydedildi: model_comparison.png")
print("CSV başarıyla kaydedildi: price_comparison_svr.csv")
print(price_comparison_svr)
