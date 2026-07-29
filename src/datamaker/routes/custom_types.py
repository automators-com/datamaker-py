from .base import BaseClient
from typing import Optional, Dict, List
from ..types import CustomDataType, DeletedResult, Endpoint, EndpointFolder


class CustomDataTypesClient(BaseClient):
    """Client for custom data type management operations."""

    def get_custom_data_types(self, project_id: str) -> List[CustomDataType]:
        """Get all custom data types for a specific project."""
        params = {"projectId": project_id}
        response = self._make_request("GET", "/customDataTypes", params=params)
        return response.json()

    def create_custom_data_type(self, data_type_data: Dict) -> CustomDataType:
        """Create a new custom data type."""
        response = self._make_request("POST", "/customDataTypes", json=data_type_data)
        return response.json()

    def update_custom_data_type(self, data_type_id: str, data_type_data: Dict) -> CustomDataType:
        """Update a custom data type."""
        response = self._make_request(
            "PUT", f"/customDataTypes/{data_type_id}", json=data_type_data
        )
        return response.json()

    def delete_custom_data_type(self, data_type_id: str) -> DeletedResult:
        """Delete a custom data type."""
        response = self._make_request("DELETE", f"/customDataTypes/{data_type_id}")
        return response.json()


class EndpointFoldersClient(BaseClient):
    """Client for endpoint folder management operations."""

    def get_endpoint_folders(self) -> List[EndpointFolder]:
        """Get all endpoint folders."""
        response = self._make_request("GET", "/endpointFolders")
        return response.json()

    def create_endpoint_folder(self, folder_data: Dict) -> EndpointFolder:
        """Create a new endpoint folder."""
        response = self._make_request("POST", "/endpointFolders", json=folder_data)
        return response.json()

    def update_endpoint_folder(self, folder_id: str, folder_data: Dict) -> EndpointFolder:
        """Update an endpoint folder."""
        response = self._make_request(
            "PUT", f"/endpointFolders/{folder_id}", json=folder_data
        )
        return response.json()

    def delete_endpoint_folder(self, folder_id: str) -> EndpointFolder:
        """Delete an endpoint folder.

        Returns the DELETED ROW, not the `{message}` its neighbours return.
        Taken from the API's response schema rather than assumed from the
        verb - `delete_endpoint` next door really does return DeletedResult.
        """
        response = self._make_request("DELETE", f"/endpointFolders/{folder_id}")
        return response.json()


class EndpointsClient(BaseClient):
    """Client for endpoint management operations."""

    def get_endpoints(self) -> List[Endpoint]:
        """Get all endpoints."""
        response = self._make_request("GET", "/endpoints")
        return response.json()

    def create_endpoint(self, endpoint_data: Dict) -> Endpoint:
        """Create a new endpoint."""
        response = self._make_request("POST", "/endpoints", json=endpoint_data)
        return response.json()

    def get_endpoint(self, endpoint_id: str) -> Endpoint:
        """Get a specific endpoint by ID."""
        response = self._make_request("GET", f"/endpoints/{endpoint_id}")
        return response.json()

    def update_endpoint(self, endpoint_id: str, endpoint_data: Dict) -> Endpoint:
        """Update an endpoint."""
        response = self._make_request(
            "PUT", f"/endpoints/{endpoint_id}", json=endpoint_data
        )
        return response.json()

    def delete_endpoint(self, endpoint_id: str) -> DeletedResult:
        """Delete an endpoint."""
        response = self._make_request("DELETE", f"/endpoints/{endpoint_id}")
        return response.json()

    def resolve_endpoint_auth(self, endpoint_id: str) -> Dict:
        """Resolve an endpoint's real, usable credentials.

        Unlike get_endpoint(), whose auth fields are masked (`*******`), this
        returns the decrypted Authorization header (Basic decrypted / OAuth2
        token exchanged) plus, for Basic auth, the real username/password.

        Returns a dict: {authType, authHeader, fetchCsrf, basic}.
        """
        response = self._make_request(
            "POST", "/endpoints/auth-resolve", json={"endpointId": endpoint_id}
        )
        return response.json()
