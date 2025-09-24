"""Tests for the route client classes."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.datamaker.routes.base import BaseClient
from src.datamaker.routes.generation import GenerationClient
from src.datamaker.routes.templates import TemplatesClient
from src.datamaker.routes.api_keys import ApiKeysClient
from src.datamaker.routes.connections import ConnectionsClient
from src.datamaker.routes.projects import ProjectsClient
from src.datamaker.routes.users import UsersClient
from src.datamaker.routes.teams import TeamsClient, TeamMembersClient
from src.datamaker.error import DataMakerError


class TestBaseClient:
    """Test cases for the BaseClient class."""

    def test_init_with_api_key(self, api_key):
        """Test BaseClient initialization with API key."""
        client = BaseClient(api_key=api_key)
        assert client.api_key == api_key
        assert client.base_url == "https://api.datamaker.automators.com"
        assert "X-API-Key" in client.headers
        assert client.headers["X-API-Key"] == api_key

    def test_init_with_env_var(self, api_key):
        """Test BaseClient initialization with environment variable."""
        with patch.dict('os.environ', {'DATAMAKER_API_KEY': api_key}):
            client = BaseClient()
            assert client.api_key == api_key

    @patch('requests.request')
    def test_make_request_success(self, mock_request, api_key):
        """Test successful API request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response
        
        client = BaseClient(api_key=api_key)
        response = client._make_request("GET", "/test")
        
        mock_request.assert_called_once()
        assert response == mock_response

    @patch('requests.request')
    def test_make_request_error(self, mock_request, api_key):
        """Test API request error handling."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_request.return_value = mock_response
        
        client = BaseClient(api_key=api_key)
        
        with pytest.raises(DataMakerError):
            client._make_request("GET", "/test")


class TestGenerationClient:
    """Test cases for the GenerationClient class."""

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_generate_with_dict(self, mock_make_request, api_key):
        """Test generation with dictionary template."""
        mock_response = Mock()
        mock_response.json.return_value = {"generated_data": "test"}
        mock_make_request.return_value = mock_response
        
        client = GenerationClient(api_key=api_key)
        template = {"fields": [{"name": "test", "type": "firstName"}]}
        
        result = client.generate(template)
        
        mock_make_request.assert_called_once_with("POST", "/datamaker", json=template)
        assert result == {"generated_data": "test"}

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_generate_with_object(self, mock_make_request, api_key):
        """Test generation with object template."""
        mock_response = Mock()
        mock_response.json.return_value = {"generated_data": "test"}
        mock_make_request.return_value = mock_response
        
        client = GenerationClient(api_key=api_key)
        template = Mock()
        template.to_dict.return_value = {"fields": [{"name": "test", "type": "firstName"}]}
        
        result = client.generate(template)
        
        mock_make_request.assert_called_once_with("POST", "/datamaker", json={"fields": [{"name": "test", "type": "firstName"}]})
        assert result == {"generated_data": "test"}


class TestTemplatesClient:
    """Test cases for the TemplatesClient class."""

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_get_templates(self, mock_make_request, api_key):
        """Test getting all templates."""
        mock_response = Mock()
        mock_response.json.return_value = [{"id": "1", "name": "Template 1"}]
        mock_make_request.return_value = mock_response
        
        client = TemplatesClient(api_key=api_key)
        result = client.get_templates()
        
        mock_make_request.assert_called_once_with("GET", "/templates")
        assert result == [{"id": "1", "name": "Template 1"}]

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_create_template(self, mock_make_request, api_key):
        """Test creating a template."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "1", "name": "New Template"}
        mock_make_request.return_value = mock_response
        
        client = TemplatesClient(api_key=api_key)
        template_data = {"name": "New Template", "fields": []}
        project_id = "test-project-id"
        team_id = "test-team-id"
        result = client.create_template(template_data, project_id, team_id)
        
        # Check that required fields were added
        expected_data = template_data.copy()
        expected_data["projectId"] = project_id
        expected_data["teamId"] = team_id
        mock_make_request.assert_called_once_with("POST", "/templates", json=expected_data)
        assert result == {"id": "1", "name": "New Template"}

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_get_template(self, mock_make_request, api_key):
        """Test getting a specific template."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "1", "name": "Template 1"}
        mock_make_request.return_value = mock_response
        
        client = TemplatesClient(api_key=api_key)
        result = client.get_template("1")
        
        mock_make_request.assert_called_once_with("GET", "/templates/1")
        assert result == {"id": "1", "name": "Template 1"}

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_get_template_by_id_fallback(self, mock_make_request, api_key):
        """Test get_template_by_id fallback behavior."""
        # First call fails (direct API call)
        mock_response_fail = Mock()
        mock_response_fail.status_code = 404
        mock_response_fail.text = "Not Found"
        
        # Second call succeeds (get all templates)
        mock_response_success = Mock()
        mock_response_success.json.return_value = [{"id": "1", "name": "Template 1"}]
        
        mock_make_request.side_effect = [DataMakerError("Not found"), mock_response_success]
        
        client = TemplatesClient(api_key=api_key)
        result = client.get_template_by_id("1")
        
        assert mock_make_request.call_count == 2
        assert result == {"id": "1", "name": "Template 1"}

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_get_template_by_id_not_found(self, mock_make_request, api_key):
        """Test get_template_by_id when template not found."""
        # First call fails (direct API call)
        mock_response_fail = Mock()
        mock_response_fail.status_code = 404
        mock_response_fail.text = "Not Found"
        
        # Second call succeeds but template not found
        mock_response_success = Mock()
        mock_response_success.json.return_value = [{"id": "2", "name": "Template 2"}]
        
        mock_make_request.side_effect = [DataMakerError("Not found"), mock_response_success]
        
        client = TemplatesClient(api_key=api_key)
        
        with pytest.raises(DataMakerError, match="You must provide ID of a template from your account"):
            client.get_template_by_id("1")


class TestApiKeysClient:
    """Test cases for the ApiKeysClient class."""

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_get_api_keys(self, mock_make_request, api_key):
        """Test getting all API keys."""
        mock_response = Mock()
        mock_response.json.return_value = [{"id": "1", "name": "Key 1"}]
        mock_make_request.return_value = mock_response
        
        client = ApiKeysClient(api_key=api_key)
        result = client.get_api_keys()
        
        mock_make_request.assert_called_once_with("GET", "/apiKeys")
        assert result == [{"id": "1", "name": "Key 1"}]

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_create_api_key(self, mock_make_request, api_key):
        """Test creating an API key."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "1", "key": "test-key"}
        mock_make_request.return_value = mock_response
        
        client = ApiKeysClient(api_key=api_key)
        result = client.create_api_key("test-key", "user", "Test Key", "team-1")
        
        expected_data = {"key": "test-key", "scope": "user", "name": "Test Key", "teamId": "team-1"}
        mock_make_request.assert_called_once_with("POST", "/apiKeys", json=expected_data)
        assert result == {"id": "1", "key": "test-key"}

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_update_api_key(self, mock_make_request, api_key):
        """Test updating an API key."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "1", "key": "updated-key"}
        mock_make_request.return_value = mock_response
        
        client = ApiKeysClient(api_key=api_key)
        result = client.update_api_key("1", "updated-key", "Updated Key")
        
        expected_data = {"key": "updated-key", "name": "Updated Key"}
        mock_make_request.assert_called_once_with("PUT", "/apiKeys/1", json=expected_data)
        assert result == {"id": "1", "key": "updated-key"}

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_delete_api_key(self, mock_make_request, api_key):
        """Test deleting an API key."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True}
        mock_make_request.return_value = mock_response
        
        client = ApiKeysClient(api_key=api_key)
        result = client.delete_api_key("1")
        
        mock_make_request.assert_called_once_with("DELETE", "/apiKeys/1")
        assert result == {"success": True}


class TestConnectionsClient:
    """Test cases for the ConnectionsClient class."""

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_get_connections(self, mock_make_request, api_key):
        """Test getting all connections."""
        mock_response = Mock()
        mock_response.json.return_value = [{"id": "1", "name": "Connection 1"}]
        mock_make_request.return_value = mock_response
        
        client = ConnectionsClient(api_key=api_key)
        result = client.get_connections()
        
        mock_make_request.assert_called_once_with("GET", "/connections")
        assert result == [{"id": "1", "name": "Connection 1"}]

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_create_connection(self, mock_make_request, api_key, sample_connection):
        """Test creating a connection."""
        mock_response = Mock()
        mock_response.json.return_value = sample_connection
        mock_make_request.return_value = mock_response
        
        client = ConnectionsClient(api_key=api_key)
        result = client.create_connection(
            name=sample_connection["name"],
            connection_type=sample_connection["type"],
            connection_string=sample_connection["connectionString"],
            created_by=sample_connection["createdBy"],
            project_id=sample_connection["projectId"],
            team_id=sample_connection["teamId"]
        )
        
        expected_data = {
            "name": sample_connection["name"],
            "type": sample_connection["type"],
            "connectionString": sample_connection["connectionString"],
            "createdBy": sample_connection["createdBy"],
            "projectId": sample_connection["projectId"],
            "teamId": sample_connection["teamId"]
        }
        mock_make_request.assert_called_once_with("POST", "/connections", json=expected_data)
        assert result == sample_connection

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_create_connection_with_optional_params(self, mock_make_request, api_key):
        """Test creating a connection with optional parameters."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "1", "name": "Test Connection"}
        mock_make_request.return_value = mock_response
        
        client = ConnectionsClient(api_key=api_key)
        result = client.create_connection(
            name="Test Connection",
            connection_type="postgresql",
            connection_string="postgresql://localhost:5432/test",
            created_by="user-1",
            project_id="project-1",
            team_id="team-1",
            read_only=True,
            endpoint_folder_id="folder-1"
        )
        
        expected_data = {
            "name": "Test Connection",
            "type": "postgresql",
            "connectionString": "postgresql://localhost:5432/test",
            "createdBy": "user-1",
            "projectId": "project-1",
            "teamId": "team-1",
            "readOnly": True,
            "endpointFolderId": "folder-1"
        }
        mock_make_request.assert_called_once_with("POST", "/connections", json=expected_data)
        assert result == {"id": "1", "name": "Test Connection"}

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_test_connection(self, mock_make_request, api_key, sample_connection):
        """Test testing a connection."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True}
        mock_make_request.return_value = mock_response
        
        client = ConnectionsClient(api_key=api_key)
        result = client.test_connection(sample_connection)
        
        mock_make_request.assert_called_once_with("POST", "/connections/test", json=sample_connection)
        assert result == {"success": True}

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_get_tables(self, mock_make_request, api_key):
        """Test getting all tables."""
        mock_response = Mock()
        mock_response.json.return_value = [{"name": "users", "schema": "public"}]
        mock_make_request.return_value = mock_response
        
        client = ConnectionsClient(api_key=api_key)
        result = client.get_tables()
        
        mock_make_request.assert_called_once_with("GET", "/connections/tables")
        assert result == [{"name": "users", "schema": "public"}]


class TestProjectsClient:
    """Test cases for the ProjectsClient class."""

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_get_projects(self, mock_make_request, api_key):
        """Test getting all projects."""
        mock_response = Mock()
        mock_response.json.return_value = [{"id": "1", "name": "Project 1"}]
        mock_make_request.return_value = mock_response
        
        client = ProjectsClient(api_key=api_key)
        result = client.get_projects()
        
        mock_make_request.assert_called_once_with("GET", "/projects")
        assert result == [{"id": "1", "name": "Project 1"}]

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_create_project(self, mock_make_request, api_key, sample_project):
        """Test creating a project."""
        mock_response = Mock()
        mock_response.json.return_value = sample_project
        mock_make_request.return_value = mock_response
        
        client = ProjectsClient(api_key=api_key)
        team_id = "test-team-id"
        result = client.create_project(sample_project, team_id)
        
        # Check that teamId was added
        expected_data = sample_project.copy()
        expected_data["teamId"] = team_id
        mock_make_request.assert_called_once_with("POST", "/projects", json=expected_data)
        assert result == sample_project


class TestUsersClient:
    """Test cases for the UsersClient class."""

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_get_users(self, mock_make_request, api_key):
        """Test getting all users."""
        mock_response = Mock()
        mock_response.json.return_value = [{"id": "1", "email": "user@example.com"}]
        mock_make_request.return_value = mock_response
        
        client = UsersClient(api_key=api_key)
        result = client.get_users()
        
        mock_make_request.assert_called_once_with("GET", "/users")
        assert result == [{"id": "1", "email": "user@example.com"}]

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_get_current_user(self, mock_make_request, api_key, sample_user):
        """Test getting current user."""
        mock_response = Mock()
        mock_response.json.return_value = sample_user
        mock_make_request.return_value = mock_response
        
        client = UsersClient(api_key=api_key)
        result = client.get_current_user()
        
        mock_make_request.assert_called_once_with("GET", "/users/me")
        assert result == sample_user


class TestTeamsClient:
    """Test cases for the TeamsClient class."""

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_get_teams(self, mock_make_request, api_key):
        """Test getting all teams."""
        mock_response = Mock()
        mock_response.json.return_value = [{"id": "1", "name": "Team 1"}]
        mock_make_request.return_value = mock_response
        
        client = TeamsClient(api_key=api_key)
        result = client.get_teams()
        
        mock_make_request.assert_called_once_with("GET", "/teams")
        assert result == [{"id": "1", "name": "Team 1"}]

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_setup_team(self, mock_make_request, api_key, sample_team):
        """Test setting up a team."""
        mock_response = Mock()
        mock_response.json.return_value = sample_team
        mock_make_request.return_value = mock_response
        
        client = TeamsClient(api_key=api_key)
        result = client.setup_team(sample_team)
        
        mock_make_request.assert_called_once_with("POST", "/setup/teams", json=sample_team)
        assert result == sample_team


class TestTeamMembersClient:
    """Test cases for the TeamMembersClient class."""

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_get_team_members(self, mock_make_request, api_key):
        """Test getting all team members."""
        mock_response = Mock()
        mock_response.json.return_value = [{"id": "1", "userId": "user-1"}]
        mock_make_request.return_value = mock_response
        
        client = TeamMembersClient(api_key=api_key)
        result = client.get_team_members()
        
        mock_make_request.assert_called_once_with("GET", "/teamMembers")
        assert result == [{"id": "1", "userId": "user-1"}]

    @patch('src.datamaker.routes.base.BaseClient._make_request')
    def test_invite_team_member(self, mock_make_request, api_key):
        """Test inviting a team member."""
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "inviteId": "invite-1"}
        mock_make_request.return_value = mock_response
        
        client = TeamMembersClient(api_key=api_key)
        invite_data = {"email": "newuser@example.com", "teamId": "team-1"}
        result = client.invite_team_member(invite_data)
        
        mock_make_request.assert_called_once_with("POST", "/teamMembers/invite", json=invite_data)
        assert result == {"success": True, "inviteId": "invite-1"}
