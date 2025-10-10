from .base import BaseClient


class GenerationClient(BaseClient):
    """Client for data generation operations."""

    def generate(self, template):
        """Generate data using a template."""
        response = self._make_request(
            "POST",
            "/datamaker",
            json=template.to_dict() if hasattr(template, "to_dict") else template,
        )
        return response.json()
