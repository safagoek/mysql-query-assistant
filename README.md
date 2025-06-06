```markdown name=README.md
# 🚀 MySQL Query Assistant

**AI destekli MySQL sorgu oluşturucu aracı** - OpenRouter ve DeepSeek modelleri ile güçlendirilmiş, kullanıcı dostu veritabanı yönetim platformu.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![OpenRouter](https://img.shields.io/badge/OpenRouter-AI-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)


## 🎯 Proje Hakkında

MySQL Query Assistant, kullanıcıların doğal dilde yazdıkları istekleri AI kullanarak MySQL sorgularına dönüştüren modern bir web uygulamasıdır. OpenRouter API ve DeepSeek modellerini kullanarak, veritabanı şemasını analiz eder ve optimize edilmiş SQL sorguları oluşturur.



## ✨ Özellikler

### 🤖 AI Özellikleri
- **Doğal dil işleme**: "Tüm kullanıcıları listele" gibi komutları anlama
- **Akıllı sorgu oluşturma**: Şema bilgilerine göre optimize edilmiş SQL
- **Multiple model desteği**: DeepSeek, GPT-4, Claude vs.
- **Güvenlik odaklı**: Sadece SELECT sorguları için güvenlik

### 🗄️ Veritabanı Özellikleri
- **Otomatik şema analizi**: Tabloları ve kolonları otomatik keşfetme
- **Gerçek zamanlı bağlantı**: MySQL veritabanlarına canlı bağlantı
- **Tablo ilişkileri**: Primary key ve foreign key tanımlama
- **Çoklu veritabanı**: Farklı MySQL veritabanları arasında geçiş


### 🔧 Teknik Özellikler
- **RESTful API**: Modern API mimarisi
- **Session yönetimi**: Kullanıcı oturumu takibi
- **Error handling**: Detaylı hata yönetimi
- **Loading states**: Yükleme durumu göstergeleri
- **Copy functionality**: Sorguları kopyalama özelliği

## 🛠️ Kullanılan Teknolojiler

### Backend
- **Flask 3.0+**: Modern Python web framework
- **MySQL Connector**: MySQL veritabanı bağlantısı
- **OpenAI Client**: OpenRouter API entegrasyonu
- **SQLParse**: SQL sorgu formatlaması

### Frontend
- **HTML5 & CSS3**: Modern web standartları
- **JavaScript ES6+**: Dinamik etkileşimler
- **Bootstrap 5**: Responsive tasarım framework
- **Font Awesome 6**: İkon kütüphanesi
- **Prism.js**: Syntax highlighting

### AI & API
- **OpenRouter**: AI model API gateway
- **DeepSeek Chat**: Ücretsiz AI modeli
- **Claude 3.5, GPT-4**: Premium model seçenekleri




 📦 Kurulum


### 1. Projeyi Klonlama

```bash
git clone https://github.com/safagoek/mysql-query-assistant.git
cd mysql-query-assistant
```

### 2. Sanal Ortam Oluşturma

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Gerekli Paketleri Kurma

```bash
pip install -r requirements.txt
```

### 4. Klasör Yapısını Oluşturma

```
mysql-query-assistant/
│
├── app.py                      # Ana Flask uygulaması
├── config.py                   # Yapılandırma ayarları
├── requirements.txt            # Python bağımlılıkları
├── .env                        # Çevre değişkenleri
├── README.md                   # Bu dosya
│
├── database/
│   ├── __init__.py
│   ├── connection.py           # MySQL bağlantı yöneticisi
│   └── schema_analyzer.py      # Veritabanı şema analizi
│
├── services/
│   ├── __init__.py
│   ├── openrouter_service.py   # OpenRouter AI entegrasyonu
│   └── query_service.py        # Sorgu işleme servisi
│
├── static/
│   ├── css/
│   │   ├── style.css          # Ana stil dosyası
│   │   └── footer.css         # Footer stilleri
│   └── js/
│       └── app.js             # JavaScript fonksiyonları
│
└── templates/
    ├── base.html              # Temel şablon
    ├── index.html             # Ana sayfa
    ├── footer.html            # Footer şablonu
    └── results.html           # Sonuç sayfası
```

## 🔧 Yapılandırma

### 1. Environment Dosyası (.env)

```env
# OpenRouter API ayarları
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxx

# MySQL bağlantı ayarları
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=your_database_name

# Flask ayarları
SECRET_KEY=your_super_secret_key_here_2025
DEBUG=True
```

### 2. OpenRouter API Key Alma

1. [OpenRouter.ai](https://openrouter.ai) sitesine gidin
2. Hesap oluşturun (GitHub ile giriş yapabilirsiniz)
3. Dashboard'a gidin
4. "Keys" bölümünden yeni API key oluşturun
5. API key'i `.env` dosyasına ekleyin

### 3. MySQL Veritabanı Hazırlama

```sql
-- Örnek veritabanı oluşturma
CREATE DATABASE test_db;
USE test_db;

-- Örnek tablo oluşturma
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Örnek veri ekleme
INSERT INTO users (name, email) VALUES 
('Ahmet Yılmaz', 'ahmet@example.com'),
('Fatma Demir', 'fatma@example.com'),
('Mehmet Kaya', 'mehmet@example.com');
```

## 🚀 Kullanım

### 1. Uygulamayı Başlatma

```bash
python app.py
```

Uygulama başladığında şu mesajı göreceksiniz:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### 2. Web Arayüzüne Erişim

Tarayıcınızda şu adrese gidin:
```
http://localhost:5000
```

### 3. Kullanım Adımları

#### Adım 1: Veritabanına Bağlanma
1. Sol panelde "Veritabanı Seç" dropdown'ından veritabanınızı seçin
2. "Bağlan" butonuna tıklayın
3. Bağlantı başarılı olduğunda şema bilgileri görünecek

#### Adım 2: AI Sorgu Oluşturma
1. Sağ panelde "Ne yapmak istiyorsunuz?" alanına isteğinizi yazın
   ```
   Örnek: "Tüm kullanıcıları listele"
   Örnek: "En yeni 10 kullanıcıyı getir"
   Örnek: "Email adresi gmail olan kullanıcıları bul"
   ```
2. "Sorgu Oluştur" butonuna tıklayın
3. AI tarafından oluşturulan SQL sorgusu görünecek

#### Adım 3: Sorguyu Çalıştırma
1. Oluşturulan sorguyu kontrol edin
2. "Sorguyu Çalıştır" butonuna tıklayın
3. Sonuçlar tablo halinde görüntülenecek

### 4. Örnek Kullanım Senaryoları

```
✅ "Son 30 günde eklenen kullanıcıları listele"
✅ "En çok kullanılan email domain'lerini say"
✅ "A harfi ile başlayan isimleri bul"
✅ "Kullanıcı sayısını göster"
✅ "Email adresi olmayan kullanıcıları listele"
```




**Safa Gök**

[![GitHub](https://img.shields.io/badge/GitHub-safagoek-181717?style=for-the-badge&logo=github)](https://github.com/safagoek)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-safagoek-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/safa-g%C3%B6k/)

---
