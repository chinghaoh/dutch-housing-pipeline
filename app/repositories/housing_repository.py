"""Repository for housing record database operations.
"""

import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence, and_
from app.models.housing import HousingRecord

logger = logging.getLogger(__name__)


class HousingRepository:
    """Handles all database operations for housing records."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[HousingRecord]:
        result = await self.db.execute(select(HousingRecord))
        return result.scalars().all()

    async def get_by_region(self, region: str) -> Sequence[HousingRecord]:
        result = await self.db.execute(
            select(HousingRecord).where(HousingRecord.region == region)
        )
        return result.scalars().all()

    async def upsert(self, records: list[dict]) -> int:
        for record in records:
            result = await self.db.execute(
                select(HousingRecord).where(
                    and_(
                        HousingRecord.country == record["country"],
                        HousingRecord.region_code == record["region_code"],
                        HousingRecord.year == record["year"],
                        HousingRecord.month == record["month"],
                        HousingRecord.period_type == record["period_type"],
                    )
                )
            )
            existing = result.scalar_one_or_none()

            if existing:
                for key, value in record.items():
                    setattr(existing, key, value)
            else:
                self.db.add(HousingRecord(**record))

        await self.db.commit()
        return len(records)