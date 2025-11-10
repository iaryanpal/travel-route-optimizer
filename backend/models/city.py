"""
City Model
Represents a city in the route optimization system
"""

class City:
    """
    Represents a city with its properties.
    
    Attributes:
        name (str): Name of the city
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
    """
    
    def __init__(self, name, latitude=0.0, longitude=0.0):
        """
        Initialize a City object.
        
        Args:
            name (str): Name of the city
            latitude (float): Latitude coordinate (default: 0.0)
            longitude (float): Longitude coordinate (default: 0.0)
        
        Raises:
            ValueError: If name is empty or invalid coordinates
        """
        if not name or not isinstance(name, str):
            raise ValueError("City name must be a non-empty string")
        
        if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
            raise ValueError("Coordinates must be numeric values")
        
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        
        self.name = name.strip()
        self.latitude = float(latitude)
        self.longitude = float(longitude)
    
    def __str__(self):
        """String representation of the city"""
        return f"{self.name} ({self.latitude}, {self.longitude})"
    
    def __repr__(self):
        """Official string representation for debugging"""
        return f"City(name='{self.name}', latitude={self.latitude}, longitude={self.longitude})"
    
    def __eq__(self, other):
        """
        Check if two cities are equal based on name.
        
        Args:
            other (City): Another city object
            
        Returns:
            bool: True if cities have the same name
        """
        if not isinstance(other, City):
            return False
        return self.name.lower() == other.name.lower()
    
    def __hash__(self):
        """
        Make City hashable so it can be used in sets and as dict keys.
        Required for graph implementations.
        """
        return hash(self.name.lower())
    
    def to_dict(self):
        """
        Convert city to dictionary format.
        Useful for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the city
        """
        return {
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a City object from a dictionary.
        
        Args:
            data (dict): Dictionary with city data
            
        Returns:
            City: New City object
            
        Raises:
            KeyError: If required keys are missing
        """
        return cls(
            name=data['name'],
            latitude=data.get('latitude', 0.0),
            longitude=data.get('longitude', 0.0)
        )
    
    def distance_to(self, other):
        """
        Calculate approximate distance to another city using Haversine formula.
        This is optional but adds realism to your project.
        
        Args:
            other (City): Another city object
            
        Returns:
            float: Distance in kilometers
        """
        from math import radians, sin, cos, sqrt, atan2
        
        if not isinstance(other, City):
            raise TypeError("Can only calculate distance to another City object")
        
        # Earth's radius in kilometers
        R = 6371.0
        
        # Convert to radians
        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(other.latitude)
        lon2 = radians(other.longitude)
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c
        return round(distance, 2)


# Example usage (for testing)
if __name__ == "__main__":
    # Create cities
    delhi = City("New Delhi", 28.6139, 77.2090)
    mumbai = City("Mumbai", 19.0760, 72.8777)
    
    print(delhi)
    print(repr(mumbai))
    print(f"Distance: {delhi.distance_to(mumbai)} km")
    
    # Test dictionary conversion
    city_dict = delhi.to_dict()
    print(f"As dict: {city_dict}")
    
    # Create from dictionary
    new_city = City.from_dict(city_dict)
    print(f"From dict: {new_city}")
    
    # Test equality
    delhi2 = City("New Delhi", 28.6139, 77.2090)
    print(f"Delhi == Delhi2: {delhi == delhi2}")