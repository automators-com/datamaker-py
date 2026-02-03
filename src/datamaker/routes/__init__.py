"""Routes package for datamaker API endpoints."""

from .base import BaseClient
from .generation import GenerationClient
from .templates import TemplatesClient
from .api_keys import ApiKeysClient
from .connections import ConnectionsClient
from .projects import ProjectsClient
from .users import UsersClient
from .teams import TeamsClient, TeamMembersClient
from .custom_types import CustomDataTypesClient, EndpointFoldersClient, EndpointsClient
from .folders_and_utils import TemplateFoldersClient, ShortcutsClient, FeedbackClient
from .export_and_validation import ExportClient, ValidationClient
from .scenario_files import ScenarioFilesClient

__all__ = [
    "BaseClient",
    "GenerationClient",
    "TemplatesClient",
    "ApiKeysClient",
    "ConnectionsClient",
    "ProjectsClient",
    "UsersClient",
    "TeamsClient",
    "TeamMembersClient",
    "CustomDataTypesClient",
    "EndpointFoldersClient",
    "EndpointsClient",
    "TemplateFoldersClient",
    "ShortcutsClient",
    "FeedbackClient",
    "ExportClient",
    "ValidationClient",
    "ScenarioFilesClient",
]
