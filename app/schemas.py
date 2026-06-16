"""Pydantic schemas for request validation and API response serialization.
"""

from pydantic import BaseModel
from typing import Optional


class HousingRecordBase(BaseModel):
    """Shared fields used by both request and response schemas."""
    country: str
    region: str
    region_code: str
    region_type: str
    year: int
    month: Optional[int] = None
    period_type: str
    average_sale_price: Optional[int] = None
    price_index: Optional[float] = None
    total_sold: Optional[int] = None
    year_over_year_change: Optional[float] = None
    total_value_sold: Optional[int] = None


class HousingRecordResponse(HousingRecordBase):
    """Schema for API responses — includes database-generated fields.
    """
    id: int

    class Config:
        from_attributes = True


class SyncResponse(BaseModel):
    """Schema for the /sync endpoint response."""
    message: str
    records_synced: int