from .base import BaseClient
from typing import Optional, Dict, List


class CustomDataTypesClient(BaseClient):
    """Client for custom data type management operations."""

    def get_custom_data_types(self, project_id: str) -> List[Dict]:
        """Get all custom data types for a specific project."""
        params = {"projectId": project_id}
        response = self._make_request("GET", "/customDataTypes", params=params)
        return response.json()

    def create_custom_data_type(self, data_type_data: Dict) -> Dict:
        """Create a new custom data type."""
        response = self._make_request("POST", "/customDataTypes", json=data_type_data)
        return response.json()

    def update_custom_data_type(self, data_type_id: str, data_type_data: Dict) -> Dict:
        """Update a custom data type."""
        response = self._make_request(
            "PUT", f"/customDataTypes/{data_type_id}", json=data_type_data
        )
        return response.json()

    def delete_custom_data_type(self, data_type_id: str) -> Dict:
        """Delete a custom data type."""
        response = self._make_request("DELETE", f"/customDataTypes/{data_type_id}")
        return response.json()


class EndpointFoldersClient(BaseClient):
    """Client for endpoint folder management operations."""

    def get_endpoint_folders(self) -> List[Dict]:
        """Get all endpoint folders."""
        response = self._make_request("GET", "/endpointFolders")
        return response.json()

    def create_endpoint_folder(self, folder_data: Dict) -> Dict:
        """Create a new endpoint folder."""
        response = self._make_request("POST", "/endpointFolders", json=folder_data)
        return response.json()

    def update_endpoint_folder(self, folder_id: str, folder_data: Dict) -> Dict:
        """Update an endpoint folder."""
        response = self._make_request(
            "PUT", f"/endpointFolders/{folder_id}", json=folder_data
        )
        return response.json()

    def delete_endpoint_folder(self, folder_id: str) -> Dict:
        """Delete an endpoint folder."""
        response = self._make_request("DELETE", f"/endpointFolders/{folder_id}")
        return response.json()


class EndpointsClient(BaseClient):
    """Client for endpoint management operations."""

    def get_endpoints(self) -> List[Dict]:
        """Get all endpoints."""
        response = self._make_request("GET", "/endpoints")
        return response.json()

    def create_endpoint(self, endpoint_data: Dict) -> Dict:
        """Create a new endpoint."""
        response = self._make_request("POST", "/endpoints", json=endpoint_data)
        return response.json()

    def get_endpoint(self, endpoint_id: str) -> Dict:
        """Get a specific endpoint by ID."""
        response = self._make_request("GET", f"/endpoints/{endpoint_id}")
        return response.json()

    def update_endpoint(self, endpoint_id: str, endpoint_data: Dict) -> Dict:
        """Update an endpoint."""
        response = self._make_request(
            "PUT", f"/endpoints/{endpoint_id}", json=endpoint_data
        )
        return response.json()

    def delete_endpoint(self, endpoint_id: str) -> Dict:
        """Delete an endpoint."""
        response = self._make_request("DELETE", f"/endpoints/{endpoint_id}")
        return response.json()
