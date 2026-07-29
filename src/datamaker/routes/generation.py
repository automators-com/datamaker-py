from .base import BaseClient
from ..types import GeneratedData


class GenerationClient(BaseClient):
    """Client for data generation operations."""

    def generate(self, template) -> GeneratedData:
        """Generate data using a template."""
        response = self._make_request(
            "POST",
            "/datamaker",
            json=template.to_dict() if hasattr(template, "to_dict") else template,
        )
        return response.json()
