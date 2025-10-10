"""Tests for the main DataMaker class."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.datamaker.main import DataMaker
from src.datamaker.error import DataMakerError


class TestDataMaker:
    """Test cases for the DataMaker main class."""

    def test_init_with_api_key(self, api_key):
        """Test DataMaker initialization with API key."""
        client = DataMaker(api_key=api_key)
        assert client.api_key == api_key
        assert client.base_url == "https://api.datamaker.automators.com"
        assert "Content-Type" in client.headers
        assert client.headers["X-API-Key"] == api_key

    def test_init_with_custom_base_url(self, api_key):
        """Test DataMaker initialization with custom base URL."""
        custom_url = "https://custom.api.com"
        client = DataMaker(api_key=api_key, base_url=custom_url)
        assert client.base_url == custom_url

    def test_init_with_custom_headers(self, api_key):
        """Test DataMaker initialization with custom headers."""
        custom_headers = {"Custom-Header": "test-value"}
        client = DataMaker(api_key=api_key, default_headers=custom_headers)
        assert "Custom-Header" in client.headers
        assert client.headers["Custom-Header"] == "test-value"

    @patch("src.datamaker.routes.generation.GenerationClient.generate")
    def test_generate(self, mock_generate, datamaker_client, sample_template):
        """Test data generation."""
        mock_generate.return_value = {"generated_data": "test"}

        result = datamaker_client.generate(sample_template)

        mock_generate.assert_called_once_with(sample_template)
        assert result == {"generated_data": "test"}

    @patch("src.datamaker.routes.templates.TemplatesClient.get_template")
    @patch("src.datamaker.routes.generation.GenerationClient.generate")
    def test_generate_from_template_id(
        self, mock_generate, mock_get_template, datamaker_client, sample_template
    ):
        """Test generation from template ID."""
        template_id = "test-template-123"
        quantity = 5

        mock_get_template.return_value = sample_template
        mock_generate.return_value = {"generated_data": "test"}

        result = datamaker_client.generate_from_template_id(template_id, quantity)

        mock_get_template.assert_called_once_with(template_id)
        mock_generate.assert_called_once()
        assert mock_generate.call_args[0][0]["quantity"] == quantity
        assert result == {"generated_data": "test"}

    # Template methods tests
    @patch("src.datamaker.routes.templates.TemplatesClient.get_templates")
    def test_get_templates(self, mock_get_templates, datamaker_client):
        """Test getting all templates."""
        mock_templates = [{"id": "1", "name": "Template 1"}]
        mock_get_templates.return_value = mock_templates

        result = datamaker_client.get_templates()

        mock_get_templates.assert_called_once()
        assert result == mock_templates

    @patch("src.datamaker.routes.templates.TemplatesClient.create_template")
    def test_create_template(
        self, mock_create_template, datamaker_client, sample_template
    ):
        """Test creating a template."""
        mock_create_template.return_value = sample_template

        project_id = "test-project-id"
        team_id = "test-team-id"
        result = datamaker_client.create_template(sample_template, project_id, team_id)

        mock_create_template.assert_called_once_with(
            sample_template, project_id, team_id
        )
        assert result == sample_template

    @patch("src.datamaker.routes.templates.TemplatesClient.get_template")
    def test_get_template(self, mock_get_template, datamaker_client, sample_template):
        """Test getting a specific template."""
        template_id = "test-template-123"
        mock_get_template.return_value = sample_template

        result = datamaker_client.get_template(template_id)

        mock_get_template.assert_called_once_with(template_id)
        assert result == sample_template

    @patch("src.datamaker.routes.templates.TemplatesClient.update_template")
    def test_update_template(
        self, mock_update_template, datamaker_client, sample_template
    ):
        """Test updating a template."""
        template_id = "test-template-123"
        mock_update_template.return_value = sample_template

        result = datamaker_client.update_template(template_id, sample_template)

        mock_update_template.assert_called_once_with(template_id, sample_template)
        assert result == sample_template

    @patch("src.datamaker.routes.templates.TemplatesClient.delete_template")
    def test_delete_template(self, mock_delete_template, datamaker_client):
        """Test deleting a template."""
        template_id = "test-template-123"
        mock_delete_template.return_value = {"success": True}

        result = datamaker_client.delete_template(template_id)

        mock_delete_template.assert_called_once_with(template_id)
        assert result == {"success": True}

    # API Key methods tests
    @patch("src.datamaker.routes.api_keys.ApiKeysClient.get_api_keys")
    def test_get_api_keys(self, mock_get_api_keys, datamaker_client):
        """Test getting all API keys."""
        mock_keys = [{"id": "1", "name": "Key 1"}]
        mock_get_api_keys.return_value = mock_keys

        result = datamaker_client.get_api_keys()

        mock_get_api_keys.assert_called_once()
        assert result == mock_keys

    @patch("src.datamaker.routes.api_keys.ApiKeysClient.create_api_key")
    def test_create_api_key(self, mock_create_api_key, datamaker_client):
        """Test creating an API key."""
        key_data = {"key": "test-key", "name": "Test Key"}
        mock_create_api_key.return_value = key_data

        result = datamaker_client.create_api_key("test-key", "user", "Test Key")

        mock_create_api_key.assert_called_once_with(
            "test-key", "user", "Test Key", None
        )
        assert result == key_data

    # Connection methods tests
    @patch("src.datamaker.routes.connections.ConnectionsClient.get_connections")
    def test_get_connections(self, mock_get_connections, datamaker_client):
        """Test getting all connections."""
        mock_connections = [{"id": "1", "name": "Connection 1"}]
        mock_get_connections.return_value = mock_connections

        result = datamaker_client.get_connections()

        mock_get_connections.assert_called_once()
        assert result == mock_connections

    @patch("src.datamaker.routes.connections.ConnectionsClient.create_connection")
    def test_create_connection(
        self, mock_create_connection, datamaker_client, sample_connection
    ):
        """Test creating a connection."""
        mock_create_connection.return_value = sample_connection

        result = datamaker_client.create_connection(
            name=sample_connection["name"],
            connection_type=sample_connection["type"],
            connection_string=sample_connection["connectionString"],
            created_by=sample_connection["createdBy"],
            project_id=sample_connection["projectId"],
            team_id=sample_connection["teamId"],
        )

        mock_create_connection.assert_called_once()
        assert result == sample_connection

    @patch("src.datamaker.routes.connections.ConnectionsClient.test_connection")
    def test_test_connection(
        self, mock_test_connection, datamaker_client, sample_connection
    ):
        """Test testing a connection."""
        mock_test_connection.return_value = {"success": True}

        result = datamaker_client.test_connection(sample_connection)

        mock_test_connection.assert_called_once_with(sample_connection)
        assert result == {"success": True}

    # Project methods tests
    @patch("src.datamaker.routes.projects.ProjectsClient.get_projects")
    def test_get_projects(self, mock_get_projects, datamaker_client):
        """Test getting all projects."""
        mock_projects = [{"id": "1", "name": "Project 1"}]
        mock_get_projects.return_value = mock_projects

        result = datamaker_client.get_projects()

        mock_get_projects.assert_called_once()
        assert result == mock_projects

    @patch("src.datamaker.routes.projects.ProjectsClient.create_project")
    def test_create_project(
        self, mock_create_project, datamaker_client, sample_project
    ):
        """Test creating a project."""
        mock_create_project.return_value = sample_project

        team_id = "test-team-id"
        result = datamaker_client.create_project(sample_project, team_id)

        mock_create_project.assert_called_once_with(sample_project, team_id)
        assert result == sample_project

    # User methods tests
    @patch("src.datamaker.routes.users.UsersClient.get_users")
    def test_get_users(self, mock_get_users, datamaker_client):
        """Test getting all users."""
        mock_users = [{"id": "1", "email": "user@example.com"}]
        mock_get_users.return_value = mock_users

        result = datamaker_client.get_users()

        mock_get_users.assert_called_once()
        assert result == mock_users

    @patch("src.datamaker.routes.users.UsersClient.get_current_user")
    def test_get_current_user(
        self, mock_get_current_user, datamaker_client, sample_user
    ):
        """Test getting current user."""
        mock_get_current_user.return_value = sample_user

        result = datamaker_client.get_current_user()

        mock_get_current_user.assert_called_once()
        assert result == sample_user

    # Team methods tests
    @patch("src.datamaker.routes.teams.TeamsClient.get_teams")
    def test_get_teams(self, mock_get_teams, datamaker_client):
        """Test getting all teams."""
        mock_teams = [{"id": "1", "name": "Team 1"}]
        mock_get_teams.return_value = mock_teams

        result = datamaker_client.get_teams()

        mock_get_teams.assert_called_once()
        assert result == mock_teams

    @patch("src.datamaker.routes.teams.TeamsClient.create_team")
    def test_create_team(self, mock_create_team, datamaker_client, sample_team):
        """Test creating a team."""
        mock_create_team.return_value = sample_team

        result = datamaker_client.create_team(sample_team)

        mock_create_team.assert_called_once_with(sample_team)
        assert result == sample_team

    # Validation methods tests
    @patch(
        "src.datamaker.routes.export_and_validation.ValidationClient.validate_api_key"
    )
    def test_validate_api_key(self, mock_validate_api_key, datamaker_client):
        """Test API key validation."""
        mock_validate_api_key.return_value = {"valid": True}

        result = datamaker_client.validate_api_key()

        mock_validate_api_key.assert_called_once()
        assert result == {"valid": True}

    # Property access tests
    def test_client_properties(self, datamaker_client):
        """Test that client properties return the correct clients."""
        assert datamaker_client.generation is not None
        assert datamaker_client.templates is not None
        assert datamaker_client.api_keys is not None
        assert datamaker_client.connections is not None
        assert datamaker_client.projects is not None
        assert datamaker_client.users is not None
        assert datamaker_client.teams is not None
        assert datamaker_client.team_members is not None
        assert datamaker_client.custom_data_types is not None
        assert datamaker_client.endpoint_folders is not None
        assert datamaker_client.endpoints is not None
        assert datamaker_client.template_folders is not None
        assert datamaker_client.shortcuts is not None
        assert datamaker_client.feedback is not None
        assert datamaker_client.export is not None
        assert datamaker_client.validation is not None
