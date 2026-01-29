# 🚲 Bike Sharing Analytics Dashboard

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

Dashboard interaktif untuk menganalisis pola penyewaan sepeda dari sistem Capital Bikeshare di Washington D.C. (2011-2012).

## 🌐 Demo

**[👉 Live Dashboard](https://bike-sharing-analysis-mkrdxiguuwuixzmnlu5hza.streamlit.app)**

## 📊 Pertanyaan Bisnis

1. **Bagaimana pengaruh kondisi cuaca (musim, suhu, kelembaban) terhadap jumlah penyewaan sepeda di Washington D.C. selama periode 2011-2012, dan kondisi cuaca mana yang menghasilkan penyewaan tertinggi?**
2. **Pada jam dan hari apa penyewaan sepeda mencapai puncaknya selama periode 2011-2012, dan bagaimana perbedaan pola penggunaan antara pengguna casual dan registered?**

## 📁 Struktur Direktori

```
├── dashboard/
│   ├── dashboard.py        # Dashboard Streamlit
│   ├── main_data.csv       # Data harian (cleaned)
│   └── hour_data.csv       # Data per jam (cleaned)
├── data/
│   ├── day.csv             # Raw data harian
│   └── hour.csv            # Raw data per jam
├── notebook.ipynb          # Notebook analisis data
├── README.md
├── requirements.txt
└── url.txt
```

## ⚙️ Setup & Installation

### 1. Clone Repository

```bash
git clone https://github.com/mergeconflictlover/bike-sharing-analysis.git
cd bike-sharing-analysis
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Menjalankan Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```

Dashboard akan terbuka di `http://localhost:8501`

## 📓 Menjalankan Notebook

```bash
jupyter notebook notebook.ipynb
```

## ✨ Fitur Dashboard

| Fitur | Deskripsi |
|-------|-----------|
| 🎛️ **Filter Interaktif** | Rentang tanggal, musim, kondisi cuaca |
| 📈 **Metrik Utama** | Total penyewaan, rata-rata harian, perbandingan user |
| 🌤️ **Analisis Cuaca** | Pengaruh musim, cuaca, korelasi suhu |
| ⏰ **Analisis Waktu** | Pola per jam, per hari, trend bulanan |
| 📊 **Clustering** | Kategorisasi hari berdasarkan tingkat penyewaan |

## 📌 Hasil Analisis

### Pengaruh Cuaca
- 🍂 Musim **Fall (Gugur)** → penyewaan tertinggi
- ☀️ Cuaca **cerah** → 2x lipat dibanding cuaca buruk
- 🌡️ **Suhu** berkorelasi positif kuat (r ≈ 0.63)

### Pola Waktu
- ⏰ **Jam puncak**: 08:00 & 17:00-18:00 (commuting hours)
- 👔 **Registered**: pola commuter (hari kerja)
- 🎉 **Casual**: meningkat 2x di weekend

## 🛠️ Tech Stack

- **Python** - Data processing & analysis
- **Pandas & NumPy** - Data manipulation
- **Matplotlib & Seaborn** - Visualization (notebook)
- **Altair** - Interactive charts (dashboard)
- **Streamlit** - Web dashboard framework

## 👨‍💻 Author

**Muhammad Himbar Buana**

[![Email](https://img.shields.io/badge/Email-mhimbarbuana@gmail.com-D14836?style=flat&logo=gmail&logoColor=white)](mailto:mhimbarbuana@gmail.com)
[![Dicoding](https://img.shields.io/badge/Dicoding-himbarbuana-2C3E50?style=flat)](https://www.dicoding.com/users/himbarbuana)
