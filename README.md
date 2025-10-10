# DataMaker

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)

The official Python library for the Automators DataMaker API.

## Installation

You can install the package using pip:

```sh
pip install datamaker-py
```

## Quick start

Basic example:

```python
from datamaker import DataMaker, Template

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
