import os
from dotenv import load_dotenv
from typing import Optional, Dict
from .routes.base import BaseClient
from .routes.generation import GenerationClient
from .routes.templates import TemplatesClient

load_dotenv()


class DataMaker:
    """Main DataMaker client that provides access to all API functionality."""
    
    def __init__(
        self,
        api_key: str = None,
        default_headers: Dict[str, Optional[str]] = None,
        base_url: Optional[str] = "https://api.datamaker.automators.com",
    ):
        if default_headers is None:
            default_headers = {"Content-Type": "application/json"}
            
        # Initialize route clients
        self._generation = GenerationClient(api_key, default_headers, base_url)
        self._templates = TemplatesClient(api_key, default_headers, base_url)
        
        # Maintain backward compatibility
        self.api_key = self._generation.api_key
        self.headers = self._generation.headers
        self.base_url = self._generation.base_url

    def generate(self, template):
        """Generate data using a template."""
        return self._generation.generate(template)

    def generate_from_template_id(self, template_id: str, quantity: int = 10):
        """Generate data from a template ID with specified quantity."""
        # Get the template
        template = self._templates.get_template_by_id(template_id)
        
        # Set the quantity
        template["quantity"] = quantity
        
        # Generate data using the template
        return self.generate(template)
