"""Generic OData client for the CBS OpenData API.
"""

import logging
import os
from typing import Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

BASE_URL = os.getenv("CBS_API_BASE_URL")


async def fetch(
    dataset: str,
    odata_filter: Optional[str] = None,
    select: Optional[str] = None,
    orderby: Optional[str] = None,
    top: Optional[int] = None,
    skip: Optional[int] = None,
) -> list[dict]:
    """Fetches raw records from a CBS OData dataset.

    Supports all standard OData query parameters. Handles pagination
    automatically by following odata.nextLink.

    Args:
        dataset: CBS dataset code e.g. '85792NED'.
        odata_filter: OData $filter query string.
        select: Comma separated list of fields to return.
        orderby: Field to order results by.
        top: Maximum number of records to return.
        skip: Number of records to skip.

    Returns:
        List of raw record dicts from CBS.

    Raises:
        httpx.HTTPStatusError: If the CBS API returns an error response.
    """
    url = f"{BASE_URL}{dataset}/TypedDataSet"

    params = {}
    if odata_filter:
        params["$filter"] = odata_filter
    if select:
        params["$select"] = select
    if orderby:
        params["$orderby"] = orderby
    if top:
        params["$top"] = top
    if skip:
        params["$skip"] = skip

    records = []

    async with httpx.AsyncClient() as client:
        while url:
            logger.info(f"Fetching from CBS dataset {dataset}: {url}")
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            records.extend(data.get("value", []))

            # CBS paginates large results via odata.nextLink
            # params are already encoded in nextLink so we clear them
            url = data.get("odata.nextLink")
            params = {}

    logger.info(f"Fetched {len(records)} raw records from dataset {dataset}")
    return records