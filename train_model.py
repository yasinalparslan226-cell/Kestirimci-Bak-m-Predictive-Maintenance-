import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

print("1. Sentetik IoT Araç Verisi Üretiliyor...")
# 5000 satırlık örnek bir veri seti oluşturalım
np.random.seed(42)
data_size = 5000

# Normal şartlarda sensör verileri
engine_temp = np.random.normal(90, 10, data_size) # Ortalama 90 derece
rpm = np.random.normal(3000, 500, data_size)      # Ortalama 3000 devir
vibration = np.random.normal(1.5, 0.5, data_size) # Ortalama 1.5 birim titreşim
oil_pressure = np.random.normal(40, 5, data_size) # Ortalama 40 psi

# Veriyi bir Pandas DataFrame'ine dönüştürelim
df = pd.DataFrame({
    'Engine_Temp': engine_temp,
    'RPM': rpm,
    'Vibration': vibration,
    'Oil_Pressure': oil_pressure
})

# Arıza durumunu (Hedef Değişken) belirleyelim. 
# Sıcaklık çok yüksek, titreşim fazla veya yağ basıncı düşükse arıza riski (1) artar.
df['Failure_Risk'] = np.where(
    (df['Engine_Temp'] > 105) | (df['Vibration'] > 2.5) | (df['Oil_Pressure'] < 30), 
    1, # Arıza yapma ihtimali yüksek
    0  # Durum normal
)

print(f"Veri seti hazır! Toplam Kayıt: {len(df)}")
print(f"Arızalı Kayıt Sayısı: {df['Failure_Risk'].sum()}")

print("\n2. Model Eğitimi Başlıyor...")
# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop('Failure_Risk', axis=1)
y = df['Failure_Risk']

# Veriyi Eğitim (%80) ve Test (%20) olarak ayıralım
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Sınıflandırıcı Modelini tanımla ve eğit
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("\n3. Model Test Ediliyor...")
# Test verisi ile tahmin yapalım
y_pred = model.predict(X_test)

# Sonuçları ekrana yazdır
print(f"Model Doğruluk Oranı (Accuracy): {accuracy_score(y_test, y_pred) * 100:.2f}%\n")
print("Sınıflandırma Raporu:")
print(classification_report(y_test, y_pred))

print("\n4. Model Dışarı Aktarılıyor...")
# Eğitilmiş modeli daha sonra API'de kullanmak üzere kaydet
model_filename = 'vehicle_predictive_model.pkl'
joblib.dump(model, model_filename)
print(f"Model başarıyla '{model_filename}' olarak kaydedildi!")
import matplotlib.pyplot as plt
import seaborn as sns

# Arayüzüne uygun karanlık tema ve font ayarları
plt.style.use('dark_background')
plt.rcParams.update({
    'font.family': 'sans-serif',
    'axes.facecolor': '#0A0A0A',
    'figure.facecolor': '#0A0A0A',
    'text.color': 'white',
    'axes.labelcolor': '#A0A0A0',
    'xtick.color': '#A0A0A0',
    'ytick.color': '#A0A0A0',
    'grid.color': '#1A1A1A'
})

# 1. Grafik: Özellik Önem Düzeyi (Feature Importance)
# Hangi sensör arızayı daha çok tetikliyor?
importances = model.feature_importances_
features = X.columns

plt.figure(figsize=(8, 5))
sns.barplot(x=importances, y=features, palette=['#00E5FF', '#00C853', '#D32F2F', '#0078D7'])
plt.title('Arıza Kestiriminde Sensörlerin Etki Oranları', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Etki Oranı (%)', fontsize=12)
plt.ylabel('Sensörler', fontsize=12)
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300) # Yüksek kalitede kaydeder

# 2. Grafik: Sıcaklık ve Titreşimin Arızaya Etkisi (Scatter Plot)
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='Engine_Temp', y='Vibration', hue='Failure_Risk', palette=['#00C853', '#D32F2F'], s=50, alpha=0.7)
plt.title('Motor Sıcaklığı ve Titreşim Analizi', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Motor Sıcaklığı (°C)', fontsize=12)
plt.ylabel('Titreşim Seviyesi (g)', fontsize=12)
plt.legend(title='Arıza Durumu', labels=['Normal', 'Arıza Riski'])
plt.tight_layout()
plt.savefig('risk_analysis.png', dpi=300)

print("Karanlık temalı grafikler başarıyla oluşturuldu!")