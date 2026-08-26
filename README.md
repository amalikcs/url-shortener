# URL Shortener

A URL shortening service built with FastAPI, PostgreSQL, SQLAlchemy, and Alembic.

The service allows users to create short URLs, redirect users to the original URLs, track click counts, and retrieve URL statistics.

---

## Features

- Create shortened URLs
- Generate unique 6-character short codes
- Prevent duplicate mappings for the same original URL
- Redirect short URLs to their original URLs
- Track click counts
- Retrieve URL statistics
- Retrieve all URL mappings
- PostgreSQL persistence
- Database migrations using Alembic
- Dockerized PostgreSQL
- Application logging
- Layered API, Service, and Repository architecture

---

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Docker
- Uvicorn

---

## Architecture

The application follows a layered architecture:

```text
Client
   |
   v
API Layer
   |
   v
Service Layer
   |
   v
Repository Layer
   |
   v
SQLAlchemy
   |
   v
PostgreSQL
```

### API Layer

Responsible for HTTP requests/responses, request validation, status codes, and dependency injection.

### Service Layer

Responsible for business logic, short-code generation, duplicate URL handling, click counting, and URL statistics.

### Repository Layer

Responsible for database queries, URL mapping persistence, click-count updates, and transaction handling.

### Database Layer

PostgreSQL stores URL mappings, generated short codes, click counts, and creation timestamps.

---

## Project Structure

```text
.
├── alembic/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       ├── f564df42fb54_create_url_mapping_table.py
│       ├── e7feb4ae66d9_add_index_to_short_code.py
│       └── 043e96dede5e_add_click_count.py
│
├── app/
│   ├── api/routes/url.py
│   ├── core/
│   │   ├── config.py
│   │   └── logger.py
│   ├── db/
│   │   ├── base.py
│   │   ├── db.py
│   │   ├── dependencies.py
│   │   └── session.py
│   ├── models/urls.py
│   ├── repositories/url_repository.py
│   ├── schemas/url.py
│   ├── services/url_service.py
│   └── main.py
│
├── tests/
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
├── pyproject.toml
├── requirements.txt
└── uv.lock
```

---

## Database Model

The `urls` table contains:

| Column | Description |
|---|---|
| `id` | Primary key |
| `original_url` | Original destination URL |
| `short_code` | Generated unique short code |
| `click_count` | Number of redirects |
| `created_at` | URL creation timestamp |

The `short_code` column is unique and indexed.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/urls/` | Retrieve all URL mappings |
| `POST` | `/urls/` | Create a short URL |
| `GET` | `/urls/short/{short_code}` | Retrieve the original URL |
| `GET` | `/urls/{short_code}` | Redirect to the original URL |
| `GET` | `/urls/stats/{short_code}` | Retrieve URL statistics |

---

## API Usage

### Create a Short URL

```http
POST /urls/
Content-Type: application/json
```

```json
{
  "original_url": "https://google.com"
}
```

Response:

```json
{
  "original_url": "https://google.com",
  "short_code": "j2RjHK"
}
```

If the same original URL already exists, the existing short code is returned.

### Redirect to Original URL

```http
GET /urls/j2RjHK
```

The service looks up the short code, increments the click count, and redirects the client using HTTP `302 Found`.

### Get Original URL

```http
GET /urls/short/j2RjHK
```

Response:

```json
{
  "original_url": "https://google.com"
}
```

### Get URL Statistics

```http
GET /urls/stats/j2RjHK
```

Response:

```json
{
  "short_code": "j2RjHK",
  "original_url": "https://google.com",
  "click_count": 5,
  "created_at": "2026-08-18T17:00:00Z"
}
```

### Get All URLs

```http
GET /urls/
```

Returns all stored URL mappings.

---

## URL Creation Flow

```text
POST /urls/
      |
      v
API Layer
      |
      v
URLService.create_url()
      |
      v
Check if original URL exists
      |
      +---- Yes ----> Return existing mapping
      |
      No
      |
      v
Generate short code
      |
      v
Check short-code uniqueness
      |
      +---- Exists ----> Generate another code
      |
      No
      |
      v
URLRepository.create()
      |
      v
PostgreSQL
```

The service attempts to generate a unique short code up to a configured maximum number of attempts.

---

## Redirect Flow

```text
GET /urls/{short_code}
        |
        v
API Layer
        |
        v
URLService.get_original_url()
        |
        v
Repository.get_by_short_code()
        |
        +---- Not Found ----> 404
        |
        v
Increment click count
        |
        v
RedirectResponse(status_code=302)
        |
        v
Original URL
```

Click-count failures do not prevent the user from being redirected.

---

## Logging

The application uses Python's built-in `logging` module.

Logging configuration is maintained in:

```text
app/core/logger.py
```

Individual modules create their own logger:

```python
import logging

logger = logging.getLogger(__name__)
```

The application currently uses:

- `INFO` for normal business events
- `WARNING` for unexpected but recoverable situations
- `ERROR` for failed operations

Example:

```text
2026-08-19 17:08:48,282 - INFO - app.services.url_service -
Generated unique short code: KYc1w4 for URL: https://redhat.com/

2026-08-19 17:08:48,300 - INFO - app.services.url_service -
Created new URL mapping: KYc1w4 for original URL: https://redhat.com/
```

---

## Database Migrations

Alembic manages database schema changes.

Run migrations:

```bash
alembic upgrade head
```

Create a migration:

```bash
alembic revision --autogenerate -m "migration message"
```

Rollback the latest migration:

```bash
alembic downgrade -1
```

Current migrations include:

- URL mapping table creation
- Short-code index
- Click-count column

---

## Running Locally

### Prerequisites

- Python 3.10+
- Docker
- Docker Compose

### 1. Clone the repository

```bash
git clone <repository-url>
cd url-shortener
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL

```bash
docker compose up -d
```

Check the container:

```bash
docker ps
```

PostgreSQL is exposed on port `65432`.

### 5. Configure environment variables

Create `.env` in the project root:

```env
APP_NAME=URL Shortener
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:65432/url_shortener
DEBUG=True
BASE_URL=http://127.0.0.1:8000
```

Do not commit `.env` to Git.

### 6. Run migrations

```bash
alembic upgrade head
```

### 7. Start the application

```bash
uvicorn app.main:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## Docker

Start PostgreSQL:

```bash
docker compose up -d
```

Stop PostgreSQL:

```bash
docker compose down
```

Stop PostgreSQL and remove its volume:

```bash
docker compose down -v
```

> Warning: Removing the volume deletes the PostgreSQL data stored in the Docker volume.

---

## Testing

Automated tests are planned for a future iteration.

Planned coverage includes:

- URL creation
- Duplicate URL handling
- Short-code generation and uniqueness
- Redirect behavior
- Non-existent short codes
- Click-count increment
- URL statistics
- Repository operations
- API endpoint behavior

---

## Error Handling

The current implementation uses `ValueError` and `HTTPException`.

A non-existent short code currently results in:

```text
404 Not Found
```

Custom application exceptions and global FastAPI exception handlers are planned for a future iteration.

---

## Future Improvements

Planned improvements include:

- Custom application exceptions
- Global exception handlers
- Automated tests
- Redis caching
- Prometheus metrics
- Grafana dashboards
- Rate limiting
- Authentication and authorization
- Improved click-count concurrency handling
- Asynchronous click tracking
- Event-driven analytics
- Analytics microservice
- Improved observability
- Production deployment configuration

---

## Learning Goals

This project is also being used to explore practical backend engineering concepts:

- FastAPI application architecture
- Service and Repository patterns
- SQLAlchemy ORM
- PostgreSQL
- Database transactions
- Alembic migrations
- Docker
- Logging and observability
- API design
- Caching
- Metrics
- Microservices
- Distributed-system considerations

---

## Project Status

### Version 1

The current version provides:

- URL creation
- Unique short-code generation
- Duplicate URL handling
- URL redirection
- Click tracking
- URL statistics
- PostgreSQL persistence
- Alembic migrations
- Application logging

The project will continue to evolve toward a production-oriented backend architecture.

---

## License

This project is for learning and portfolio purposes.