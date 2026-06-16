"""Custom exception classes for the Dutch Housing Pipeline.

"""

class HousingPipelineException(Exception):
    """Base exception for all application errors."""
    pass

class RegionNotFoundException(HousingPipelineException):
    """Raised when a requested region does not exist in the database."""
    def __init__(self, region: str):
        self.region = region
        super().__init__(f"Region '{region}' not found")

class CBSAPIException(HousingPipelineException):
    """Raised when the CBS API returns an unexpected response."""
    def __init__(self, message: str):
        super().__init__(f"CBS API error: {message}")

class SyncException(HousingPipelineException):
    """Raised when the sync process fails."""
    pass