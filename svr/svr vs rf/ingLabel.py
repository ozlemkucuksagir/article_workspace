import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import sqlite3
import numpy as np

# Veriyi oku
df = pd.read_csv("D:/Projects/Github/article_workspace/svr/oteller.csv")

# Eksik değerleri en sık tekrarlanan değerlerle doldur
df.fillna(df.mode().iloc[0], inplace=True)

# Bağımsız ve bağımlı değişkenleri ayır
X = df.drop(['otel_ad', 'fiyat', 'imageurl', 'bolge', 'id'], axis=1)
y = df['fiyat']

# Eğitim ve test setlerini oluştur
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SVR modelini oluştur ve eğit
model = SVR(kernel='linear')
model.fit(X_train, y_train)

# Tahmin yap
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Hata metriklerini hesapla
train_rmse = mean_squared_error(y_train, y_train_pred, squared=False)
test_rmse = mean_squared_error(y_test, y_test_pred, squared=False)
print("Eğitim seti RMSE:", train_rmse)
print("Test seti RMSE:", test_rmse)
# Özelliklerin katsayılarını yazdırın
print("Özelliklerin Katsayıları:")
for i, feature in enumerate(X.columns):
    print(feature + ":", model.coef_[0][i])
    
# Özelliklerin katsayılarını al
coefficients = model.coef_[0]
features = X.columns

# Özellik isimlerini İngilizce'ye çevir ve numaralandır
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

# Numara ekleyerek yeni özellik isimleri oluştur
features_numbered = [f"{i+1}. {feature_names.get(f, f)}" for i, f in enumerate(features)]

# Grafik oluştur
plt.figure(figsize=(12, 8))
colors = ['orange' if abs(c) > np.percentile(abs(coefficients), 90) else 'turquoise' for c in coefficients]
plt.bar(range(len(coefficients)), coefficients, color=colors)
plt.xlabel('Feature Index')
plt.ylabel('Support Vector Coefficients')
plt.title('Feature Contributions to Support Vectors')
plt.xticks(range(len(features)), range(1, len(features) + 1), rotation=90)
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Grafiği kaydet
plt.savefig("D:/Projects/Github/article_workspace/svr/feature_importance.png", dpi=300, bbox_inches='tight')
plt.close()

# Açıklamaları ayrı bir görsele kaydet
fig, ax = plt.subplots(figsize=(4, len(features) * 0.4))
ax.axis("off")
for i, feature in enumerate(features_numbered):
    ax.text(0, 1 - (i / len(features)), feature, fontsize=10, verticalalignment='center', fontfamily='monospace')
plt.savefig("D:/Projects/article_workspace/svr/img/feature_labels.png", dpi=300, bbox_inches='tight')
plt.close()



# Step 1: Make Your Predictions
predicted_prices = model.predict(X)

# Round the predicted prices to one decimal place
predicted_prices_rounded = [round(abs(price), 1) * (-1 if price < 0 else 1) for price in predicted_prices]

# Step 2: Compare Predictions with Actual Prices and Add Hotel Names and other columns
price_comparison = pd.DataFrame({
    'otel_ad': df['otel_ad'], 
    'fiyat': y, 
    'denize_uzakligi': df['denize_uzakligi'],
    'plaj': df['plaj'],
    'a_la_carte_restoran': df['a_la_carte_restoran'],
    'asansor': df['asansor'],
    'acik_restoran': df['acik_restoran'],
    'kapali_restoran': df['kapali_restoran'],
    'acik_havuz': df['acik_havuz'],
    'kapali_havuz': df['kapali_havuz'],
    'bedensel_engelli_odasi': df['bedensel_engelli_odasi'],
    'bar': df['bar'],
    'su_kaydiragi': df['su_kaydiragi'],
    'balo_salonu': df['balo_salonu'],
    'kuafor': df['kuafor'],
    'otopark': df['otopark'],
    'market': df['market'],
    'sauna': df['sauna'],
    'doktor': df['doktor'],
    'beach_voley': df['beach_voley'],
    'fitness': df['fitness'],
    'canli_eglence': df['canli_eglence'],
    'wireless_internet': df['wireless_internet'],
    'animasyon': df['animasyon'],
    'sorf': df['sorf'],
    'parasut': df['parasut'],
    'arac_kiralama': df['arac_kiralama'],
    'kano': df['kano'],
    'spa': df['spa'],
    'masaj': df['masaj'],
    'masa_tenisi': df['masa_tenisi'],
    'cocuk_havuzu': df['cocuk_havuzu'],
    'cocuk_parki': df['cocuk_parki'],
    'Predicted Price': predicted_prices_rounded
})

# Step 3: Analyze the Calculated Price Difference
price_comparison['Price Difference'] = price_comparison['fiyat'] - price_comparison['Predicted Price']

# Round the price differences to one decimal place
price_comparison['Price Difference'] = [round(abs(diff), 1) * (-1 if diff < 0 else 1) for diff in price_comparison['Price Difference']]

# Step 4: Fine-Tuning
fair_price_threshold = 500  # Let's set a threshold, for example, 500 TL

# Step 5: Calculate fair-price percentage
price_comparison['Fair Price Percentage'] = abs(price_comparison['Price Difference'] / price_comparison['fiyat'] * 100)

# Round fair-price percentage to two decimal places
price_comparison['Fair Price Percentage'] = price_comparison['Fair Price Percentage'].round(2)

# Determine fair price range based on fair-price percentage
price_comparison['Fair Price Range'] = ''
price_comparison.loc[price_comparison['Price Difference'] < 0, 'Fair Price Range'] += ' (Underpriced)'

# Handle division by zero or NaN
price_comparison.loc[price_comparison['fiyat'] == 0, 'Fair Price Percentage'] = float('NaN')
price_comparison.loc[price_comparison['Predicted Price'] == 0, 'Fair Price Percentage'] = float('NaN')

# Determine fair price range based on fair-price percentage
price_comparison['Fair Price Range'] = ''
price_comparison.loc[price_comparison['Fair Price Percentage'] <= 5, 'Fair Price Range'] = 'Fair'
price_comparison.loc[price_comparison['Fair Price Percentage'] > 5, 'Fair Price Range'] = 'Slight Overpriced'
price_comparison.loc[price_comparison['Fair Price Percentage'] > 10, 'Fair Price Range'] = 'Overpriced'
price_comparison.loc[price_comparison['Fair Price Percentage'] > 20, 'Fair Price Range'] = 'Significantly Overpriced'
price_comparison.loc[price_comparison['Price Difference'] < 0, 'Fair Price Range'] += ' (Underpriced)'

# Add + or - sign to Fair Price Percentage column
price_comparison['Fair Price Percentage'] = price_comparison.apply(lambda x: f"{'- ' if x['Price Difference'] > 0 else '+ '}{abs(x['Fair Price Percentage'])}", axis=1)

# Sıralama listesi oluştur
desired_columns = ['otel_ad', 'fiyat', 'Predicted Price', 'Price Difference', 'Fair Price Range', 'Fair Price Percentage',
                   'bar', 'a_la_carte_restoran', 'plaj', 'acik_havuz', 'kapali_havuz', 'fitness',
                   'iskele', 'acik_restoran', 'sauna', 'animasyon', 'kuafor', 'spa', 'masa_tenisi',
                   'market', 'su_kaydiragi', 'beach_voley', 'doktor', 'otopark', 'wireless_internet',
                   'sorf', 'kapali_restoran', 'kano', 'cocuk_parki', 'arac_kiralama', 'balo_salonu',
                   'masaj', 'cocuk_havuzu', 'parasut', 'denize_uzakligi']

# Sıralamayı uygula
price_comparison = price_comparison.reindex(columns=desired_columns)


# Sonuçları veritabanına yaz
conn = sqlite3.connect('otel_veritabani_DB4.db')
df.to_sql('otel_veritabani_DB4', conn, if_exists='replace', index=False)
conn.close()

print("Grafikler başarıyla kaydedildi: feature_importance.png ve feature_labels.png")
print()
# Display price comparison and fair price range
print(price_comparison)