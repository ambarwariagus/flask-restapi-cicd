# Panduan Praktikum REST API, Docker, dan CI/CD

Panduan ini memakai proyek `flask-restapi-cicd`. Satu tim berisi lima mahasiswa. Hasil akhir: Flask REST API CRUD berjalan dalam Docker, diuji otomatis oleh GitHub Actions, lalu image container dipublikasikan ke GitHub Container Registry (GHCR).

## 1. Tujuan Praktikum

Setelah praktikum, setiap anggota mampu:

- Menjelaskan resource, endpoint, HTTP method, request JSON, response JSON, dan HTTP status code.
- Membuat dan menguji operasi CRUD REST API.
- Menggunakan API key untuk endpoint yang mengubah data.
- Menjalankan aplikasi Flask dengan Docker Compose.
- Menggunakan branch, commit, pull request, dan review GitHub.
- Membaca dan memperbaiki kegagalan pipeline CI/CD.
- Mengambil image aplikasi dari GHCR.

## 2. Prasyarat

Setiap anggota menyiapkan:

- Akun GitHub.
- Git.
- Python 3.12 atau lebih baru.
- Docker Desktop.
- Editor kode.
- Akses ke repository tim.

Ketua tim membuat repository GitHub dari template atau fork proyek ini. Jangan commit file `.env`, database `*.db`, token GitHub, atau API key produksi.

## 3. Pembagian Kerja Tim

| Anggota | Peran | Tanggung jawab | Bukti kerja |
|---|---|---|---|
| 1 | Lead / integrator | Membuat repo, branch protection bila tersedia, review dan merge pull request | PR merge dan catatan integrasi |
| 2 | Backend | Mengembangkan endpoint, model SQLite, validasi input, HTTP status | PR endpoint atau validasi |
| 3 | Frontend / API consumer | Mengembangkan atau menguji halaman `/app`, Swagger, dan cURL | PR frontend atau hasil pengujian API |
| 4 | QA | Menulis atau memperbaiki `pytest`, menjalankan test, membuat skenario gagal | PR test dan log test |
| 5 | DevOps | Dockerfile, Docker Compose, workflow GitHub Actions, GHCR | PR workflow/Docker dan log Actions |

Setiap anggota wajib membuat minimal satu branch, satu commit bermakna, satu pull request, dan satu review pull request anggota lain.

## 4. Alur Kerja Git Tim

Gunakan `main` hanya untuk kode stabil. Semua perubahan lewat branch dan pull request.

```bash
# Clone repository
 git clone https://github.com/<username>/flask-restapi-cicd.git
cd flask-restapi-cicd

# Ambil perubahan terbaru
 git switch main
git pull origin main

# Contoh branch tiap peran
 git switch -c feature/backend-validation
# atau
 git switch -c test/api-user-validation
# atau
 git switch -c chore/docker-healthcheck
```

Setelah perubahan selesai:

```bash
git status
git add <file-yang-diubah>
git commit -m "feat: tambah validasi user"
git push -u origin feature/backend-validation
```

Di GitHub:

1. Buka tab **Pull requests**.
2. Buat pull request dari branch ke `main`.
3. Minta minimal satu anggota lain melakukan review.
4. Pastikan workflow **CI/CD Pipeline** hijau.
5. Merge hanya setelah lint dan test sukses.

## 5. Memahami Struktur Proyek

| Lokasi | Fungsi |
|---|---|
| `app/__init__.py` | Membuat Flask app, koneksi database, halaman `/app`, health check |
| `app/routes.py` | Endpoint REST API, validasi, dokumentasi Swagger |
| `app/models.py` | Operasi SQLite untuk user |
| `app/auth.py` | Pemeriksaan header `X-API-KEY` |
| `app/templates/index.html` | Halaman web CRUD sederhana |
| `tests/test_api.py` | Test otomatis API dan halaman aplikasi |
| `Dockerfile` | Definisi image container aplikasi |
| `docker-compose.yml` | Menjalankan aplikasi container lokal |
| `.github/workflows/ci-cd.yml` | Pipeline GitHub Actions |

## 6. Jalankan Aplikasi Lokal

### Opsi A: Python

Buat environment variable berdasarkan `.env.example`, lalu install dependency.

**PowerShell:**

```powershell
Copy-Item .env.example .env
Get-Content .env
python -m pip install -r requirements.txt
python run.py
```

Buka:

- Halaman CRUD: `http://localhost:5000/app`
- Swagger UI: `http://localhost:5000/docs`
- Health check: `http://localhost:5000/health`

### Opsi B: Docker Compose

```bash
docker compose up --build
```

Hentikan aplikasi dengan `Ctrl+C`. Jalankan background dengan `docker compose up --build -d`, lalu lihat log dengan:

```bash
docker compose logs -f web
```

## 7. Praktik RESTful API

Resource aplikasi adalah `users`.

| Operasi | Method | Endpoint | Auth | Status sukses |
|---|---|---|---|---|
| List user | GET | `/api/` | Tidak | 200 |
| Detail user | GET | `/api/<id>` | Tidak | 200 |
| Buat user | POST | `/api/` | Ya | 201 |
| Ubah user | PUT | `/api/<id>` | Ya | 200 |
| Hapus user | DELETE | `/api/<id>` | Ya | 204 |

API key demo lokal:

```text
my-secret-api-key-123
```

API key ini hanya untuk praktikum. Ganti melalui environment variable `API_KEY` sebelum deployment nyata.

### 7.1 Uji dengan Swagger UI

1. Buka `http://localhost:5000/docs`.
2. Klik **Authorize**.
3. Masukkan API key `my-secret-api-key-123` pada field `apikey`.
4. Coba `POST /api/` dengan body:

```json
{
  "username": "budi",
  "email": "budi@example.com",
  "full_name": "Budi Santoso"
}
```

5. Jalankan `GET /api/` dan pastikan user baru muncul.
6. Jalankan `PUT /api/1`, lalu `DELETE /api/1`.

### 7.2 Uji dengan cURL

```bash
# Health check
curl http://localhost:5000/health

# Create
curl -X POST http://localhost:5000/api/ \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: my-secret-api-key-123" \
  -d '{"username":"budi","email":"budi@example.com","full_name":"Budi Santoso"}'

# Read
curl http://localhost:5000/api/

# Update
curl -X PUT http://localhost:5000/api/1 \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: my-secret-api-key-123" \
  -d '{"username":"budi2","email":"budi2@example.com","full_name":"Budi Santoso"}'

# Delete
curl -X DELETE http://localhost:5000/api/1 \
  -H "X-API-KEY: my-secret-api-key-123"
```

Expected error untuk didiskusikan:

| Skenario | Status | Makna |
|---|---:|---|
| POST tanpa `X-API-KEY` | 401 | Request tidak terautentikasi |
| Email tidak valid | 400 | Request tidak lolos validasi |
| `GET /api/999` | 404 | Resource tidak ditemukan |
| Username atau email duplikat | 409 | Data konflik |

## 8. Test Otomatis dan Lint

Jalankan sebelum membuat pull request:

```bash
python -m flake8 app/ tests/ --max-line-length=120 --count --show-source --statistics
python -m pytest tests/ -v
```

Expected result:

- flake8 mengeluarkan `0`.
- pytest menampilkan seluruh test `PASSED`.

Test mengurangi risiko regresi: perubahan baru tidak boleh merusak CRUD yang sudah berjalan.

## 9. Docker dan Health Check

Bangun dan jalankan container:

```bash
docker compose up --build -d
docker compose ps
```

Uji container:

```bash
curl http://localhost:5000/health
docker compose logs --tail=50 web
docker compose down
```

Perhatikan pada `Dockerfile`:

- `python:3.12-slim` menjadi base image.
- `requirements.txt` di-install ke image.
- Gunicorn menjalankan `run:app` pada port 5000.
- `HEALTHCHECK` memanggil endpoint `/health`.

## 10. Memahami Pipeline CI/CD

Workflow berada di `.github/workflows/ci-cd.yml`.

```text
Push atau Pull Request
        |
        v
Lint: flake8
        |
        v
Test: pytest
        |
        v
Push ke main saja
        |
        v
Build image Docker dan push ke GHCR
```

### Continuous Integration (CI)

CI berjalan saat push atau pull request menuju `main`:

1. Job **Lint** mengecek gaya dan error statis Python.
2. Job **Test** menjalankan pytest bila lint sukses.

Jika lint atau test gagal, kode tidak siap merge. Job berikutnya tidak berjalan.

### Continuous Delivery (CD)

CD berjalan hanya saat push ke branch `main` dan lint plus test sukses:

1. GitHub Actions login ke GitHub Container Registry memakai `GITHUB_TOKEN`.
2. Docker build image dari `Dockerfile`.
3. Image dipush dengan tag `latest` dan tag commit SHA.

Image hasil pipeline:

```text
ghcr.io/<username>/flask-restapi-cicd:latest
```

Buka GitHub repository → **Actions** → pilih workflow run → klik job → klik step untuk membaca command dan log.

## 11. Praktikum Kegagalan Pipeline

Lakukan pada branch latihan, bukan `main`.

### Skenario A: Lint gagal

1. Buat branch `practice/fail-lint`.
2. Tambahkan baris Python yang sengaja melebihi 120 karakter pada file Python.
3. Commit, push, lalu buat pull request.
4. Buka tab **Actions**. Job **Lint** harus gagal.
5. Buka log step **Run flake8**. Catat nama file, nomor baris, dan kode error.
6. Perbaiki baris tersebut, commit, push ulang.
7. Pastikan Lint dan Test berubah hijau.

### Skenario B: Test gagal

1. Buat branch `practice/fail-test` dari `main` terbaru.
2. Ubah sementara assertion pada satu test menjadi nilai salah, contoh:

```python
assert resp.status_code == 201
```

ubah menjadi:

```python
assert resp.status_code == 200
```

3. Commit, push, lalu buat pull request.
4. Job **Test** harus gagal dan job build tidak akan berjalan.
5. Baca traceback untuk menemukan test dan assertion gagal.
6. Kembalikan assertion benar, commit, push, lalu pastikan pipeline hijau.

Jangan merge branch latihan ini ke `main`.

## 12. Praktikum Perubahan Fitur Tim

Setiap anggota membuat satu perubahan kecil sesuai perannya. Contoh aman:

- Backend: tambah validasi panjang `full_name`.
- Frontend: tambah pesan error yang lebih jelas.
- QA: tambah test untuk username duplikat.
- DevOps: perbaiki konfigurasi health check atau dokumentasi command Docker.
- Lead: review pull request, cek Actions, dan merge perubahan yang lulus.

Untuk tiap perubahan:

1. Buat issue GitHub singkat berisi tujuan dan acceptance criteria.
2. Buat branch dari `main` terbaru.
3. Ubah kode dan jalankan lint/test lokal.
4. Commit dengan pesan jelas.
5. Push branch dan buat pull request.
6. Minta review anggota lain.
7. Periksa workflow hijau.
8. Merge pull request.

## 13. Deployment Image dari GHCR

Setelah workflow CD sukses, package muncul pada halaman **Packages** repository atau profil organisasi/pemilik repo. Jika package public, mesin lain dapat menarik image:

```bash
docker pull ghcr.io/<username>/flask-restapi-cicd:latest
docker run --rm -p 5000:5000 \
  -e API_KEY="ganti-dengan-api-key-kuat" \
  -e SECRET_KEY="ganti-dengan-secret-kuat" \
  -e DATABASE_PATH=/app/data/app.db \
  ghcr.io/<username>/flask-restapi-cicd:latest
```

Untuk production, gunakan secret acak kuat, reverse proxy HTTPS, storage database persisten, dan secret manager platform deployment. Jangan memakai API key demo.

## 14. Bukti Pengumpulan

Kumpulkan satu dokumen atau slide berisi:

1. URL repository GitHub tim.
2. Daftar anggota dan peran.
3. Screenshot Swagger request POST sukses dan response `201`.
4. Screenshot halaman `/app` setelah CRUD.
5. Screenshot command lint dan pytest sukses.
6. Screenshot Docker container dan health check sukses.
7. Screenshot workflow GitHub Actions hijau.
8. Screenshot satu workflow gagal beserta log dan perbaikannya.
9. URL lima pull request, minimal satu per anggota.
10. URL package GHCR atau screenshot image berhasil dipush.

## 15. Checklist Akhir

- [ ] Semua anggota dapat clone dan menjalankan aplikasi.
- [ ] CRUD API diuji melalui Swagger atau cURL.
- [ ] POST, PUT, DELETE memakai `X-API-KEY`.
- [ ] `python -m flake8 app/ tests/ --max-line-length=120 --count --show-source --statistics` sukses.
- [ ] `python -m pytest tests/ -v` sukses.
- [ ] `docker compose up --build` sukses.
- [ ] `/health` mengembalikan status healthy.
- [ ] Minimal lima pull request dibuat dan direview.
- [ ] Workflow Actions hijau pada branch `main`.
- [ ] Image tersedia di GHCR setelah push ke `main`.
