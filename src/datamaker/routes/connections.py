from .base import BaseClient
from typing import Optional, Dict, List, Literal


class ConnectionsClient(BaseClient):
    """Client for database connection management operations."""
    
    def get_connections(self) -> List[Dict]:
        """Get all connections."""
        response = self._make_request("GET", "/connections")
        return response.json()
    
    def create_connection(self, name: str, connection_type: Literal["db2", "postgresql", "mysql", "mssql", "mongodb", "oracle"],
                         connection_string: str, created_by: str, project_id: str, team_id: str,
                         read_only: Optional[bool] = None, endpoint_folder_id: Optional[str] = None) -> Dict:
        """Create a new database connection."""
        data = {
            "name": name,
            "type": connection_type,
            "connectionString": connection_string,
            "createdBy": created_by,
            "projectId": project_id,
            "teamId": team_id
        }
        if read_only is not None:
            data["readOnly"] = read_only
        if endpoint_folder_id:
            data["endpointFolderId"] = endpoint_folder_id
            
        response = self._make_request("POST", "/connections", json=data)
        return response.json()
    
    def update_connection(self, connection_id: str, name: str, connection_type: Literal["db2", "postgresql", "mysql", "mssql", "mongodb", "oracle"],
                         connection_string: str, created_by: str, project_id: str, team_id: str,
                         read_only: Optional[bool] = None, endpoint_folder_id: Optional[str] = None) -> Dict:
        """Update a database connection."""
        data = {
            "name": name,
            "type": connection_type,
            "connectionString": connection_string,
            "createdBy": created_by,
            "projectId": project_id,
            "teamId": team_id
        }
        if read_only is not None:
            data["readOnly"] = read_only
        if endpoint_folder_id:
            data["endpointFolderId"] = endpoint_folder_id
            
        response = self._make_request("PUT", f"/connections/{connection_id}", json=data)
        return response.json()
    
    def delete_connection(self, connection_id: str) -> Dict:
        """Delete a database connection."""
        response = self._make_request("DELETE", f"/connections/{connection_id}")
        return response.json()
    
    def test_connection(self, connection_data: Dict) -> Dict:
        """Test a database connection."""
        response = self._make_request("POST", "/connections/test", json=connection_data)
        return response.json()
    
    def get_tables(self) -> List[Dict]:
        """Get all tables from connections."""
        response = self._make_request("GET", "/connections/tables")
        return response.json()