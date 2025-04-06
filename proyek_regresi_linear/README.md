# Aplikasi Prediksi Penjualan Menggunakan Regresi Linear

Aplikasi web sederhana yang menggunakan regresi linear untuk memprediksi penjualan berdasarkan pengeluaran iklan.

## Fitur

- Input manual pengeluaran iklan untuk prediksi penjualan
- Upload dataset CSV untuk melatih model baru
- Visualisasi data dalam bentuk grafik scatter plot dan garis regresi
- Antarmuka yang responsif menggunakan Bootstrap

## Cara Penggunaan

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Jalankan aplikasi:
   ```bash
   python app.py
   ```

3. Buka browser dan akses `http://localhost:5000`

## Format Dataset CSV

- File CSV harus memiliki minimal 2 kolom
- Kolom pertama: pengeluaran iklan (dalam juta rupiah)
- Kolom kedua: penjualan (dalam ribu unit)
- Lihat `sample_dataset.csv` sebagai contoh format yang benar

## Teknologi yang Digunakan

- Flask
- scikit-learn
- pandas
- numpy
- Chart.js
- Bootstrap

## Deployment

Aplikasi ini dapat di-deploy ke berbagai platform hosting gratis seperti:
- Heroku
- PythonAnywhere
- Google Cloud Platform (dengan free tier)
- Railway

## Kontribusi

Silakan berkontribusi dengan membuat pull request atau melaporkan issues.
