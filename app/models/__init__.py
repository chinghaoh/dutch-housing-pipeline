"""Import all models here so they are registered with Base.metadata.

Any new model added to this package must be imported here,
otherwise Alembic won't detect it during autogenerate.
"""

from app.models.housing import HousingRecord

__all__ = ["HousingRecord"]