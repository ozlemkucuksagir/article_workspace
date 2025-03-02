import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

# 📌 **Feature listesi kaydetme fonksiyonu (Updated version without Top part)**
def save_feature_labels(features, filename):
    feature_names = {
        "score": "User Ratings", "hava_alanina_uzakligi": "Distance to Airport",
        "denize_uzakligi": "Distance to Sea", "plaj": "Beach", "iskele": "Pier",
        "a_la_carte_restoran": "A La Carte Restaurant", "asansor": "Elevator",
        "acik_restoran": "Open Restaurant", "kapali_restoran": "Indoor Restaurant",
        "acik_havuz": "Outdoor Pool", "kapali_havuz": "Indoor Pool",
        "bedensel_engelli_odasi": "Disabled Room", "bar": "Bar",
        "su_kaydiragi": "Water Slide", "balo_salonu": "Ballroom",
        "kuafor": "Hairdresser", "otopark": "Parking", "market": "Market",
        "sauna": "Sauna", "doktor": "Doctor", "beach_voley": "Beach Volleyball",
        "fitness": "Fitness", "canli_eglence": "Live Entertainment",
        "wireless_internet": "WiFi", "animasyon": "Animation", "sorf": "Surf",
        "parasut": "Parachute", "arac_kiralama": "Car Rental",
        "kano": "Canoe", "spa": "Spa", "masaj": "Massage",
        "masa_tenisi": "Table Tennis", "cocuk_havuzu": "Kids Pool",
        "cocuk_parki": "Kids Park"
    }

    fig, ax = plt.subplots(figsize=(3.5, len(features) * 0.4))
    ax.axis("off")

    # 📌 **Feature listesi yazımı**
    for i, f in enumerate(features):
        ax.text(0, 1 - (i / len(features)), f"{i+1}. {feature_names.get(f, f)}", fontsize=10,
                verticalalignment='center', fontfamily='monospace', color='black')

    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

# Function to plot feature importance comparison (with SVR, Ridge, Lasso, RandomForest) and average SVR & RandomForest
def plot_combined_feature_importance(norm_coeff_df, features, filename):
    # Normalize feature importance
    svr_vals = norm_coeff_df['SVR'].values
    ridge_vals = norm_coeff_df['Ridge'].values
    lasso_vals = norm_coeff_df['Lasso'].values
    rf_vals = norm_coeff_df['RandomForest'].values
    svr_rf_avg_importance = (svr_vals + rf_vals) / 2

    # Sort values in descending order
    sorted_idx = np.argsort(svr_rf_avg_importance)[::-1]  # Sort by the average importance (SVR + RF)
    
    # Sorted features and importance values
    sorted_features = np.array(features)[sorted_idx]
    sorted_svr_vals = svr_vals[sorted_idx]
    sorted_ridge_vals = ridge_vals[sorted_idx]
    sorted_lasso_vals = lasso_vals[sorted_idx]
    sorted_rf_vals = rf_vals[sorted_idx]
    sorted_svr_rf_avg_importance = svr_rf_avg_importance[sorted_idx]

    # Bar positions
    x = np.arange(len(sorted_features))
    width = 0.2

    # Create color mapping for top 20% features based on SVR & RandomForest average importance
    top_20_percent = int(0.2 * len(sorted_features))
    color_mapping = {i: 'turquoise' if i < top_20_percent else 'gray' for i in range(len(sorted_features))}

    # Plot
    plt.figure(figsize=(16, 8))
    
    # Define bar positions
    pos_svr = x - 1.5 * width
    pos_ridge = x - 0.5 * width
    pos_lasso = x + 0.5 * width
    pos_rf = x + 1.5 * width
    
    # Plot bars
    plt.bar(pos_svr, sorted_svr_vals, width, color='blue', label='SVR')
    plt.bar(pos_ridge, sorted_ridge_vals, width, color='green', label='Ridge')
    plt.bar(pos_lasso, sorted_lasso_vals, width, color='purple', label='Lasso')
    plt.bar(pos_rf, sorted_rf_vals, width, color='orange', label='RandomForest')
    
    # Plot the average of SVR & RandomForest as a line
    plt.plot(x, sorted_svr_rf_avg_importance, color='red', label='SVR & RandomForest Avg', linewidth=2, marker='o')

    # Labeling and formatting
    plt.xlabel('Feature Index', fontsize=12)
    plt.ylabel('Normalized Importance', fontsize=12)
    plt.title('Feature Importance Comparison (Sorted) & SVR & RandomForest Avg', fontsize=14)
    plt.xticks(x, range(1, len(sorted_features) + 1), rotation=90)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Save plot
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

    # 📌 **Save feature labels with corresponding sorted features based on average importance**
    save_feature_labels(sorted_features, "twoMean/feature_labels.png")

# Read data
df = pd.read_csv("D:/Projects/Github/article_workspace/svr/oteller.csv")
df.fillna(df.mode().iloc[0], inplace=True)

# Split independent and dependent variables
X = df.drop(['otel_ad', 'fiyat', 'imageurl', 'bolge', 'id'], axis=1)
y = df['fiyat']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Models
defined_models = {
    'SVR': SVR(kernel='linear'),
    'Ridge': Ridge(),
    'Lasso': Lasso(),
    'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42)
}

coefficients_dict = {}
rmse_results_test = {}

for name, model in defined_models.items():
    model.fit(X_train, y_train)
    y_pred_test = model.predict(X_test)
    rmse_results_test[name] = np.sqrt(mean_squared_error(y_test, y_pred_test))
    
    if hasattr(model, 'coef_'):
        coef = model.coef_
        if coef.ndim > 1:
            coef = coef[0]
        coefficients_dict[name] = coef
    elif hasattr(model, 'feature_importances_'):
        coefficients_dict[name] = model.feature_importances_

# Normalize feature importance
normalized_coeffs = {name: coeff / np.sum(np.abs(coeff)) for name, coeff in coefficients_dict.items()}
norm_coeff_df = pd.DataFrame(normalized_coeffs, index=X.columns)

# Save combined feature importance plot
plot_combined_feature_importance(norm_coeff_df, X.columns, "twoMean/combined_feature_importance.png")

# SVR & RandomForest average prediction
predictions = {name: model.predict(X) for name, model in defined_models.items()}
preds_svr_rf = (predictions['SVR'] + predictions['RandomForest']) / 2
predicted_prices_rounded = [round(abs(price), 1) * (-1 if price < 0 else 1) for price in preds_svr_rf]

# Fair Price Calculation
price_comparison = pd.DataFrame({
    'otel_ad': df['otel_ad'],
    'fiyat': y,
    'Predicted Price (SVR & RF)': predicted_prices_rounded
})

price_comparison['Price Difference'] = price_comparison['fiyat'] - price_comparison['Predicted Price (SVR & RF)']
price_comparison['Fair Price Percentage'] = abs(price_comparison['Price Difference'] / price_comparison['fiyat'] * 100).round(2)

price_comparison['Fair Price Range'] = ''
price_comparison.loc[price_comparison['Fair Price Percentage'] <= 5, 'Fair Price Range'] = 'Fair'
price_comparison.loc[(price_comparison['Fair Price Percentage'] > 5) & (price_comparison['Fair Price Percentage'] <= 10), 'Fair Price Range'] = 'Slight Overpriced'
price_comparison.loc[(price_comparison['Fair Price Percentage'] > 10) & (price_comparison['Fair Price Percentage'] <= 20), 'Fair Price Range'] = 'Overpriced'
price_comparison.loc[price_comparison['Fair Price Percentage'] > 20, 'Fair Price Range'] = 'Significantly Overpriced'

# Save results
price_comparison.to_csv("twoMean/price_comparison_svr_rf.csv", index=False)
print("Combined feature importance plot saved: combined_feature_importance.png")
print("Feature labels saved: feature_labels.png")
print("Fair price calculation completed based on SVR & RF average.")
