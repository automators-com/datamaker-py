# DataMakerLibrary.py should be created separately with the following content:

from datamaker import DataMaker, Template
from robot.api.deco import keyword


class DataMakerLibrary:
    def __init__(self):
        self.datamaker = DataMaker()

    @keyword
    def create_template(self):
        return Template(
            name="user registration",
            quantity=1,
            fields=[
                {"name": "first_name", "type": "First Name"},
                {"name": "last_name", "type": "Last Name"},
                {
                    "name": "email",
                    "type": "Derived",
                    "options": {"value": "{{first_name}}.{{last_name}}@automators.com"},
                },
            ],
        )

    @keyword
    def generate_data(self, template):
        return self.datamaker.generate(template)
