"""Client for key map operations - old-to-new key mappings for migrations.

A "key map" records which source-system key became which target-system key
during a migration (e.g. legacy material number to new material number).
Unlike a set (one JSON blob), every mapping is its own row on the server, so
lookups are indexed and batch writes from parallel load workers are
concurrency-safe. Entries are unique per (project, map name, object, old key)
and the last write wins for the new key.
"""

import os
from typing import Dict, List, Optional
from .base import BaseClient
from ..error import DataMakerError


class KeyMapsClient(BaseClient):
    """Client for key map operations (old-to-new key mappings)."""

    def get_keymaps(self, project_id: Optional[str] = None) -> List[Dict]:
        """List key maps for a project: one row per (mapName, object).

        Args:
            project_id: Optional project ID to scope the listing to. Falls back
                to the DATAMAKER_PROJECT_ID env var.

        Returns:
            A list of dictionaries with ``mapName``, ``object``, ``entryCount``
            and ``updatedAt``.
        """
        project_id = project_id or os.environ.get("DATAMAKER_PROJECT_ID")

        endpoint = "/keymaps"
        if project_id:
            endpoint += f"?projectId={project_id}"

        response = self._make_request("GET", endpoint)
        return response.json()

    def keymap_put(
        self,
        map_name: str,
        object: str,
        entries: Dict[str, str],
        run_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Dict:
        """Record old-to-new key mappings in a named key map (batch upsert).

        Use after creating records in a target system to remember which source
        key became which target key, so dependent data can reference the right
        keys later. Writing the same old key again overwrites its new key.
        Batches are capped at 5000 entries per call - page larger writes.

        Args:
            map_name: Logical map name grouping the entries, e.g.
                "sap-material-migration".
            object: The domain object type the keys belong to, e.g. "Material"
                or "BusinessPartner".
            entries: Mapping of old key to new key.
            run_id: Optional run/job id that minted these keys.
            project_id: Optional project ID. Falls back to DATAMAKER_PROJECT_ID.

        Returns:
            A dictionary with ``mapName``, ``object`` and ``upserted`` (count).

        Raises:
            DataMakerError: If ``map_name``, ``object`` or ``entries`` is empty.

        Example:
            >>> dm = DataMaker()
            >>> dm.keymap_put(
            ...     "sap-material-migration",
            ...     "Material",
            ...     {"MAT-001": "700001", "MAT-002": "700002"},
            ... )
        """
        if not map_name:
            raise DataMakerError("map_name is required to put key map entries.")
        if not object:
            raise DataMakerError("object is required to put key map entries.")
        if not entries:
            raise DataMakerError("entries must not be empty.")

        project_id = project_id or os.environ.get("DATAMAKER_PROJECT_ID")

        payload: Dict = {
            "mapName": map_name,
            "object": object,
            "entries": [
                {"oldKey": old_key, "newKey": new_key}
                for old_key, new_key in entries.items()
            ],
        }
        if run_id is not None:
            payload["runId"] = run_id
        if project_id:
            payload["projectId"] = project_id

        response = self._make_request("POST", "/keymaps/entries", json=payload)
        return response.json()

    def keymap_lookup(
        self,
        map_name: str,
        object: str,
        old_keys: List[str],
        project_id: Optional[str] = None,
    ) -> Dict:
        """Translate source-system keys to target-system keys (batch lookup).

        Use when generating or migrating data that references records migrated
        earlier (e.g. orders that need the NEW material numbers for OLD ones).
        Lookups are capped at 5000 keys per call - page larger reads.

        Args:
            map_name: The key map to look up in.
            object: The domain object type, e.g. "Material".
            old_keys: Source-system keys to translate.
            project_id: Optional project ID. Falls back to DATAMAKER_PROJECT_ID.

        Returns:
            A dictionary with ``mappings`` (old key to new key for the keys
            that were found) and ``missing`` (keys with no mapping yet).

        Raises:
            DataMakerError: If ``map_name``, ``object`` or ``old_keys`` is empty.

        Example:
            >>> dm = DataMaker()
            >>> result = dm.keymap_lookup(
            ...     "sap-material-migration", "Material", ["MAT-001", "MAT-999"]
            ... )
            >>> result["mappings"]
            {'MAT-001': '700001'}
            >>> result["missing"]
            ['MAT-999']
        """
        if not map_name:
            raise DataMakerError("map_name is required to look up key mappings.")
        if not object:
            raise DataMakerError("object is required to look up key mappings.")
        if not old_keys:
            raise DataMakerError("old_keys must not be empty.")

        project_id = project_id or os.environ.get("DATAMAKER_PROJECT_ID")

        payload: Dict = {
            "mapName": map_name,
            "object": object,
            "oldKeys": old_keys,
        }
        if project_id:
            payload["projectId"] = project_id

        response = self._make_request("POST", "/keymaps/lookup", json=payload)
        return response.json()

    def get_keymap_entries(
        self,
        map_name: str,
        object: Optional[str] = None,
        page: int = 1,
        page_size: int = 100,
        project_id: Optional[str] = None,
    ) -> Dict:
        """Fetch a page of a key map's entries for inspection.

        Args:
            map_name: The key map to read.
            object: Optional domain object type filter.
            page: 1-based page number.
            page_size: Entries per page (server-capped at 500).
            project_id: Optional project ID. Falls back to DATAMAKER_PROJECT_ID.

        Returns:
            A dictionary with ``entries``, ``total``, ``page`` and ``pageSize``.
        """
        project_id = project_id or os.environ.get("DATAMAKER_PROJECT_ID")

        params = [f"page={page}", f"pageSize={page_size}"]
        if object:
            params.append(f"object={object}")
        if project_id:
            params.append(f"projectId={project_id}")

        endpoint = f"/keymaps/{map_name}/entries?" + "&".join(params)
        response = self._make_request("GET", endpoint)
        return response.json()

    def delete_keymap(
        self,
        map_name: str,
        object: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Dict:
        """Drop a key map (all its entries).

        Args:
            map_name: The key map to delete.
            object: Optional domain object type - when given, only that
                object's entries are dropped.
            project_id: Optional project ID. Falls back to DATAMAKER_PROJECT_ID.

        Returns:
            Confirmation response with the deleted entry count.
        """
        project_id = project_id or os.environ.get("DATAMAKER_PROJECT_ID")

        params = []
        if object:
            params.append(f"object={object}")
        if project_id:
            params.append(f"projectId={project_id}")

        endpoint = f"/keymaps/{map_name}"
        if params:
            endpoint += "?" + "&".join(params)

        response = self._make_request("DELETE", endpoint)
        return response.json()
