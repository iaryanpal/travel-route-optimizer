"""
Dijkstra's Algorithm Implementation
Finds shortest and cheapest paths between cities
"""

import heapq
import itertools
from graph import Graph
from trip import Trip
from city import City


class PathFinder:
    """
    Implements Dijkstra's algorithm for finding optimal paths.
    Supports optimization by distance or cost.
    """
    
    def __init__(self, graph):
        """
        Initialize PathFinder with a graph.
        
        Args:
            graph (Graph): Graph object containing cities and routes
            
        Raises:
            TypeError: If graph is not a Graph object
        """
        if not isinstance(graph, Graph):
            raise TypeError("Must provide a Graph object")
        
        self.graph = graph
        self.counter = itertools.count()  # Used for tiebreaking in priority queue
    
    def find_path(self, origin_name, destination_name, optimize_by='distance'):
        """
        Find optimal path between two cities using Dijkstra's algorithm.
        
        Args:
            origin_name (str): Name of the starting city
            destination_name (str): Name of the destination city
            optimize_by (str): 'distance' or 'cost' (default: 'distance')
            
        Returns:
            Trip: Trip object with the calculated path, or empty Trip if no path exists
            
        Raises:
            ValueError: If cities don't exist or optimize_by is invalid
        """
        # Validate inputs
        if optimize_by not in ['distance', 'cost']:
            raise ValueError("optimize_by must be 'distance' or 'cost'")
        
        origin = self.graph.get_city(origin_name)
        destination = self.graph.get_city(destination_name)
        
        if origin is None:
            raise ValueError(f"Origin city '{origin_name}' not found in graph")
        if destination is None:
            raise ValueError(f"Destination city '{destination_name}' not found in graph")
        
        # Create trip object
        trip = Trip(origin, destination, optimization_type=optimize_by)
        
        # If origin and destination are the same
        if origin == destination:
            trip.set_path([origin], [])
            return trip
        
        # Run Dijkstra's algorithm
        path, routes = self._dijkstra(origin, destination, optimize_by)
        
        # Set path in trip if found
        if path:
            trip.set_path(path, routes)
        
        return trip
    
    def _dijkstra(self, origin, destination, optimize_by):
        """
        Core Dijkstra's algorithm implementation.
        
        Args:
            origin (City): Starting city
            destination (City): Destination city
            optimize_by (str): 'distance' or 'cost'
            
        Returns:
            tuple: (path as list of cities, routes as list of Route objects)
                   Returns ([], []) if no path exists
        """
        # Initialize data structures
        # distances: stores the minimum cost/distance to reach each city
        distances = {city: float('infinity') for city in self.graph.get_all_cities()}
        distances[origin] = 0
        
        # previous: stores the previous city in the optimal path
        previous = {city: None for city in self.graph.get_all_cities()}
        
        # previous_route: stores the route taken to reach each city
        previous_route = {city: None for city in self.graph.get_all_cities()}
        
        # Priority queue: (distance/cost, counter, city)
        # counter is used to break ties when distances are equal
        pq = [(0, next(self.counter), origin)]
        
        # visited set to track processed cities
        visited = set()
        
        while pq:
            # Get city with minimum distance/cost
            current_distance, _, current_city = heapq.heappop(pq)
            
            # Skip if already visited
            if current_city in visited:
                continue
            
            visited.add(current_city)
            
            # If we reached destination, we can stop
            if current_city == destination:
                break
            
            # Skip if this path is already longer than recorded
            if current_distance > distances[current_city]:
                continue
            
            # Check all neighbors
            for route in self.graph.get_neighbors(current_city):
                neighbor = route.destination
                
                # Skip if already visited
                if neighbor in visited:
                    continue
                
                # Calculate new distance/cost through current city
                if optimize_by == 'distance':
                    weight = route.distance
                else:  # optimize_by == 'cost'
                    weight = route.cost
                
                new_distance = distances[current_city] + weight
                
                # If we found a better path, update it
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_city
                    previous_route[neighbor] = route
                    heapq.heappush(pq, (new_distance, next(self.counter), neighbor))
        
        # Reconstruct path
        path = []
        routes = []
        current = destination
        
        # Check if destination is reachable
        if previous[destination] is None and destination != origin:
            return [], []  # No path found
        
        # Build path from destination to origin
        while current is not None:
            path.append(current)
            if previous[current] is not None:
                routes.append(previous_route[current])
            current = previous[current]
        
        # Reverse to get path from origin to destination
        path.reverse()
        routes.reverse()
        
        return path, routes
    
    def find_all_paths(self, origin_name, destination_name):
        """
        Find both shortest and cheapest paths.
        Convenient method to compare both optimization strategies.
        
        Args:
            origin_name (str): Name of the starting city
            destination_name (str): Name of the destination city
            
        Returns:
            dict: Dictionary with 'by_distance' and 'by_cost' Trip objects
        """
        shortest_trip = self.find_path(origin_name, destination_name, optimize_by='distance')
        cheapest_trip = self.find_path(origin_name, destination_name, optimize_by='cost')
        
        return {
            'by_distance': shortest_trip,
            'by_cost': cheapest_trip
        }
    
    def get_reachable_cities(self, origin_name):
        """
        Get all cities reachable from the origin.
        
        Args:
            origin_name (str): Name of the starting city
            
        Returns:
            list: List of reachable city names
        """
        origin = self.graph.get_city(origin_name)
        if origin is None:
            return []
        
        reachable = set()
        visited = set()
        queue = [origin]
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            
            visited.add(current)
            reachable.add(current.name)
            
            for route in self.graph.get_neighbors(current):
                if route.destination not in visited:
                    queue.append(route.destination)
        
        reachable.discard(origin_name)  # Remove origin itself
        return sorted(list(reachable))


# Example usage and testing
if __name__ == "__main__":
    from route import Route
    
    # Create a sample graph
    print("=== Creating Sample Travel Network ===\n")
    graph = Graph()
    
    # Add cities
    delhi = City("New Delhi", 28.6139, 77.2090)
    mumbai = City("Mumbai", 19.0760, 72.8777)
    bangalore = City("Bangalore", 12.9716, 77.5946)
    chennai = City("Chennai", 13.0827, 80.2707)
    kolkata = City("Kolkata", 22.5726, 88.3639)
    
    # Add routes with varying distances and costs
    routes = [
        Route(delhi, mumbai, 1400, 5000),           # Direct but expensive
        Route(delhi, kolkata, 1500, 3000),          # Longer but cheaper
        Route(mumbai, bangalore, 980, 3500),
        Route(bangalore, chennai, 350, 1500),
        Route(kolkata, chennai, 1670, 4000),
        Route(delhi, bangalore, 2150, 8000),        # Very expensive direct route
        Route(mumbai, chennai, 1340, 5500)          # Alternative route
    ]
    
    for route in routes:
        graph.add_route(route)
    
    print(f"Graph: {graph}")
    print(f"Cities: {', '.join([c.name for c in graph.get_all_cities()])}\n")
    
    # Create PathFinder
    pathfinder = PathFinder(graph)
    
    # Test 1: Find shortest path by distance
    print("=== Test 1: Shortest Path (by Distance) ===")
    trip1 = pathfinder.find_path("New Delhi", "Chennai", optimize_by='distance')
    print(trip1)
    print()
    
    # Test 2: Find cheapest path by cost
    print("=== Test 2: Cheapest Path (by Cost) ===")
    trip2 = pathfinder.find_path("New Delhi", "Chennai", optimize_by='cost')
    print(trip2)
    print()
    
    # Test 3: Compare both strategies
    print("=== Test 3: Comparison ===")
    comparison = trip1.compare_with(trip2)
    print(f"Distance difference: {comparison['distance_difference']:.2f} km")
    print(f"Cost difference: ${comparison['cost_difference']:.2f}")
    print(f"Shortest path saves: {abs(comparison['distance_difference']):.2f} km")
    print(f"Cheapest path saves: ${abs(comparison['cost_difference']):.2f}")
    print()
    
    # Test 4: Find both paths at once
    print("=== Test 4: Find All Paths ===")
    all_paths = pathfinder.find_all_paths("Mumbai", "Kolkata")
    print("By Distance:")
    print(all_paths['by_distance'])
    print("\nBy Cost:")
    print(all_paths['by_cost'])
    print()
    
    # Test 5: Get reachable cities
    print("=== Test 5: Reachable Cities from Mumbai ===")
    reachable = pathfinder.get_reachable_cities("Mumbai")
    print(f"Cities reachable from Mumbai: {', '.join(reachable)}")
    print()
    
    # Test 6: No path scenario
    print("=== Test 6: Testing No Path Scenario ===")
    isolated_city = City("Isolated City", 0, 0)
    graph.add_city(isolated_city)
    trip_no_path = pathfinder.find_path("Mumbai", "Isolated City", optimize_by='distance')
    print(trip_no_path)