# Dutch Housing Pipeline

A backend data pipeline that fetches housing market data from the CBS (Dutch Statistics Bureau) OpenData API, stores it in MySQL, and exposes it via a FastAPI REST API.

## Stack
- **FastAPI** — REST API framework
- **SQLAlchemy** — async ORM for MySQL
- **Pydantic** — data validation and response schemas
- **MySQL** — database (runs in Docker)
- **httpx** — async HTTP client for CBS API
- **Alembic** — database migrations
- **python-dotenv** — environment variable management

## Architecture
- **Repository pattern** — database logic separated from business logic
- **Service layer** — CBS API calls and data transformation
- **Anti-Corruption Layer** — CBS field names never leak into the domain model
- **Open/Closed principle** — adding a new country means adding a new service, not modifying existing code

## Project Structure
dutch-housing-pipeline/

├── app/
│   ├── config/
│   │   └── nl_regions.py        # NL region codes and names
│   ├── models/
│   │   └── housing.py           # SQLAlchemy ORM model
│   ├── repositories/
│   │   └── housing_repository.py # Database operations
│   ├── routers/
│   │   └── nl_housing.py        # FastAPI endpoints
│   ├── services/
│   │   ├── opendata_client.py   # Generic CBS OData client
│   │   └── nl_housing_service.py # NL housing data + ACL
│   ├── database.py              # Engine, session, Base
│   └── schemas.py               # Pydantic schemas
├── alembic/                     # Database migrations
├── main.py                      # Application entry point
├── requirements.txt
├── docker-compose.yml
├── .env.example
└── README.md

## Setup

**1. Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/dutch-housing-pipeline.git
cd dutch-housing-pipeline
```

**2. Create and fill in your environment variables:**
```bash
cp .env.example .env
```

**3. Start MySQL:**
```bash
docker-compose up -d
```

**4. Install dependencies:**
```bash
pip install -r requirements.txt
```

**5. Run database migrations:**
```bash
alembic upgrade head
```

**6. Start the server:**
```bash
uvicorn main:app --reload
```

**7. Open API docs:**
## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/housing/` | All housing records |
| GET | `/housing/{region}` | Records for a specific region |
| POST | `/housing/sync` | Trigger fresh sync from CBS |
| GET | `/health` | Health check |

## Data Source
- **CBS OpenData** — dataset `85792NED` (Bestaande koopwoningen; verkoopprijzen, prijsindex 2020=100, regio)
- 13 regions: Netherlands + 12 provinces
- Yearly data from 2015 onwards

## Future Extensions
- Add Belgian housing data (CadGis) via a new `BEHousingService`
- Scheduled sync using APScheduler or Celery
- Redis caching layer for frequently requested regions
- Kadaster transaction data with API access