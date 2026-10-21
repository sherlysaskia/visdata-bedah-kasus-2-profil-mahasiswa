# 🎓 Dashboard Profil Mahasiswa

**Bedah Kasus 2 · Visualisasi Data**  
Sherly Saskia Rani · NIM 241051002

🔗 **Demo:** (isi setelah deploy)

Dashboard interaktif berbasis Streamlit untuk menganalisis profil mahasiswa. Dataset berisi **1.000 data sintesis** yang dikembangkan dari 2 baris seed pada materi kuliah (Sistem Informasi dan Manajemen).

## Data seed

| Jurusan | Semester | IPK | Usia |
|---|---|---|---|
| Sistem Informasi | 3 | 3,85 | 20 |
| Manajemen | 1 | 3,50 | 19 |

Data sintesis dibangkitkan dengan asumsi: 8 jurusan, semester 1 sampai 8, IPK berkisar 1,5 sampai 4,0, usia naik seiring semester, serta sebagian kecil mahasiswa lebih tua atau ber-IPK rendah sebagai outlier. Data ini hanya untuk latihan, bukan data mahasiswa sebenarnya.

## Skala pengukuran data

| Kolom | Skala | Visualisasi |
|---|---|---|
| Jurusan | Nominal | Bar chart, pie chart |
| Semester | Ordinal | Bar chart berurutan |
| IPK, Usia | Rasio (kontinu) | Histogram, box plot |

**Catatan:** semester bersifat ordinal, jadi ada urutan 1 sampai 8 tetapi jarak antar tingkat tidak bisa dianggap sama. Karena itu dipakai bar chart berurutan, ringkasan dengan median dan modus, serta korelasi Spearman.

## Fitur dashboard

- 5 kartu KPI: jumlah mahasiswa, rata-rata IPK, median IPK, median usia, potensi cum laude
- Filter sidebar: jurusan, rentang semester, rentang IPK
- 5 tab: Nominal, Ordinal, Kontinu, Korelasi & Uji, Data
- Uji statistik: Spearman dan Kruskal-Wallis
- Deteksi outlier dengan metode IQR
- Unduh data hasil filter dalam format CSV

## Temuan utama

- Jurusan terbanyak: Sistem Informasi (21,4%). IPK rata-rata tertinggi di Desain Komunikasi Visual dan Psikologi (3,37), terendah di Teknik Sipil (2,99).
- IPK rata-rata 3,23, miring ke kiri karena ada IPK rendah dan batas atas 4,0.
- Usia median 20 tahun, dengan sebagian kecil mahasiswa berusia di atas 25.
- Semester vs usia berkorelasi kuat (Spearman ρ = 0,74), semester vs IPK lemah tetapi signifikan (ρ = 0,19).
- Perbedaan IPK antar jurusan signifikan (Kruskal-Wallis, p < 0,001).

## Struktur file

| File | Fungsi |
|---|---|
| `generate_data.py` | Membangkitkan 1.000 data sintesis |
| `analisis.py` | Analisis statistik detail di terminal |
| `app.py` | Dashboard Streamlit |
| `data_mahasiswa_sintesis.csv` | Dataset hasil sintesis |
| `hasil_analisis.txt` | Keluaran `analisis.py` |
| `requirements.txt` | Daftar library |

## Cara menjalankan

```bash
pip install -r requirements.txt
python generate_data.py      # opsional, untuk membuat ulang data
python analisis.py           # opsional, analisis di terminal
streamlit run app.py
```

## Teknologi

Python · Pandas · NumPy · SciPy · Plotly · Streamlit
