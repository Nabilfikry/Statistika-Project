# Statistika Project: Analisis Faktor Demografi & Perilaku Belajar

Proyek ini telah diperbarui untuk melakukan analisis statistik menggunakan Python terhadap dataset **Student Performance** (khusus mata pelajaran Bahasa Portugis).

## 🗂 Struktur Proyek

```
Statistika-Project/
│
├── dataset/
│   ├── raw/                 # Input Data: 'student-por.csv' (Delimiter ';')
│   └── processed/           # Output Data: 'data_clean.csv'
│
├── notebooks/               # Script Analisis (Berurutan 0-4)
│   ├── 0_data_preparation.py
│   ├── 1_analisis_deskriptif.py
│   ├── 2_uji_hipotesis_chisquare.py
│   ├── 3_uji_anova.py
│   └── 4_analisis_regresi.py
│
├── outputs/                 # Hasil Visualisasi & Tabel
│   └── figures/             # File PNG (Histogram, Boxplot, dll)
│
└── requirements.txt         # Daftar Library Python
```

## 🚀 Panduan Eksekusi (Urutan Wajib)

Proyek ini dirancang untuk dijalankan secara berurutan dari file `0` hingga `4`. Berikut adalah deskripsi fungsi setiap script:

### 1. Data Preparation
```bash
python notebooks/0_data_preparation.py
```
*   **Fungsi**: Membaca file mentah `student-por.csv`, menyeleksi variabel relevan (G3, sex, Mjob, studytime, dll), dan membersihkan data dari nilai yang tidak valid (range G3 0-20).
*   **Output**: `dataset/processed/data_clean.csv`

### 2. Analisis Deskriptif
```bash
python notebooks/1_analisis_deskriptif.py
```
*   **Fungsi**: Menampilkan statistik dasar (Mean, Max, Min) dan membuat visualisasi awal (Histogram Nilai, Pie Chart Gender, Bar Chart Pekerjaan Ibu).
*   **Output**: Grafik disimpan di `outputs/figures/`

### 3. Uji Hipotesis (Chi-Square)
```bash
python notebooks/2_uji_hipotesis_chisquare.py
```
*   **Kasus**: Hubungan antara **Gender** (sex) dan **Minat Kuliah** (higher).
*   **Hasil**: P-Value > 0.05 (Independen/Tidak ada hubungan).

### 4. Uji ANOVA (One-Way)
```bash
python notebooks/3_uji_anova.py
```
*   **Kasus**: Perbedaan rata-rata **Nilai Akhir (G3)** berdasarkan **Pekerjaan Ibu (Mjob)**.
*   **Hasil**: P-Value < 0.05 (Signifikan). Pekerjaan Ibu mempengaruhi prestasi siswa.

### 5. Analisis Regresi Linear Berganda
```bash
python notebooks/4_analisis_regresi.py
```
*   **Model**: `G3 ~ studytime + absences + G1`
*   **Fungsi**: Memodelkan faktor-faktor yang mempengaruhi nilai akhir. Dilengkapi dengan **Uji Asumsi Klasik** (Normalitas, Multikolinearitas, Homoskedastisitas, Autokorelasi).

## 🛠 Instalasi

Pastikan Python telah terinstall. Install dependencies dengan:

```bash
pip install -r requirements.txt
```

*(Library utama: pandas, matplotlib, seaborn, scipy, statsmodels)*

## 📝 Catatan Tambahan
*   Semua script telah menerapkan **Clean Code** (Error Handling, Validasi Kolom, dan Komentar Bahasa Indonesia).
*   Gambar grafik otomatis tersimpan dengan resolusi tinggi (300 DPI) agar siap ditempel ke Laporan Bab IV.
