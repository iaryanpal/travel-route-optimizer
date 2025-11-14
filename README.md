# Travel Route Optimizer 🗺️

A full-stack web application that finds optimal travel routes between Indian cities using **Dijkstra's Algorithm**. Users can optimize routes by either shortest distance or lowest cost.


## 🌐 Live Demo

**🚀 Try it now**: [https://travel-route-optimizer.vercel.app](https://travel-route-optimizer.vercel.app)

**📚 API Documentation**: [https://travel-route-optimizer.onrender.com/docs](https://travel-route-optimizer.onrender.com/docs)

**🔗 Backend API**: [https://travel-route-optimizer.onrender.com](https://travel-route-optimizer.onrender.com)

> **Note**: Backend hosted on Render's free tier. First request may take 30 seconds to wake up the server.

---

## 🌟 Key Features

### 🎯 Dual Optimization Modes
- **Shortest Distance**: Find the fastest route by kilometers
- **Lowest Cost**: Find the most economical route by price
- **Side-by-Side Comparison**: Compare both strategies instantly

### 💻 Modern Tech Stack
- **Backend**: Python + FastAPI + Dijkstra's Algorithm
- **Frontend**: Vanilla JavaScript with modern UI/UX
- **Testing**: 56 comprehensive unit and integration tests
- **Deployment**: Production-ready on Render + Vercel

### 📊 Real Dataset
- 15 major Indian cities with actual coordinates
- 25 bidirectional routes with realistic distances and costs
- Haversine formula for distance calculations

### 🎨 User Experience
- Clean, gradient-based modern interface
- Real-time route calculation and visualization
- Interactive API documentation (Swagger UI)
- Responsive design for mobile and desktop
- Visual route display with colored city nodes

---

## 🛠️ Tech Stack

### Backend
- **Python 3.11**: Core programming language
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: Lightning-fast ASGI server
- **PyTest**: Comprehensive testing framework

### Frontend
- **HTML5**: Semantic, accessible markup
- **CSS3**: Modern styling with gradients, animations, and flexbox
- **JavaScript (ES6+)**: Async/await, fetch API, DOM manipulation
- **Font Awesome**: Professional iconography

### Algorithms & Data Structures
- **Dijkstra's Algorithm**: Shortest path finding (O((V+E)logV))
- **Graph (Adjacency List)**: Efficient route network representation
- **Priority Queue (Heap)**: Optimized city selection
- **Object-Oriented Design**: Clean, maintainable, scalable code

### Deployment
- **Render**: Backend API hosting (auto-deploy from GitHub)
- **Vercel**: Frontend hosting with global CDN
- **GitHub Actions**: CI/CD pipeline (planned)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Git
- Modern web browser

### Local Setup

```bash
# Clone repository
git clone https://github.com/iaryanpal/travel-route-optimizer.git
cd travel-route-optimizer

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run tests (optional but recommended)
pytest backend/tests/ -v

# Start backend server
python -m uvicorn main:app --reload
```

Server runs at: `http://localhost:8000`

API Docs at: `http://localhost:8000/docs`

### Open Frontend

Simply open `frontend/index.html` in your browser or:

```bash
# Windows
start frontend/index.html

# Mac
open frontend/index.html

# Linux
xdg-open frontend/index.html
```

---

## 📖 Usage

### Web Interface

1. **Select Origin**: Choose starting city from dropdown
2. **Select Destination**: Choose destination city
3. **Choose Optimization**: Pick "Shortest Distance" or "Lowest Cost"
4. **Find Route**: Click button to calculate optimal path
5. **View Results**: See route, distance, cost, and detailed breakdown
6. **Compare Options**: Use compare button to see both strategies

### API Usage

#### Get All Cities
```bash
curl https://travel-route-optimizer.onrender.com/cities
```

#### Find Optimal Route
```bash
curl -X POST "https://travel-route-optimizer.onrender.com/find-path" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "New Delhi",
    "destination": "Mumbai",
    "optimize_by": "distance"
  }'
```

#### Response Example
```json
{
  "origin": "New Delhi",
  "destination": "Mumbai",
  "path": ["New Delhi", "Mumbai"],
  "total_distance": 1400.0,
  "total_cost": 5500.0,
  "stops": 0,
  "optimization_type": "distance",
  "segments": [...],
  "valid": true
}
```

---

## 🏗️ System Architecture

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Frontend   │────────▶│   FastAPI    │────────▶│   Backend    │
│ (Vercel CDN) │  HTTPS  │     API      │  Calls  │   (Render)   │
└──────────────┘         │  (REST API)  │         │  (Python)    │
                         └──────────────┘         └──────────────┘
                               │                          │
                               │                          │
                               ▼                          ▼
                         ┌──────────┐            ┌──────────────┐
                         │ Pydantic │            │  Dijkstra's  │
                         │Validation│            │   Algorithm  │
                         └──────────┘            └──────────────┘
                                                        │
                                                        ▼
                                                ┌──────────────┐
                                                │    Graph     │
                                                │ (Adj. List)  │
                                                └──────────────┘
```

### Key Design Decisions

**Object-Oriented Programming**
- `City`: Encapsulates location data with validation
- `Route`: Represents connections with distance and cost
- `Graph`: Manages network using adjacency list (O(1) lookup)
- `Trip`: Stores and analyzes pathfinding results

**Algorithm Efficiency**
- Time Complexity: O((V + E) log V) where V=cities, E=routes
- Space Complexity: O(V)
- Guaranteed optimal solution for non-negative weights

**API Design**
- RESTful endpoints following best practices
- Pydantic models for request/response validation
- Auto-generated OpenAPI documentation
- CORS configured for secure cross-origin requests

---

## 🧪 Testing

The project includes comprehensive testing coverage:

### Run All Tests
```bash
pytest backend/tests/ -v
```

### Test Breakdown
- **35 Model Tests**: City, Route, Graph, Trip classes
- **21 API Tests**: All endpoints with various scenarios
- **Total: 56 tests** with 92%+ code coverage

### Run with Coverage Report
```bash
pytest backend/tests/ --cov=backend --cov=main --cov-report=html
```

View detailed report: `htmlcov/index.html`

---

## 📁 Project Structure

```
travel-route-optimizer/
├── backend/
│   ├── models/
│   │   ├── city.py           # City class with coordinates
│   │   ├── route.py          # Route/edge representation
│   │   ├── graph.py          # Graph data structure
│   │   └── trip.py           # Trip result container
│   ├── algorithms/
│   │   └── dijkstra.py       # Pathfinding algorithm
│   ├── data/
│   │   ├── cities.json       # 15 Indian cities
│   │   └── routes.json       # 25 bidirectional routes
│   ├── utils/
│   │   └── data_loader.py    # JSON data loader
│   └── tests/
│       ├── test_models.py    # Model unit tests
│       ├── test_dijkstra.py  # Algorithm tests
│       └── test_api.py       # API integration tests
├── frontend/
│   ├── index.html            # Main application page
│   ├── css/
│   │   └── style.css         # Modern styling
│   └── js/
│       └── app.js            # Frontend logic
├── docs/
│   └── architecture.md       # System design docs
├── main.py                   # FastAPI application
├── requirements.txt          # Python dependencies
├── Procfile                  # Render deployment config
├── runtime.txt               # Python version specification
└── README.md                 # This file
```

---

## 🔍 Algorithm Deep Dive

### Dijkstra's Algorithm Implementation

**Why Dijkstra?**
- Guarantees finding the optimal (shortest/cheapest) path
- Efficient for sparse graphs (realistic road networks)
- Industry-standard for navigation systems
- Well-tested and reliable

**How It Works:**
1. Start from origin city with distance 0
2. Visit nearest unvisited city
3. Update distances to neighbors
4. Repeat until destination reached
5. Reconstruct path from stored previous nodes

**Optimizations:**
- Priority queue (heap) for O(log n) operations
- Early termination when destination found
- Visited set prevents reprocessing
- Supports dual metrics (distance and cost)

---

## 📊 Dataset Details

### Cities (15 Major Indian Cities)
New Delhi, Mumbai, Bangalore, Chennai, Kolkata, Hyderabad, Pune, Ahmedabad, Jaipur, Lucknow, Chandigarh, Kochi, Indore, Bhopal, Goa

Each city includes:
- Accurate latitude/longitude coordinates
- Real geographic location data
- Haversine distance calculations

### Routes (25 Connections)
Bidirectional routes with realistic values:
- **Distance**: Actual road distances in kilometers
- **Cost**: Realistic travel costs in Indian Rupees (₹)
- **Examples**:
  - New Delhi ↔ Mumbai: 1400 km, ₹5500
  - Mumbai ↔ Bangalore: 980 km, ₹4000
  - Bangalore ↔ Chennai: 350 km, ₹1800

---

## 🎓 What I Learned

### Technical Skills
- Building production-ready REST APIs with FastAPI
- Implementing classical algorithms (Dijkstra's)
- Writing comprehensive tests (TDD approach)
- Deploying full-stack applications
- Managing CORS and API security
- Using Git for version control

### Software Engineering
- Object-Oriented Programming principles
- Clean code architecture (separation of concerns)
- API design and documentation
- Error handling and validation
- Performance optimization (time/space complexity)

### DevOps & Deployment
- CI/CD with GitHub integration
- Platform-as-a-Service (Render, Vercel)
- Environment configuration
- Production vs development settings

---

## 🚀 Future Enhancements

- [ ] **A* Algorithm**: Faster pathfinding with heuristics
- [ ] **Interactive Map**: Leaflet.js visualization with route drawing
- [ ] **Multiple Routes**: Show top 3 alternative paths
- [ ] **User Authentication**: Save favorite routes
- [ ] **Route History**: Track past searches
- [ ] **Real-time Traffic**: Integrate live traffic data
- [ ] **More Cities**: Expand to 50+ cities
- [ ] **Mobile App**: React Native version
- [ ] **Export to PDF**: Download route details
- [ ] **Multi-stop Routes**: Add intermediate waypoints
- [ ] **Price Predictions**: ML-based cost estimation
- [ ] **Social Sharing**: Share routes on social media

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Contribution Ideas
- Add more cities and routes
- Implement additional algorithms (A*, Bellman-Ford)
- Improve UI/UX design
- Add more test cases
- Optimize performance
- Improve documentation

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Aryan Pal**

🔗 **GitHub**: [@iaryanpal](https://github.com/iaryanpal)  
💼 **LinkedIn**: [LinkedIn] (https://www.linkedin.com/in/aryan-pal-1025a432a/)
🚀 **Live Demo**: [travel-route-optimizer.vercel.app](https://travel-route-optimizer.vercel.app)

---

## 🙏 Acknowledgments

- **Edsger W. Dijkstra** - For the elegant shortest path algorithm (1959)
- **FastAPI** - Created by Sebastián Ramírez
- **Python Community** - For excellent libraries and tools
- **Indian Railways** - Inspiration for realistic route data
- **Open Source Community** - For various tools and resources used

---

## 📞 Support

Found a bug? Have a suggestion?

- 🐛 **Report Issues**: [GitHub Issues](https://github.com/iaryanpal/travel-route-optimizer/issues)
- 💡 **Feature Requests**: Open an issue with the "enhancement" label
- 📧 **Email**: [raghuveeraj108@gmail.com]

---

## ⭐ Show Your Support

If this project helped you learn or build something, please consider:
- ⭐ Starring the repository
- 🍴 Forking for your own projects
- 📢 Sharing with others
- 🐛 Reporting bugs or suggesting features

---

<div align="center">

**Built with ❤️ using Python, FastAPI, and Dijkstra's Algorithm**

[Live Demo](https://travel-route-optimizer.vercel.app) • [API Docs](https://travel-route-optimizer.onrender.com/docs) • [GitHub](https://github.com/iaryanpal/travel-route-optimizer)

</div>

---

## 📈 Project Stats

- **Lines of Code**: ~2,500+
- **Test Coverage**: 92%+
- **API Endpoints**: 8
- **Cities**: 15
- **Routes**: 25
- **Tests**: 56

---

*Last Updated: November 2025*