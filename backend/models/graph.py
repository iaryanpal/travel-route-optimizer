"""
Graph Model
Manages the network of cities and routes
"""

from collections import defaultdict
from city import City
from route import Route


class Graph:
    """
    Represents a graph of cities and routes.
    Uses adjacency list representation for efficient pathfinding.
    
    Attributes:
        cities (dict): Dictionary mapping city names to City objects
        adjacency_list (dict): Dictionary mapping cities to their connected routes
    """
    
    def __init__(self):
        """Initialize an empty graph"""
        self.cities = {}  # {city_name: City object}
        self.adjacency_list = defaultdict(list)  # {City: [Route, Route, ...]}
    
    def add_city(self, city):
        """
        Add a city to the graph.
        
        Args:
            city (City): City object to add
            
        Raises:
            TypeError: If city is not a City object
            ValueError: If city already exists
        """
        if not isinstance(city, City):
            raise TypeError("Must provide a City object")
        
        if city.name in self.cities:
            raise ValueError(f"City '{city.name}' already exists in graph")
        
        self.cities[city.name] = city
        # Initialize empty adjacency list for this city
        if city not in self.adjacency_list:
            self.adjacency_list[city] = []
    
    def add_route(self, route):
        """
        Add a route to the graph.
        Automatically adds cities if they don't exist.
        
        Args:
            route (Route): Route object to add
            
        Raises:
            TypeError: If route is not a Route object
        """
        if not isinstance(route, Route):
            raise TypeError("Must provide a Route object")
        
        # Add cities if they don't exist
        if route.origin.name not in self.cities:
            self.add_city(route.origin)
        if route.destination.name not in self.cities:
            self.add_city(route.destination)
        
        # Add route to adjacency list
        self.adjacency_list[route.origin].append(route)
        
        # If bidirectional, add reverse route
        if route.bidirectional:
            reverse_route = Route(
                route.destination,
                route.origin,
                route.distance,
                route.cost,
                bidirectional=False  # Avoid infinite loop
            )
            self.adjacency_list[route.destination].append(reverse_route)
    
    def get_city(self, city_name):
        """
        Get a city by name.
        
        Args:
            city_name (str): Name of the city
            
        Returns:
            City: City object if found, None otherwise
        """
        return self.cities.get(city_name)
    
    def get_neighbors(self, city):
        """
        Get all routes from a city.
        
        Args:
            city (City): City object
            
        Returns:
            list: List of Route objects from this city
        """
        if isinstance(city, str):
            city = self.get_city(city)
        
        if city is None:
            return []
        
        return self.adjacency_list.get(city, [])
    
    def get_all_cities(self):
        """
        Get all cities in the graph.
        
        Returns:
            list: List of City objects
        """
        return list(self.cities.values())
    
    def get_all_routes(self):
        """
        Get all routes in the graph.
        
        Returns:
            list: List of unique Route objects
        """
        routes = []
        seen = set()
        
        for city, route_list in self.adjacency_list.items():
            for route in route_list:
                # Create unique identifier for route
                route_id = tuple(sorted([route.origin.name, route.destination.name]))
                if route_id not in seen:
                    routes.append(route)
                    seen.add(route_id)
        
        return routes
    
    def city_count(self):
        """Get total number of cities"""
        return len(self.cities)
    
    def route_count(self):
        """Get total number of unique routes"""
        return len(self.get_all_routes())
    
    def has_path(self, origin_name, destination_name):
        """
        Check if a path exists between two cities using BFS.
        
        Args:
            origin_name (str): Name of origin city
            destination_name (str): Name of destination city
            
        Returns:
            bool: True if path exists, False otherwise
        """
        origin = self.get_city(origin_name)
        destination = self.get_city(destination_name)
        
        if origin is None or destination is None:
            return False
        
        if origin == destination:
            return True
        
        visited = set()
        queue = [origin]
        
        while queue:
            current = queue.pop(0)
            if current == destination:
                return True
            
            if current in visited:
                continue
            
            visited.add(current)
            
            for route in self.get_neighbors(current):
                if route.destination not in visited:
                    queue.append(route.destination)
        
        return False
    
    def __str__(self):
        """String representation of the graph"""
        return f"Graph(cities={self.city_count()}, routes={self.route_count()})"
    
    def __repr__(self):
        """Detailed representation for debugging"""
        cities_str = ", ".join(self.cities.keys())
        return f"Graph(cities=[{cities_str}])"
    
    def to_dict(self):
        """
        Convert graph to dictionary format.
        
        Returns:
            dict: Dictionary with cities and routes
        """
        return {
            'cities': [city.to_dict() for city in self.cities.values()],
            'routes': [route.to_dict() for route in self.get_all_routes()]
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Graph from dictionary data.
        
        Args:
            data (dict): Dictionary with 'cities' and 'routes' keys
            
        Returns:
            Graph: New Graph object
        """
        graph = cls()
        
        # Add all cities first
        for city_data in data.get('cities', []):
            city = City.from_dict(city_data)
            graph.add_city(city)
        
        # Add all routes
        for route_data in data.get('routes', []):
            route = Route.from_dict(route_data, graph.cities)
            graph.add_route(route)
        
        return graph


# Example usage (for testing)
if __name__ == "__main__":
    # Create graph
    graph = Graph()
    
    # Create cities
    delhi = City("New Delhi", 28.6139, 77.2090)
    mumbai = City("Mumbai", 19.0760, 72.8777)
    bangalore = City("Bangalore", 12.9716, 77.5946)
    chennai = City("Chennai", 13.0827, 80.2707)
    
    # Create routes
    route1 = Route(delhi, mumbai, 1400, 5000)
    route2 = Route(mumbai, bangalore, 980, 3500)
    route3 = Route(bangalore, chennai, 350, 1500)
    route4 = Route(delhi, bangalore, 2150, 6000)
    
    # Add to graph
    graph.add_route(route1)
    graph.add_route(route2)
    graph.add_route(route3)
    graph.add_route(route4)
    
    print(f"Graph created: {graph}")
    print(f"\nAll cities: {[city.name for city in graph.get_all_cities()]}")
    print(f"\nRoutes from Mumbai:")
    for route in graph.get_neighbors(mumbai):
        print(f"  {route}")
    
    print(f"\nPath exists Delhi -> Chennai: {graph.has_path('New Delhi', 'Chennai')}")
    print(f"Path exists Chennai -> Delhi: {graph.has_path('Chennai', 'New Delhi')}")
    
    # Test dictionary conversion
    graph_dict = graph.to_dict()
    print(f"\nGraph as dictionary has {len(graph_dict['cities'])} cities and {len(graph_dict['routes'])} routes")