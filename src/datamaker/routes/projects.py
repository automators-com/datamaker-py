from .base import BaseClient
from typing import Optional, Dict, List
from ..types import DeletedResult, Project


class ProjectsClient(BaseClient):
    """Client for project management operations."""

    def get_projects(self) -> List[Project]:
        """Get all projects."""
        response = self._make_request("GET", "/projects")
        return response.json()

    def create_project(self, project_data: Dict, team_id: str) -> Project:
        """Create a new project."""
        # Ensure required teamId is present
        project_data["teamId"] = team_id
        response = self._make_request("POST", "/projects", json=project_data)
        return response.json()

    def get_project(self, project_id: str) -> Project:
        """Get a specific project by ID."""
        response = self._make_request("GET", f"/projects/{project_id}")
        return response.json()

    def update_project(self, project_id: str, project_data: Dict) -> Project:
        """Update a project."""
        response = self._make_request(
            "PUT", f"/projects/{project_id}", json=project_data
        )
        return response.json()

    def delete_project(self, project_id: str) -> DeletedResult:
        """Delete a project."""
        response = self._make_request("DELETE", f"/projects/{project_id}")
        return response.json()
