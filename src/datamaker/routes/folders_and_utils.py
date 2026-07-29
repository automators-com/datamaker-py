from .base import BaseClient
from typing import Optional, Dict, List
from ..types import DeletedResult, Feedback, Shortcut, TemplateFolder


class TemplateFoldersClient(BaseClient):
    """Client for template folder management operations."""

    def get_template_folders(self) -> List[TemplateFolder]:
        """Get all template folders."""
        response = self._make_request("GET", "/templateFolders")
        return response.json()

    def create_template_folder(self, folder_data: Dict) -> TemplateFolder:
        """Create a new template folder."""
        response = self._make_request("POST", "/templateFolders", json=folder_data)
        return response.json()

    def update_template_folder(self, folder_id: str, folder_data: Dict) -> TemplateFolder:
        """Update a template folder."""
        response = self._make_request(
            "PUT", f"/templateFolders/{folder_id}", json=folder_data
        )
        return response.json()

    def delete_template_folder(self, folder_id: str) -> DeletedResult:
        """Delete a template folder."""
        response = self._make_request("DELETE", f"/templateFolders/{folder_id}")
        return response.json()


class ShortcutsClient(BaseClient):
    """Client for shortcuts management operations."""

    def get_shortcuts(self) -> List[Shortcut]:
        """Get all shortcuts."""
        response = self._make_request("GET", "/shortcuts")
        return response.json()

    def create_shortcut(self, shortcut_data: Dict) -> Shortcut:
        """Create a new shortcut."""
        response = self._make_request("POST", "/shortcuts", json=shortcut_data)
        return response.json()

    def update_shortcut(self, shortcut_id: str, shortcut_data: Dict) -> Shortcut:
        """Update a shortcut."""
        response = self._make_request(
            "PUT", f"/shortcuts/{shortcut_id}", json=shortcut_data
        )
        return response.json()

    def delete_shortcut(self, shortcut_id: str) -> DeletedResult:
        """Delete a shortcut."""
        response = self._make_request("DELETE", f"/shortcuts/{shortcut_id}")
        return response.json()


class FeedbackClient(BaseClient):
    """Client for feedback management operations."""

    def get_feedback(self) -> List[Feedback]:
        """Get all feedback."""
        response = self._make_request("GET", "/feedback")
        return response.json()

    def submit_feedback(self, feedback_data: Dict) -> Feedback:
        """Submit new feedback."""
        response = self._make_request("POST", "/feedback", json=feedback_data)
        return response.json()

    def update_feedback(self, feedback_id: str, feedback_data: Dict) -> Feedback:
        """Update feedback."""
        response = self._make_request(
            "PUT", f"/feedback/{feedback_id}", json=feedback_data
        )
        return response.json()

    def delete_feedback(self, feedback_id: str) -> DeletedResult:
        """Delete feedback."""
        response = self._make_request("DELETE", f"/feedback/{feedback_id}")
        return response.json()
