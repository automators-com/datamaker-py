"""Client for Tosca Cloud test data sets.

A Tosca Cloud data set (Prepare > Test data) is what a test step reads with
``{TDM[<data set>][<subset>][<column>]}``. The push goes through DataMaker:
the API reads the rows with the caller's own access, uploads them to Tosca
with the connection's credentials and writes the audit event, so a scenario
never holds Tosca credentials or calls Tosca itself.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, cast
from urllib.parse import quote

from .base import BaseClient
from ..types import ToscaDatasetPush
from ..error import (
    DataMakerAPIError,
    DataMakerError,
    ReadOnlyConnectionError,
    ToscaDatasetExistsError,
    ToscaDatasetLockedError,
    ToscaDatasetSchemaChangedError,
    ToscaDatasetTooLargeError,
)

ON_EXISTING = ("fail", "overwrite", "new")
ON_SCHEMA_CHANGE = ("refuse", "recreate")


@dataclass(frozen=True)
class ToscaDatasetPushResult:
    """The data set as Tosca holds it after a push."""

    dataset_id: str
    name: str
    space: str
    rows_count: int
    # "created", "overwritten", "recreated" or "copied"
    outcome: str
    # A ready-to-paste reference, e.g. "{TDM[Orders][Customer]}"
    example: str
    # [{"name", "type"}] as Tosca typed them: String, Double, Boolean, DateTime
    columns: List[Dict[str, str]] = field(default_factory=list)
    # Columns an overwrite added to the existing data set
    added_columns: List[str] = field(default_factory=list)
    # {"created": [names], "existing": [names], "skipped": count,
    #  "unaddressable": [values with [ or ], which {TDM[...]} cannot address]}
    subsets: Dict[str, Any] = field(default_factory=dict)
    # Columns a test step cannot read by name because they hold [ or ]. Their
    # data is in the data set; rename them to read it with {TDM[...]}.
    unaddressable_columns: List[str] = field(default_factory=list)
    # The API's response as sent, for fields this class does not name yet.
    raw: ToscaDatasetPush = field(
        default_factory=lambda: cast(ToscaDatasetPush, {}), repr=False, compare=False
    )


class ToscaClient(BaseClient):
    """Client for Tosca Cloud test data operations."""

    def get_tosca_datasets(
        self, integration_id: str, space: Optional[str] = None
    ) -> Dict[str, Any]:
        """List the test data sets in a Tosca Cloud space.

        Args:
            integration_id: The Tosca Cloud connection to read through.
            space: The Tosca Cloud space (id or name). Defaults to "default".

        Returns:
            A dictionary with ``space`` and ``items``, each item carrying
            ``id``, ``name``, ``subsetCount`` and ``isLocked``.
        """
        if not integration_id:
            raise DataMakerError("integration_id is required to list Tosca data sets.")

        endpoint = f"/integrations/{integration_id}/tosca/datasets"
        if space:
            endpoint += f"?space={quote(space, safe='')}"

        response = self._make_request("GET", endpoint)
        return response.json()

    def push_tosca_dataset(
        self,
        integration_id: str,
        name: str,
        *,
        set_id: Optional[str] = None,
        input_set_id: Optional[str] = None,
        version: Optional[Union[int, str]] = None,
        dataset_id: Optional[str] = None,
        rows: Optional[List[Dict[str, Any]]] = None,
        allow_unlocked: bool = False,
        on_existing: str = "fail",
        on_schema_change: str = "refuse",
        subsets_by: Optional[Union[str, bool]] = None,
        space: str = "default",
    ) -> ToscaDatasetPushResult:
        """Create or replace a Tosca Cloud data set from DataMaker rows.

        Give exactly one source: ``set_id``, ``input_set_id`` (with an optional
        ``version``), ``dataset_id`` or ``rows``.

        Args:
            integration_id: The Tosca Cloud connection to push through.
            name: The Tosca data set name. Unique per space; test steps
                reference the data set by this name.
            set_id: Push the rows of this DataMaker set. The set must be
                locked unless ``allow_unlocked`` is True.
            input_set_id: Push a frozen version of this input set.
            version: The input set version number, or "latest" (the default).
                Only valid with ``input_set_id``.
            dataset_id: Push the rows of this DataMaker dataset.
            rows: Inline rows, each a dictionary of column name to value.
                Column types are inferred.
            allow_unlocked: Push a set that is not locked. Only valid with
                ``set_id``.
            on_existing: What to do when a data set called ``name`` exists:
                "fail" (default), "overwrite" (replace its rows, keeping its
                id and subsets) or "new" (Tosca creates a copy beside it).
            on_schema_change: On overwrite, when the rows drop a column the
                data set has: "refuse" (default) or "recreate" (delete and
                recreate it; test steps keep working, its id and subsets are
                lost). Added columns are always handled.
            subsets_by: Create one subset per distinct value of this column,
                so each Tosca test case reads only its rows. Left unset, an
                input set is split by "TestCase" and other sources are not
                split. False turns it off.
            space: The Tosca Cloud space (id or name). Defaults to "default".

        Returns:
            A ``ToscaDatasetPushResult`` with ``dataset_id``, ``name``,
            ``space``, ``rows_count``, ``outcome``, ``columns``,
            ``added_columns``, ``subsets``, ``unaddressable_columns`` and
            ``example``. Names holding ``[`` or ``]`` cannot appear in
            ``{TDM[...]}``: such columns are listed in
            ``unaddressable_columns`` and such subset values in
            ``subsets["unaddressable"]``.

        Raises:
            DataMakerError: If the arguments do not describe exactly one source.
            ReadOnlyConnectionError: 403, the connection is read-only.
            ToscaDatasetExistsError: 409, the name is taken and ``on_existing``
                is "fail". Carries ``dataset_id``.
            ToscaDatasetLockedError: 409, an overwrite of a data set that is
                locked in Tosca Cloud. Carries ``dataset_id``.
            ToscaDatasetSchemaChangedError: 409, an overwrite would drop
                columns. Carries ``added_columns`` and ``removed_columns``.
            ToscaDatasetTooLargeError: 413, more rows or bytes than one push
                allows. Carries ``max_rows`` or ``max_bytes`` when the API
                sends them.
            DataMakerAPIError: Any other non-2xx answer, with ``status_code``
                and ``body``.

        Example:
            >>> dm = DataMaker()
            >>> result = dm.push_tosca_dataset(
            ...     integration_id,
            ...     name="Orders",
            ...     input_set_id="is_123",
            ...     on_existing="overwrite",
            ... )
            >>> result.example
            '{TDM[Orders][Customer]}'
        """
        if not integration_id:
            raise DataMakerError("integration_id is required to push a Tosca data set.")
        if not name:
            raise DataMakerError("name is required to push a Tosca data set.")
        if on_existing not in ON_EXISTING:
            raise DataMakerError(
                f"on_existing must be one of {', '.join(ON_EXISTING)}; got {on_existing!r}."
            )
        if on_schema_change not in ON_SCHEMA_CHANGE:
            raise DataMakerError(
                f"on_schema_change must be one of {', '.join(ON_SCHEMA_CHANGE)}; "
                f"got {on_schema_change!r}."
            )
        if subsets_by is True or subsets_by == "":
            raise DataMakerError("subsets_by must be a column name or False.")

        given = [
            label
            for label, value in (
                ("set_id", set_id),
                ("input_set_id", input_set_id),
                ("dataset_id", dataset_id),
                ("rows", rows),
            )
            if value is not None
        ]
        if len(given) != 1:
            raise DataMakerError(
                "Give exactly one source: set_id, input_set_id, dataset_id or rows"
                + (f"; got {', '.join(given)}." if given else "; got none.")
            )
        if version is not None and input_set_id is None:
            raise DataMakerError("version only applies to input_set_id.")
        if allow_unlocked and set_id is None:
            raise DataMakerError("allow_unlocked only applies to set_id.")

        source: Dict[str, Any]
        if set_id is not None:
            source = {"kind": "set", "setId": set_id}
            if allow_unlocked:
                source["allowUnlocked"] = True
        elif input_set_id is not None:
            source = {
                "kind": "inputSet",
                "inputSetId": input_set_id,
                "version": "latest" if version is None else version,
            }
        elif dataset_id is not None:
            source = {"kind": "dataset", "datasetId": dataset_id}
        else:
            if not rows:
                raise DataMakerError("rows must not be empty.")
            source = {"kind": "rows", "rows": rows}

        payload: Dict[str, Any] = {
            "space": space,
            "name": name,
            "source": source,
            "onExisting": on_existing,
            "onSchemaChange": on_schema_change,
        }
        if subsets_by is not None:
            payload["subsetsBy"] = subsets_by

        try:
            response = self._make_request(
                "POST", f"/integrations/{integration_id}/tosca/datasets", json=payload
            )
        except DataMakerAPIError as error:
            raise self._typed_error(error, on_existing) from error

        data: ToscaDatasetPush = response.json()
        return ToscaDatasetPushResult(
            dataset_id=data["datasetId"],
            name=data["name"],
            space=data["space"],
            rows_count=data["rowsCount"],
            outcome=data["outcome"],
            example=data["example"],
            columns=[
                {"name": column["name"], "type": column["type"]}
                for column in data["columns"]
            ],
            added_columns=data["addedColumns"],
            # "unaddressable" is always present, so callers can index it even
            # against an API from before datamaker#3683, which omits it.
            subsets={"unaddressable": [], **dict(data["subsets"])},
            # Read with .get: an API from before datamaker#3683 omits the key.
            unaddressable_columns=list(data.get("unaddressableColumns") or []),
            raw=data,
        )

    @staticmethod
    def _typed_error(error: DataMakerAPIError, on_existing: str) -> DataMakerAPIError:
        """Narrow a failed push to the error a scenario can act on."""
        body = error.body if isinstance(error.body, dict) else {}
        args = (str(error), error.status_code, error.body)

        # 403 is also what a caller without read access to the source gets,
        # so the status alone does not mean the connection is read-only.
        if error.status_code == 403 and "read-only" in str(body.get("error", "")):
            return ReadOnlyConnectionError(*args)
        if error.status_code == 409:
            by_code = {
                "exists": ToscaDatasetExistsError,
                "locked": ToscaDatasetLockedError,
                "schemaChanged": ToscaDatasetSchemaChangedError,
            }
            if body.get("code") in by_code:
                return by_code[body["code"]](*args)
            # No code: an API from before the 409s were named. "Name taken"
            # and "locked" then share a body shape, and which one it is
            # follows from what the push asked for.
            if "added" in body or "removed" in body:
                return ToscaDatasetSchemaChangedError(*args)
            if "datasetId" in body and on_existing == "fail":
                return ToscaDatasetExistsError(*args)
            if "datasetId" in body and on_existing == "overwrite":
                return ToscaDatasetLockedError(*args)
        if error.status_code == 413:
            return ToscaDatasetTooLargeError(*args)
        return error
