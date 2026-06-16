"""Application entry point."""

import logging
from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse
from fastapi.exceptions import RequestValidationError

from app.routers.nl_housing import router as housing_router
from app.exceptions.exceptions import (
    RegionNotFoundException,
    CBSAPIException,
    SyncException,
)
from app.exceptions.exception_handlers import (
    region_not_found_handler,
    cbs_api_exception_handler,
    sync_exception_handler,
    http_exception_handler,
    global_exception_handler,
    validation_exception_handler
)

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

# Register exception handlers — order matters, specific before generic
app.add_exception_handler(RegionNotFoundException, region_not_found_handler)
app.add_exception_handler(CBSAPIException, cbs_api_exception_handler)
app.add_exception_handler(SyncException, sync_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(housing_router)


@app.get("/health")
async def health():
    """Health check endpoint — confirms the API is running."""
    return {"status": "ok"}

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)