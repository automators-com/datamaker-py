from .base import BaseClient
from typing import Optional, Dict, List


class TemplateFoldersClient(BaseClient):
    """Client for template folder management operations."""
    
    def get_template_folders(self) -> List[Dict]:
        """Get all template folders."""
        response = self._make_request("GET", "/templateFolders")
        return response.json()
    
    def create_template_folder(self, folder_data: Dict) -> Dict:
        """Create a new template folder."""
        response = self._make_request("POST", "/templateFolders", json=folder_data)
        return response.json()
    
    def update_template_folder(self, folder_id: str, folder_data: Dict) -> Dict:
        """Update a template folder."""
        response = self._make_request("PUT", f"/templateFolders/{folder_id}", json=folder_data)
        return response.json()
    
    def delete_template_folder(self, folder_id: str) -> Dict:
        """Delete a template folder."""
        response = self._make_request("DELETE", f"/templateFolders/{folder_id}")
        return response.json()


class ShortcutsClient(BaseClient):
    """Client for shortcuts management operations."""
    
    def get_shortcuts(self) -> List[Dict]:
        """Get all shortcuts."""
        response = self._make_request("GET", "/shortcuts")
        return response.json()
    
    def create_shortcut(self, shortcut_data: Dict) -> Dict:
        """Create a new shortcut."""
        response = self._make_request("POST", "/shortcuts", json=shortcut_data)
        return response.json()
    
    def update_shortcut(self, shortcut_id: str, shortcut_data: Dict) -> Dict:
        """Update a shortcut."""
        response = self._make_request("PUT", f"/shortcuts/{shortcut_id}", json=shortcut_data)
        return response.json()
    
    def delete_shortcut(self, shortcut_id: str) -> Dict:
        """Delete a shortcut."""
        response = self._make_request("DELETE", f"/shortcuts/{shortcut_id}")
        return response.json()


class FeedbackClient(BaseClient):
    """Client for feedback management operations."""
    
    def get_feedback(self) -> List[Dict]:
        """Get all feedback."""
        response = self._make_request("GET", "/feedback")
        return response.json()
    
    def submit_feedback(self, feedback_data: Dict) -> Dict:
        """Submit new feedback."""
        response = self._make_request("POST", "/feedback", json=feedback_data)
        return response.json()
    
    def update_feedback(self, feedback_id: str, feedback_data: Dict) -> Dict:
        """Update feedback."""
        response = self._make_request("PUT", f"/feedback/{feedback_id}", json=feedback_data)
        return response.json()
    
    def delete_feedback(self, feedback_id: str) -> Dict:
        """Delete feedback."""
        response = self._make_request("DELETE", f"/feedback/{feedback_id}")
        return response.json()