import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

# Function to plot feature importance comparison (without average)
def plot_feature_importance(norm_coeff_df, features, filename):
    x = np.arange(len(features))
    width = 0.2
    plt.figure(figsize=(16, 8))
    
    # Define bar positions
    pos_svr = x - 1.5 * width
    pos_ridge = x - 0.5 * width
    pos_lasso = x + 0.5 * width
    pos_rf = x + 1.5 * width
    
    # Retrieve normalized values
    svr_vals = norm_coeff_df['SVR'].values
    ridge_vals = norm_coeff_df['Ridge'].values
    lasso_vals = norm_coeff_df['Lasso'].values
    rf_vals = norm_coeff_df['RandomForest'].values
    
    # Plot bars
    plt.bar(pos_svr, svr_vals, width, color='blue', label='SVR')
    plt.bar(pos_ridge, ridge_vals, width, color='green', label='Ridge')
    plt.bar(pos_lasso, lasso_vals, width, color='purple', label='Lasso')
    plt.bar(pos_rf, rf_vals, width, color='orange', label='RandomForest')
    
    plt.xlabel('Feature Index', fontsize=12)
    plt.ylabel('Normalized Importance', fontsize=12)
    plt.title('Feature Importance Comparison', fontsize=14)
    plt.xticks(x, range(1, len(features) + 1), rotation=90)
    plt.legend(title='Model', loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

# Function to plot the average of SVR and RandomForest feature importance
def plot_svr_rf_avg(norm_coeff_df, features, filename):
    svr_rf_avg_importance = (norm_coeff_df['SVR'] + norm_coeff_df['RandomForest']) / 2
    x = np.arange(len(features))
    width = 0.4
    
    plt.figure(figsize=(16, 8))
    
    # Plot the bars for average feature importance
    plt.bar(x, svr_rf_avg_importance, width, color='gray', label='Average Importance (SVR & RF)')
    
    # Plot the line for SVR & RandomForest average
    plt.plot(x, svr_rf_avg_importance, color='red', linewidth=2, label='SVR & RandomForest Average (Line)')
    
    # Adding legend
    plt.xlabel('Feature Index', fontsize=12)
    plt.ylabel('Average Importance', fontsize=12)
    plt.title('SVR & RandomForest Average Feature Importance', fontsize=14)
    plt.xticks(x, range(1, len(features) + 1), rotation=90)
    plt.legend(title='Models', loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

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

# Save feature importance plots
plot_feature_importance(norm_coeff_df, X.columns, "twoMean/feature_importance.png")
plot_svr_rf_avg(norm_coeff_df, X.columns, "twoMean/svr_rf_avg_importance.png")

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
print("Feature importance plots saved: feature_importance.png & svr_rf_avg_importance.png")
print("Fair price calculation completed based on SVR & RF average.")
