"""
Unit Tests for Dijkstra's Algorithm
"""

import pytest
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'models'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'algorithms'))

from city import City
from route import Route
from graph import Graph
from trip import Trip
from dijkstra import PathFinder


class TestPathFinder:
    """Test cases for PathFinder (Dijkstra's Algorithm)"""
    
    @pytest.fixture
    def sample_graph(self):
        """Create a sample graph for testing"""
        graph = Graph()
        
        # Create cities
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        bangalore = City("Bangalore", 12.9716, 77.5946)
        chennai = City("Chennai", 13.0827, 80.2707)
        
        # Create routes
        routes = [
            Route(delhi, mumbai, 1400, 5000),
            Route(mumbai, bangalore, 980, 3500),
            Route(bangalore, chennai, 350, 1500),
            Route(delhi, bangalore, 2150, 6000),
            Route(mumbai, chennai, 1340, 5500)
        ]
        
        for route in routes:
            graph.add_route(route)
        
        return graph
    
    def test_create_pathfinder(self, sample_graph):
        """Test creating PathFinder instance"""
        pathfinder = PathFinder(sample_graph)
        assert pathfinder.graph == sample_graph
    
    def test_pathfinder_invalid_graph(self):
        """Test that invalid graph raises error"""
        with pytest.raises(TypeError):
            PathFinder("not a graph")
    
    def test_find_shortest_path_by_distance(self, sample_graph):
        """Test finding shortest path by distance"""
        pathfinder = PathFinder(sample_graph)
        trip = pathfinder.find_path("Delhi", "Chennai", optimize_by='distance')
        
        assert trip.is_valid() == True
        assert trip.origin.name == "Delhi"
        assert trip.destination.name == "Chennai"
        assert trip.optimization_type == 'distance'
        assert trip.total_distance > 0
    
    def test_find_cheapest_path_by_cost(self, sample_graph):
        """Test finding cheapest path by cost"""
        pathfinder = PathFinder(sample_graph)
        trip = pathfinder.find_path("Delhi", "Chennai", optimize_by='cost')
        
        assert trip.is_valid() == True
        assert trip.optimization_type == 'cost'
        assert trip.total_cost > 0
    
    def test_same_origin_destination(self, sample_graph):
        """Test path when origin and destination are same"""
        pathfinder = PathFinder(sample_graph)
        trip = pathfinder.find_path("Delhi", "Delhi", optimize_by='distance')
        
        assert trip.is_valid() == True
        assert len(trip.path) == 1
        assert trip.total_distance == 0
        assert trip.total_cost == 0
    
    def test_no_path_exists(self, sample_graph):
        """Test when no path exists between cities"""
        # Add an isolated city
        isolated = City("Isolated", 0, 0)
        sample_graph.add_city(isolated)
        
        pathfinder = PathFinder(sample_graph)
        trip = pathfinder.find_path("Delhi", "Isolated", optimize_by='distance')
        
        assert trip.is_valid() == False
    
    def test_invalid_city_names(self, sample_graph):
        """Test that invalid city names raise errors"""
        pathfinder = PathFinder(sample_graph)
        
        with pytest.raises(ValueError):
            pathfinder.find_path("InvalidCity", "Delhi", optimize_by='distance')
        
        with pytest.raises(ValueError):
            pathfinder.find_path("Delhi", "InvalidCity", optimize_by='distance')
    
    def test_invalid_optimization_type(self, sample_graph):
        """Test that invalid optimization type raises error"""
        pathfinder = PathFinder(sample_graph)
        
        with pytest.raises(ValueError):
            pathfinder.find_path("Delhi", "Mumbai", optimize_by='invalid')
    
    def test_direct_vs_indirect_path(self, sample_graph):
        """Test that algorithm chooses correct path"""
        pathfinder = PathFinder(sample_graph)
        
        # By distance: should prefer shorter total distance
        trip_dist = pathfinder.find_path("Delhi", "Chennai", optimize_by='distance')
        
        # By cost: might choose different path if cheaper
        trip_cost = pathfinder.find_path("Delhi", "Chennai", optimize_by='cost')
        
        assert trip_dist.is_valid() == True
        assert trip_cost.is_valid() == True
        
        # At least one should have stops (not direct path to Chennai)
        # since we have intermediate cities offering better routes
        assert (trip_dist.get_number_of_stops() > 0 or 
                trip_cost.get_number_of_stops() > 0)
    
    def test_find_all_paths(self, sample_graph):
        """Test finding both distance and cost optimized paths"""
        pathfinder = PathFinder(sample_graph)
        all_paths = pathfinder.find_all_paths("Delhi", "Bangalore")
        
        assert 'by_distance' in all_paths
        assert 'by_cost' in all_paths
        assert all_paths['by_distance'].is_valid() == True
        assert all_paths['by_cost'].is_valid() == True
    
    def test_get_reachable_cities(self, sample_graph):
        """Test getting all reachable cities from origin"""
        pathfinder = PathFinder(sample_graph)
        reachable = pathfinder.get_reachable_cities("Delhi")
        
        assert "Mumbai" in reachable
        assert "Bangalore" in reachable
        assert "Chennai" in reachable
        assert "Delhi" not in reachable  # Origin not included
    
    def test_bidirectional_routes(self):
        """Test that bidirectional routes work both ways"""
        graph = Graph()
        
        delhi = City("Delhi", 28.6139, 77.2090)
        mumbai = City("Mumbai", 19.0760, 72.8777)
        
        # Add bidirectional route
        route = Route(delhi, mumbai, 1400, 5000, bidirectional=True)
        graph.add_route(route)
        
        pathfinder = PathFinder(graph)
        
        # Should work both directions
        trip1 = pathfinder.find_path("Delhi", "Mumbai", optimize_by='distance')
        trip2 = pathfinder.find_path("Mumbai", "Delhi", optimize_by='distance')
        
        assert trip1.is_valid() == True
        assert trip2.is_valid() == True
        assert trip1.total_distance == trip2.total_distance
    
    def test_complex_network(self):
        """Test pathfinding in a more complex network"""
        graph = Graph()
        
        # Create multiple cities
        cities = {
            'A': City('A', 0, 0),
            'B': City('B', 1, 1),
            'C': City('C', 2, 2),
            'D': City('D', 3, 3),
            'E': City('E', 4, 4)
        }
        
        # Create multiple routes with different costs
        routes = [
            Route(cities['A'], cities['B'], 10, 100),
            Route(cities['A'], cities['C'], 50, 80),  # Longer but cheaper
            Route(cities['B'], cities['D'], 10, 100),
            Route(cities['C'], cities['D'], 10, 20),   # Cheaper connection
            Route(cities['D'], cities['E'], 10, 100)
        ]
        
        for route in routes:
            graph.add_route(route)
        
        pathfinder = PathFinder(graph)
        
        # By distance: A -> B -> D -> E (shorter)
        trip_dist = pathfinder.find_path('A', 'E', optimize_by='distance')
        
        # By cost: A -> C -> D -> E (cheaper)
        trip_cost = pathfinder.find_path('A', 'E', optimize_by='cost')
        
        assert trip_dist.is_valid() == True
        assert trip_cost.is_valid() == True
        
        # Distance-optimized should be shorter
        assert trip_dist.total_distance < trip_cost.total_distance
        
        # Cost-optimized should be cheaper
        assert trip_cost.total_cost < trip_dist.total_cost


class TestPathFinderWithRealData:
    """Test PathFinder with loaded data from JSON files"""
    
    @pytest.fixture
    def loaded_graph(self):
        """Load graph from data files"""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
        from data_loader import DataLoader
        
        try:
            graph = DataLoader.load_default_graph()
            return graph
        except FileNotFoundError:
            pytest.skip("Data files not found")
    
    def test_pathfinding_with_real_data(self, loaded_graph):
        """Test pathfinding with real Indian cities data"""
        pathfinder = PathFinder(loaded_graph)
        
        # Test a known path
        trip = pathfinder.find_path("New Delhi", "Kochi", optimize_by='distance')
        
        assert trip.is_valid() == True
        assert trip.total_distance > 0
        assert trip.total_cost > 0
        assert len(trip.path) >= 2
    
    def test_all_cities_reachable(self, loaded_graph):
        """Test that all cities in the network are reachable from Delhi"""
        pathfinder = PathFinder(loaded_graph)
        reachable = pathfinder.get_reachable_cities("New Delhi")
        
        # Should have multiple reachable cities
        assert len(reachable) > 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])