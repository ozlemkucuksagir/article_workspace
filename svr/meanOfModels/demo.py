import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

# Data cleaning function
def clean_data(df):
    df.fillna(df.mode().iloc[0], inplace=True)
    return df

# Function to save feature labels as a separate image
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

# Read and clean data
df = pd.read_csv("D:/Projects/Github/article_workspace/svr/oteller.csv")
df = clean_data(df)

# Split independent and dependent variables
X = df.drop(['otel_ad', 'fiyat', 'imageurl', 'bolge', 'id'], axis=1)
y = df['fiyat']

# Create training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the models to be used
models = {
    'SVR': SVR(kernel='linear'),
    'Ridge': Ridge(),
    'Lasso': Lasso(),
    'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42)
}

# Store each model's coefficients or feature importances
coefficients_dict = {}
rmse_results = {}  # RMSE değerlerini saklamak için bir sözlük

for name, model in models.items():
    model.fit(X_train, y_train)

    # Tahmin yap ve RMSE hesapla
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    rmse_results[name] = rmse

    if hasattr(model, 'coef_'):
        coef = model.coef_
        if coef.ndim > 1:
            coef = coef[0]
        coefficients_dict[name] = coef
    elif hasattr(model, 'feature_importances_'):
        coefficients_dict[name] = model.feature_importances_

# RMSE sonuçlarını ekrana bastır
print("\nRoot Mean Squared Error (RMSE) for each model:")
for name, rmse in rmse_results.items():
    print(f"{name}: {rmse:.2f}")

# Save the price comparison table as CSV
price_comparison = pd.DataFrame({
    'otel_ad': df['otel_ad'],
    'fiyat': y,
})
price_comparison.to_csv("price_comparison.csv", index=False)

# Save the data to a SQLite database
conn = sqlite3.connect('otel_veritabani_DB4.db')
df.to_sql('otel_veritabani_DB4', conn, if_exists='replace', index=False)
conn.close()

print("Price comparison table saved as 'price_comparison.csv'.")
