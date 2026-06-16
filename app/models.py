"""SQLAlchemy ORM model representing the housing_records table."""

from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class HousingRecord(Base):
    """Represents a single housing market record per region per period.
    """

    __tablename__ = "housing_records"

    country = Column(String(100), nullable=False, index=True)
    region = Column(String(100), nullable=False, index=True)
    region_code = Column(String(10), nullable=False)
    region_type = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=True)
    period_type = Column(String(10), nullable=False)
    average_sale_price = Column(Integer, nullable=True)
    price_index = Column(Float, nullable=True)
    total_sold = Column(Integer, nullable=True)
    year_over_year_change = Column(Float, nullable=True)
    total_value_sold = Column(Integer, nullable=True)  # in millions of euros

    __table_args__ = (
        UniqueConstraint('country', 'region_code', 'year', 'month', 'period_type', name='uq_country_region_period'),
    )