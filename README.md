# User Registration API

Demo RESTful API untuk materi kuliah: **REST API**, **Docker**, **CI/CD**, dan **Security**.

Panduan praktikum tim lima mahasiswa: [PANDUAN_CICD_MAHASISWA.md](PANDUAN_CICD_MAHASISWA.md).

## Tech Stack

- **Backend**: Python / Flask + flask-restx (Swagger UI)
- **Database**: SQLite
- **Container**: Docker + docker-compose
- **CI/CD**: GitHub Actions → GitHub Container Registry (ghcr.io)

## Quick Start

### Local Development

```bash
# Clone repo
git clone https://github.com/<username>/register_cicd.git
cd register_cicd

# Setup environment
cp .env.example .env
pip install -r requirements.txt

# Run
python run.py
```

### Docker

```bash
# Build & run
docker compose up --build

# Atau pull dari GitHub Container Registry
docker pull ghcr.io/<username>/register_cicd:latest
docker run -p 5000:5000 -e API_KEY=my-key ghcr.io/<username>/register_cicd:latest
```

## API Endpoints

| Method | Path             | Auth | Deskripsi         |
|--------|------------------|------|-------------------|
| GET    | `/health`        | No   | Health check      |
| GET    | `/api/`          | No   | List semua users  |
| GET    | `/api/<id>`      | No   | Get user by ID    |
| POST   | `/api/`          | Yes  | Buat user baru    |
| PUT    | `/api/<id>`      | Yes  | Update user       |
| DELETE | `/api/<id>`      | Yes  | Hapus user        |

## Swagger UI

Buka `http://localhost:5000/docs` untuk interactive API documentation.

## Authentication

Endpoint yang mengubah data (POST, PUT, DELETE) membutuhkan header:

```
X-API-KEY: my-secret-api-key-123
```

## Contoh Request

```bash
# List users
curl http://localhost:5000/api/

# Create user (dengan auth)
curl -X POST http://localhost:5000/api/ \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: my-secret-api-key-123" \
  -d '{"username": "john", "email": "john@example.com", "full_name": "John Doe"}'

# Get user
curl http://localhost:5000/api/1

# Update user
curl -X PUT http://localhost:5000/api/1 \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: my-secret-api-key-123" \
  -d '{"username": "john_updated", "email": "john2@example.com", "full_name": "John Updated"}'

# Delete user
curl -X DELETE http://localhost:5000/api/1 \
  -H "X-API-KEY: my-secret-api-key-123"
```

## CI/CD Pipeline

```
Push ke main → Lint (flake8) → Test (pytest) → Build Docker → Push ke ghcr.io
```

Pipeline otomatis berjalan saat:
- **Push** ke branch `main`
- **Pull Request** ke branch `main`

## Testing

```bash
pip install pytest
pytest tests/ -v
```

## Materi yang Dicakup

### 1. RESTful API
- CRUD operations (Create, Read, Update, Delete)
- HTTP methods (GET, POST, PUT, DELETE)
- Status codes (200, 201, 204, 400, 401, 404, 409)
- Request/Response JSON format
- API documentation (Swagger/OpenAPI)

### 2. Security
- API Key authentication
- Input validation
- CORS configuration
- Environment variables untuk secrets
- `.env` file (tidak di-commit ke repo)

### 3. Docker & Deployment
- Dockerfile (containerization)
- docker-compose (orchestration)
- Health check endpoint
- Gunicorn (production WSGI server)

### 4. CI/CD
- GitHub Actions workflow
- Automated linting (flake8)
- Automated testing (pytest)
- Docker image build & push
- GitHub Container Registry (ghcr.io)
