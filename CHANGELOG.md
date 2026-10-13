# datamaker-py

> Entries below 0.3.0 were carried over from the JavaScript package (`@automators/datamaker`)
> when this file was copied, and the 0.3.0-0.9.0 releases were never recorded here.
> Left as-is rather than reconstructed from memory.

## 0.11.2

### Patch Changes

- `ToscaDatasetPushResult` gains `unaddressable_columns`: columns a Tosca test step
  cannot read by name because they contain `[` or `]`, which `{TDM[...]}` uses as
  delimiters. Their data is still in the data set. `result.subsets["unaddressable"]`
  lists subset values skipped for the same reason (datamaker#3683). Both are empty
  against an API from before that change, which omits the fields.

- The generated types are synced to the API at datamaker `08e88b635`: `ToscaDatasetPush`
  gains `unaddressableColumns` and `subsets.unaddressable`.

## 0.11.1

### Patch Changes

- The generated types are synced to the current API: `spec/openapi.json` had fallen 111
  paths behind. `datamaker.types` goes from 120 to 177 names, including
  `ToscaDatasetPush`, the response `push_tosca_dataset` reads, which now types
  `ToscaDatasetPushResult.raw`.

- `GeneratedTemplateField` now describes the keys the API sends, `_inference` and
  `_inferenceReason`. The generator had renamed them to `field_inference` and
  `field_inferenceReason`, which no response contains.

- The generated module stays importable with the standard library alone. The API now
  marks some objects `additionalProperties: false`, which the generator emits as a
  closed `TypedDict` imported from `typing_extensions`; the closedness is dropped
  instead of adding a dependency.

- `DatasetDetail` and `InputSetDetail` join the schemas that cannot be generated,
  because they are composed with `allOf`.

## 0.11.0

### Minor Changes

- `push_tosca_dataset(integration_id, name, ...)` creates or replaces a native Tosca
  Cloud data set, the kind a test step reads with `{TDM[<data set>][<subset>][<column>]}`.
  Exactly one source is accepted (`set_id`, `input_set_id` with an optional `version`,
  `dataset_id`, or inline `rows`) and that is checked before any request is made.
  `on_existing`, `on_schema_change`, `subsets_by` and `allow_unlocked` map to the API's
  options. It returns a `ToscaDatasetPushResult` with `dataset_id`, `name`, `space`,
  `rows_count`, `outcome`, `columns`, `added_columns`, `subsets` and `example`.

- `get_tosca_datasets(integration_id, space=None)` lists the data sets in a Tosca Cloud
  space.

- API failures now raise `DataMakerAPIError`, a `DataMakerError` subclass that adds
  `status_code` and the decoded `body`. Existing `except DataMakerError` handlers are
  unaffected. A failed Tosca push narrows further: `ReadOnlyConnectionError` (403),
  `ToscaDatasetExistsError` and `ToscaDatasetLockedError` (409, with `dataset_id`),
  `ToscaDatasetSchemaChangedError`
  (409, with `added_columns` and `removed_columns`) and `ToscaDatasetTooLargeError`
  (413, with `max_rows` or `max_bytes`).

- The error classes are importable from the package root (`from datamaker import
  DataMakerError`), as `llms.txt` already documented.

- The autocomplete artifact now lists keyword-only parameters, which it used to drop.

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
