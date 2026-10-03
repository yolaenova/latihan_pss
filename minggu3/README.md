# Praktikum Minggu 3 - Docker Containerization

Proyek backend Python HTTP server sederhana yang terhubung ke database PostgreSQL menggunakan Docker Compose, persistent volume, dan environment variables.

## Prasyarat
- Docker Desktop aktif
- Docker Compose

## Cara Menjalankan

1. Salin environment template:
cp .env.example .env

2. Jalankan container:
docker compose up --build -d

Uji endpoint:
Buka browser atau jalankan:
curl http://localhost:8000/health

Output: {"app": "ok", "database": "ok"}

3. Perintah Pengujian
Cek status container: docker compose ps

Uji koneksi database:
docker compose exec db psql -U user-1 -d db-latihan -c "SELECT 1;"

Hentikan container (data tetap aman):
docker compose down