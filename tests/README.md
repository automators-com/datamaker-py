# DataMaker Python Client Tests

This directory contains all test-related files for the DataMaker Python client.

## Directory Structure

```
tests/
├── README.md                 # This file
├── __init__.py              # Test package initialization
├── test_main.py             # Unit tests for main DataMaker class
├── test_routes.py           # Unit tests for route client classes
├── test_integration.py      # Integration tests with real API calls
├── config/                  # Test configuration files
│   └── pytest.ini          # Pytest configuration
├── docs/                    # Test documentation
│   ├── API_KEY_ERROR_LOGS.md
│   ├── AUTHENTICATION_ANALYSIS.md
│   ├── TEST_REPORT.md
│   └── TEST_RESULTS_AFTER_AUTH_FIX.md
├── conftest.py             # Pytest fixtures and configuration
└── scripts/                 # Test utility scripts
    ├── run_tests.py         # Test runner script
    └── demo.py              # Demo script showing client usage
```

## Running Tests

### From Project Root
```bash
# Run all tests
python -m pytest

# Run only unit tests
python -m pytest tests/test_main.py tests/test_routes.py

# Run only integration tests
python -m pytest tests/test_integration.py

# Run with coverage
python -m pytest --cov=src/datamaker --cov-report=term-missing
```

### Using Test Scripts
```bash
# Run the test runner script
python tests/scripts/run_tests.py

# Run the demo script
python tests/scripts/demo.py
```

## Test Types

### Unit Tests (`test_main.py`, `test_routes.py`)
- Test individual methods and classes in isolation
- Use mocked API calls for fast, reliable testing
- Verify client logic, request formatting, and error handling

### Integration Tests (`test_integration.py`)
- Test complete system with real API calls
- Validate API contracts and response formats
- Require valid API key and running server

## Configuration

- **pytest.ini**: Main pytest configuration (in project root)
- **tests/config/pytest.ini**: Additional pytest configuration
- **tests/fixtures/conftest.py**: Shared fixtures and test data

## Documentation

- **tests/docs/**: Contains test-related documentation and analysis
- **API_KEY_ERROR_LOGS.md**: Logs of API key authentication issues
- **AUTHENTICATION_ANALYSIS.md**: Analysis of authentication methods
- **TEST_REPORT.md**: Test execution reports
- **TEST_RESULTS_AFTER_AUTH_FIX.md**: Results after authentication fixes

## Fixtures

The `tests/fixtures/conftest.py` file contains shared pytest fixtures:
- `api_key`: Test API key
- `datamaker_client`: DataMaker client instance
- `sample_template`: Sample template data
- `sample_project`: Sample project data
- `sample_user`: Sample user data
- `sample_team`: Sample team data
- `sample_api_key`: Sample API key data
- `sample_connection`: Sample connection data
- Mock data fixtures for various API responses
