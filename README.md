# MySQL Query Assistant

AI destekli MySQL sorgu oluşturucu aracı - OpenRouter ve DeepSeek modelleri ile güçlendirilmiş veritabanı yönetim platformu.

## Özellikler

- **Doğal dil işleme**: "Tüm kullanıcıları listele" gibi komutları MySQL sorgularına çevirir
- **Akıllı sorgu oluşturma**: Veritabanı şemasını analiz ederek optimize edilmiş SQL üretir
- **Güvenlik odaklı**: Sadece SELECT sorguları çalıştırır
- **Otomatik şema analizi**: Tabloları ve kolonları otomatik keşfeder
- **Çoklu AI model desteği**: DeepSeek, GPT-4, Claude gibi modeller

## Teknolojiler

- **Backend**: Flask, MySQL Connector, OpenAI Client
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI**: OpenRouter API, DeepSeek Chat

## Kurulum

### 1. Projeyi klonlayın
```bash
git clone https://github.com/safagoek/mysql-query-assistant.git
cd mysql-query-assistant
```

### 2. Sanal ortam oluşturun
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# veya
venv\Scripts\activate     # Windows
```

### 3. Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

### 4. Environment dosyası (.env) oluşturun
```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxx
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database
SECRET_KEY=your_secret_key
DEBUG=True
```

### 5. Uygulamayı başlatın
```bash
python app.py
```

Tarayıcınızda `http://localhost:5000` adresine gidin.

## Kullanım

1. **Veritabanına bağlanın**: Sol panelden veritabanınızı seçin
2. **Doğal dilde isteğinizi yazın**: 
   - "Tüm kullanıcıları listele"
   - "Son 10 kullanıcıyı getir" 
   - "Email adresi gmail olan kullanıcıları bul"
3. **AI sorguyu oluştursun**: "Sorgu Oluştur" butonuna tıklayın
4. **Sonuçları görün**: "Sorguyu Çalıştır" ile verileri görüntüleyin

## Proje Yapısı

```
mysql-query-assistant/
├── app.py                  # Ana Flask uygulaması
├── config.py              # Yapılandırma
├── requirements.txt       # Bağımlılıklar
├── database/             # Veritabanı modülleri
├── services/             # AI ve sorgu servisleri
├── static/               # CSS ve JavaScript
└── templates/            # HTML şablonları
```

## OpenRouter API Key

1. [OpenRouter.ai](https://openrouter.ai) hesabı oluşturun
2. Dashboard'dan API key alın
3. `.env` dosyasına ekleyin

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## Lisans

MIT License - detaylar için [LICENSE](LICENSE) dosyasını inceleyin.

## İletişim

**Safa Gök**
- GitHub: [@safagoek](https://github.com/safagoek)
- LinkedIn: [safa-gök](https://www.linkedin.com/in/safa-g%C3%B6k/)
