"""
Travel Route Optimizer API
FastAPI application for route calculation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.utils.data_loader import DataLoader
from backend.algorithms.dijkstra import PathFinder

# Create FastAPI app
app = FastAPI(
    title="Travel Route Optimizer API",
    description="Find optimal travel routes between cities using Dijkstra's algorithm",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://travel-route-optimizer.vercel.app/","http://localhost:8000","http://127.0.0.1:8000",],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load graph data on startup
try:
    graph = DataLoader.load_default_graph()
    pathfinder = PathFinder(graph)
    print(f"✅ Graph loaded: {graph.city_count()} cities, {graph.route_count()} routes")
except Exception as e:
    print(f"❌ Error loading graph: {e}")
    graph = None
    pathfinder = None


# Pydantic models for request/response validation
class CityResponse(BaseModel):
    name: str
    latitude: float
    longitude: float


class RouteResponse(BaseModel):
    origin: str
    destination: str
    distance: float
    cost: float
    bidirectional: bool


class PathRequest(BaseModel):
    origin: str
    destination: str
    optimize_by: str = "distance"  # "distance" or "cost"


class PathSegment(BaseModel):
    step: int
    from_city: str
    to_city: str
    distance: float
    cost: float


class PathResponse(BaseModel):
    origin: str
    destination: str
    path: List[str]
    total_distance: float
    total_cost: float
    stops: int
    optimization_type: str
    segments: List[PathSegment]
    valid: bool


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None


# API Endpoints

@app.get("/", tags=["General"])
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Travel Route Optimizer API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "cities": "/cities",
            "routes": "/routes",
            "find_path": "/find-path",
            "docs": "/docs"
        }
    }


@app.get("/health", tags=["General"])
async def health_check():
    """Health check endpoint"""
    if graph is None or pathfinder is None:
        raise HTTPException(status_code=503, detail="Service unavailable - graph not loaded")
    
    return {
        "status": "healthy",
        "cities_loaded": graph.city_count(),
        "routes_loaded": graph.route_count()
    }


@app.get("/cities", response_model=List[CityResponse], tags=["Data"])
async def get_cities():
    """Get all available cities"""
    if graph is None:
        raise HTTPException(status_code=503, detail="Graph data not loaded")
    
    cities = []
    for city in graph.get_all_cities():
        cities.append(CityResponse(
            name=city.name,
            latitude=city.latitude,
            longitude=city.longitude
        ))
    
    return sorted(cities, key=lambda x: x.name)


@app.get("/cities/{city_name}", response_model=CityResponse, tags=["Data"])
async def get_city(city_name: str):
    """Get details of a specific city"""
    if graph is None:
        raise HTTPException(status_code=503, detail="Graph data not loaded")
    
    city = graph.get_city(city_name)
    if city is None:
        raise HTTPException(status_code=404, detail=f"City '{city_name}' not found")
    
    return CityResponse(
        name=city.name,
        latitude=city.latitude,
        longitude=city.longitude
    )


@app.get("/routes", response_model=List[RouteResponse], tags=["Data"])
async def get_routes():
    """Get all available routes"""
    if graph is None:
        raise HTTPException(status_code=503, detail="Graph data not loaded")
    
    routes = []
    for route in graph.get_all_routes():
        routes.append(RouteResponse(
            origin=route.origin.name,
            destination=route.destination.name,
            distance=route.distance,
            cost=route.cost,
            bidirectional=route.bidirectional
        ))
    
    return routes


@app.get("/routes/from/{city_name}", response_model=List[RouteResponse], tags=["Data"])
async def get_routes_from_city(city_name: str):
    """Get all routes from a specific city"""
    if graph is None:
        raise HTTPException(status_code=503, detail="Graph data not loaded")
    
    city = graph.get_city(city_name)
    if city is None:
        raise HTTPException(status_code=404, detail=f"City '{city_name}' not found")
    
    routes = []
    for route in graph.get_neighbors(city):
        routes.append(RouteResponse(
            origin=route.origin.name,
            destination=route.destination.name,
            distance=route.distance,
            cost=route.cost,
            bidirectional=route.bidirectional
        ))
    
    return routes


@app.post("/find-path", response_model=PathResponse, tags=["Pathfinding"])
async def find_path(request: PathRequest):
    """
    Find optimal path between two cities
    
    - **origin**: Starting city name
    - **destination**: Destination city name
    - **optimize_by**: Optimization criteria ("distance" or "cost")
    """
    if pathfinder is None:
        raise HTTPException(status_code=503, detail="Pathfinding service not available")
    
    # Validate optimization type
    if request.optimize_by not in ["distance", "cost"]:
        raise HTTPException(
            status_code=400,
            detail="optimize_by must be 'distance' or 'cost'"
        )
    
    try:
        # Find the path
        trip = pathfinder.find_path(
            request.origin,
            request.destination,
            optimize_by=request.optimize_by
        )
        
        # Build segments
        segments = []
        for segment_data in trip.get_detailed_route():
            segments.append(PathSegment(
                step=segment_data['step'],
                from_city=segment_data['from'],
                to_city=segment_data['to'],
                distance=segment_data['distance'],
                cost=segment_data['cost']
            ))
        
        return PathResponse(
            origin=trip.origin.name,
            destination=trip.destination.name,
            path=trip.get_path_names(),
            total_distance=trip.total_distance,
            total_cost=trip.total_cost,
            stops=trip.get_number_of_stops(),
            optimization_type=trip.optimization_type,
            segments=segments,
            valid=trip.is_valid()
        )
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/reachable/{city_name}", response_model=List[str], tags=["Pathfinding"])
async def get_reachable_cities(city_name: str):
    """Get all cities reachable from a given city"""
    if pathfinder is None:
        raise HTTPException(status_code=503, detail="Pathfinding service not available")
    
    city = graph.get_city(city_name)
    if city is None:
        raise HTTPException(status_code=404, detail=f"City '{city_name}' not found")
    
    reachable = pathfinder.get_reachable_cities(city_name)
    return reachable


# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)