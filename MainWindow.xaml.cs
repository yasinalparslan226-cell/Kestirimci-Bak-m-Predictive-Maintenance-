using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Media;
using System.Windows.Threading;

namespace AkilliAracDashboard
{
    public partial class MainWindow : Window
    {
        private DispatcherTimer timer;
        private Random random;
        private static readonly HttpClient client = new HttpClient();

        public MainWindow()
        {
            InitializeComponent();
            random = new Random();

            // Her 2 saniyede bir veri üretecek zamanlayıcı
            timer = new DispatcherTimer();
            timer.Interval = TimeSpan.FromSeconds(2);
            timer.Tick += Timer_Tick;
        }

        private void btnSimulate_Click(object sender, RoutedEventArgs e)
        {
            if (timer.IsEnabled)
            {
                timer.Stop();
                btnSimulate.Content = "SİMÜLASYONU BAŞLAT";
                btnSimulate.Background = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#0078D7"));
            }
            else
            {
                timer.Start();
                btnSimulate.Content = "SİMÜLASYONU DURDUR";
                btnSimulate.Background = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#D32F2F"));
            }
        }

        private async void Timer_Tick(object sender, EventArgs e)
        {
            // 1. Sentetik Sensör Verisi Üretimi (Ara sıra arıza durumu yaratmak için değerleri zorluyoruz)
            bool createAnomaly = random.Next(1, 10) > 7; // %30 ihtimalle arıza simülasyonu

            double engineTemp = createAnomaly ? random.Next(105, 120) : random.Next(85, 100);
            double rpm = random.Next(2500, 4000);
            double vibration = createAnomaly ? random.NextDouble() * 2 + 2.0 : random.NextDouble() + 1.0;
            double oilPressure = createAnomaly ? random.Next(20, 29) : random.Next(35, 50);

            // Arayüzü Güncelle
            txtTemp.Text = $"{engineTemp} °C";
            txtRpm.Text = $"{rpm} RPM";
            txtVibration.Text = $"{Math.Round(vibration, 2)} g";
            txtOil.Text = $"{oilPressure} PSI";

            // 2. Python API'ye Gönderilecek Veriyi Hazırlama
            var sensorData = new
            {
                Engine_Temp = engineTemp,
                RPM = rpm,
                Vibration = vibration,
                Oil_Pressure = oilPressure
            };

            string jsonString = JsonSerializer.Serialize(sensorData);
            var content = new StringContent(jsonString, Encoding.UTF8, "application/json");

            try
            {
                // 3. API'ye İstek Atma
                HttpResponseMessage response = await client.PostAsync("http://127.0.0.1:8000/predict", content);
                response.EnsureSuccessStatusCode();

                string responseBody = await response.Content.ReadAsStringAsync();

                // 4. Yanıtı Çözümleme
                using (JsonDocument doc = JsonDocument.Parse(responseBody))
                {
                    JsonElement root = doc.RootElement;
                    int riskStatus = root.GetProperty("risk_status").GetInt32();
                    double failureProbability = root.GetProperty("failure_probability").GetDouble();
                    string message = root.GetProperty("message").GetString();

                    UpdateStatusUI(riskStatus, failureProbability, message);
                }
            }
            catch (Exception ex)
            {
                txtMessage.Text = "API Bağlantı Hatası: " + ex.Message;
            }
        }

        private void UpdateStatusUI(int riskStatus, double failureProbability, string message)
        {
            txtRisk.Text = $"Arıza Riski: %{Math.Round(failureProbability * 100, 1)}";
            txtMessage.Text = message;

            if (riskStatus == 1)
            {
                // Riskli Durum - Kırmızı Tema
                StatusIndicator.Background = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#D32F2F"));
                txtStatusIcon.Text = "!";
            }
            else
            {
                // Normal Durum - Yeşil Tema
                StatusIndicator.Background = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#00C853"));
                txtStatusIcon.Text = "OK";
            }
        }
    }
}