# Genieva AI Assistant

Genieva adalah asisten AI yang dikembangkan untuk mempermudah pengguna Grab dalam melakukan transaksi Grab Food, Grab Bike, Grab Car, dan layanan transportasi Grab lainnya.

## Daftar Isi
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Fitur Utama](#fitur-utama)
- [Struktur Proyek](#struktur-proyek)
- [Instalasi dan Penggunaan](#instalasi-dan-penggunaan)
- [API Endpoints](#api-endpoints)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

## Teknologi yang Digunakan

Genieva dibangun menggunakan stack teknologi modern yang mencakup:

- **FastAPI**: Framework Python yang cepat untuk membangun API dengan performa tinggi.
- **LangChain**: Library untuk pengembangan aplikasi yang didukung oleh model bahasa.
- **Gemini**: Model AI dari Google untuk pemrosesan bahasa alami dan generasi teks.
- **Google Maps API**: Untuk fungsionalitas terkait lokasi dan pemetaan.
- **SQL Agent**: Untuk interaksi dengan database dan query yang kompleks.
- **Docker & Docker Compose**: Untuk kontainerisasi dan orkestrasi layanan.

## Fitur Utama

1. **Pemesanan Makanan**: Membantu pengguna memesan makanan melalui Grab Food dengan rekomendasi personalisasi.
2. **Transportasi**: Mempermudah pemesanan Grab Bike dan Grab Car.
3. **Rekomendasi Rute**: Memberikan saran rute optimal untuk perjalanan.
4. **Asisten Percakapan**: Menjawab pertanyaan pengguna tentang layanan Grab.
5. **Integrasi Lokasi**: Memanfaatkan data lokasi untuk memberikan pengalaman yang lebih baik.

## Struktur Proyek

```
geniva-artificial-intelligence/
├── core/
│   ├── db/
│   ├── models/
│   ├── temporary-data/
│   ├── tools/
│   ├── app.py
│   ├── config.py
│   ├── Dockerfile
│   ├── prompt.py
│   └── requirements.txt
├── documentation/
├── images/
│   ├──Dockerfile
├── tests/
├── .env (not uploaded)
├── .gitignore
├── docker-compose-database.yml
├── docker-compose-service.yml
├── ingest_direct.py
├── README.md
```

## Instalasi dan Penggunaan

Proyek ini menggunakan Docker Compose untuk mengelola layanan-layanannya. File `docker-compose-database.yml` dan `docker-compose-service.yml` tidak disertakan dalam repositori publik karena alasan keamanan.

Untuk menjalankan proyek:

1. Pastikan Docker dan Docker Compose terinstal di sistem Anda.

2. Clone repositori ini:
   ```
   https://github.com/GeniVA-HackJakarta/geniva-artificial-intelligence.git
   ```

3. Masuk ke direktori proyek:
   ```
   cd geniva-artificial-intelligence
   ```

4. Salin file `.env.example` menjadi `.env` dan isi dengan konfigurasi yang sesuai:
   ```
   cp .env.example .env
   ```

5. Hubungi administrator proyek di alif.datascientist@gmail.com untuk mendapatkan file `docker-compose-database.yml` dan `docker-compose-service.yml`.

6. Jalankan layanan menggunakan Docker Compose:
   ```
   docker-compose -f docker-compose-database.yml -f docker-compose-service.yml up -d
   ```

Catatan: Pastikan untuk tidak mengunggah file Docker Compose ke repositori publik jika berisi informasi sensitif.

## API Endpoints

Berdasarkan struktur proyek, endpoint spesifik mungkin didefinisikan dalam `core/app.py`. Untuk informasi lebih lanjut tentang penggunaan API, Anda bisa merujuk ke dokumentasi yang terletak di folder `documentation/`.