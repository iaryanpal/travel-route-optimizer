"""
Trip Model
Represents the result of a path calculation
"""

from city import City
from route import Route


class Trip:
    """
    Represents a calculated trip/path between cities.
    Stores the result of pathfinding algorithms.
    
    Attributes:
        origin (City): Starting city
        destination (City): Ending city
        path (list): List of City objects in the path
        routes (list): List of Route objects taken
        total_distance (float): Total distance in kilometers
        total_cost (float): Total cost
        optimization_type (str): 'distance' or 'cost'
    """
    
    def __init__(self, origin, destination, optimization_type='distance'):
        """
        Initialize a Trip object.
        
        Args:
            origin (City): Starting city
            destination (City): Ending city
            optimization_type (str): 'distance' or 'cost' (default: 'distance')
        
        Raises:
            TypeError: If cities are not City objects
            ValueError: If optimization_type is invalid
        """
        if not isinstance(origin, City):
            raise TypeError("Origin must be a City object")
        if not isinstance(destination, City):
            raise TypeError("Destination must be a City object")
        
        if optimization_type not in ['distance', 'cost']:
            raise ValueError("optimization_type must be 'distance' or 'cost'")
        
        self.origin = origin
        self.destination = destination
        self.path = []  # Will be filled by pathfinding algorithm
        self.routes = []  # Will be filled by pathfinding algorithm
        self.total_distance = 0.0
        self.total_cost = 0.0
        self.optimization_type = optimization_type
    
    def set_path(self, path, routes):
        """
        Set the path and calculate totals.
        
        Args:
            path (list): List of City objects representing the path
            routes (list): List of Route objects taken
            
        Raises:
            ValueError: If path is empty or routes don't match path
        """
        if not path:
            raise ValueError("Path cannot be empty")
        
        if len(routes) != len(path) - 1:
            raise ValueError("Number of routes must be one less than number of cities")
        
        self.path = path
        self.routes = routes
        
        # Calculate totals
        self.total_distance = sum(route.distance for route in routes)
        self.total_cost = sum(route.cost for route in routes)
    
    def get_path_names(self):
        """
        Get list of city names in the path.
        
        Returns:
            list: List of city names
        """
        return [city.name for city in self.path]
    
    def get_number_of_stops(self):
        """
        Get number of intermediate stops (excluding origin and destination).
        
        Returns:
            int: Number of stops
        """
        return max(0, len(self.path) - 2)
    
    def is_valid(self):
        """
        Check if the trip has a valid path.
        
        Returns:
            bool: True if trip has a path, False otherwise
        """
        return len(self.path) > 0
    
    def get_summary(self):
        """
        Get a summary of the trip.
        
        Returns:
            dict: Dictionary with trip summary
        """
        if not self.is_valid():
            return {
                'status': 'No path found',
                'origin': self.origin.name,
                'destination': self.destination.name
            }
        
        return {
            'origin': self.origin.name,
            'destination': self.destination.name,
            'path': self.get_path_names(),
            'stops': self.get_number_of_stops(),
            'total_distance': round(self.total_distance, 2),
            'total_cost': round(self.total_cost, 2),
            'optimized_by': self.optimization_type
        }
    
    def __str__(self):
        """String representation of the trip"""
        if not self.is_valid():
            return f"No path found from {self.origin.name} to {self.destination.name}"
        
        path_str = " -> ".join(self.get_path_names())
        return (f"Trip: {path_str}\n"
                f"Distance: {self.total_distance:.2f} km\n"
                f"Cost: ${self.total_cost:.2f}\n"
                f"Stops: {self.get_number_of_stops()}\n"
                f"Optimized by: {self.optimization_type}")
    
    def __repr__(self):
        """Detailed representation for debugging"""
        return (f"Trip(origin={self.origin.name}, destination={self.destination.name}, "
                f"cities={len(self.path)}, distance={self.total_distance:.2f}, "
                f"cost={self.total_cost:.2f})")
    
    def to_dict(self):
        """
        Convert trip to dictionary format.
        
        Returns:
            dict: Dictionary representation of the trip
        """
        return {
            'origin': self.origin.name,
            'destination': self.destination.name,
            'path': self.get_path_names(),
            'routes': [route.to_dict() for route in self.routes],
            'total_distance': round(self.total_distance, 2),
            'total_cost': round(self.total_cost, 2),
            'stops': self.get_number_of_stops(),
            'optimization_type': self.optimization_type,
            'valid': self.is_valid()
        }
    
    def get_detailed_route(self):
        """
        Get detailed information about each segment of the trip.
        
        Returns:
            list: List of dictionaries with segment details
        """
        if not self.is_valid():
            return []
        
        segments = []
        for i, route in enumerate(self.routes):
            segment = {
                'step': i + 1,
                'from': route.origin.name,
                'to': route.destination.name,
                'distance': route.distance,
                'cost': route.cost,
                'cost_per_km': route.cost_per_km()
            }
            segments.append(segment)
        
        return segments
    
    def compare_with(self, other_trip):
        """
        Compare this trip with another trip.
        
        Args:
            other_trip (Trip): Another Trip object
            
        Returns:
            dict: Comparison results
        """
        if not isinstance(other_trip, Trip):
            raise TypeError("Can only compare with another Trip object")
        
        return {
            'distance_difference': self.total_distance - other_trip.total_distance,
            'cost_difference': self.total_cost - other_trip.total_cost,
            'stops_difference': self.get_number_of_stops() - other_trip.get_number_of_stops(),
            'this_trip_better_by_distance': self.total_distance < other_trip.total_distance,
            'this_trip_better_by_cost': self.total_cost < other_trip.total_cost
        }


# Example usage (for testing)
if __name__ == "__main__":
    # Create cities
    delhi = City("New Delhi", 28.6139, 77.2090)
    mumbai = City("Mumbai", 19.0760, 72.8777)
    bangalore = City("Bangalore", 12.9716, 77.5946)
    
    # Create a trip
    trip = Trip(delhi, bangalore, optimization_type='distance')
    
    # Simulate path result (this will normally come from Dijkstra's algorithm)
    path = [delhi, mumbai, bangalore]
    routes = [
        Route(delhi, mumbai, 1400, 5000),
        Route(mumbai, bangalore, 980, 3500)
    ]
    
    trip.set_path(path, routes)
    
    print(trip)
    print(f"\n{repr(trip)}")
    print(f"\nPath: {' -> '.join(trip.get_path_names())}")
    print(f"\nSummary: {trip.get_summary()}")
    
    print("\n--- Detailed Route ---")
    for segment in trip.get_detailed_route():
        print(f"Step {segment['step']}: {segment['from']} -> {segment['to']} "
              f"({segment['distance']}km, ${segment['cost']}, ${segment['cost_per_km']}/km)")
    
    # Test invalid trip
    print("\n--- Invalid Trip ---")
    empty_trip = Trip(delhi, bangalore)
    print(empty_trip)