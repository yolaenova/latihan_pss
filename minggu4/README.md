# Praktikum 4 - Django Framework & ORM (Core LMS)

Praktikum implementasi Core LMS Models menggunakan **Django 5.x** dan **PostgreSQL 17** di dalam container Docker.

---

## 📋 Persyaratan Sistem

Sebelum memulai, pastikan perangkat Anda telah terpasang:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (pastikan engine aktif)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Git](https://git-scm.com/)

---

## 🚀 Cara Menjalankan Project

Ikuti langkah-langkah berikut secara berurutan untuk menjalankan project secara lokal:

### 1. Clone Repository
```bash
git clone <URL_REPOSITORY>
cd minggu4
```

### 2. Konfigurasi Environment Variables
Buat file `.env` pada root project dan sesuaikan isinya:
```env
DB_NAME=lms_db
DB_USER=lms_user
DB_PASSWORD=lms_password
```

### 3. Build & Jalankan Container
Jalankan Docker Compose dalam mode background (*detached*):
```bash
docker compose up -d --build
```

### 4. Terapkan Migrasi Database
Jalankan perintah migrasi skema tabel ke PostgreSQL:
```bash
docker compose exec app python manage.py migrate
```

### 5. Seeding Data Awal
Isi database dengan data demonstrasi (*initial seed*):
```bash
docker compose exec app python manage.py seed_demo
```

### 6. Jalankan Unit Test
Pastikan seluruh pengujian model dan fungsi lulus validasi:
```bash
docker compose exec app python manage.py test catalog
```

### 7. Akses Aplikasi
Buka web browser dan akses Django Admin melalui tautan berikut:
- **URL Admin:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 💾 Version Control (Git Milestone)

Gunakan perintah berikut untuk menyimpan milestone praktikum ke repository Git lokal:

```bash
git init
git add .
git commit -m "feat: complete week 4 django orm core lms models"
git branch -M main
```

### Push ke GitHub Remote
Hubungkan repository lokal ke GitHub dan lakukan push:

```bash
git remote add origin https://github.com/USERNAME/NAMA_REPO.git
git push -u origin main
```