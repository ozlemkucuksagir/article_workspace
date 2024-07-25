# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 23:28:18 2024

@author: usnis
"""



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import pandas as pd

# Yorumları yükle
analiz_sonuclari_df = pd.read_csv('analiz_sonuclari.csv')

# TF-IDF vektörleştirici kullanarak metin verisini sayısal verilere dönüştür
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(analiz_sonuclari_df['yorum'])

# Etiketleri sayısal verilere dönüştür
y = analiz_sonuclari_df['opinion'].apply(lambda x: 1 if x == 'olumlu' else 0)

# Veriyi eğitim ve test setlerine böl
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# RandomForest modelini tanımla
rf = RandomForestClassifier()

# GridSearchCV ile hiperparametre arama
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'max_features': ['sqrt', 'log2']
}
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# En iyi modeli seç
best_rf = grid_search.best_estimator_

# Test verisi ile tahmin yap ve doğruluk oranını hesapla
y_pred = best_rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model doğruluk oranı: {accuracy:.2f}")

# Doğruluk oranını sonuç CSV dosyasına ekle
result_df = analiz_sonuclari_df.groupby('otel_id').apply(lambda df: pd.Series({
    'positive_reviews': df[df['opinion'] == 'olumlu'].shape[0],
    'negative_reviews': df[df['opinion'] == 'olumsuz'].shape[0],
    'total_reviews': df.shape[0],
    'score': (df[df['opinion'] == 'olumlu'].shape[0] / df.shape[0]) * 10,
    'accuracy': accuracy
})).reset_index()

# Sonuçları CSV dosyasına yazma
result_df.to_csv('otel_skorlari.csv', index=False)

print("Analiz ve puanlama tamamlandı. Sonuçlar 'otel_skorlari.csv' dosyasına kaydedildi.")

