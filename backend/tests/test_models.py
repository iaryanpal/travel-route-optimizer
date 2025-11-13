"""
Unit Tests for Models (City, Route, Graph, Trip)
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'models'))

from city import City
from route import Route
from graph import Graph
from trip import Trip


class TestCity:
    """Test cases for City class"""
    
    def test_create_city_valid(self):
        """Test creating a valid city"""
        city = City("Mumbai", 19.0760, 72.8777)
        assert city.name == "Mumbai"
        assert city.latitude == 19.0760
        assert city.longitude == 72.8777
    
    def test_create_city_invalid_name(self):
        """Test that empty name raises error"""
        with pytest.raises(ValueError):
            City("", 19.0760, 72.8777)
    
    def test_create_city_invalid_coordinates(self):
        """Test that invalid coordinates raise errors"""
        with pytest.raises(ValueError):
            City("Mumbai", 100, 72.8777)  # Invalid latitude
        
        with pytest.raises(ValueError):
            City("Mumbai", 19.0760, 200)  # Invalid longitude
    
    def test_city_equality(self):
        """Test that cities with same name are equal"""
        city1 = City("Delhi", 28.6139, 77.2090)
        city2 = City("Delhi", 28.6139, 77.2090)
        city3 = City("Mumbai", 19.0760, 72.8777)
        
        assert city1 == city2
        assert city1 != city3
    
    def test_city_hashable(self):
        """Test that cities can be used in sets and dicts"""
        city1 = City("Delhi", 28.6139, 77.2090)
        city2 = City("Mumbai", 19.0760, 72.8777)
        
        city_set = {city1, city2}
        assert len(city_set) == 2
        
        city_dict = {city1: "Capital", city2: "Financial"}
        assert city_dict[city1] == "Capital"
    
    def test_distance_calculation(self):
        """Test distance calculation between cities"""
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        
        distance = delhi.distance_to(mumbai)
        assert isinstance(distance, float)
        assert 1100 < distance < 1200  # Approximate real distance
    
    def test_to_dict(self):
        """Test city to dictionary conversion"""
        city = City("Chennai", 13.0827, 80.2707)
        city_dict = city.to_dict()
        
        assert city_dict['name'] == "Chennai"
        assert city_dict['latitude'] == 13.0827
        assert city_dict['longitude'] == 80.2707
    
    def test_from_dict(self):
        """Test creating city from dictionary"""
        data = {'name': 'Bangalore', 'latitude': 12.9716, 'longitude': 77.5946}
        city = City.from_dict(data)
        
        assert city.name == "Bangalore"
        assert city.latitude == 12.9716


class TestRoute:
    """Test cases for Route class"""
    
    def test_create_route_valid(self):
        """Test creating a valid route"""
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        route = Route(delhi, mumbai, 1400, 5000)
        
        assert route.origin == delhi
        assert route.destination == mumbai
        assert route.distance == 1400
        assert route.cost == 5000
        assert route.bidirectional == True
    
    def test_create_route_invalid_cities(self):
        """Test that same origin/destination raises error"""
        delhi = City("Delhi", 28.6139, 77.2090)
        
        with pytest.raises(ValueError):
            Route(delhi, delhi, 100, 500)
    
    def test_create_route_negative_values(self):
        """Test that negative distance/cost raise errors"""
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        
        with pytest.raises(ValueError):
            Route(delhi, mumbai, -100, 500)
        
        with pytest.raises(ValueError):
            Route(delhi, mumbai, 100, -500)
    
    def test_route_reverse(self):
        """Test getting reverse route"""
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        route = Route(delhi, mumbai, 1400, 5000)
        
        reverse = route.get_reverse()
        assert reverse.origin == mumbai
        assert reverse.destination == delhi
        assert reverse.distance == 1400
        assert reverse.cost == 5000
    
    def test_cost_per_km(self):
        """Test cost per kilometer calculation"""
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        route = Route(delhi, mumbai, 1400, 5600)
        
        assert route.cost_per_km() == 4.0


class TestGraph:
    """Test cases for Graph class"""
    
    def test_create_empty_graph(self):
        """Test creating an empty graph"""
        graph = Graph()
        assert graph.city_count() == 0
        assert graph.route_count() == 0
    
    def test_add_city(self):
        """Test adding cities to graph"""
        graph = Graph()
        delhi = City("Delhi", 28.6139, 77.2090)
        
        graph.add_city(delhi)
        assert graph.city_count() == 1
        assert graph.get_city("Delhi") == delhi
    
    def test_add_duplicate_city(self):
        """Test that adding duplicate city raises error"""
        graph = Graph()
        delhi = City("Delhi", 28.6139, 77.2090)
        
        graph.add_city(delhi)
        with pytest.raises(ValueError):
            graph.add_city(delhi)
    
    def test_add_route(self):
        """Test adding routes to graph"""
        graph = Graph()
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        route = Route(delhi, mumbai, 1400, 5000)
        
        graph.add_route(route)
        assert graph.city_count() == 2
        assert graph.route_count() == 1
    
    def test_get_neighbors(self):
        """Test getting neighbors of a city"""
        graph = Graph()
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        bangalore = City("Bangalore", 12.9716, 77.5946)
        
        route1 = Route(delhi, mumbai, 1400, 5000)
        route2 = Route(delhi, bangalore, 2150, 8000)
        
        graph.add_route(route1)
        graph.add_route(route2)
        
        neighbors = graph.get_neighbors(delhi)
        assert len(neighbors) == 2
    
    def test_has_path(self):
        """Test checking if path exists between cities"""
        graph = Graph()
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        bangalore = City("Bangalore", 12.9716, 77.5946)
        isolated = City("Isolated", 0, 0)
        
        route1 = Route(delhi, mumbai, 1400, 5000)
        route2 = Route(mumbai, bangalore, 980, 4000)
        
        graph.add_route(route1)
        graph.add_route(route2)
        graph.add_city(isolated)
        
        assert graph.has_path("Delhi", "Bangalore") == True
        assert graph.has_path("Delhi", "Isolated") == False


class TestTrip:
    """Test cases for Trip class"""
    
    def test_create_trip(self):
        """Test creating a trip"""
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        
        trip = Trip(delhi, mumbai, optimization_type='distance')
        assert trip.origin == delhi
        assert trip.destination == mumbai
        assert trip.optimization_type == 'distance'
    
    def test_trip_invalid_optimization(self):
        """Test that invalid optimization type raises error"""
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        
        with pytest.raises(ValueError):
            Trip(delhi, mumbai, optimization_type='invalid')
    
    def test_set_path(self):
        """Test setting path in trip"""
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        bangalore = City("Bangalore", 12.9716, 77.5946)
        
        trip = Trip(delhi, bangalore)
        path = [delhi, mumbai, bangalore]
        routes = [
            Route(delhi, mumbai, 1400, 5000),
            Route(mumbai, bangalore, 980, 4000)
        ]
        
        trip.set_path(path, routes)
        assert len(trip.path) == 3
        assert trip.total_distance == 2380
        assert trip.total_cost == 9000
    
    def test_get_number_of_stops(self):
        """Test calculating number of stops"""
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        bangalore = City("Bangalore", 12.9716, 77.5946)
        
        trip = Trip(delhi, bangalore)
        path = [delhi, mumbai, bangalore]
        routes = [
            Route(delhi, mumbai, 1400, 5000),
            Route(mumbai, bangalore, 980, 4000)
        ]
        
        trip.set_path(path, routes)
        assert trip.get_number_of_stops() == 1  # One intermediate stop
    
    def test_trip_is_valid(self):
        """Test checking if trip is valid"""
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        
        trip = Trip(delhi, mumbai)
        assert trip.is_valid() == False  # No path set yet
        
        path = [delhi, mumbai]
        routes = [Route(delhi, mumbai, 1400, 5000)]
        trip.set_path(path, routes)
        
        assert trip.is_valid() == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])