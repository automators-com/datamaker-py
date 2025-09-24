import os
from dotenv import load_dotenv
from typing import Optional, Dict
from .routes.base import BaseClient
from .routes.generation import GenerationClient
from .routes.templates import TemplatesClient
from .routes.api_keys import ApiKeysClient
from .routes.connections import ConnectionsClient
from .routes.projects import ProjectsClient
from .routes.users import UsersClient
from .routes.teams import TeamsClient, TeamMembersClient
from .routes.custom_types import CustomDataTypesClient, EndpointFoldersClient, EndpointsClient
from .routes.folders_and_utils import TemplateFoldersClient, ShortcutsClient, FeedbackClient
from .routes.export_and_validation import ExportClient, ValidationClient

load_dotenv()


class DataMaker:
    """Main DataMaker client that provides access to all API functionality."""
    
    def __init__(
        self,
        api_key: str = None,
        default_headers: Dict[str, Optional[str]] = None,
        base_url: Optional[str] = "https://api.datamaker.automators.com",
    ):
        if default_headers is None:
            default_headers = {"Content-Type": "application/json"}
            
        # Initialize all route clients
        self._generation = GenerationClient(api_key, default_headers, base_url)
        self._templates = TemplatesClient(api_key, default_headers, base_url)
        self._api_keys = ApiKeysClient(api_key, default_headers, base_url)
        self._connections = ConnectionsClient(api_key, default_headers, base_url)
        self._projects = ProjectsClient(api_key, default_headers, base_url)
        self._users = UsersClient(api_key, default_headers, base_url)
        self._teams = TeamsClient(api_key, default_headers, base_url)
        self._team_members = TeamMembersClient(api_key, default_headers, base_url)
        self._custom_data_types = CustomDataTypesClient(api_key, default_headers, base_url)
        self._endpoint_folders = EndpointFoldersClient(api_key, default_headers, base_url)
        self._endpoints = EndpointsClient(api_key, default_headers, base_url)
        self._template_folders = TemplateFoldersClient(api_key, default_headers, base_url)
        self._shortcuts = ShortcutsClient(api_key, default_headers, base_url)
        self._feedback = FeedbackClient(api_key, default_headers, base_url)
        self._export = ExportClient(api_key, default_headers, base_url)
        self._validation = ValidationClient(api_key, default_headers, base_url)
        
        # Maintain backward compatibility
        self.api_key = self._generation.api_key
        self.headers = self._generation.headers
        self.base_url = self._generation.base_url

    # =================== GENERATION METHODS ===================
    def generate(self, template):
        """Generate data using a template."""
        return self._generation.generate(template)

    def generate_from_template_id(self, template_id: str, quantity: int = 10):
        """Generate data from a template ID with specified quantity."""
        # Get the template
        template = self._templates.get_template_by_id(template_id)
        
        # Set the quantity
        template["quantity"] = quantity
        
        # Generate data using the template
        return self.generate(template)

    # =================== TEMPLATE METHODS ===================
    def get_templates(self):
        """Fetch all templates from the API."""
        return self._templates.get_templates()
    
    def create_template(self, template_data: Dict, project_id: str, team_id: str):
        """Create a new template."""
        return self._templates.create_template(template_data, project_id, team_id)
    
    def get_template(self, template_id: str):
        """Get a specific template by ID."""
        return self._templates.get_template(template_id)
    
    def update_template(self, template_id: str, template_data: Dict):
        """Update a template."""
        return self._templates.update_template(template_id, template_data)
    
    def delete_template(self, template_id: str):
        """Delete a template."""
        return self._templates.delete_template(template_id)

    # =================== API KEY METHODS ===================
    def get_api_keys(self):
        """Get all API keys."""
        return self._api_keys.get_api_keys()
    
    def create_api_key(self, key: str, scope: str, name: Optional[str] = None, team_id: Optional[str] = None):
        """Create a new API key."""
        return self._api_keys.create_api_key(key, scope, name, team_id)
    
    def update_api_key(self, key_id: str, key: str, name: Optional[str] = None, team_id: Optional[str] = None):
        """Update an API key."""
        return self._api_keys.update_api_key(key_id, key, name, team_id)
    
    def delete_api_key(self, key_id: str):
        """Delete an API key."""
        return self._api_keys.delete_api_key(key_id)

    # =================== CONNECTION METHODS ===================
    def get_connections(self):
        """Get all connections."""
        return self._connections.get_connections()
    
    def create_connection(self, name: str, connection_type: str, connection_string: str, 
                         created_by: str, project_id: str, team_id: str, **kwargs):
        """Create a new database connection."""
        return self._connections.create_connection(name, connection_type, connection_string, 
                                                 created_by, project_id, team_id, **kwargs)
    
    def update_connection(self, connection_id: str, name: str, connection_type: str, 
                         connection_string: str, created_by: str, project_id: str, team_id: str, **kwargs):
        """Update a database connection."""
        return self._connections.update_connection(connection_id, name, connection_type, 
                                                 connection_string, created_by, project_id, team_id, **kwargs)
    
    def delete_connection(self, connection_id: str):
        """Delete a database connection."""
        return self._connections.delete_connection(connection_id)
    
    def test_connection(self, connection_data: Dict):
        """Test a database connection."""
        return self._connections.test_connection(connection_data)
    
    def get_tables(self):
        """Get all tables from connections."""
        return self._connections.get_tables()

    # =================== PROJECT METHODS ===================
    def get_projects(self):
        """Get all projects."""
        return self._projects.get_projects()
    
    def create_project(self, project_data: Dict, team_id: str):
        """Create a new project."""
        return self._projects.create_project(project_data, team_id)
    
    def get_project(self, project_id: str):
        """Get a specific project by ID."""
        return self._projects.get_project(project_id)
    
    def update_project(self, project_id: str, project_data: Dict):
        """Update a project."""
        return self._projects.update_project(project_id, project_data)
    
    def delete_project(self, project_id: str):
        """Delete a project."""
        return self._projects.delete_project(project_id)

    # =================== USER METHODS ===================
    def get_users(self):
        """Get all users."""
        return self._users.get_users()
    
    def create_user(self, user_data: Dict, user_id: str):
        """Create a new user."""
        return self._users.create_user(user_data, user_id)
    
    def get_current_user(self):
        """Get current user information."""
        return self._users.get_current_user()
    
    def provision_user(self, user_data: Dict):
        """Provision a new user."""
        return self._users.provision_user(user_data)
    
    def update_user(self, user_id: str, user_data: Dict):
        """Update a user."""
        return self._users.update_user(user_id, user_data)
    
    def patch_user(self, user_id: str, user_data: Dict):
        """Partially update a user."""
        return self._users.patch_user(user_id, user_data)
    
    def delete_user(self, user_id: str):
        """Delete a user."""
        return self._users.delete_user(user_id)

    # =================== TEAM METHODS ===================
    def get_teams(self):
        """Get all teams."""
        return self._teams.get_teams()
    
    def create_team(self, team_data: Dict):
        """Create a new team."""
        return self._teams.create_team(team_data)
    
    def update_team(self, team_id: str, team_data: Dict):
        """Update a team."""
        return self._teams.update_team(team_id, team_data)
    
    def delete_team(self, team_id: str):
        """Delete a team."""
        return self._teams.delete_team(team_id)
    
    def setup_team(self, team_data: Dict):
        """Setup a new team."""
        return self._teams.setup_team(team_data)

    # =================== TEAM MEMBER METHODS ===================
    def get_team_members(self):
        """Get all team members."""
        return self._team_members.get_team_members()
    
    def add_team_member(self, member_data: Dict):
        """Add a new team member."""
        return self._team_members.add_team_member(member_data)
    
    def invite_team_member(self, invite_data: Dict):
        """Invite a new team member."""
        return self._team_members.invite_team_member(invite_data)
    
    def update_team_member(self, member_id: str, member_data: Dict):
        """Update a team member."""
        return self._team_members.update_team_member(member_id, member_data)
    
    def remove_team_member(self, member_id: str):
        """Remove a team member."""
        return self._team_members.remove_team_member(member_id)

    # =================== CUSTOM DATA TYPE METHODS ===================
    def get_custom_data_types(self, project_id: str):
        """Get all custom data types for a specific project."""
        return self._custom_data_types.get_custom_data_types(project_id)
    
    def create_custom_data_type(self, data_type_data: Dict):
        """Create a new custom data type."""
        return self._custom_data_types.create_custom_data_type(data_type_data)
    
    def update_custom_data_type(self, data_type_id: str, data_type_data: Dict):
        """Update a custom data type."""
        return self._custom_data_types.update_custom_data_type(data_type_id, data_type_data)
    
    def delete_custom_data_type(self, data_type_id: str):
        """Delete a custom data type."""
        return self._custom_data_types.delete_custom_data_type(data_type_id)

    # =================== ENDPOINT FOLDER METHODS ===================
    def get_endpoint_folders(self):
        """Get all endpoint folders."""
        return self._endpoint_folders.get_endpoint_folders()
    
    def create_endpoint_folder(self, folder_data: Dict):
        """Create a new endpoint folder."""
        return self._endpoint_folders.create_endpoint_folder(folder_data)
    
    def update_endpoint_folder(self, folder_id: str, folder_data: Dict):
        """Update an endpoint folder."""
        return self._endpoint_folders.update_endpoint_folder(folder_id, folder_data)
    
    def delete_endpoint_folder(self, folder_id: str):
        """Delete an endpoint folder."""
        return self._endpoint_folders.delete_endpoint_folder(folder_id)

    # =================== ENDPOINT METHODS ===================
    def get_endpoints(self):
        """Get all endpoints."""
        return self._endpoints.get_endpoints()
    
    def create_endpoint(self, endpoint_data: Dict):
        """Create a new endpoint."""
        return self._endpoints.create_endpoint(endpoint_data)
    
    def get_endpoint(self, endpoint_id: str):
        """Get a specific endpoint by ID."""
        return self._endpoints.get_endpoint(endpoint_id)
    
    def update_endpoint(self, endpoint_id: str, endpoint_data: Dict):
        """Update an endpoint."""
        return self._endpoints.update_endpoint(endpoint_id, endpoint_data)
    
    def delete_endpoint(self, endpoint_id: str):
        """Delete an endpoint."""
        return self._endpoints.delete_endpoint(endpoint_id)

    # =================== TEMPLATE FOLDER METHODS ===================
    def get_template_folders(self):
        """Get all template folders."""
        return self._template_folders.get_template_folders()
    
    def create_template_folder(self, folder_data: Dict):
        """Create a new template folder."""
        return self._template_folders.create_template_folder(folder_data)
    
    def update_template_folder(self, folder_id: str, folder_data: Dict):
        """Update a template folder."""
        return self._template_folders.update_template_folder(folder_id, folder_data)
    
    def delete_template_folder(self, folder_id: str):
        """Delete a template folder."""
        return self._template_folders.delete_template_folder(folder_id)

    # =================== SHORTCUT METHODS ===================
    def get_shortcuts(self):
        """Get all shortcuts."""
        return self._shortcuts.get_shortcuts()
    
    def create_shortcut(self, shortcut_data: Dict):
        """Create a new shortcut."""
        return self._shortcuts.create_shortcut(shortcut_data)
    
    def update_shortcut(self, shortcut_id: str, shortcut_data: Dict):
        """Update a shortcut."""
        return self._shortcuts.update_shortcut(shortcut_id, shortcut_data)
    
    def delete_shortcut(self, shortcut_id: str):
        """Delete a shortcut."""
        return self._shortcuts.delete_shortcut(shortcut_id)

    # =================== FEEDBACK METHODS ===================
    def get_feedback(self):
        """Get all feedback."""
        return self._feedback.get_feedback()
    
    def submit_feedback(self, feedback_data: Dict):
        """Submit new feedback."""
        return self._feedback.submit_feedback(feedback_data)
    
    def update_feedback(self, feedback_id: str, feedback_data: Dict):
        """Update feedback."""
        return self._feedback.update_feedback(feedback_id, feedback_data)
    
    def delete_feedback(self, feedback_id: str):
        """Delete feedback."""
        return self._feedback.delete_feedback(feedback_id)

    # =================== EXPORT METHODS ===================
    def export_to_rest(self, export_data: Dict):
        """Export data to REST API."""
        return self._export.export_to_rest(export_data)
    
    def export_to_database(self, export_data: Dict):
        """Export data to database."""
        return self._export.export_to_database(export_data)

    # =================== VALIDATION METHODS ===================
    def validate_api_key(self):
        """Test API key authentication."""
        return self._validation.validate_api_key()

    # =================== PROPERTY ACCESS TO CLIENTS ===================
    # For advanced users who want direct access to specific clients
    @property
    def generation(self):
        """Access to generation client."""
        return self._generation
    
    @property
    def templates(self):
        """Access to templates client."""
        return self._templates
    
    @property
    def api_keys(self):
        """Access to API keys client."""
        return self._api_keys
    
    @property
    def connections(self):
        """Access to connections client."""
        return self._connections
    
    @property
    def projects(self):
        """Access to projects client."""
        return self._projects
    
    @property
    def users(self):
        """Access to users client."""
        return self._users
    
    @property
    def teams(self):
        """Access to teams client."""
        return self._teams
    
    @property
    def team_members(self):
        """Access to team members client."""
        return self._team_members
    
    @property
    def custom_data_types(self):
        """Access to custom data types client."""
        return self._custom_data_types
    
    @property
    def endpoint_folders(self):
        """Access to endpoint folders client."""
        return self._endpoint_folders
    
    @property
    def endpoints(self):
        """Access to endpoints client."""
        return self._endpoints
    
    @property
    def template_folders(self):
        """Access to template folders client."""
        return self._template_folders
    
    @property
    def shortcuts(self):
        """Access to shortcuts client."""
        return self._shortcuts
    
    @property
    def feedback(self):
        """Access to feedback client."""
        return self._feedback
    
    @property
    def export(self):
        """Access to export client."""
        return self._export
    
    @property
    def validation(self):
        """Access to validation client."""
        return self._validation
