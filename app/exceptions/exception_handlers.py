"""Exception handlers registered in main.py.

Separating handlers from main.py keeps the entry point clean
and makes it easy to add new handlers without touching other code.
"""

import logging
from datetime import datetime, timezone
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.exceptions.exceptions import (
    RegionNotFoundException,
    CBSAPIException,
    SyncException,
)

logger = logging.getLogger(__name__)


def _error_response(status_code: int, detail: str) -> JSONResponse:
    """Helper that builds a consistent error response with timestamp.

    """
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": detail,
            "status_code": status_code,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


async def region_not_found_handler(request: Request, exc: RegionNotFoundException):
    """Returns a 404 when a region is not found."""
    logger.warning(f"Region not found: {exc.region}")
    return _error_response(404, str(exc))


async def cbs_api_exception_handler(request: Request, exc: CBSAPIException):
    """Returns a 502 when the CBS API fails — it's an upstream problem."""
    logger.error(f"CBS API error: {exc}")
    return _error_response(502, str(exc))


async def sync_exception_handler(request: Request, exc: SyncException):
    """Returns a 500 when the sync process fails."""
    logger.error(f"Sync failed: {exc}")
    return _error_response(500, str(exc))


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handles standard FastAPI HTTP exceptions."""
    logger.warning(f"HTTP {exc.status_code}: {exc.detail}")
    return _error_response(exc.status_code, exc.detail)


async def global_exception_handler(request: Request, exc: Exception):
    """Catches any unhandled exception — last line of defense."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return _error_response(500, "An unexpected error occurred")


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Returns a 422 when request data fails Pydantic validation.

    Includes the specific fields that failed so the caller knows what to fix.
    """
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "status_code": 422,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )