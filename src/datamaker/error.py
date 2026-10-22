from typing import Any, List, Optional


class DataMakerError(Exception):
    pass


class DataMakerAPIError(DataMakerError):
    """The API answered with a non-2xx status.

    Subclasses ``DataMakerError`` and keeps its message, so existing
    ``except DataMakerError`` handlers are unaffected. Adds the status code and
    the decoded JSON body (``None`` when the body was not JSON).
    """

    def __init__(self, message: str, status_code: int, body: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body

    def _detail(self, key: str) -> Any:
        return self.body.get(key) if isinstance(self.body, dict) else None


class ReadOnlyConnectionError(DataMakerAPIError):
    """403: the connection is read-only, so DataMaker refused the write."""


class ToscaDatasetExistsError(DataMakerAPIError):
    """409: a Tosca data set of that name exists and ``on_existing`` is "fail"."""

    @property
    def dataset_id(self) -> Optional[str]:
        """The id of the data set that is already there."""
        return self._detail("datasetId")


class ToscaDatasetLockedError(DataMakerAPIError):
    """409: the data set is locked in Tosca Cloud, so it cannot be overwritten.

    A test run or a "Test data - Expert" step holds it. Retry once it is
    unlocked.
    """

    @property
    def dataset_id(self) -> Optional[str]:
        return self._detail("datasetId")


class ToscaDatasetSchemaChangedError(DataMakerAPIError):
    """409: an overwrite would drop columns the Tosca data set has.

    Tosca only overwrites in place when the columns match. Added columns are
    handled by the API; a removed column is refused unless the push asks for
    ``on_schema_change="recreate"``.
    """

    @property
    def dataset_id(self) -> Optional[str]:
        return self._detail("datasetId")

    @property
    def added_columns(self) -> List[str]:
        return self._detail("added") or []

    @property
    def removed_columns(self) -> List[str]:
        return self._detail("removed") or []


class ToscaDatasetTooLargeError(DataMakerAPIError):
    """413: more rows or bytes than one push may write.

    The row pair (``max_rows``, ``rows``) or the byte pair (``max_bytes``,
    ``bytes``) is set, depending on which cap was hit. A set, input set or
    dataset refused before its rows are loaded carries neither; the message
    names the cap.
    """

    @property
    def max_rows(self) -> Optional[int]:
        return self._detail("maxRows")

    @property
    def rows(self) -> Optional[int]:
        return self._detail("rows")

    @property
    def max_bytes(self) -> Optional[int]:
        return self._detail("maxBytes")

    @property
    def bytes(self) -> Optional[int]:
        return self._detail("bytes")


class ToscaDatasetAppendIncompleteError(DataMakerAPIError):
    """502: an append stopped part way, so only some rows were added.

    Pushing the same rows again would add the ones already added a second
    time. Push only the rows at ``not_appended_rows``.
    """

    @property
    def dataset_id(self) -> Optional[str]:
        return self._detail("datasetId")

    @property
    def appended_rows(self) -> int:
        return self._detail("appendedRows") or 0

    @property
    def not_appended_rows(self) -> List[int]:
        """Positions, in the pushed rows, of the rows that were not added."""
        return self._detail("notAppendedRows") or []
