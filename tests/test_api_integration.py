"""
Integration Tests for Population Density API
Test Cases: TC20-TC32

Run tests:
    pytest tests/test_api_integration.py -v                    # All tests
    pytest tests/test_api_integration.py::TestAPIIntegration -v  # Only API tests
    pytest tests/test_api_integration.py::TestAPIIntegration::test_tc20_valid_api_request -v  # Single test
    pytest tests/test_api_integration.py -v -s                 # With print output
"""

import pytest 
import time
import os
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture(scope="class")
def client():
    """Create test client with real dataset."""
    with TestClient(app) as test_client:
        health = test_client.get("/health")
        if health.json().get("status") != "healthy":
            pytest.skip("Dataset not available")
        yield test_client


class TestAPIIntegration:
    """Integration tests for API endpoints (TC20-TC27)."""
    
    def test_tc20_valid_api_request(self, client):
      
        response = client.get("/density?lat=43.6045&lon=1.444")
        
        assert response.status_code == 200
        data = response.json()
        assert "lat" in data and "lon" in data and "density" in data
        assert data["lat"] == 43.6045 and data["lon"] == 1.444
        assert data["density"] > 0

    def test_tc21_missing_latitude(self, client):
        
        response = client.get("/density?lon=1.444")
        assert response.status_code == 422
        assert "lat" in str(response.json()["detail"]).lower()

    def test_tc22_missing_longitude(self, client):
        
        response = client.get("/density?lat=43.6045")
        assert response.status_code == 422
        assert "lon" in str(response.json()["detail"]).lower()

    def test_tc23_invalid_latitude(self, client):
        
        response = client.get("/density?lat=91&lon=0")
        assert response.status_code == 422

    def test_tc24_invalid_longitude(self, client):
       
        response = client.get("/density?lat=0&lon=181")
        assert response.status_code == 422

    def test_tc25_out_of_bounds(self, client):
       
        # Test South Pole (no population)
        response = client.get("/density?lat=-85&lon=0")
        assert response.status_code == 200
        assert response.json()["density"] == 0.0

    def test_tc26_service_initialization_verified(self, client):
        
        # Verify service is initialized and operational
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data.get("status") == "healthy"
        assert data.get("service_initialized") == True
        
        # Also verify that density endpoint works (proves service is operational)
        density_response = client.get("/density?lat=43.6045&lon=1.444")
        assert density_response.status_code == 200  # Not 503!

    def test_tc27_health_endpoint(self, client):
       
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data and "service_initialized" in data
        if data["status"] == "healthy":
            assert "dataset_path" in data and "dataset_crs" in data
            assert "dataset_bounds" in data and "dataset_shape" in data


class TestPerformance:
   
    
    def test_tc28_response_time(self, client):
        
        client.get("/density?lat=43.6045&lon=1.444")  
        
        start = time.time()
        response = client.get("/density?lat=48.8566&lon=2.3522")
        elapsed_ms = (time.time() - start) * 1000
        
        assert response.status_code == 200
        assert elapsed_ms < 500

    def test_tc29_startup_time(self):
       
        from src.service.population_service import PopulationDensityService
        
        path = "data/geographic_data/GHS_POP_E2030_GLOBE_R2023A_54009_100_V1_0_R4_C19.tif"
        if not os.path.exists(path):
            pytest.skip("Dataset not found")
        
        service = PopulationDensityService(path)
        start = time.time()
        service.start()
        elapsed = time.time() - start
        service.stop()
        
        assert elapsed < 900


class TestResponseFormat:
    
    
    def test_tc30_unit_conversion(self, client):
        
        response = client.get("/density?lat=43.6045&lon=1.444")
        assert response.status_code == 200
        density = response.json()["density"]
        assert 100 < density < 50000  # Reasonable city density

    def test_tc31_response_fields(self, client):
        
        response = client.get("/density?lat=48.8566&lon=2.3522")
        assert response.status_code == 200
        data = response.json()
        for field in ["lat", "lon", "density"]:
            assert field in data
            assert isinstance(data[field], (int, float))

    def test_tc32_error_structure(self, client):
        
        response = client.get("/density?lat=91&lon=0")
        assert response.status_code in [400, 422]
        data = response.json()
        assert "detail" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])