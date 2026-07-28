"""Client for Plan operations.

A Plan is a reviewable description of work the agent (or a person) intends to
carry out: which entities, which targets, how many rows, and against which
environment. Plans are the governed path - they are authored, reviewed and only
then run - which is why this client covers authoring and inspection rather than
execution.

The plan RUN endpoints (`/plans/{id}/run`, `/runs`, `/signoffs`) are not wrapped
yet: they carry artifacts, logs and multi-step state, and their response shapes
are not described in the API's OpenAPI document at the time of writing. Use
``client.plans._make_request`` or add them here once the API types them.
"""

from typing import Any, Dict, List

from .base import BaseClient


class PlansClient(BaseClient):
    """Client for plan operations."""

    def get_plans(self) -> List[Dict[str, Any]]:
        """List the plans in the caller's active project.

        Returns:
            A list of plan dictionaries, newest first.
        """
        response = self._make_request("GET", "/plans")
        return response.json()

    def get_plan(self, plan_id: str) -> Dict[str, Any]:
        """Get a single plan by ID, including its full ``spec`` and ``history``.

        Args:
            plan_id: The plan's ID.

        Returns:
            The plan dictionary.
        """
        response = self._make_request("GET", f"/plans/{plan_id}")
        return response.json()

    def update_plan(self, plan_id: str, **fields: Any) -> Dict[str, Any]:
        """Update a plan.

        Args:
            plan_id: The plan's ID.
            **fields: Fields to change, e.g. ``title``, ``summary``, ``status``.

        Returns:
            The updated plan dictionary.
        """
        response = self._make_request("PATCH", f"/plans/{plan_id}", json=fields)
        return response.json()

    def delete_plan(self, plan_id: str) -> Dict[str, Any]:
        """Delete a plan.

        Note:
            This endpoint answers ``{"success": true}``, unlike the other
            resources, which answer ``{"message": ...}``. Returned as-is rather
            than normalised, so the SDK reports what the API actually sent.

        Args:
            plan_id: The plan's ID.

        Returns:
            ``{"success": True}``.
        """
        response = self._make_request("DELETE", f"/plans/{plan_id}")
        return response.json()
