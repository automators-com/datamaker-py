from .base import BaseClient
from typing import Optional, Dict, List
from ..types import DeletedResult, MemberInviteResult, Team, TeamMember, TeamSetupResult


class TeamsClient(BaseClient):
    """Client for team management operations."""

    def get_teams(self) -> List[Team]:
        """Get all teams."""
        response = self._make_request("GET", "/teams")
        return response.json()

    def create_team(self, team_data: Dict) -> Team:
        """Create a new team."""
        response = self._make_request("POST", "/teams", json=team_data)
        return response.json()

    def update_team(self, team_id: str, team_data: Dict) -> Team:
        """Update a team."""
        response = self._make_request("PUT", f"/teams/{team_id}", json=team_data)
        return response.json()

    def delete_team(self, team_id: str) -> DeletedResult:
        """Delete a team."""
        response = self._make_request("DELETE", f"/teams/{team_id}")
        return response.json()

    def setup_team(self, team_data: Dict) -> TeamSetupResult:
        """Setup a new team."""
        response = self._make_request("POST", "/setup/teams", json=team_data)
        return response.json()


class TeamMembersClient(BaseClient):
    """Client for team member management operations."""

    def get_team_members(self) -> List[TeamMember]:
        """Get all team members."""
        response = self._make_request("GET", "/teamMembers")
        return response.json()

    def add_team_member(self, member_data: Dict) -> TeamMember:
        """Add a new team member."""
        response = self._make_request("POST", "/teamMembers", json=member_data)
        return response.json()

    def invite_team_member(self, invite_data: Dict) -> MemberInviteResult:
        """Invite a new team member."""
        response = self._make_request("POST", "/teamMembers/invite", json=invite_data)
        return response.json()

    def update_team_member(self, member_id: str, member_data: Dict) -> TeamMember:
        """Update a team member."""
        response = self._make_request(
            "PUT", f"/teamMembers/{member_id}", json=member_data
        )
        return response.json()

    def remove_team_member(self, member_id: str) -> DeletedResult:
        """Remove a team member."""
        response = self._make_request("DELETE", f"/teamMembers/{member_id}")
        return response.json()
