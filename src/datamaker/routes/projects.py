from .base import BaseClient
from typing import Optional, Dict, List


class ProjectsClient(BaseClient):
    """Client for project management operations."""
    
    def get_projects(self) -> List[Dict]:
        """Get all projects."""
        response = self._make_request("GET", "/projects")
        return response.json()
    
    def create_project(self, project_data: Dict) -> Dict:
        """Create a new project."""
        response = self._make_request("POST", "/projects", json=project_data)
        return response.json()
    
    def get_project(self, project_id: str) -> Dict:
        """Get a specific project by ID."""
        response = self._make_request("GET", f"/projects/{project_id}")
        return response.json()
    
    def update_project(self, project_id: str, project_data: Dict) -> Dict:
        """Update a project."""
        response = self._make_request("PUT", f"/projects/{project_id}", json=project_data)
        return response.json()
    
    def delete_project(self, project_id: str) -> Dict:
        """Delete a project."""
        response = self._make_request("DELETE", f"/projects/{project_id}")
        return response.json()