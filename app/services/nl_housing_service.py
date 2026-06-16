"""Netherlands housing data service.

Fetches data from CBS dataset 85792NED and transforms it into our
internal domain model. This is the Anti-Corruption Layer — CBS field
names and conventions are translated here and never leak elsewhere.
"""

import logging
from typing import Optional
from app.config.nl_regions import REGIONS
from app.services.opendata_client import fetch

logger = logging.getLogger(__name__)

DATASET = "85792NED"
START_YEAR = "2015JJ00"

SELECT_FIELDS = ",".join([
    "RegioS",
    "Perioden",
    "GemiddeldeVerkoopprijs_7",
    "PrijsindexVerkoopprijzen_1",
    "VerkochteWoningen_4",
    "OntwikkelingTOVEenJaarEerder_3",
    "TotaleWaardeVerkoopprijzen_8",
])


class NLHousingService:
    """Fetches and transforms Dutch housing data from CBS OpenData."""

    def _build_filter(self) -> str:
        """Builds the OData filter for NL regions and yearly data from 2015.

        Returns:
            str: OData $filter string.
        """
        region_filter = " or ".join(
            [f"RegioS eq '{code}  '" for code in REGIONS.keys()]
        )
        return f"({region_filter}) and Perioden ge '2015JJ00'"

    def _parse_period(self, perioden: str) -> tuple[int, Optional[int], str]:
        """Parses CBS Perioden string into year, month and period_type.

        Args:
            perioden: Raw CBS period string e.g. '2024JJ00'.

        Returns:
            Tuple of (year, month, period_type).
        """
        year = int(perioden[:4])

        if "JJ" in perioden:
            return year, None, "yearly"
        elif "MM" in perioden:
            month = int(perioden[6:8])
            return year, month, "monthly"
        else:
            return year, None, "unknown"

    def _transform(self, raw: dict) -> Optional[dict]:
        """Transforms a raw CBS record into our internal domain model.

        This is the Anti-Corruption Layer — all CBS field names are
        mapped to our clean domain fields here and nowhere else.

        Args:
            raw: Raw record dict from CBS API.

        Returns:
            Transformed record dict, or None if region is out of scope.
        """
        region_code = raw.get("RegioS", "").strip()

        if region_code not in REGIONS:
            return None

        year, month, period_type = self._parse_period(raw["Perioden"])

        if period_type != "yearly":
            return None

        return {
            "country": "NL",
            "region": REGIONS[region_code]["name"],
            "region_code": region_code,
            "region_type": REGIONS[region_code]["type"],
            "year": year,
            "month": month,
            "period_type": period_type,
            "average_sale_price": raw.get("GemiddeldeVerkoopprijs_7"),
            "price_index": raw.get("PrijsindexVerkoopprijzen_1"),
            "total_sold": raw.get("VerkochteWoningen_4"),
            "year_over_year_change": raw.get("OntwikkelingTOVEenJaarEerder_3"),
            "total_value_sold": raw.get("TotaleWaardeVerkoopprijzen_8"),
        }

    async def fetch_housing_data(self) -> list[dict]:
        """Fetches and transforms NL housing data from CBS.

        Returns:
            List of transformed housing record dicts.
        """
        raw_records = await fetch(
            dataset=DATASET,
            odata_filter=self._build_filter(),
            select=SELECT_FIELDS,
        )
        transformed = [self._transform(r) for r in raw_records]
        result = [r for r in transformed if r is not None]
        logger.info(f"Transformed {len(result)} NL housing records")
        return result