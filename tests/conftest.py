"""Test configuration and fixtures for datamaker-py tests."""

import pytest
import os
from unittest.mock import Mock, patch
from src.datamaker.main import DataMaker


@pytest.fixture
def api_key():
    """Test API key fixture."""
    return "dm-d10d3fc0a795a6ece3c1da53b638061725436cf863d75fd1fabc2786ab9bad18"


@pytest.fixture
def datamaker_client(api_key):
    """DataMaker client fixture with test API key."""
    return DataMaker(api_key=api_key)


@pytest.fixture
def mock_response():
    """Mock response fixture."""
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"success": True, "data": "test_data"}
    return mock_resp


@pytest.fixture
def mock_error_response():
    """Mock error response fixture."""
    mock_resp = Mock()
    mock_resp.status_code = 400
    mock_resp.text = "Bad Request"
    return mock_resp


@pytest.fixture
def sample_template():
    """Sample template fixture."""
    return {
        "id": "test-template-123",
        "name": "Test Template",
        "fields": [
            {"name": "firstName", "type": "firstName"},
            {"name": "lastName", "type": "lastName"},
            {"name": "email", "type": "email"},
        ],
        "quantity": 10,
    }


@pytest.fixture
def sample_project():
    """Sample project fixture."""
    return {
        "id": "test-project-123",
        "name": "Test Project",
        "description": "A test project",
    }


@pytest.fixture
def sample_user():
    """Sample user fixture."""
    return {
        "id": "test-user-123",
        "email": "test@example.com",
        "firstName": "Test",
        "lastName": "User",
    }


@pytest.fixture
def sample_team():
    """Sample team fixture."""
    return {"id": "test-team-123", "name": "Test Team", "description": "A test team"}


@pytest.fixture
def sample_connection():
    """Sample connection fixture."""
    return {
        "id": "test-connection-123",
        "name": "Test Connection",
        "type": "postgresql",
        "connectionString": "postgresql://user:pass@localhost:5432/testdb",
        "createdBy": "test-user-123",
        "projectId": "test-project-123",
        "teamId": "test-team-123",
    }
