from .base import BaseClient
from ..error import DataMakerError
from typing import Dict, List


class TemplatesClient(BaseClient):
    """Client for template operations."""

    def get_templates(self) -> List[Dict]:
        """Fetch all templates from the API."""
        response = self._make_request("GET", "/templates")
        return response.json()

    def create_template(
        self, template_data: Dict, project_id: str, team_id: str
    ) -> Dict:
        """Create a new template."""
        # Ensure required fields are present
        template_data["projectId"] = project_id
        template_data["teamId"] = team_id

        # Ensure all fields have the 'active' property set to True by default
        if "fields" in template_data:
            for field in template_data["fields"]:
                if "active" not in field:
                    field["active"] = True

        response = self._make_request("POST", "/templates", json=template_data)
        return response.json()

    def get_template(self, template_id: str) -> Dict:
        """Get a specific template by ID."""
        response = self._make_request("GET", f"/templates/{template_id}")
        return response.json()

    def update_template(self, template_id: str, template_data: Dict) -> Dict:
        """Update a template."""
        response = self._make_request(
            "PUT", f"/templates/{template_id}", json=template_data
        )
        return response.json()

    def delete_template(self, template_id: str) -> Dict:
        """Delete a template."""
        response = self._make_request("DELETE", f"/templates/{template_id}")
        return response.json()

    def get_template_by_id(self, template_id: str) -> Dict:
        """Get a specific template by ID (legacy method for backward compatibility)."""
        try:
            # Try direct API call first (more efficient)
            return self.get_template(template_id)
        except:
            # Fallback to searching through all templates (legacy behavior)
            templates = self.get_templates()

            if not templates:
                raise DataMakerError("No templates found in your account.")

            template = next(
                (temp for temp in templates if temp["id"] == template_id), None
            )

            if not template:
                raise DataMakerError(
                    "You must provide ID of a template from your account."
                )

            return template
