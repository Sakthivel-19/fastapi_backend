import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestEndpoints:
    """Test all API endpoints"""
    
    def test_read_root(self):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}
    
    def test_read_test(self):
        """Test the /test endpoint"""
        response = client.get("/test")
        assert response.status_code == 200
        assert response.json() == {"Hello": "Test World"}
    
    def test_read_try(self):
        """Test the /try endpoint"""
        response = client.get("/try")
        assert response.status_code == 200
        assert response.json() == {"Hello": "Try World"}
    
    def test_read_work(self):
        """Test the /work endpoint"""
        response = client.get("/work")
        assert response.status_code == 200
        assert response.json() == {"Hello": "Work World"}
    
    def test_read_testing(self):
        """Test the /testing endpoint"""
        response = client.get("/testing")
        assert response.status_code == 200
        assert response.json() == {"Hello": "Testing World"}
    
    def test_read_ansible(self):
        """Test the /ansible endpoint"""
        response = client.get("/ansible")
        assert response.status_code == 200
        assert response.json() == {"Ansible": "Deployment using Ansible done successfully"}
    
    def test_nonexistent_endpoint(self):
        """Test that nonexistent endpoints return 404"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_metrics_endpoint(self):
        """Test that Prometheus metrics endpoint is available"""
        response = client.get("/metrics")
        assert response.status_code == 200
        # Metrics should contain prometheus format data
        assert "# HELP" in response.text or "# TYPE" in response.text


class TestResponseHeaders:
    """Test response headers and content types"""
    
    def test_content_type_json(self):
        """Test that endpoints return JSON content type"""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"
    
    def test_metrics_content_type(self):
        """Test that metrics endpoint returns plain text"""
        response = client.get("/metrics")
        assert "text/plain" in response.headers["content-type"]


class TestHTTPMethods:
    """Test HTTP method restrictions"""
    
    def test_post_not_allowed_on_get_endpoints(self):
        """Test that POST is not allowed on GET-only endpoints"""
        response = client.post("/")
        assert response.status_code == 405  # Method Not Allowed
    
    def test_put_not_allowed_on_get_endpoints(self):
        """Test that PUT is not allowed on GET-only endpoints"""
        response = client.put("/test")
        assert response.status_code == 405  # Method Not Allowed
    
    def test_delete_not_allowed_on_get_endpoints(self):
        """Test that DELETE is not allowed on GET-only endpoints"""
        response = client.delete("/work")
        assert response.status_code == 405  # Method Not Allowed


class TestResponseStructure:
    """Test response data structure and validation"""
    
    @pytest.mark.parametrize("endpoint,expected_key", [
        ("/", "Hello"),
        ("/test", "Hello"),
        ("/try", "Hello"),
        ("/work", "Hello"),
        ("/testing", "Hello"),
        ("/ansible", "Ansible"),
    ])
    def test_response_structure(self, endpoint, expected_key):
        """Test that responses have expected structure"""
        response = client.get(endpoint)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert expected_key in data
        assert isinstance(data[expected_key], str)
    
    def test_response_values_are_strings(self):
        """Test that all response values are strings"""
        endpoints = ["/", "/test", "/try", "/work", "/testing", "/ansible"]
        for endpoint in endpoints:
            response = client.get(endpoint)
            data = response.json()
            for value in data.values():
                assert isinstance(value, str), f"Value in {endpoint} is not a string: {value}"