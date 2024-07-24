import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import sqlite3

# Veritabanınızdan verileri çekin
df = pd.read_csv("D:/Projects/Github/article_workspace/svr/duzenlenmis_otel_veritabani_DB4.csv")


#df.dropna(inplace=True)

# Eksik değerleri ortalama değerlerle doldur
#df.fillna(df.mean(), inplace=True)

# Eksik değerleri en sık tekrarlanan değerlerle doldur
df.fillna(df.mode().iloc[0], inplace=True)
print(df)

# Eğitim ve test setleri
X = df.drop(['otel_ad', 'fiyat','imageurl', 'bolge', 'id'], axis=1) # Bağımsız değişkenler
y = df['fiyat'] # Bağımlı değişken



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SVR modelini
model = SVR(kernel='linear')  # Linear kernel kullanarak SVR modeli
model.fit(X_train, y_train)

# Eğitim ve test setleri üzerinde tahmin
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Hata metriklerini hesap
train_rmse = mean_squared_error(y_train, y_train_pred, squared=False)
test_rmse = mean_squared_error(y_test, y_test_pred, squared=False)


print("Eğitim seti RMSE:", train_rmse)
print("Test seti RMSE:", test_rmse)


# Özelliklerin katsayılarını yazdırın
print("Özelliklerin Katsayıları:")
for i, feature in enumerate(X.columns):
    print(feature + ":", model.coef_[0][i])
    


# Destek vektörlerinin katsayıları
coefficients = model.coef_[0]


# Özellik isimlerini alın
features = X.columns


# Özelliklerin destek vektörlerine katkısını gösteren bir plot
plt.figure(figsize=(100, 50))
plt.bar(features, coefficients, color='green')
plt.xlabel('Özellikler')
plt.ylabel('Destek Vektör Katsayıları')
plt.title('Özelliklerin Destek Vektörlerine Katkısı')
plt.xticks(rotation=90)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()


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

# Create a SQLite database and write the DataFrame to it
conn = sqlite3.connect('otel_veritabani_DB4.db')
price_comparison.to_sql('otel_veritabani_DB4', conn, if_exists='replace', index=False)
conn.close()

# Display price comparison and fair price range
print(price_comparison)