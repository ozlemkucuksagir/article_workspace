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

# Function to plot grouped bar chart for each model's normalized feature importance,
# the average across models, and highlight outliers (features above 90th percentile in average)
def plot_grouped_bar(norm_coeff_df, features, filename):
    x = np.arange(len(features))
    width = 0.15
    plt.figure(figsize=(16, 8))
    
    # Colors for each model and average
    colors = {
        'SVR': 'blue',
        'Ridge': 'green',
        'Lasso': 'purple',
        'RandomForest': 'orange',
        'Average': 'red'
    }
    
    # Define bar positions for each model output and average
    pos_svr = x - 2*width
    pos_ridge = x - width
    pos_lasso = x
    pos_rf = x + width
    pos_avg = x + 2*width
    
    # Retrieve normalized importance values for each model and average
    svr_vals = norm_coeff_df['SVR'].values
    ridge_vals = norm_coeff_df['Ridge'].values
    lasso_vals = norm_coeff_df['Lasso'].values
    rf_vals = norm_coeff_df['RandomForest'].values
    avg_vals = norm_coeff_df['Average'].values
    
    # Plot bars for each model with their respective colors
    plt.bar(pos_svr, svr_vals, width, color=colors['SVR'], label='SVR')
    plt.bar(pos_ridge, ridge_vals, width, color=colors['Ridge'], label='Ridge')
    plt.bar(pos_lasso, lasso_vals, width, color=colors['Lasso'], label='Lasso')
    plt.bar(pos_rf, rf_vals, width, color=colors['RandomForest'], label='RandomForest')
    plt.bar(pos_avg, avg_vals, width, color=colors['Average'], label='Average')
    
    # Highlight outliers in the Average values (above 90th percentile)
    threshold = np.percentile(np.abs(avg_vals), 90)
    outlier_labeled = False
    for i, val in enumerate(avg_vals):
        if abs(val) > threshold:
            if not outlier_labeled:
                plt.scatter(pos_avg[i], val, color='gold', marker='*', s=200, zorder=5, label='Outliers')
                outlier_labeled = True
            else:
                plt.scatter(pos_avg[i], val, color='gold', marker='*', s=200, zorder=5)
    
    plt.xlabel('Feature Index', fontsize=12)
    plt.ylabel('Normalized Importance', fontsize=12)
    plt.title('Feature Importance Comparison', fontsize=14)
    plt.xticks(x, range(1, len(features) + 1), rotation=90)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
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
rmse_results_train = {}  # RMSE değerlerini saklamak için bir sözlük (eğitim seti)
rmse_results_test = {}  # RMSE değerlerini saklamak için bir sözlük (test seti)

for name, model in models.items():
    model.fit(X_train, y_train)
    

    # Tahmin yap ve RMSE hesapla (Test Seti)
    y_pred_test = model.predict(X_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    rmse_results_test[name] = rmse_test

    # Tahmin yap ve RMSE hesapla (Eğitim Seti)
    y_pred_train = model.predict(X_train)
    rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
    rmse_results_train[name] = rmse_train
  
    if hasattr(model, 'coef_'):
        coef = model.coef_
        if coef.ndim > 1:
            coef = coef[0]
        coefficients_dict[name] = coef
    elif hasattr(model, 'feature_importances_'):
        coefficients_dict[name] = model.feature_importances_

# RMSE sonuçlarını ekrana bastır
print("\nRoot Mean Squared Error (RMSE) for each model:")
print("Test Set Results:")
for name, rmse in rmse_results_test.items():
    print(f"{name}: {rmse:.2f}")

print("\nTraining Set Results:")
for name, rmse in rmse_results_train.items():
    print(f"{name}: {rmse:.2f}")
        

# Create a DataFrame with coefficients/importances for each model
coeff_df = pd.DataFrame(coefficients_dict, index=X.columns)
print("Feature coefficients/importances for each model:")
print(coeff_df)

# Normalize each model's coefficients/importances (dividing by the sum of absolute values)
normalized_coeffs = {}
for name, coeff in coefficients_dict.items():
    normalized_coeffs[name] = coeff / np.sum(np.abs(coeff))

norm_coeff_df = pd.DataFrame(normalized_coeffs, index=X.columns)
norm_coeff_df['Average'] = norm_coeff_df.mean(axis=1)
print("\nNormalized and averaged feature importances:")
print(norm_coeff_df['Average'])

# Plot the grouped bar chart showing each model's output, the average, and highlighted outliers
plot_grouped_bar(norm_coeff_df, X.columns, "D:/Projects/article_workspace/svr/img/model_importance_grouped.png")

# Save feature labels separately
save_feature_labels(X.columns, "D:/Projects/article_workspace/svr/img/feature_labels.png")

# ----------------- Price Prediction Based on Average of All Models ----------------- #
# Compute predictions for each model
predictions = {}
for name, model in models.items():
    predictions[name] = model.predict(X)

# Stack predictions and compute average prediction across models
preds = np.column_stack(list(predictions.values()))
avg_prediction = preds.mean(axis=1)
predicted_prices_rounded = [round(abs(price), 1) * (-1 if price < 0 else 1) for price in avg_prediction]

# Create a price comparison DataFrame using the average prediction
price_comparison = pd.DataFrame({
    'otel_ad': df['otel_ad'],
    'fiyat': y,
    'Predicted Price (Average)': predicted_prices_rounded
})

# Calculate the price difference and fair price percentage based on the average prediction
price_comparison['Price Difference'] = price_comparison['fiyat'] - price_comparison['Predicted Price (Average)']
price_comparison['Price Difference'] = [round(abs(diff), 1) * (-1 if diff < 0 else 1) for diff in price_comparison['Price Difference']]
price_comparison['Fair Price Percentage'] = abs(price_comparison['Price Difference'] / price_comparison['fiyat'] * 100).round(2)

# Determine Fair Price Range based on the average prediction
price_comparison['Fair Price Range'] = ''
price_comparison.loc[price_comparison['Fair Price Percentage'] <= 5, 'Fair Price Range'] = 'Fair'
price_comparison.loc[(price_comparison['Fair Price Percentage'] > 5) & (price_comparison['Fair Price Percentage'] <= 10), 'Fair Price Range'] = 'Slight Overpriced'
price_comparison.loc[(price_comparison['Fair Price Percentage'] > 10) & (price_comparison['Fair Price Percentage'] <= 20), 'Fair Price Range'] = 'Overpriced'
price_comparison.loc[price_comparison['Fair Price Percentage'] > 20, 'Fair Price Range'] = 'Significantly Overpriced'
# ------------------------------------------------------------------------------------ #

# Save the data to a SQLite database
conn = sqlite3.connect('otel_veritabani_DB4.db')
df.to_sql('otel_veritabani_DB4', conn, if_exists='replace', index=False)
conn.close()

# Save the price comparison table as CSV
price_comparison.to_csv("price_comparison.csv", index=False)

print("Plots saved successfully: model_importance_grouped.png and feature_labels.png")
print("\nPrice comparison table based on the average prediction:")
print(price_comparison)
