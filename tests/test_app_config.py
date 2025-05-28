import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestAppConfiguration:
    """Test FastAPI application configuration"""
    
    def test_app_instance(self):
        """Test that app is a FastAPI instance"""
        from fastapi import FastAPI
        assert isinstance(app, FastAPI)
    
    def test_prometheus_instrumentation(self):
        """Test that Prometheus instrumentation is properly configured"""
        client = TestClient(app)
        
        # Make a request to generate metrics
        response = client.get("/")
        assert response.status_code == 200
        
        # Check that metrics endpoint exists and returns data
        metrics_response = client.get("/metrics")
        assert metrics_response.status_code == 200
        
        # Verify metrics contain FastAPI-specific metrics
        metrics_text = metrics_response.text
        assert "http_requests_total" in metrics_text or "http_request_duration_seconds" in metrics_text
    
    def test_app_routes_registered(self):
        """Test that all expected routes are registered"""
        expected_paths = ["/", "/test", "/try", "/work", "/testing", "/ansible"]
        
        # Get all routes from the app
        routes = [route.path for route in app.routes if hasattr(route, 'path')]
        
        for path in expected_paths:
            assert path in routes, f"Route {path} not found in registered routes"
    
    def test_openapi_schema_generation(self):
        """Test that OpenAPI schema is generated correctly"""
        client = TestClient(app)
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
        
        # Check that our endpoints are in the schema
        paths = schema["paths"]
        assert "/" in paths
        assert "/test" in paths
        assert "/ansible" in paths
    
    def test_docs_endpoints(self):
        """Test that documentation endpoints are available"""
        client = TestClient(app)
        
        # Test Swagger UI
        docs_response = client.get("/docs")
        assert docs_response.status_code == 200
        assert "text/html" in docs_response.headers["content-type"]
        
        # Test ReDoc
        redoc_response = client.get("/redoc")
        assert redoc_response.status_code == 200
        assert "text/html" in redoc_response.headers["content-type"]


class TestConcurrentRequests:
    """Test handling of concurrent requests"""
    
    def test_multiple_simultaneous_requests(self):
        """Test that the app can handle multiple simultaneous requests"""
        import threading
        import time
        
        client = TestClient(app)
        results = []
        
        def make_request(endpoint):
            response = client.get(endpoint)
            results.append((endpoint, response.status_code, response.json()))
        
        # Create threads for concurrent requests
        threads = []
        endpoints = ["/", "/test", "/try", "/work", "/testing", "/ansible"]
        
        for endpoint in endpoints:
            thread = threading.Thread(target=make_request, args=(endpoint,))
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all requests succeeded
        assert len(results) == len(endpoints)
        for endpoint, status_code, response_data in results:
            assert status_code == 200
            assert isinstance(response_data, dict)


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_http_methods(self):
        """Test various invalid HTTP methods"""
        client = TestClient(app)
        
        invalid_methods = ["PATCH", "OPTIONS"]
        endpoints = ["/", "/test", "/work"]
        
        for endpoint in endpoints:
            for method in invalid_methods:
                response = client.request(method, endpoint)
                # OPTIONS should be allowed (CORS), PATCH should not
                if method == "OPTIONS":
                    assert response.status_code in [200, 405]  # Depends on CORS configuration
                else:
                    assert response.status_code == 405
    
    def test_malformed_urls(self):
        """Test handling of malformed URLs"""
        client = TestClient(app)
        
        # URLs that should return 404
        invalid_urls = [
            "/test/extra/path",  # Extra path segments
            "/TEST",  # Wrong case (FastAPI is case-sensitive)
            "/nonexistent",  # Completely invalid path
            "/test/subpath",  # Subpath that doesn't exist
        ]
        
        for url in invalid_urls:
            response = client.get(url)
            assert response.status_code == 404, f"Expected 404 for {url}, got {response.status_code}"
        
        # URLs that FastAPI normalizes and should work
        normalized_urls = [
            ("/test//", "/test"),  # Double slash gets normalized
            ("//test", "/"),  # Leading double slash gets normalized to root
        ]
        
        for malformed_url, expected_endpoint in normalized_urls:
            response = client.get(malformed_url)
            expected_response = client.get(expected_endpoint)
            assert response.status_code == 200
            assert response.json() == expected_response.json()
    
    def test_large_number_of_requests(self):
        """Test handling a large number of sequential requests"""
        client = TestClient(app)
        
        # Make 50 requests to ensure stability
        for i in range(50):
            response = client.get("/")
            assert response.status_code == 200
            assert response.json() == {"Hello": "World"}
    
    def test_request_headers_handling(self):
        """Test that custom headers are handled properly"""
        client = TestClient(app)
        
        custom_headers = {
            "X-Custom-Header": "test-value",
            "User-Agent": "test-agent",
            "Accept": "application/json"
        }
        
        response = client.get("/", headers=custom_headers)
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}