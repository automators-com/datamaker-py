from .base import BaseClient
from typing import Optional, Dict, List


class ApiKeysClient(BaseClient):
    """Client for API key management operations."""
    
    def get_api_keys(self) -> List[Dict]:
        """Get all API keys."""
        response = self._make_request("GET", "/apiKeys")
        return response.json()
    
    def create_api_key(self, key: str, scope: str, name: Optional[str] = None, 
                      team_id: Optional[str] = None) -> Dict:
        """Create a new API key."""
        data = {
            "key": key,
            "scope": scope
        }
        if name:
            data["name"] = name
        if team_id:
            data["teamId"] = team_id
            
        response = self._make_request("POST", "/apiKeys", json=data)
        return response.json()
    
    def update_api_key(self, key_id: str, key: str, name: Optional[str] = None,
                      team_id: Optional[str] = None) -> Dict:
        """Update an API key."""
        data = {"key": key}
        if name:
            data["name"] = name
        if team_id:
            data["teamId"] = team_id
            
        response = self._make_request("PUT", f"/apiKeys/{key_id}", json=data)
        return response.json()
    
    def delete_api_key(self, key_id: str) -> Dict:
        """Delete an API key."""
        response = self._make_request("DELETE", f"/apiKeys/{key_id}")
        return response.json()