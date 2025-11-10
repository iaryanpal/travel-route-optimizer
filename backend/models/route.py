"""
Route Model
Represents a connection/edge between two cities
"""

from city import City


class Route:
    """
    Represents a route (edge) between two cities.
    
    Attributes:
        origin (City): Starting city
        destination (City): Ending city
        distance (float): Distance in kilometers
        cost (float): Travel cost in currency units
        bidirectional (bool): Whether route works both ways
    """
    
    def __init__(self, origin, destination, distance, cost, bidirectional=True):
        """
        Initialize a Route object.
        
        Args:
            origin (City): Starting city
            destination (City): Ending city
            distance (float): Distance in kilometers
            cost (float): Travel cost
            bidirectional (bool): If True, route works both ways (default: True)
        
        Raises:
            TypeError: If cities are not City objects
            ValueError: If distance or cost are negative
        """
        if not isinstance(origin, City):
            raise TypeError("Origin must be a City object")
        if not isinstance(destination, City):
            raise TypeError("Destination must be a City object")
        
        if origin == destination:
            raise ValueError("Origin and destination cannot be the same city")
        
        if not isinstance(distance, (int, float)) or distance <= 0:
            raise ValueError("Distance must be a positive number")
        
        if not isinstance(cost, (int, float)) or cost <= 0:
            raise ValueError("Cost must be a positive number")
        
        self.origin = origin
        self.destination = destination
        self.distance = float(distance)
        self.cost = float(cost)
        self.bidirectional = bidirectional
    
    def __str__(self):
        """String representation of the route"""
        arrow = "<->" if self.bidirectional else "->"
        return f"{self.origin.name} {arrow} {self.destination.name} ({self.distance}km, ${self.cost})"
    
    def __repr__(self):
        """Official string representation for debugging"""
        return (f"Route(origin={self.origin.name}, destination={self.destination.name}, "
                f"distance={self.distance}, cost={self.cost}, bidirectional={self.bidirectional})")
    
    def __eq__(self, other):
        """
        Check if two routes are equal.
        
        Args:
            other (Route): Another route object
            
        Returns:
            bool: True if routes connect same cities
        """
        if not isinstance(other, Route):
            return False
        
        if self.bidirectional and other.bidirectional:
            # For bidirectional routes, order doesn't matter
            return ((self.origin == other.origin and self.destination == other.destination) or
                    (self.origin == other.destination and self.destination == other.origin))
        else:
            # For directional routes, order matters
            return (self.origin == other.origin and self.destination == other.destination)
    
    def get_reverse(self):
        """
        Get the reverse route (only if bidirectional).
        
        Returns:
            Route: A new Route object in the opposite direction
            
        Raises:
            ValueError: If route is not bidirectional
        """
        if not self.bidirectional:
            raise ValueError("Cannot reverse a unidirectional route")
        
        return Route(
            origin=self.destination,
            destination=self.origin,
            distance=self.distance,
            cost=self.cost,
            bidirectional=True
        )
    
    def cost_per_km(self):
        """
        Calculate cost per kilometer.
        
        Returns:
            float: Cost efficiency (cost per km)
        """
        return round(self.cost / self.distance, 2)
    
    def to_dict(self):
        """
        Convert route to dictionary format.
        
        Returns:
            dict: Dictionary representation of the route
        """
        return {
            'origin': self.origin.name,
            'destination': self.destination.name,
            'distance': self.distance,
            'cost': self.cost,
            'bidirectional': self.bidirectional
        }
    
    @classmethod
    def from_dict(cls, data, cities_dict):
        """
        Create a Route object from a dictionary.
        
        Args:
            data (dict): Dictionary with route data
            cities_dict (dict): Dictionary mapping city names to City objects
            
        Returns:
            Route: New Route object
            
        Raises:
            KeyError: If required keys are missing or cities not found
        """
        origin_name = data['origin']
        destination_name = data['destination']
        
        if origin_name not in cities_dict:
            raise KeyError(f"Origin city '{origin_name}' not found")
        if destination_name not in cities_dict:
            raise KeyError(f"Destination city '{destination_name}' not found")
        
        return cls(
            origin=cities_dict[origin_name],
            destination=cities_dict[destination_name],
            distance=data['distance'],
            cost=data['cost'],
            bidirectional=data.get('bidirectional', True)
        )


# Example usage (for testing)
if __name__ == "__main__":
    # Create cities
    delhi = City("New Delhi", 28.6139, 77.2090)
    mumbai = City("Mumbai", 19.0760, 72.8777)
    bangalore = City("Bangalore", 12.9716, 77.5946)
    
    # Create routes
    route1 = Route(delhi, mumbai, 1400, 5000)
    route2 = Route(mumbai, bangalore, 980, 3500)
    route3 = Route(delhi, bangalore, 2150, 6000, bidirectional=False)
    
    print(route1)
    print(route2)
    print(route3)
    
    print(f"\nCost per km (Delhi-Mumbai): ${route1.cost_per_km()}/km")
    
    # Test reverse
    reverse_route = route1.get_reverse()
    print(f"\nReverse: {reverse_route}")
    
    # Test dictionary conversion
    route_dict = route1.to_dict()
    print(f"\nAs dict: {route_dict}")