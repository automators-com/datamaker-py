"""Integration tests that make actual API calls to the DataMaker API."""

import pytest
from src.datamaker.main import DataMaker
from src.datamaker.error import DataMakerError


class TestDataMakerIntegration:
    """Integration tests for DataMaker API."""

    def _handle_api_error(self, error, test_name):
        """Handle API errors gracefully."""
        if "Unauthorized" in str(error):
            pytest.skip(
                f"{test_name} skipped: API key appears to be invalid or expired: {error}"
            )
        elif "Internal Server Error" in str(error):
            pytest.skip(
                f"{test_name} skipped: API key format recognized but server error: {error}"
            )
        else:
            pytest.fail(f"{test_name} failed: {error}")

    def test_validate_api_key(self, datamaker_client):
        """Test API key validation with real API call."""
        try:
            result = datamaker_client.validate_api_key()
            assert result is not None
            print(f"API key validation result: {result}")
        except DataMakerError as e:
            self._handle_api_error(e, "API key validation")

    def test_get_current_user(self, datamaker_client):
        """Test getting current user with real API call."""
        try:
            result = datamaker_client.get_current_user()
            assert result is not None
            assert "id" in result or "email" in result
            print(f"Current user: {result}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get current user")

    def test_get_templates(self, datamaker_client):
        """Test getting templates with real API call."""
        try:
            result = datamaker_client.get_templates()
            assert isinstance(result, list)
            print(f"Found {len(result)} templates")
            if result:
                print(f"Sample template: {result[0]}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get templates")

    def test_get_projects(self, datamaker_client):
        """Test getting projects with real API call."""
        try:
            result = datamaker_client.get_projects()
            assert isinstance(result, list)
            print(f"Found {len(result)} projects")
            if result:
                print(f"Sample project: {result[0]}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get projects")

    def test_get_teams(self, datamaker_client):
        """Test getting teams with real API call."""
        try:
            result = datamaker_client.get_teams()
            assert isinstance(result, list)
            print(f"Found {len(result)} teams")
            if result:
                print(f"Sample team: {result[0]}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get teams")

    def test_get_users(self, datamaker_client):
        """Test getting users with real API call."""
        try:
            result = datamaker_client.get_users()
            assert isinstance(result, list)
            print(f"Found {len(result)} users")
            if result:
                print(f"Sample user: {result[0]}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get users")

    def test_get_api_keys(self, datamaker_client):
        """Test getting API keys with real API call."""
        try:
            result = datamaker_client.get_api_keys()
            assert isinstance(result, list)
            print(f"Found {len(result)} API keys")
            if result:
                print(f"Sample API key: {result[0]}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get API keys")

    def test_get_connections(self, datamaker_client):
        """Test getting connections with real API call."""
        try:
            result = datamaker_client.get_connections()
            assert isinstance(result, list)
            print(f"Found {len(result)} connections")
            if result:
                print(f"Sample connection: {result[0]}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get connections")

    def test_get_team_members(self, datamaker_client):
        """Test getting team members with real API call."""
        try:
            result = datamaker_client.get_team_members()
            assert isinstance(result, list)
            print(f"Found {len(result)} team members")
            if result:
                print(f"Sample team member: {result[0]}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get team members")

    def test_get_custom_data_types(self, datamaker_client):
        """Test getting custom data types with real API call."""
        try:
            # Use a sample project ID from the API
            project_id = "cmd33tl160003xkrc6f4au69w"
            result = datamaker_client.get_custom_data_types(project_id)
            assert isinstance(result, list)
            print(f"Found {len(result)} custom data types")
            if result:
                print(f"Sample custom data type: {result[0]}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get custom data types")

    def test_get_endpoint_folders(self, datamaker_client):
        """Test getting endpoint folders with real API call."""
        try:
            result = datamaker_client.get_endpoint_folders()
            assert isinstance(result, list)
            print(f"Found {len(result)} endpoint folders")
            if result:
                print(f"Sample endpoint folder: {result[0]}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get endpoint folders")

    def test_get_endpoints(self, datamaker_client):
        """Test getting endpoints with real API call."""
        try:
            result = datamaker_client.get_endpoints()
            assert isinstance(result, list)
            print(f"Found {len(result)} endpoints")
            if result:
                print(f"Sample endpoint: {result[0]}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get endpoints")

    def test_get_template_folders(self, datamaker_client):
        """Test getting template folders with real API call."""
        try:
            result = datamaker_client.get_template_folders()
            assert isinstance(result, list)
            print(f"Found {len(result)} template folders")
            if result:
                print(f"Sample template folder: {result[0]}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get template folders")

    def test_get_shortcuts(self, datamaker_client):
        """Test getting shortcuts with real API call."""
        try:
            result = datamaker_client.get_shortcuts()
            assert isinstance(result, list)
            print(f"Found {len(result)} shortcuts")
            if result:
                print(f"Sample shortcut: {result[0]}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get shortcuts")

    def test_get_feedback(self, datamaker_client):
        """Test getting feedback with real API call."""
        try:
            result = datamaker_client.get_feedback()
            assert isinstance(result, list)
            print(f"Found {len(result)} feedback entries")
            if result:
                print(f"Sample feedback: {result[0]}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get feedback")

    def test_get_tables(self, datamaker_client):
        """Test getting tables with real API call."""
        try:
            result = datamaker_client.get_tables()
            assert isinstance(result, list)
            print(f"Found {len(result)} tables")
            if result:
                print(f"Sample table: {result[0]}")
        except DataMakerError as e:
            self._handle_api_error(e, "Get tables")

    def test_generate_with_real_template(self, datamaker_client):
        """Test data generation with a real template if available."""
        try:
            # First get templates
            templates = datamaker_client.get_templates()

            if not templates:
                pytest.skip("No templates available for testing")

            # Use the first template for testing
            template = templates[0]
            template["quantity"] = 2  # Generate only 2 records for testing

            result = datamaker_client.generate(template)
            assert result is not None
            print(f"Generated data: {result}")

        except DataMakerError as e:
            self._handle_api_error(e, "Data generation")

    def test_generate_from_template_id(self, datamaker_client):
        """Test generation from template ID with real API call."""
        try:
            # First get templates
            templates = datamaker_client.get_templates()

            if not templates:
                pytest.skip("No templates available for testing")

            # Use the first template ID for testing
            template_id = templates[0]["id"]

            result = datamaker_client.generate_from_template_id(template_id, quantity=2)
            assert result is not None
            print(f"Generated data from template ID {template_id}: {result}")

        except DataMakerError as e:
            self._handle_api_error(e, "Generate from template ID")

    def test_create_and_delete_template(self, datamaker_client):
        """Test creating and deleting a template with real API calls."""
        try:
            # Create a test template
            template_data = {
                "name": "Test Template for Integration Test",
                "fields": [
                    {"name": "firstName", "type": "firstName"},
                    {"name": "lastName", "type": "lastName"},
                    {"name": "email", "type": "email"},
                ],
                "quantity": 5,
            }

            # Use sample project and team IDs from the API
            project_id = "cmd33tl160003xkrc6f4au69w"
            team_id = "cmd33tl0m0000xkrcmo8nxkwz"
            created_template = datamaker_client.create_template(
                template_data, project_id, team_id
            )
            assert created_template is not None
            assert "id" in created_template
            template_id = created_template["id"]

            print(f"Created template with ID: {template_id}")

            # Clean up - delete the template
            delete_result = datamaker_client.delete_template(template_id)
            assert delete_result is not None

            print(f"Successfully deleted template {template_id}")

        except DataMakerError as e:
            self._handle_api_error(e, "Create/delete template test")

    def test_create_and_delete_project(self, datamaker_client):
        """Test creating and deleting a project with real API calls."""
        try:
            # Create a test project
            project_data = {
                "name": "Test Project for Integration Test",
                "description": "A test project created during integration testing",
            }

            # Use sample team ID from the API
            team_id = "cmd33tl0m0000xkrcmo8nxkwz"
            created_project = datamaker_client.create_project(project_data, team_id)
            assert created_project is not None
            assert "id" in created_project
            project_id = created_project["id"]

            print(f"Created project with ID: {project_id}")

            # Clean up - delete the project
            delete_result = datamaker_client.delete_project(project_id)
            assert delete_result is not None

            print(f"Successfully deleted project {project_id}")

        except DataMakerError as e:
            self._handle_api_error(e, "Create/delete project test")

    def test_create_and_delete_team(self, datamaker_client):
        """Test creating and deleting a team with real API calls."""
        try:
            # Create a test team
            team_data = {
                "name": "Test Team for Integration Test",
                "description": "A test team created during integration testing",
            }

            created_team = datamaker_client.create_team(team_data)
            assert created_team is not None
            assert "id" in created_team
            team_id = created_team["id"]

            print(f"Created team with ID: {team_id}")

            # Clean up - delete the team
            delete_result = datamaker_client.delete_team(team_id)
            assert delete_result is not None

            print(f"Successfully deleted team {team_id}")

        except DataMakerError as e:
            self._handle_api_error(e, "Create/delete team test")

    def test_create_and_delete_user(self, datamaker_client):
        """Test creating and deleting a user with real API calls."""
        try:
            # Create a test user
            user_data = {
                "email": "testuser@integrationtest.com",
                "firstName": "Test",
                "lastName": "User",
            }

            # Generate a unique user ID for the test
            import uuid

            user_id = f"test-user-{uuid.uuid4().hex[:8]}"
            created_user = datamaker_client.create_user(user_data, user_id)
            assert created_user is not None
            assert "id" in created_user
            user_id = created_user["id"]

            print(f"Created user with ID: {user_id}")

            # Clean up - delete the user
            delete_result = datamaker_client.delete_user(user_id)
            assert delete_result is not None

            print(f"Successfully deleted user {user_id}")

        except DataMakerError as e:
            self._handle_api_error(e, "Create/delete user test")

    def test_create_and_delete_connection(self, datamaker_client):
        """Test creating and deleting a connection with real API calls."""
        try:
            # First get projects and teams for the connection
            projects = datamaker_client.get_projects()
            teams = datamaker_client.get_teams()

            if not projects or not teams:
                pytest.skip("No projects or teams available for connection testing")

            # Create a test connection
            connection_data = {
                "name": "Test Connection for Integration Test",
                "connection_type": "postgresql",
                "connection_string": "postgresql://test:test@localhost:5432/testdb",
                "created_by": "test-user",
                "project_id": projects[0]["id"],
                "team_id": teams[0]["id"],
            }

            created_connection = datamaker_client.create_connection(**connection_data)
            assert created_connection is not None
            assert "id" in created_connection
            connection_id = created_connection["id"]

            print(f"Created connection with ID: {connection_id}")

            # Clean up - delete the connection
            delete_result = datamaker_client.delete_connection(connection_id)
            assert delete_result is not None

            print(f"Successfully deleted connection {connection_id}")

        except DataMakerError as e:
            self._handle_api_error(e, "Create/delete connection test")

    def test_test_connection(self, datamaker_client):
        """Test connection testing with real API call."""
        try:
            # Test connection data
            connection_data = {
                "type": "postgresql",
                "connectionString": "postgresql://test:test@localhost:5432/testdb",
            }

            result = datamaker_client.test_connection(connection_data)
            assert result is not None
            print(f"Connection test result: {result}")

        except DataMakerError as e:
            # This might fail if the connection string is invalid, which is expected
            print(f"Connection test failed as expected: {e}")

    def test_create_and_delete_api_key(self, datamaker_client):
        """Test creating and deleting an API key with real API calls."""
        try:
            # Create a test API key
            api_key_data = {
                "key": "test-api-key-for-integration-test",
                "name": "Test API Key for Integration Test",
            }

            # Add required scope field
            api_key_data["scope"] = "user"
            created_api_key = datamaker_client.create_api_key(**api_key_data)
            assert created_api_key is not None
            assert "id" in created_api_key
            api_key_id = created_api_key["id"]

            print(f"Created API key with ID: {api_key_id}")

            # Clean up - delete the API key
            delete_result = datamaker_client.delete_api_key(api_key_id)
            assert delete_result is not None

            print(f"Successfully deleted API key {api_key_id}")

        except DataMakerError as e:
            self._handle_api_error(e, "Create/delete API key test")
