# FastAPI Backend

A simple FastAPI backend application with Prometheus monitoring.

## Features

- 6 API endpoints with JSON responses
- Prometheus metrics integration
- Comprehensive test suite with 100% coverage
- Docker support

## API Endpoints

- `GET /` - Returns `{"Hello": "World"}`
- `GET /test` - Returns `{"Hello": "Test World"}`
- `GET /try` - Returns `{"Hello": "Try World"}`
- `GET /work` - Returns `{"Hello": "Work World"}`
- `GET /testing` - Returns `{"Hello": "Testing World"}`
- `GET /ansible` - Returns `{"Ansible": "Deployment using Ansible done successfully"}`
- `GET /metrics` - Prometheus metrics endpoint

## Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
uvicorn app.main:app --reload
```

### Run Tests
```bash
pytest tests/ -v
```

### Test Coverage
```bash
coverage run -m pytest tests/
coverage report --include="app/*"
```

## Testing

The project includes a comprehensive test suite located in the `tests/` directory with 100% code coverage. See `tests/README.md` for detailed information about the test structure and categories.