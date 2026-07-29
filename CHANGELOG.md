# datamaker-py

> Entries below 0.3.0 were carried over from the JavaScript package (`@automators/datamaker`)
> when this file was copied, and the 0.3.0-0.9.0 releases were never recorded here.
> Left as-is rather than reconstructed from memory.

## 0.10.0

### Minor Changes

- Response types are now generated from the API's OpenAPI document instead of every
  method returning `Dict`. 93 methods across 15 route modules return named
  `TypedDict`s, imported from `datamaker.types`.

  Nothing changes at runtime: methods still return the plain dicts `response.json()`
  produces, so `project["name"]` works exactly as before. The types are checker-only,
  and no existing code needs to change.

  Three schemas (`SetDetail`, `PackInstallListItem`, `SchemaGraphNavigation`) are
  composed with `allOf`, which the generator merges away rather than emitting; methods
  returning those keep `Dict`.

## 0.2.0

### Minor Changes

- 98a25ed: Add additional export methods

## 0.1.0

### Minor Changes

- e013c71: Implement basic instance instantiation and generate method to create data according to specified template.

  Exporting Template and Field types to enable improved editor completions.

## 0.0.1

### Patch Changes

- 0dbb2df: Initial version of datamaker ts/js package.
