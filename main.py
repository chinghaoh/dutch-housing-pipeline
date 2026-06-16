"""Application entry point.
"""

import logging
from fastapi import FastAPI
from app.routers.nl_housing import router as housing_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Dutch Housing Pipeline",
    description="Housing market data from CBS OpenData, exposed via REST API.",
    version="0.1.0",
)

app.include_router(housing_router)


@app.get("/health")
async def health():
    """Health check endpoint — confirms the API is running."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)