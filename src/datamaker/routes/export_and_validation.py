from .base import BaseClient
from typing import Dict


class ExportClient(BaseClient):
    """Client for export operations."""
    
    def export_to_rest(self, export_data: Dict) -> Dict:
        """Export data to REST API."""
        response = self._make_request("POST", "/export/rest", json=export_data)
        return response.json()
    
    def export_to_database(self, export_data: Dict) -> Dict:
        """Export data to database."""
        response = self._make_request("POST", "/export/db", json=export_data)
        return response.json()


class ValidationClient(BaseClient):
    """Client for validation operations."""
    
    def validate_api_key(self) -> Dict:
        """Test API key authentication."""
        response = self._make_request("GET", "/validate/apiKey")
        return response.json()