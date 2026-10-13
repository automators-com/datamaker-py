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

## Push a set into Tosca Cloud

`push_tosca_dataset` creates or replaces a native Tosca Cloud data set from a saved
set, an input set version, a dataset or inline rows. A Tosca test step reads it with
`{TDM[<data set>][<subset>][<column>]}`.

```python
from datamaker import DataMaker, ToscaDatasetSchemaChangedError

dm = DataMaker()

try:
    result = dm.push_tosca_dataset(
        integration_id,
        name="Orders",
        input_set_id="is_123",        # or set_id=..., dataset_id=..., rows=[...]
        on_existing="overwrite",      # "fail" (default) | "overwrite" | "new"
    )
    print(result.dataset_id, result.rows_count, result.outcome, result.example)
except ToscaDatasetSchemaChangedError as e:
    # The rows dropped a column the data set has. Pass on_schema_change="recreate"
    # to delete and recreate it instead.
    print("removed:", e.removed_columns, "added:", e.added_columns)
```

An input set gets one Tosca subset per test case by default; `subsets_by` picks another
column or turns it off with `False`. `get_tosca_datasets(integration_id)` lists what a
space already holds.

## Autocomplete Types

This SDK automatically generates TypeScript autocomplete definitions for use in the [datamaker application](https://github.com/automators/datamaker). 

The artifact is generated automatically on every push to the `main` branch and can be fetched from:

```
https://raw.githubusercontent.com/automators/datamaker-py/main/artifacts/autocomplete-types.ts
```

See [`artifacts/README.md`](artifacts/README.md) for more details.

## Development & Contibutions

See the [contributing.md](/CONTRIBUTING.md) guide for details on how to contribute to this project.

## Types

Response types are **generated** from the API's OpenAPI document, not hand-written:

```
spec/openapi.json  ->  src/datamaker/generated/schema.py  ->  src/datamaker/types.py
```

Import from `datamaker.types`, which resolves each spec schema name to the class
that really matches it:

```python
from datamaker.types import Project, Plan, Template

projects: list[Project] = dm.get_projects()
```

They are `TypedDict`s, so nothing changes at runtime — methods still return the
plain dicts `response.json()` produces, and `project["name"]` works exactly as
before. The types are checker-only.

To regenerate after the API changes:

```bash
python scripts/generate_schema.py
```

CI runs `python scripts/generate_schema.py --check` and fails if the committed
types drift from the spec.

Five schemas cannot currently be generated (`SetDetail`, `DatasetDetail`,
`InputSetDetail`, `PackInstallListItem`, `SchemaGraphNavigation`): they are composed
with `allOf`, or only appear inside a union, so the generator does not emit them as a
named class. Methods returning those keep
`Dict`. The generator script lists them explicitly and fails if the set grows.
