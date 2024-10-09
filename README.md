# DataMaker

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## What is it?

The official Python library for the datamaker API. Datamaker assists with generating realistic relational data for testing and development purposes.

## Installation

Package name TBD

```sh
pip install datamaker
```

## Quick start

Basic example:

```python
from src.main import DataMaker
from src.template import Template

# Create an instance of DataMaker
datamaker = DataMaker()


def main():
    # Define the template
    template = Template(
        name="basic template",
        quantity=2,
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

    # Generate data using the template
    result = datamaker.generate(template)
    print(result)


if __name__ == "__main__":
    main()

```

## Development & Contibutions

See the [contributing.md](/CONTRIBUTING.md) guide for details on how to contribute to this project.

## License

[MIT](https://github.com/automators-com/datamaker-py/blob/main/LICENSE)
