from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# 1. Eğittiğimiz Modeli Yüklüyoruz
model = joblib.load('vehicle_predictive_model.pkl')

# 2. API Uygulamasını Başlatıyoruz
app = FastAPI(title="Araç Sağlık Takip ve Kestirimci Bakım API")

# 3. C#'tan Gelecek Verinin Yapısını (Şemasını) Tanımlıyoruz
class SensorData(BaseModel):
    Engine_Temp: float
    RPM: float
    Vibration: float
    Oil_Pressure: float

# 4. Tahmin Uç Noktası (Endpoint) Oluşturuyoruz
@app.post("/predict")
def predict_failure(data: SensorData):
    # C#'tan gelen JSON verisini Pandas DataFrame'e çeviriyoruz (Modelin anladığı dil)
    input_data = pd.DataFrame([{
        'Engine_Temp': data.Engine_Temp,
        'RPM': data.RPM,
        'Vibration': data.Vibration,
        'Oil_Pressure': data.Oil_Pressure
    }])
    
    # Modelden tahmini ve risk olasılığını alıyoruz
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1] # Arıza(1) olma olasılığı
    
    # Sonucu C#'a JSON formatında geri gönderiyoruz
    return {
        "risk_status": int(prediction), # 0 (Normal) veya 1 (Riskli)
        "failure_probability": float(probability), # Örneğin 0.85 (%85 risk)
        "message": "Arıza riski tespit edildi!" if prediction == 1 else "Sistem normal çalışıyor."
    }