import os
import requests
from typing import Optional, Dict
from ..error import DataMakerError


class BaseClient:
    """Base client for DataMaker API operations."""

    def __init__(
        self,
        api_key: str = None,
        default_headers: Dict[str, Optional[str]] = None,
        base_url: Optional[str] = None,
    ):
        if default_headers is None:
            default_headers = {"Content-Type": "application/json"}

        self.api_key = api_key or os.getenv("DATAMAKER_API_KEY")
        self.headers = {
            "X-API-Key": self.api_key,
            **(default_headers or {}),
        }
        # Use DATAMAKER_API_URL environment variable if base_url is not provided
        self.base_url = base_url or os.getenv("DATAMAKER_API_URL") or "https://api.datamaker.automators.com"

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an HTTP request to the API."""
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)

        if response.status_code not in [200, 201]:
            raise DataMakerError(f"API request failed: {response.text}")

        return response
