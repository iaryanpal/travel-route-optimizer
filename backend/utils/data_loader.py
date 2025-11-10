"""
Data Loader Utility
Loads cities and routes from JSON files into Graph
"""

import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'models'))
from graph import Graph 
from city import City
from route import Route


class DataLoader:
    """
    Utility class to load graph data from JSON files.
    """
    
    @staticmethod
    def load_graph_from_files(cities_file, routes_file):
        """
        Load a complete graph from JSON files.
        
        Args:
            cities_file (str): Path to cities JSON file
            routes_file (str): Path to routes JSON file
            
        Returns:
            Graph: Populated Graph object
            
        Raises:
            FileNotFoundError: If files don't exist
            json.JSONDecodeError: If JSON is invalid
        """
        # Check if files exist
        if not os.path.exists(cities_file):
            raise FileNotFoundError(f"Cities file not found: {cities_file}")
        if not os.path.exists(routes_file):
            raise FileNotFoundError(f"Routes file not found: {routes_file}")
        
        # Load cities
        with open(cities_file, 'r', encoding='utf-8') as f:
            cities_data = json.load(f)
        
        # Load routes
        with open(routes_file, 'r', encoding='utf-8') as f:
            routes_data = json.load(f)
        
        # Create graph
        graph = Graph()
        
        # Add cities to graph
        for city_data in cities_data:
            city = City.from_dict(city_data)
            graph.add_city(city)
        
        # Add routes to graph
        for route_data in routes_data:
            route = Route.from_dict(route_data, graph.cities)
            graph.add_route(route)
        
        return graph
    
    @staticmethod
    def load_default_graph():
        """
        Load graph from default data files in backend/data directory.
        
        Returns:
            Graph: Populated Graph object
        """
        # Get the directory of this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construct paths to data files
        data_dir = os.path.join(os.path.dirname(current_dir), 'data')
        cities_file = os.path.join(data_dir, 'cities.json')
        routes_file = os.path.join(data_dir, 'routes.json')
        
        return DataLoader.load_graph_from_files(cities_file, routes_file)
    
    @staticmethod
    def save_graph_to_files(graph, cities_file, routes_file):
        """
        Save a graph to JSON files.
        
        Args:
            graph (Graph): Graph object to save
            cities_file (str): Path to save cities JSON
            routes_file (str): Path to save routes JSON
        """
        graph_dict = graph.to_dict()
        
        # Save cities
        with open(cities_file, 'w', encoding='utf-8') as f:
            json.dump(graph_dict['cities'], f, indent=2)
        
        # Save routes
        with open(routes_file, 'w', encoding='utf-8') as f:
            json.dump(graph_dict['routes'], f, indent=2)
    
    @staticmethod
    def validate_data(cities_data, routes_data):
        """
        Validate loaded data for common issues.
        
        Args:
            cities_data (list): List of city dictionaries
            routes_data (list): List of route dictionaries
            
        Returns:
            dict: Validation results with 'valid' (bool) and 'errors' (list)
        """
        errors = []
        
        # Check for empty data
        if not cities_data:
            errors.append("No cities found in data")
        if not routes_data:
            errors.append("No routes found in data")
        
        # Check for duplicate cities
        city_names = [city['name'] for city in cities_data]
        if len(city_names) != len(set(city_names)):
            duplicates = [name for name in city_names if city_names.count(name) > 1]
            errors.append(f"Duplicate cities found: {set(duplicates)}")
        
        # Check if routes reference existing cities
        for route in routes_data:
            if route['origin'] not in city_names:
                errors.append(f"Route references unknown origin city: {route['origin']}")
            if route['destination'] not in city_names:
                errors.append(f"Route references unknown destination city: {route['destination']}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }


# Example usage and testing
if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from algorithms.dijkstra import PathFinder
    
    print("=== Loading Graph from Data Files ===\n")
    
    try:
        # Load the graph
        graph = DataLoader.load_default_graph()
        
        print(f"✅ Graph loaded successfully!")
        print(f"   Cities: {graph.city_count()}")
        print(f"   Routes: {graph.route_count()}")
        print(f"\nAvailable cities:")
        for city in sorted([c.name for c in graph.get_all_cities()]):
            print(f"   - {city}")
        
        # Test pathfinding with loaded data
        print("\n=== Testing Pathfinding with Real Data ===\n")
        pathfinder = PathFinder(graph)
        
        # Test 1: Delhi to Kochi
        print("Test 1: New Delhi → Kochi")
        trip1 = pathfinder.find_path("New Delhi", "Kochi", optimize_by='distance')
        if trip1.is_valid():
            print(f"   Path: {' → '.join(trip1.get_path_names())}")
            print(f"   Distance: {trip1.total_distance} km")
            print(f"   Cost: ₹{trip1.total_cost}")
        print()
        
        # Test 2: Mumbai to Kolkata (compare both)
        print("Test 2: Mumbai → Kolkata (Comparison)")
        all_paths = pathfinder.find_all_paths("Mumbai", "Kolkata")
        
        print("   By Distance:")
        trip_dist = all_paths['by_distance']
        if trip_dist.is_valid():
            print(f"      Path: {' → '.join(trip_dist.get_path_names())}")
            print(f"      Distance: {trip_dist.total_distance} km")
            print(f"      Cost: ₹{trip_dist.total_cost}")
        
        print("\n   By Cost:")
        trip_cost = all_paths['by_cost']
        if trip_cost.is_valid():
            print(f"      Path: {' → '.join(trip_cost.get_path_names())}")
            print(f"      Distance: {trip_cost.total_distance} km")
            print(f"      Cost: ₹{trip_cost.total_cost}")
        
        # Show savings
        if trip_dist.is_valid() and trip_cost.is_valid():
            savings = trip_dist.total_cost - trip_cost.total_cost
            print(f"\n   💰 Cost savings: ₹{savings:.2f}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\nMake sure cities.json and routes.json exist in backend/data/")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")