from .base import BaseClient
from typing import Optional, Dict, List


class UsersClient(BaseClient):
    """Client for user management operations."""

    def get_users(self) -> List[Dict]:
        """Get all users."""
        response = self._make_request("GET", "/users")
        return response.json()

    def create_user(self, user_data: Dict, user_id: str) -> Dict:
        """Create a new user."""
        # Ensure required id is present
        user_data["id"] = user_id
        response = self._make_request("POST", "/users", json=user_data)
        return response.json()

    def get_current_user(self) -> Dict:
        """Get current user information."""
        response = self._make_request("GET", "/users/me")
        return response.json()

    def provision_user(self, user_data: Dict) -> Dict:
        """Provision a new user."""
        response = self._make_request("POST", "/users/provision", json=user_data)
        return response.json()

    def update_user(self, user_id: str, user_data: Dict) -> Dict:
        """Update a user."""
        response = self._make_request("PUT", f"/users/{user_id}", json=user_data)
        return response.json()

    def patch_user(self, user_id: str, user_data: Dict) -> Dict:
        """Partially update a user."""
        response = self._make_request("PATCH", f"/users/{user_id}", json=user_data)
        return response.json()

    def delete_user(self, user_id: str) -> Dict:
        """Delete a user."""
        response = self._make_request("DELETE", f"/users/{user_id}")
        return response.json()
