"""Client for masking policy operations.

A masking policy is the set of field rules a masked generation or export
applies. Two flags decide how it behaves, and they are easy to confuse:

``consistent``
    The same input masks to the same output within the policy, so joins across
    masked tables still line up.

``reversible``
    The mapping is recorded so it can be reversed later. A reversible policy
    mints its mappings into the KeyMap named by ``key_map_name``, which is why
    that argument only means anything alongside it.
"""

import os
from typing import Any, Dict, List, Optional

from .base import BaseClient


class MaskingPoliciesClient(BaseClient):
    """Client for masking policy operations."""

    def get_masking_policies(
        self, project_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Fetch the masking policies in the caller's project/team scope.

        Args:
            project_id: Optional project ID to scope the listing to. Falls back
                to the DATAMAKER_PROJECT_ID env var.

        Returns:
            A list of masking policy dictionaries.
        """
        project_id = project_id or os.environ.get("DATAMAKER_PROJECT_ID")

        endpoint = "/masking-policies"
        if project_id:
            endpoint += f"?projectId={project_id}"

        response = self._make_request("GET", endpoint)
        return response.json()

    def get_masking_policy(self, policy_id: str) -> Dict[str, Any]:
        """Get a single masking policy by ID.

        Args:
            policy_id: The policy's ID.

        Returns:
            The masking policy dictionary.
        """
        response = self._make_request("GET", f"/masking-policies/{policy_id}")
        return response.json()

    def create_masking_policy(
        self,
        name: str,
        fields: Any,
        description: Optional[str] = None,
        consistent: Optional[bool] = None,
        reversible: Optional[bool] = None,
        key_map_name: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a masking policy.

        Args:
            name: The policy name.
            fields: The field rule list. Shape varies by rule type.
            description: Optional description.
            consistent: Same input masks to the same output. Defaults to the
                API's own default (True) when omitted.
            reversible: Record the mapping so masking can be reversed. Requires
                ``key_map_name`` to be useful.
            key_map_name: The KeyMap a reversible policy mints mappings into.
            project_id: Project to create it in. Falls back to
                DATAMAKER_PROJECT_ID.

        Returns:
            The created masking policy dictionary.
        """
        project_id = project_id or os.environ.get("DATAMAKER_PROJECT_ID")

        # Only send what the caller set: omitting a key lets the API apply its
        # own default, whereas sending null would override it.
        payload: Dict[str, Any] = {"name": name, "fields": fields}
        if description is not None:
            payload["description"] = description
        if consistent is not None:
            payload["consistent"] = consistent
        if reversible is not None:
            payload["reversible"] = reversible
        if key_map_name is not None:
            payload["keyMapName"] = key_map_name
        if project_id:
            payload["projectId"] = project_id

        response = self._make_request("POST", "/masking-policies", json=payload)
        return response.json()

    def update_masking_policy(self, policy_id: str, **fields: Any) -> Dict[str, Any]:
        """Update a masking policy.

        Args:
            policy_id: The policy's ID.
            **fields: Fields to change. Use API spellings for multi-word keys,
                e.g. ``keyMapName``.

        Returns:
            The updated masking policy dictionary.
        """
        response = self._make_request(
            "PATCH", f"/masking-policies/{policy_id}", json=fields
        )
        return response.json()

    def delete_masking_policy(self, policy_id: str) -> Dict[str, Any]:
        """Delete a masking policy.

        Args:
            policy_id: The policy's ID.

        Returns:
            ``{"message": "Masking policy deleted"}``.
        """
        response = self._make_request("DELETE", f"/masking-policies/{policy_id}")
        return response.json()
