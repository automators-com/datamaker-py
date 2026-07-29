from .base import BaseClient
from typing import Optional, Dict, List
from ..types import CurrentUser, DeletedResult, User


class UsersClient(BaseClient):
    """Client for user management operations."""

    def get_users(self) -> List[User]:
        """Get all users."""
        response = self._make_request("GET", "/users")
        return response.json()

    def create_user(self, user_data: Dict, user_id: str) -> User:
        """Create a new user."""
        # Ensure required id is present
        user_data["id"] = user_id
        response = self._make_request("POST", "/users", json=user_data)
        return response.json()

    def get_current_user(self) -> CurrentUser:
        """Get current user information."""
        response = self._make_request("GET", "/users/me")
        return response.json()

    def provision_user(self, user_data: Dict) -> DeletedResult:
        """Provision a new user.

        Returns `DeletedResult` despite the name: the API answers this route
        with a bare `{message}` and puts the meaning in the status code, and
        `DeletedResult` is the schema it shares with the delete routes.
        """
        response = self._make_request("POST", "/users/provision", json=user_data)
        return response.json()

    def update_user(self, user_id: str, user_data: Dict) -> User:
        """Update a user."""
        response = self._make_request("PUT", f"/users/{user_id}", json=user_data)
        return response.json()

    def patch_user(self, user_id: str, user_data: Dict) -> User:
        """Partially update a user."""
        response = self._make_request("PATCH", f"/users/{user_id}", json=user_data)
        return response.json()

    def delete_user(self, user_id: str) -> DeletedResult:
        """Delete a user."""
        response = self._make_request("DELETE", f"/users/{user_id}")
        return response.json()
