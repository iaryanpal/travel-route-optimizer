"""
API Endpoint Tests
Tests for FastAPI routes
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from main import app

# Create test client
client = TestClient(app)


class TestGeneralEndpoints:
    """Test general API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["status"] == "running"
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "cities_loaded" in data
        assert "routes_loaded" in data
        assert data["cities_loaded"] > 0
        assert data["routes_loaded"] > 0


class TestCityEndpoints:
    """Test city-related endpoints"""
    
    def test_get_all_cities(self):
        """Test getting all cities"""
        response = client.get("/cities")
        assert response.status_code == 200
        cities = response.json()
        assert isinstance(cities, list)
        assert len(cities) > 0
        
        # Check structure of first city
        first_city = cities[0]
        assert "name" in first_city
        assert "latitude" in first_city
        assert "longitude" in first_city
    
    def test_get_specific_city(self):
        """Test getting a specific city"""
        response = client.get("/cities/New Delhi")
        assert response.status_code == 200
        city = response.json()
        assert city["name"] == "New Delhi"
        assert isinstance(city["latitude"], float)
        assert isinstance(city["longitude"], float)
    
    def test_get_nonexistent_city(self):
        """Test getting a city that doesn't exist"""
        response = client.get("/cities/NonexistentCity")
        assert response.status_code == 404
        error = response.json()
        assert "detail" in error


class TestRouteEndpoints:
    """Test route-related endpoints"""
    
    def test_get_all_routes(self):
        """Test getting all routes"""
        response = client.get("/routes")
        assert response.status_code == 200
        routes = response.json()
        assert isinstance(routes, list)
        assert len(routes) > 0
        
        # Check structure of first route
        first_route = routes[0]
        assert "origin" in first_route
        assert "destination" in first_route
        assert "distance" in first_route
        assert "cost" in first_route
        assert "bidirectional" in first_route
    
    def test_get_routes_from_city(self):
        """Test getting routes from a specific city"""
        response = client.get("/routes/from/Mumbai")
        assert response.status_code == 200
        routes = response.json()
        assert isinstance(routes, list)
        
        # All routes should originate from Mumbai
        for route in routes:
            assert route["origin"] == "Mumbai"
    
    def test_get_routes_from_nonexistent_city(self):
        """Test getting routes from a city that doesn't exist"""
        response = client.get("/routes/from/NonexistentCity")
        assert response.status_code == 404


class TestPathfindingEndpoints:
    """Test pathfinding endpoints"""
    
    def test_find_path_by_distance(self):
        """Test finding path optimized by distance"""
        request_data = {
            "origin": "New Delhi",
            "destination": "Mumbai",
            "optimize_by": "distance"
        }
        response = client.post("/find-path", json=request_data)
        assert response.status_code == 200
        
        result = response.json()
        assert result["origin"] == "New Delhi"
        assert result["destination"] == "Mumbai"
        assert result["optimization_type"] == "distance"
        assert result["valid"] == True
        assert result["total_distance"] > 0
        assert result["total_cost"] > 0
        assert isinstance(result["path"], list)
        assert len(result["path"]) >= 2
        assert result["path"][0] == "New Delhi"
        assert result["path"][-1] == "Mumbai"
    
    def test_find_path_by_cost(self):
        """Test finding path optimized by cost"""
        request_data = {
            "origin": "New Delhi",
            "destination": "Mumbai",
            "optimize_by": "cost"
        }
        response = client.post("/find-path", json=request_data)
        assert response.status_code == 200
        
        result = response.json()
        assert result["optimization_type"] == "cost"
        assert result["valid"] == True
    
    def test_find_path_same_city(self):
        """Test finding path when origin and destination are the same"""
        request_data = {
            "origin": "Mumbai",
            "destination": "Mumbai",
            "optimize_by": "distance"
        }
        response = client.post("/find-path", json=request_data)
        assert response.status_code == 200
        
        result = response.json()
        assert result["valid"] == True
        assert result["total_distance"] == 0
        assert result["total_cost"] == 0
        assert len(result["path"]) == 1
    
    def test_find_path_invalid_optimization(self):
        """Test finding path with invalid optimization type"""
        request_data = {
            "origin": "New Delhi",
            "destination": "Mumbai",
            "optimize_by": "invalid"
        }
        response = client.post("/find-path", json=request_data)
        assert response.status_code == 400
        error = response.json()
        assert "detail" in error
    
    def test_find_path_nonexistent_origin(self):
        """Test finding path with nonexistent origin city"""
        request_data = {
            "origin": "NonexistentCity",
            "destination": "Mumbai",
            "optimize_by": "distance"
        }
        response = client.post("/find-path", json=request_data)
        assert response.status_code == 404
    
    def test_find_path_nonexistent_destination(self):
        """Test finding path with nonexistent destination city"""
        request_data = {
            "origin": "Mumbai",
            "destination": "NonexistentCity",
            "optimize_by": "distance"
        }
        response = client.post("/find-path", json=request_data)
        assert response.status_code == 404
    
    def test_path_segments(self):
        """Test that path includes detailed segments"""
        request_data = {
            "origin": "New Delhi",
            "destination": "Chennai",
            "optimize_by": "distance"
        }
        response = client.post("/find-path", json=request_data)
        assert response.status_code == 200
        
        result = response.json()
        assert "segments" in result
        segments = result["segments"]
        assert isinstance(segments, list)
        
        if len(segments) > 0:
            first_segment = segments[0]
            assert "step" in first_segment
            assert "from_city" in first_segment
            assert "to_city" in first_segment
            assert "distance" in first_segment
            assert "cost" in first_segment
    
    def test_get_reachable_cities(self):
        """Test getting reachable cities from a city"""
        response = client.get("/reachable/New Delhi")
        assert response.status_code == 200
        
        reachable = response.json()
        assert isinstance(reachable, list)
        assert len(reachable) > 0
        assert "New Delhi" not in reachable  # Origin not included
    
    def test_get_reachable_from_nonexistent_city(self):
        """Test getting reachable cities from nonexistent city"""
        response = client.get("/reachable/NonexistentCity")
        assert response.status_code == 404


class TestPathOptimizationComparison:
    """Test comparing distance vs cost optimization"""
    
    def test_distance_vs_cost_optimization(self):
        """Test that distance and cost optimization may give different paths"""
        # Get path by distance
        distance_request = {
            "origin": "New Delhi",
            "destination": "Kochi",
            "optimize_by": "distance"
        }
        distance_response = client.post("/find-path", json=distance_request)
        assert distance_response.status_code == 200
        distance_result = distance_response.json()
        
        # Get path by cost
        cost_request = {
            "origin": "New Delhi",
            "destination": "Kochi",
            "optimize_by": "cost"
        }
        cost_response = client.post("/find-path", json=cost_request)
        assert cost_response.status_code == 200
        cost_result = cost_response.json()
        
        # Both should be valid
        assert distance_result["valid"] == True
        assert cost_result["valid"] == True
        
        # Distance-optimized should have less or equal distance
        assert distance_result["total_distance"] <= cost_result["total_distance"]


class TestAPIResponseFormat:
    """Test API response formats and data types"""
    
    def test_city_response_format(self):
        """Test that city responses have correct format"""
        response = client.get("/cities")
        cities = response.json()
        
        for city in cities:
            assert isinstance(city["name"], str)
            assert isinstance(city["latitude"], (int, float))
            assert isinstance(city["longitude"], (int, float))
            assert -90 <= city["latitude"] <= 90
            assert -180 <= city["longitude"] <= 180
    
    def test_route_response_format(self):
        """Test that route responses have correct format"""
        response = client.get("/routes")
        routes = response.json()
        
        for route in routes:
            assert isinstance(route["origin"], str)
            assert isinstance(route["destination"], str)
            assert isinstance(route["distance"], (int, float))
            assert isinstance(route["cost"], (int, float))
            assert isinstance(route["bidirectional"], bool)
            assert route["distance"] > 0
            assert route["cost"] > 0
    
    def test_path_response_format(self):
        """Test that path responses have correct format"""
        request_data = {
            "origin": "Mumbai",
            "destination": "Bangalore",
            "optimize_by": "distance"
        }
        response = client.post("/find-path", json=request_data)
        result = response.json()
        
        assert isinstance(result["origin"], str)
        assert isinstance(result["destination"], str)
        assert isinstance(result["path"], list)
        assert isinstance(result["total_distance"], (int, float))
        assert isinstance(result["total_cost"], (int, float))
        assert isinstance(result["stops"], int)
        assert isinstance(result["optimization_type"], str)
        assert isinstance(result["segments"], list)
        assert isinstance(result["valid"], bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])