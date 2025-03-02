import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
from math import ceil
from matplotlib.patches import Patch

# 📌 **Daha kontrastlı renkler seçildi**
TOP_COLORS = [
    '#E41A1C',  # Kırmızı
    '#377EB8',  # Mavi
    '#4DAF4A',  # Yeşil
    '#984EA3',  # Mor
    '#FF4500',  # Koyu Turuncu (Önceden Sarı Olan Renk Değiştirildi)
    '#A65628',  # Kahverengi
    '#F781BF',  # Pembe
    '#999999',  # Gri
    '#66C2A5',  # Turkuaz
    '#FF1493'   # Pembe (Ekstra Kontrastlı)
]
OTHER_COLOR = 'gray'

# Özellik önem skoru çizimi (SVR + RF ortalaması)
def plot_svr_rf_avg(norm_coeff_df, features, filename):
    svr_rf_avg_importance = (norm_coeff_df['SVR'] + norm_coeff_df['RandomForest']) / 2
    x = np.arange(len(features))
    width = 0.4

    top_n = int(ceil(0.2 * len(features)))
    top_indices = np.argsort(svr_rf_avg_importance)[-top_n:]
    sorted_top = sorted(top_indices, key=lambda i: svr_rf_avg_importance[i], reverse=True)

    color_mapping = {i: TOP_COLORS[sorted_top.index(i) % len(TOP_COLORS)] for i in sorted_top}
    colors = [color_mapping[i] if i in color_mapping else OTHER_COLOR for i in range(len(features))]

    plt.figure(figsize=(16, 8))
    plt.bar(x, svr_rf_avg_importance, width, color=colors, label='SVR & RandomForest Avg')

    legend_elements = [Patch(facecolor=color_mapping[i], label=f"Top {sorted_top.index(i)+1}: Feature {i+1}") for i in sorted_top]
    legend_elements.append(Patch(facecolor=OTHER_COLOR, label='Other Features'))

    plt.legend(handles=legend_elements, fontsize=10)
    plt.xlabel('Feature Number', fontsize=14)
    plt.ylabel('Average Importance', fontsize=14)
    plt.title('SVR & RandomForest Average Feature Importance', fontsize=16)
    plt.xticks(x, [str(i+1) for i in range(len(features))], rotation=0, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

    return top_indices, color_mapping

# 📌 **Feature listesi kaydetme fonksiyonu**
def save_feature_labels(features, filename, top_indices, color_mapping):
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
        color = color_mapping.get(i, 'black')
        ax.text(0, 1 - (i / len(features)), f"{i+1}. {feature_names.get(f, f)}", fontsize=10,
                verticalalignment='center', fontfamily='monospace', color=color)

    # 📌 **Top %20 Features kutusu**
    ax.text(0, -0.1, "Top 20% Features", fontsize=12, fontweight='bold', fontfamily='monospace', color='black')
    for idx, i in enumerate(sorted(top_indices, key=lambda i: color_mapping[i])):
        ax.text(0, -0.12 - (idx * 0.02), f"{i+1}. {feature_names.get(features[i], features[i])}",
                fontsize=10, fontfamily='monospace', color=color_mapping[i])

    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

# 📌 **Veri yükleme**
df = pd.read_csv("D:/Projects/Github/article_workspace/svr/oteller.csv")
df.fillna(df.mode().iloc[0], inplace=True)

X = df.drop(['otel_ad', 'fiyat', 'imageurl', 'bolge', 'id'], axis=1)
y = df['fiyat']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

defined_models = {
    'SVR': SVR(kernel='linear'), 'Ridge': Ridge(),
    'Lasso': Lasso(), 'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42)
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

normalized_coeffs = {name: coeff / np.sum(np.abs(coeff)) for name, coeff in coefficients_dict.items()}
norm_coeff_df = pd.DataFrame(normalized_coeffs, index=X.columns)

# 📌 **Grafik ve Feature Listesi Kaydetme**
top_indices, color_mapping = plot_svr_rf_avg(norm_coeff_df, X.columns, "twoMean/svr_rf_avg_importance.png")
save_feature_labels(X.columns, "twoMean/feature_labels.png", top_indices, color_mapping)
