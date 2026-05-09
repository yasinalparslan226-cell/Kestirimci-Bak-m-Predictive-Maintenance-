# 🚗 Akıllı Araç Kestirimci Bakım Sistemi (Predictive Maintenance & Digital Twin)

![C#](https://img.shields.io/badge/C%23-%23239120.svg?style=for-the-badge&logo=c-sharp&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![WPF](https://img.shields.io/badge/WPF-Windows_Presentation_Foundation-blue?style=for-the-badge)

Bu proje, otomotiv sektöründeki IoT ve bağlantılı araç (Connected Car) konseptlerinden ilham alınarak geliştirilmiş bir **Kestirimci Bakım (Predictive Maintenance)** ve **Dijital İkiz (Digital Twin)** uygulamasıdır. Araç sensörlerinden gelen anlık veriler makine öğrenmesi ile analiz edilerek arıza riskleri önceden tahmin edilir.

## 🚀 Proje Hakkında

Sistem iki temel bileşenden oluşur:
1. **Veri Bilimi ve Yapay Zeka (Arka Plan):** Araçların geçmiş sensör verileriyle eğitilmiş bir **Random Forest** algoritması. Sistem, gelen yeni veriler ışığında anlık risk hesaplaması yapar.
2. **Dijital İkiz Arayüzü (Ön Yüz):** C# ve WPF kullanılarak tasarlanmış modern bir gösterge paneli (Dashboard). Bu panel, sentetik IoT sensör verileri üretir ve arka plandaki yapay zeka ile anlık olarak haberleşir.

## 🏗️ Sistem Mimarisi

- **Sensör Simülasyonu:** C# arayüzü; motor sıcaklığı, devir (RPM), titreşim ve yağ basıncı gibi verileri anlık olarak simüle eder.
- **FastAPI Köprüsü:** Üretilen JSON formatındaki sensör verileri, Python FastAPI üzerinden makine öğrenmesi modeline iletilir.
- **Karar Mekanizması:** Yapay zeka modeli verileri işler, risk oranını hesaplar ve C# arayüzüne geri gönderir. Arayüz bu sonuca göre görsel uyarılar (Yeşil/Kırmızı) verir.

## 📸 Ekran Görüntüleri

<!-- Buraya projenin çalışırken alınmış bir ekran görüntüsünü ekleyin -->
![Dashboard Ekran Görüntüsü](https://github.com/yasinalparslan226-cell/Kestirimci-Bak-m-Predictive-Maintenance-/blob/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202026-05-09%20160117.png)

## 💻 Kullanılan Teknolojiler

* **Makine Öğrenmesi:** Python, Scikit-Learn (Random Forest), Pandas, NumPy, Joblib
* **API & Sunucu:** FastAPI, Uvicorn
* **Kullanıcı Arayüzü (UI):** C#, WPF (Windows Presentation Foundation), XAML
* **Haberleşme:** HTTP Client, JSON Serileştirme

## ⚙️ Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

### 1. Python (Arka Plan) Kurulumu
Gerekli kütüphaneleri yükleyin:
```bash
pip install pandas numpy scikit-learn joblib fastapi uvicorn pydantic Modeli eğitmek için Python_Backend klasörüne gidin ve şu komutu çalıştırın:

Bash
python train_model.py
API sunucusunu ayağa kaldırın:

Bash
uvicorn api:app --reload
(API, http://127.0.0.1:8000 adresinde çalışmaya başlayacaktır.)

2. C# WPF (Ön Yüz) Çalıştırma
CSharp_Frontend klasöründeki çözüm dosyasını (.sln) Visual Studio ile açın.

Projeyi başlatmak için F5 tuşuna basın.

Arayüz açıldığında "SİMÜLASYONU BAŞLAT" butonuna tıklayarak gerçek zamanlı veri akışını ve yapay zeka analizini izleyebilirsiniz.

🔮 Gelecek Geliştirmeler (Yol Haritası)
[ ] Gerçek bir OBD-II cihazı üzerinden canlı araç verilerinin (CAN Bus) sisteme entegre edilmesi.

[ ] API mimarisinin Azure veya AWS platformlarına taşınarak bulut tabanlı hale getirilmesi.

[ ] Zaman serisi analizleri için LSTM gibi Derin Öğrenme modellerinin sisteme dahil edilmesi.

👨‍💻 Geliştirici
Yasin Alparslan

Automotive Data & IoT

LinkedIn Profilim | GitHub Profilim

***
