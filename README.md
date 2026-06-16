# Dutch Housing Price Pipeline

A backend data pipeline that fetches housing price data from the CBS (Dutch Statistics Bureau) Open Data API, stores it in MySQL, and exposes it via a REST API.

## Stack
- FastAPI, SQLAlchemy, Pydantic, MySQL, httpx, Alembic, python-dotenv

## Setup
1. Copy `.env.example` to `.env` and fill in your values
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `alembic upgrade head`
4. Start the server: `uvicorn main:app --reload`
