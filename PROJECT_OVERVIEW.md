# Binus Insurance Cost Analytics - Data Warehouse & Dashboard

## 🎯 Tujuan Proyek

Proyek ini bertujuan untuk membangun **sistem analisis biaya asuransi kesehatan** yang komprehensif dengan mengimplementasikan konsep data warehouse dan dashboard interaktif. Sistem ini memungkinkan analisis mendalam terhadap faktor-faktor yang mempengaruhi biaya asuransi dan menyediakan prediksi biaya untuk profil pengguna tertentu.

### Objektif Utama:
- 📊 Analisis pola biaya asuransi berdasarkan demografi (umur, jenis kelamin, region)
- 🚬 Evaluasi dampak gaya hidup (status merokok, BMI) terhadap biaya asuransi
- 🎯 Prediksi biaya asuransi personal dengan rekomendasi penghematan
- 🏗️ Implementasi arsitektur data warehouse dengan star schema
- 📈 Visualisasi data interaktif untuk insight bisnis

## 🛠️ Teknologi yang Digunakan

### Backend & Data Processing
- **Python 3.x** - Bahasa pemrograman utama
- **Flask** - Web framework untuk REST API
- **PostgreSQL** - Database untuk data warehouse
- **SQLAlchemy** - ORM untuk koneksi database
- **Pandas** - Data manipulation dan analysis
- **NumPy** - Numerical computing

### Frontend & Visualisasi
- **HTML5/CSS3** - Structure dan styling
- **JavaScript (Vanilla)** - Interactive dashboard
- **Chart.js** - Data visualization library

### Infrastructure & DevOps
- **Docker & Docker Compose** - Containerization
- **python-dotenv** - Environment configuration

### Data Management
- **Star Schema Design** - Data warehouse architecture
- **ETL Pipeline** - Extract, Transform, Load process

## 🏗️ Arsitektur Sistem

### 1. Data Warehouse (Star Schema)
```
Fact Table: fact_insurance
├── age_id → dim_age
├── sex_id → dim_sex
├── children_id → dim_children
├── smoker_id → dim_smoker
├── region_id → dim_region
└── measures: bmi, charges
```

### 2. ETL Pipeline
- **Extract**: Load data dari CSV insurance dataset
- **Transform**: Kategorisasi umur, normalisasi data
- **Load**: Insert ke dimension tables dan fact table

### 3. REST API Endpoints
- `/api/region-avg` - Rata-rata biaya per region
- `/api/age-avg` - Rata-rata biaya per kelompok umur
- `/api/boxplot-smoker` - Perbandingan biaya smoker vs non-smoker
- `/api/corr` - Korelasi antar variabel numerik
- `/api/predict` - Prediksi biaya personal dengan rekomendasi

### 4. Dashboard Interface
- **Analytics Dashboard** - Visualisasi data agregat
- **Prediction Tool** - Kalkulator biaya personal
- **Responsive Design** - Mobile-friendly interface

## 🚀 Cara Menjalankan Aplikasi

### Prerequisites
- Docker & Docker Compose
- Python 3.8+
- Git

### Quick Start
```bash
# 1. Clone repository
git clone [GITHUB_REPOSITORY_URL]
cd binus-dwmp

# 2. Setup database dengan Docker
docker-compose up -d

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env  # Edit sesuai konfigurasi

# 5. Jalankan ETL pipeline
cd etl
python etl.py

# 6. Start aplikasi
cd ../app
python app.py
```

### Akses Aplikasi
- **Dashboard**: http://localhost:5000
- **Prediction Tool**: http://localhost:5000/predict
- **API Documentation**: Lihat `insurance_api.http`

## 📊 Fitur Utama

### Analytics Dashboard
- 📈 **Regional Analysis** - Perbandingan biaya rata-rata antar region
- 👥 **Demographic Insights** - Analisis berdasarkan umur dan jenis kelamin
- 🚬 **Lifestyle Impact** - Visualisasi dampak merokok terhadap biaya
- 🔗 **Correlation Matrix** - Hubungan antar variabel

### Prediction Engine
- 🎯 **Personal Cost Estimation** - Prediksi biaya berdasarkan profil
- 💡 **Smart Recommendations** - Saran penghematan biaya
- 📊 **Scenario Comparison** - Bandingkan dampak perubahan gaya hidup

## 🔗 Links & Resources

### 🌐 Live Application
- **Production URL**: https://asura.alfian.app/
<!-- - **Demo Video**: `[MASUKKAN_LINK_DEMO]` -->

### 📂 Source Code
- **GitHub Repository**: https://github.com/fnzip/binus-dwmp
<!-- - **Documentation**: `[MASUKKAN_LINK_DOKUMENTASI]` -->

### 📋 Additional Resources
<!-- - **API Documentation**: `[MASUKKAN_SWAGGER/POSTMAN_COLLECTION]` -->
- **Database Schema**: `/dw/schema.sql`
- **Sample Data**: `/data/insurance.csv`

---

## 👥 Tim Pengembang
<!-- - **Developer**: [NAMA_PENGEMBANG] -->
- **Institution**: Binus University
- **Course**: Data Warehouse Mini Project

## 📝 Catatan Presentasi

### Key Points untuk Presentasi:
1. **Problem Statement** - Kompleksitas analisis biaya asuransi
2. **Solution Architecture** - Star schema dan ETL pipeline
3. **Technical Implementation** - Full-stack development dengan Python
4. **Business Value** - Insight actionable untuk decision making
5. **Demo** - Live demonstration of dashboard dan prediction tool

### Metrics yang Dapat Dipresentasikan:
- Performance ETL pipeline
- Response time API endpoints
- Data accuracy dan completeness
- User experience dashboard

---
*Generated for Binus Data Warehouse Mini Project - Ready for Presentation*
