# Proyek Analisis Data: Bike Sharing Dataset

## Deskripsi Proyek

Proyek ini merupakan analisis data penyewaan sepeda dari sistem Capital Bikeshare di Washington D.C. periode 2011-2012. Analisis ini bertujuan untuk menjawab dua pertanyaan bisnis utama:

1. **Bagaimana pengaruh kondisi cuaca (musim, suhu, kelembaban) terhadap jumlah penyewaan sepeda?**
2. **Pada jam dan hari apa penyewaan sepeda mencapai puncaknya, dan bagaimana perbedaan pola antara pengguna casual dan registered?**

## Struktur Direktori

```
submission/
├── dashboard/
│   ├── dashboard.py        # Dashboard Streamlit
│   ├── main_data.csv       # Data harian yang sudah dibersihkan
│   └── hour_data.csv       # Data per jam yang sudah dibersihkan
├── data/
│   ├── day.csv             # Data mentah harian
│   └── hour.csv            # Data mentah per jam
├── notebook.ipynb          # Notebook analisis data
├── README.md               # Dokumentasi proyek
├── requirements.txt        # Daftar library yang dibutuhkan
└── url.txt                 # Link dashboard (jika di-deploy)
```

## Instalasi

### 1. Clone Repository / Download Project

### 2. Buat Virtual Environment (Opsional tapi Disarankan)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Menjalankan Notebook

1. Pastikan Jupyter Notebook sudah terinstall
2. Buka terminal dan navigasi ke folder `submission`
3. Jalankan perintah:

```bash
jupyter notebook notebook.ipynb
```

4. Jalankan semua cell dari atas ke bawah untuk melihat analisis lengkap

## Menjalankan Dashboard Streamlit

1. Pastikan sudah menjalankan notebook terlebih dahulu (untuk generate `main_data.csv` dan `hour_data.csv`)
2. Navigasi ke folder dashboard:

```bash
cd submission/dashboard
```

3. Jalankan Streamlit:

```bash
streamlit run dashboard.py
```

4. Dashboard akan terbuka di browser pada alamat `http://localhost:8501`

## Fitur Dashboard

- **Filter Interaktif**: Pilih rentang tanggal dan musim
- **Metrik Utama**: Total penyewaan, rata-rata harian, casual vs registered
- **Analisis Cuaca**: Visualisasi pengaruh musim, kondisi cuaca, dan korelasi suhu
- **Analisis Waktu**: Pola penyewaan per jam, per hari, dan trend bulanan
- **Clustering**: Kategorisasi hari berdasarkan tingkat penyewaan

## Dataset

Dataset yang digunakan adalah **Bike Sharing Dataset** dari UCI Machine Learning Repository. Dataset ini berisi informasi harian dan per jam tentang penyewaan sepeda, termasuk:

- Informasi waktu (tanggal, jam, hari, bulan, tahun)
- Kondisi cuaca (musim, suhu, kelembaban, kecepatan angin)
- Tipe hari (hari kerja, libur, weekend)
- Jumlah penyewaan (casual, registered, total)

## Hasil Analisis

### Kesimpulan Pertanyaan 1
- Musim **Fall (Gugur)** memiliki rata-rata penyewaan tertinggi
- Cuaca **cerah** meningkatkan penyewaan hingga 2x lipat dibanding cuaca buruk
- **Suhu** berkorelasi positif kuat dengan penyewaan (r ≈ 0.63)

### Kesimpulan Pertanyaan 2
- **Jam puncak**: 08:00 pagi dan 17:00-18:00 sore
- Pengguna **registered** menunjukkan pola commuter (berangkat-pulang kerja)
- Pengguna **casual** meningkat 2x lipat di weekend

## Author

**Muhammad Himbar Buana**
- Email: [email Anda]
- ID Dicoding: [ID Dicoding Anda]
