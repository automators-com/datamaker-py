"""Tests for pushing rows into Tosca Cloud data sets."""

import json

import pytest
from unittest.mock import Mock, patch

from src.datamaker.main import DataMaker
from src.datamaker.error import (
    DataMakerAPIError,
    DataMakerError,
    ReadOnlyConnectionError,
    ToscaDatasetExistsError,
    ToscaDatasetLockedError,
    ToscaDatasetSchemaChangedError,
    ToscaDatasetTooLargeError,
)
from src.datamaker.routes.tosca import ToscaDatasetPushResult

PUSHED = {
    "datasetId": "TDS-1",
    "name": "Orders",
    "space": "default",
    "rowsCount": 2,
    "columns": [{"name": "Customer", "type": "String"}],
    "outcome": "created",
    "addedColumns": [],
    "subsets": {"created": ["TC-1"], "existing": [], "skipped": 0},
    "example": "{TDM[Orders][Customer]}",
}


def ok(body=None, status_code=201):
    response = Mock()
    response.status_code = status_code
    response.json.return_value = body or PUSHED
    return response


def failed(status_code, body):
    response = Mock()
    response.status_code = status_code
    response.text = json.dumps(body)
    response.json.return_value = body
    return response


def push(api_key, **kwargs):
    return DataMaker(api_key=api_key).push_tosca_dataset(
        "int-1", name="Orders", **kwargs
    )


class TestPushToscaDataset:
    """The request each source kind sends, and the result it returns."""

    @patch("requests.request")
    def test_set_source(self, mock_request, api_key):
        mock_request.return_value = ok()

        result = push(api_key, set_id="set-1")

        method, url = mock_request.call_args.args
        assert method == "POST"
        assert url.endswith("/integrations/int-1/tosca/datasets")
        assert mock_request.call_args.kwargs["json"] == {
            "space": "default",
            "name": "Orders",
            "source": {"kind": "set", "setId": "set-1"},
            "onExisting": "fail",
            "onSchemaChange": "refuse",
        }
        assert isinstance(result, ToscaDatasetPushResult)
        assert result.dataset_id == "TDS-1"
        assert result.name == "Orders"
        assert result.space == "default"
        assert result.rows_count == 2
        assert result.outcome == "created"
        assert result.columns == [{"name": "Customer", "type": "String"}]
        assert result.added_columns == []
        assert result.subsets == {"created": ["TC-1"], "existing": [], "skipped": 0}
        assert result.example == "{TDM[Orders][Customer]}"
        assert result.raw == PUSHED

    @patch("requests.request")
    def test_unlocked_set(self, mock_request, api_key):
        mock_request.return_value = ok()

        push(api_key, set_id="set-1", allow_unlocked=True)

        assert mock_request.call_args.kwargs["json"]["source"] == {
            "kind": "set",
            "setId": "set-1",
            "allowUnlocked": True,
        }

    @patch("requests.request")
    def test_input_set_source_defaults_to_latest(self, mock_request, api_key):
        mock_request.return_value = ok()

        push(api_key, input_set_id="is-1")

        payload = mock_request.call_args.kwargs["json"]
        assert payload["source"] == {
            "kind": "inputSet",
            "inputSetId": "is-1",
            "version": "latest",
        }
        # Left out so the API applies its own default (TestCase for an input set).
        assert "subsetsBy" not in payload

    @patch("requests.request")
    def test_input_set_source_with_options(self, mock_request, api_key):
        mock_request.return_value = ok(
            {**PUSHED, "outcome": "overwritten", "addedColumns": ["Region"]},
            status_code=200,
        )

        result = push(
            api_key,
            input_set_id="is-1",
            version=3,
            on_existing="overwrite",
            on_schema_change="recreate",
            subsets_by="Region",
            space="qa",
        )

        payload = mock_request.call_args.kwargs["json"]
        assert payload["source"]["version"] == 3
        assert payload["onExisting"] == "overwrite"
        assert payload["onSchemaChange"] == "recreate"
        assert payload["subsetsBy"] == "Region"
        assert payload["space"] == "qa"
        assert result.outcome == "overwritten"
        assert result.added_columns == ["Region"]

    @patch("requests.request")
    def test_subsets_can_be_turned_off(self, mock_request, api_key):
        mock_request.return_value = ok()

        push(api_key, input_set_id="is-1", subsets_by=False)

        assert mock_request.call_args.kwargs["json"]["subsetsBy"] is False

    @patch("requests.request")
    def test_dataset_source(self, mock_request, api_key):
        mock_request.return_value = ok()

        push(api_key, dataset_id="ds-1")

        assert mock_request.call_args.kwargs["json"]["source"] == {
            "kind": "dataset",
            "datasetId": "ds-1",
        }

    @patch("requests.request")
    def test_rows_source(self, mock_request, api_key):
        mock_request.return_value = ok({**PUSHED, "outcome": "copied"})
        rows = [{"Customer": "0042"}, {"Customer": "0043"}]

        result = push(api_key, rows=rows, on_existing="new")

        payload = mock_request.call_args.kwargs["json"]
        assert payload["source"] == {"kind": "rows", "rows": rows}
        assert payload["onExisting"] == "new"
        assert result.outcome == "copied"


def test_hand_built_result_has_an_empty_raw():
    result = ToscaDatasetPushResult(
        dataset_id="TDS-1",
        name="Orders",
        space="default",
        rows_count=0,
        outcome="created",
        example="",
    )
    assert result.raw == {}
    assert result.raw.get("datasetId") is None


class TestPushToscaDatasetValidation:
    """Bad arguments are refused before any request is made."""

    @pytest.mark.parametrize(
        "kwargs, match",
        [
            ({}, "exactly one source"),
            ({"set_id": "s", "input_set_id": "i"}, "exactly one source"),
            ({"set_id": "s", "rows": [{"a": 1}]}, "exactly one source"),
            ({"input_set_id": "i", "dataset_id": "d"}, "exactly one source"),
            ({"rows": []}, "rows must not be empty"),
            ({"set_id": "s", "version": 2}, "version only applies"),
            ({"dataset_id": "d", "allow_unlocked": True}, "allow_unlocked only applies"),
            ({"set_id": "s", "on_existing": "replace"}, "on_existing must be one of"),
            ({"set_id": "s", "on_schema_change": "drop"}, "on_schema_change must be"),
            ({"set_id": "s", "subsets_by": True}, "subsets_by must be"),
        ],
    )
    @patch("requests.request")
    def test_rejected_locally(self, mock_request, api_key, kwargs, match):
        with pytest.raises(DataMakerError, match=match):
            push(api_key, **kwargs)
        mock_request.assert_not_called()

    @patch("requests.request")
    def test_requires_integration_id_and_name(self, mock_request, api_key):
        dm = DataMaker(api_key=api_key)
        with pytest.raises(DataMakerError, match="integration_id is required"):
            dm.push_tosca_dataset("", name="Orders", set_id="s")
        with pytest.raises(DataMakerError, match="name is required"):
            dm.push_tosca_dataset("int-1", name="", set_id="s")
        mock_request.assert_not_called()


class TestPushToscaDatasetErrors:
    """Each failure a scenario can act on arrives as its own type."""

    @patch("requests.request")
    def test_read_only_connection(self, mock_request, api_key):
        body = {
            "error": "This Tosca connection is read-only, so creating a test "
            "data set is blocked."
        }
        mock_request.return_value = failed(403, body)

        with pytest.raises(ReadOnlyConnectionError, match="read-only") as raised:
            push(api_key, set_id="s")

        assert raised.value.status_code == 403
        assert raised.value.body == body

    @patch("requests.request")
    def test_403_for_an_unreadable_source_is_not_read_only(
        self, mock_request, api_key
    ):
        mock_request.return_value = failed(403, {"error": "Missing set:read"})

        with pytest.raises(DataMakerAPIError) as raised:
            push(api_key, set_id="s")

        assert type(raised.value) is DataMakerAPIError
        assert raised.value.status_code == 403

    @patch("requests.request")
    def test_schema_change(self, mock_request, api_key):
        mock_request.return_value = failed(
            409,
            {
                "error": "The rows no longer have column Country",
                "datasetId": "TDS-1",
                "added": ["Region"],
                "removed": ["Country"],
            },
        )

        with pytest.raises(ToscaDatasetSchemaChangedError) as raised:
            push(api_key, set_id="s", on_existing="overwrite")

        assert raised.value.status_code == 409
        assert raised.value.dataset_id == "TDS-1"
        assert raised.value.added_columns == ["Region"]
        assert raised.value.removed_columns == ["Country"]

    @patch("requests.request")
    def test_name_exists(self, mock_request, api_key):
        mock_request.return_value = failed(
            409, {"error": "A data set named Orders exists", "datasetId": "TDS-1"}
        )

        with pytest.raises(ToscaDatasetExistsError) as raised:
            push(api_key, set_id="s")

        assert raised.value.status_code == 409
        assert raised.value.dataset_id == "TDS-1"

    @pytest.mark.parametrize(
        "body, on_existing, expected",
        [
            ({"code": "exists", "datasetId": "TDS-1"}, "fail", ToscaDatasetExistsError),
            ({"code": "locked", "datasetId": "TDS-1"}, "overwrite", ToscaDatasetLockedError),
            (
                {"code": "schemaChanged", "datasetId": "TDS-1", "added": [], "removed": ["A"]},
                "overwrite",
                ToscaDatasetSchemaChangedError,
            ),
            # The code wins over what the request's on_existing would suggest.
            ({"code": "locked", "datasetId": "TDS-1"}, "fail", ToscaDatasetLockedError),
        ],
    )
    @patch("requests.request")
    def test_409_code_names_the_reason(
        self, mock_request, api_key, body, on_existing, expected
    ):
        mock_request.return_value = failed(409, {"error": "refused", **body})

        with pytest.raises(expected) as raised:
            push(api_key, set_id="s", on_existing=on_existing)

        assert type(raised.value) is expected
        assert raised.value.dataset_id == "TDS-1"

    @patch("requests.request")
    def test_409_with_an_unknown_code_stays_generic(self, mock_request, api_key):
        mock_request.return_value = failed(409, {"error": "refused", "code": "other"})

        with pytest.raises(DataMakerAPIError) as raised:
            push(api_key, set_id="s", on_existing="new")

        assert type(raised.value) is DataMakerAPIError

    @patch("requests.request")
    def test_locked_data_set(self, mock_request, api_key):
        # No code: same body shape as "name exists", told apart by the request.
        mock_request.return_value = failed(
            409, {"error": 'Data set "Orders" is locked', "datasetId": "TDS-1"}
        )

        with pytest.raises(ToscaDatasetLockedError) as raised:
            push(api_key, set_id="s", on_existing="overwrite")

        assert raised.value.dataset_id == "TDS-1"

    @patch("requests.request")
    def test_too_large_before_loading_names_no_numbers(self, mock_request, api_key):
        mock_request.return_value = failed(
            413, {"error": "A push may write at most 50000 rows; dataset has 60000."}
        )

        with pytest.raises(ToscaDatasetTooLargeError, match="50000") as raised:
            push(api_key, dataset_id="d")

        assert raised.value.max_rows is None
        assert raised.value.max_bytes is None

    @patch("requests.request")
    def test_too_many_rows(self, mock_request, api_key):
        mock_request.return_value = failed(
            413, {"error": "Too many rows", "maxRows": 50000, "rows": 60000}
        )

        with pytest.raises(ToscaDatasetTooLargeError) as raised:
            push(api_key, set_id="s")

        assert raised.value.status_code == 413
        assert raised.value.max_rows == 50000
        assert raised.value.rows == 60000
        assert raised.value.max_bytes is None

    @patch("requests.request")
    def test_too_many_bytes(self, mock_request, api_key):
        mock_request.return_value = failed(
            413, {"error": "Too large", "maxBytes": 1000, "bytes": 2000}
        )

        with pytest.raises(ToscaDatasetTooLargeError) as raised:
            push(api_key, set_id="s")

        assert raised.value.max_bytes == 1000
        assert raised.value.bytes == 2000
        assert raised.value.max_rows is None

    @pytest.mark.parametrize(
        "status_code, body",
        [
            (400, {"error": "The set is not locked"}),
            (404, {"error": "Set not found"}),
            (429, {"message": "Too many Tosca data set pushes. Try again in 60s."}),
            (502, {"error": "Tosca refused the data set", "toscaError": "boom"}),
        ],
    )
    @patch("requests.request")
    def test_other_failures_carry_status_and_body(
        self, mock_request, api_key, status_code, body
    ):
        mock_request.return_value = failed(status_code, body)

        with pytest.raises(DataMakerAPIError) as raised:
            push(api_key, set_id="s")

        assert type(raised.value) is DataMakerAPIError
        assert raised.value.status_code == status_code
        assert raised.value.body == body

    @patch("requests.request")
    def test_typed_errors_are_still_datamaker_errors(self, mock_request, api_key):
        mock_request.return_value = failed(413, {"error": "too big", "maxRows": 10})

        with pytest.raises(DataMakerError):
            push(api_key, set_id="s")


class TestGetToscaDatasets:
    @patch("requests.request")
    def test_lists_a_space(self, mock_request, api_key):
        listing = {
            "space": "qa",
            "items": [
                {"id": "TDS-1", "name": "Orders", "subsetCount": 2, "isLocked": False}
            ],
        }
        mock_request.return_value = ok(listing, status_code=200)

        result = DataMaker(api_key=api_key).get_tosca_datasets("int-1", space="my qa")

        method, url = mock_request.call_args.args
        assert method == "GET"
        assert url.endswith("/integrations/int-1/tosca/datasets?space=my%20qa")
        assert result == listing

    @patch("requests.request")
    def test_default_space(self, mock_request, api_key):
        mock_request.return_value = ok({"space": "default", "items": []}, 200)

        DataMaker(api_key=api_key).get_tosca_datasets("int-1")

        assert mock_request.call_args.args[1].endswith(
            "/integrations/int-1/tosca/datasets"
        )


class TestApiErrorDetails:
    """Every failed request now carries its status and body."""

    @patch("requests.request")
    def test_non_json_body(self, mock_request, api_key):
        response = Mock()
        response.status_code = 502
        response.text = "Bad Gateway"
        response.json.side_effect = ValueError("not json")
        mock_request.return_value = response

        with pytest.raises(DataMakerAPIError, match="Bad Gateway") as raised:
            DataMaker(api_key=api_key).get_projects()

        assert raised.value.status_code == 502
        assert raised.value.body is None
