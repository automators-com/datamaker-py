import os
import requests
from dotenv import load_dotenv
from typing import Optional, Dict

load_dotenv()


class DataMaker:
    def __init__(
        self,
        api_key: str = None,
        default_headers: Dict[str, Optional[str]] = {
            "Content-Type": "application/json"
        },
        base_url: Optional[str] = "https://cloud.datamaker.app/api",
    ):
        self.api_key = api_key or os.getenv("DATAMAKER_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            **(default_headers or {}),
        }
        self.base_url = base_url

    def generate(self, template):
        url = f"{self.base_url}/datamaker"
        res = requests.post(
            url=url,
            headers=self.headers,
            json=template.to_dict(),
        )
        if res.status_code != 200:
            raise Exception(f"Failed to generate data: {res.text}")
        else:
            return res.json()

    def generate_from_template_id(self, template_id: str, quantity: int = 10):
        url = f"{self.base_url}/templates"
        print(self.headers)

        # Fetch templates from the API
        response = requests.get(url, headers=self.headers)
        print(response.text)
        if response.status_code != 200:
            raise Exception("Failed to fetch templates from the server.")

        template_data = response.json()

        # Find the template by ID
        template = next(
            (temp for temp in template_data if temp["id"] == template_id), None
        )

        if not template_data:
            raise Exception("No templates found in your account.")

        if not template:
            raise Exception("You must provide ID of a template from your account.")

        template["quantity"] = quantity

        return self.generate(template)
