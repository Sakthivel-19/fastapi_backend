# Test Suite

This directory contains comprehensive tests for the FastAPI backend application.

## Test Structure

- `test_main.py` - Tests for all API endpoints and core functionality
- `test_app_config.py` - Tests for application configuration, error handling, and edge cases

## Test Categories

### Endpoint Tests (`test_main.py`)
- **TestEndpoints**: Tests all API endpoints for correct responses
- **TestResponseHeaders**: Tests response headers and content types
- **TestHTTPMethods**: Tests HTTP method restrictions
- **TestResponseStructure**: Tests response data structure and validation

### Configuration Tests (`test_app_config.py`)
- **TestAppConfiguration**: Tests FastAPI app setup and Prometheus integration
- **TestConcurrentRequests**: Tests handling of concurrent requests
- **TestErrorHandling**: Tests error handling and edge cases

## Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run specific test file:
```bash
pytest tests/test_main.py -v
```

### Run with coverage:
```bash
coverage run -m pytest tests/
coverage report --include="app/*"
coverage html  # Generate HTML coverage report
```

## Test Coverage

The test suite achieves 100% code coverage for the main application code, testing:

- All 6 API endpoints (`/`, `/test`, `/try`, `/work`, `/testing`, `/ansible`)
- Prometheus metrics integration
- HTTP method restrictions
- Response structure validation
- Error handling for invalid URLs
- Concurrent request handling
- OpenAPI schema generation
- Documentation endpoints

## Dependencies

The tests require the following packages (already included in requirements.txt):
- `pytest` - Test framework
- `pytest-asyncio` - Async test support
- `httpx` - HTTP client for testing (used by FastAPI TestClient)

## Test Configuration

- `pytest.ini` - Pytest configuration
- `.coveragerc` - Coverage configuration