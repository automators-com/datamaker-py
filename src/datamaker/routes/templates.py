from .base import BaseClient
from ..error import DataMakerError


class TemplatesClient(BaseClient):
    """Client for template operations."""
    
    def get_templates(self):
        """Fetch all templates from the API."""
        response = self._make_request("GET", "/templates")
        return response.json()
    
    def get_template_by_id(self, template_id: str):
        """Get a specific template by ID."""
        templates = self.get_templates()
        
        if not templates:
            raise DataMakerError("No templates found in your account.")
            
        template = next(
            (temp for temp in templates if temp["id"] == template_id), None
        )
        
        if not template:
            raise DataMakerError("You must provide ID of a template from your account.")
            
        return template