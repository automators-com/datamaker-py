"""Client for set operations - persistent named snapshots of rows.

A "set" is a saved snapshot of generated or fetched rows (e.g. a pinned
regression dataset, a shared fixture, or an audit copy of what was masked and
exported). Sets are scoped to a project/team and show up on the DataMaker Sets
page.
"""

import os
from typing import Dict, List, Optional, Any
from .base import BaseClient
from ..error import DataMakerError


class SetsClient(BaseClient):
    """Client for set operations (persistent saved row snapshots)."""

    def get_sets(self, project_id: Optional[str] = None) -> List[Dict]:
        """Fetch all saved sets for the caller's project/team scope.

        Args:
            project_id: Optional project ID to scope the listing to. Falls back
                to the DATAMAKER_PROJECT_ID env var. When omitted, the API
                returns every set the API key can access.

        Returns:
            A list of set metadata dictionaries.
        """
        project_id = project_id or os.environ.get("DATAMAKER_PROJECT_ID")

        endpoint = "/sets"
        if project_id:
            endpoint += f"?projectId={project_id}"

        response = self._make_request("GET", endpoint)
        return response.json()

    def get_set(self, set_id: str) -> Dict:
        """Get a single saved set by ID, including its full ``data`` payload.

        Args:
            set_id: The unique identifier of the set.

        Returns:
            The set dictionary (including its saved rows in ``data``).
        """
        response = self._make_request("GET", f"/sets/{set_id}")
        return response.json()

    def create_set(
        self,
        name: str,
        data: Optional[Any] = None,
        description: Optional[str] = None,
        row_count: Optional[int] = None,
        project_id: Optional[str] = None,
    ) -> Dict:
        """Create (save) a new set.

        Args:
            name: A name for the saved set.
            data: The rows payload to save - typically a list of row dicts.
                When omitted, an empty set is created.
            description: Optional short description of what the set captures.
            row_count: Optional explicit row count. Derived from ``data`` by the
                API when omitted.
            project_id: Optional project ID the set belongs to. Falls back to the
                DATAMAKER_PROJECT_ID env var. Required when the API key is not
                already scoped to a single project.

        Returns:
            The created set dictionary.

        Raises:
            DataMakerError: If ``name`` is not provided.
        """
        if not name:
            raise DataMakerError("name is required to create a set.")

        project_id = project_id or os.environ.get("DATAMAKER_PROJECT_ID")

        set_data: Dict[str, Any] = {"name": name}
        if data is not None:
            set_data["data"] = data
        if description is not None:
            set_data["description"] = description
        if row_count is not None:
            set_data["rowCount"] = row_count
        if project_id:
            set_data["projectId"] = project_id

        response = self._make_request("POST", "/sets", json=set_data)
        return response.json()

    def update_set(
        self,
        set_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        data: Optional[Any] = None,
        row_count: Optional[int] = None,
    ) -> Dict:
        """Update a saved set.

        Only the fields that are provided are sent; the rest are left unchanged.

        Args:
            set_id: The unique identifier of the set to update.
            name: New name for the set.
            description: New description (pass ``None`` to leave unchanged).
            data: Replacement rows payload. The API keeps ``rowCount`` in sync
                whenever ``data`` changes.
            row_count: Explicit row count override.

        Returns:
            The updated set dictionary.
        """
        update_data: Dict[str, Any] = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if data is not None:
            update_data["data"] = data
        if row_count is not None:
            update_data["rowCount"] = row_count

        response = self._make_request("PATCH", f"/sets/{set_id}", json=update_data)
        return response.json()

    def delete_set(self, set_id: str) -> Dict:
        """Delete a saved set by ID.

        Args:
            set_id: The unique identifier of the set to delete.

        Returns:
            Confirmation response.
        """
        response = self._make_request("DELETE", f"/sets/{set_id}")
        return response.json()

    def save_set(
        self,
        name: str,
        data: Any,
        description: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Dict:
        """Convenience method to save rows as a named set.

        This is the most common entry point: hand it a name and the rows you
        want to keep. Project context is pulled from the DATAMAKER_PROJECT_ID
        env var when not provided, which is convenient inside DataMaker sandbox
        environments where it is pre-configured.

        Args:
            name: A name for the saved set.
            data: The rows to save - typically a list of row dicts.
            description: Optional short description of what the set captures.
            project_id: Optional project ID. Falls back to DATAMAKER_PROJECT_ID.

        Returns:
            The created set dictionary.

        Example:
            >>> dm = DataMaker()
            >>> rows = dm.generate(template)
            >>> result = dm.save_set("nightly-regression", rows)
            >>> print(f"Saved set: {result['name']} ({result['rowCount']} rows)")
        """
        return self.create_set(
            name=name,
            data=data,
            description=description,
            project_id=project_id,
        )
