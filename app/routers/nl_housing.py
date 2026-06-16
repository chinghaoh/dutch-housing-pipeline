"""Housing price API endpoints.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.housing_repository import HousingRepository
from app.schemas import HousingRecordResponse, SyncResponse, PaginatedHousingResponse
from app.services.nl_housing_service import NLHousingService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/housing", tags=["housing"])

def get_repository(db: AsyncSession = Depends(get_db)) -> HousingRepository:
    """FastAPI dependency that provides a HousingRepository instance.

    Args:
        db: Injected database session.

    Returns:
        HousingRepository instance.
    """
    return HousingRepository(db)


@router.get("/", response_model=PaginatedHousingResponse)
async def get_all(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    repo = HousingRepository(db)
    total, records = await repo.get_all(skip=skip, limit=limit)
    return PaginatedHousingResponse(
        total=total,
        skip=skip,
        limit=limit,
        data=records
    )


@router.get("/{region}", response_model=list[HousingRecordResponse])
async def get_housing_by_region(
    region: str,
    repo: HousingRepository = Depends(get_repository),
):
    """Returns all housing records for a specific region.

    Available regions: Netherlands (whole country), Groningen, Fryslân, Drenthe,
    Overijssel, Flevoland, Gelderland, Utrecht, Noord-Holland,
    Zuid-Holland, Zeeland, Noord-Brabant, Limburg.
    """
    records = await repo.get_by_region(region)
    if not records:
        raise HTTPException(status_code=404, detail=f"No data found for region: {region}")
    return records


@router.post("/sync", response_model=SyncResponse)
async def sync_housing_data(
    repo: HousingRepository = Depends(get_repository),
):
    """Triggers a fresh sync from CBS OpenData.

    Safe to call multiple times — idempotent by design.
    """
    logger.info("Starting CBS housing data sync")
    service = NLHousingService()
    records = await service.fetch_housing_data()
    count = await repo.upsert(records)
    logger.info(f"Sync completed — {count} records upserted")
    return SyncResponse(message="Sync completed successfully", records_synced=count)