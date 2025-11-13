// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const routeForm = document.getElementById('routeForm');
const originSelect = document.getElementById('origin');
const destinationSelect = document.getElementById('destination');
const findRouteBtn = document.getElementById('findRouteBtn');
const compareBtn = document.getElementById('compareBtn');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const comparison = document.getElementById('comparison');
const error = document.getElementById('error');

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    loadCities();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    routeForm.addEventListener('submit', handleFindRoute);
    compareBtn.addEventListener('click', handleCompare);
}

// Load cities from API
async function loadCities() {
    try {
        const response = await fetch(`${API_BASE_URL}/cities`);
        
        if (!response.ok) {
            throw new Error('Failed to load cities');
        }
        
        const cities = await response.json();
        populateCitySelects(cities);
    } catch (err) {
        showError('Failed to load cities. Make sure the API server is running.');
        console.error('Error loading cities:', err);
    }
}

// Populate city select dropdowns
function populateCitySelects(cities) {
    const cityOptions = cities.map(city => 
        `<option value="${city.name}">${city.name}</option>`
    ).join('');
    
    originSelect.innerHTML = '<option value="">Select starting city...</option>' + cityOptions;
    destinationSelect.innerHTML = '<option value="">Select destination city...</option>' + cityOptions;
}

// Handle find route form submission
async function handleFindRoute(e) {
    e.preventDefault();
    
    const origin = originSelect.value;
    const destination = destinationSelect.value;
    const optimizeBy = document.querySelector('input[name="optimize"]:checked').value;
    
    if (!origin || !destination) {
        showError('Please select both origin and destination cities');
        return;
    }
    
    if (origin === destination) {
        showError('Origin and destination cannot be the same city');
        return;
    }
    
    hideAllResults();
    showLoading();
    
    try {
        const route = await findPath(origin, destination, optimizeBy);
        hideLoading();
        displayResults(route);
    } catch (err) {
        hideLoading();
        showError(err.message);
    }
}

// Handle compare button click
async function handleCompare() {
    const origin = originSelect.value;
    const destination = destinationSelect.value;
    
    if (!origin || !destination) {
        showError('Please select both origin and destination cities');
        return;
    }
    
    if (origin === destination) {
        showError('Origin and destination cannot be the same city');
        return;
    }
    
    hideAllResults();
    showLoading();
    
    try {
        const [distanceRoute, costRoute] = await Promise.all([
            findPath(origin, destination, 'distance'),
            findPath(origin, destination, 'cost')
        ]);
        
        hideLoading();
        displayComparison(distanceRoute, costRoute);
    } catch (err) {
        hideLoading();
        showError(err.message);
    }
}

// Find path via API
async function findPath(origin, destination, optimizeBy) {
    const response = await fetch(`${API_BASE_URL}/find-path`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            origin: origin,
            destination: destination,
            optimize_by: optimizeBy
        })
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to find route');
    }
    
    return await response.json();
}

// Display single route results
function displayResults(route) {
    if (!route.valid) {
        showError('No path found between the selected cities');
        return;
    }
    
    // Update summary
    document.getElementById('totalDistance').textContent = `${route.total_distance.toFixed(2)} km`;
    document.getElementById('totalCost').textContent = `₹${route.total_cost.toFixed(2)}`;
    document.getElementById('totalStops').textContent = route.stops;
    
    // Display path
    displayPath(route.path);
    
    // Display segments
    displaySegments(route.segments);
    
    // Show results card
    results.classList.remove('hidden');
}

// Display path with visual nodes
function displayPath(path) {
    const pathDisplay = document.getElementById('pathDisplay');
    pathDisplay.innerHTML = '';
    
    path.forEach((city, index) => {
        // Add city node
        const cityNode = document.createElement('div');
        cityNode.className = 'city-node';
        
        if (index === 0) {
            cityNode.classList.add('start');
        } else if (index === path.length - 1) {
            cityNode.classList.add('end');
        }
        
        cityNode.textContent = city;
        pathDisplay.appendChild(cityNode);
        
        // Add arrow between cities
        if (index < path.length - 1) {
            const arrow = document.createElement('i');
            arrow.className = 'fas fa-arrow-right path-arrow';
            pathDisplay.appendChild(arrow);
        }
    });
}

// Display route segments
function displaySegments(segments) {
    const segmentsDisplay = document.getElementById('segmentsDisplay');
    segmentsDisplay.innerHTML = '';
    
    segments.forEach(segment => {
        const segmentDiv = document.createElement('div');
        segmentDiv.className = 'segment';
        
        segmentDiv.innerHTML = `
            <div class="segment-header">
                <span class="segment-step">Step ${segment.step}</span>
                <span class="segment-route">
                    <i class="fas fa-map-marker-alt" style="color: #2563eb;"></i>
                    ${segment.from_city} 
                    <i class="fas fa-arrow-right"></i> 
                    ${segment.to_city}
                </span>
            </div>
            <div class="segment-details">
                <span><i class="fas fa-road"></i> ${segment.distance.toFixed(2)} km</span>
                <span><i class="fas fa-rupee-sign"></i> ₹${segment.cost.toFixed(2)}</span>
            </div>
        `;
        
        segmentsDisplay.appendChild(segmentDiv);
    });
}

// Display comparison results
function displayComparison(distanceRoute, costRoute) {
    const distanceResults = document.getElementById('distanceResults');
    const costResults = document.getElementById('costResults');
    
    // Distance optimized results
    distanceResults.innerHTML = `
        <div class="comparison-summary">
            <div class="comparison-item">
                <span class="comparison-label">Total Distance:</span>
                <span class="comparison-value">${distanceRoute.total_distance.toFixed(2)} km</span>
            </div>
            <div class="comparison-item">
                <span class="comparison-label">Total Cost:</span>
                <span class="comparison-value">₹${distanceRoute.total_cost.toFixed(2)}</span>
            </div>
            <div class="comparison-item">
                <span class="comparison-label">Stops:</span>
                <span class="comparison-value">${distanceRoute.stops}</span>
            </div>
        </div>
        <div class="comparison-path">
            <strong>Route:</strong><br>
            ${distanceRoute.path.join(' → ')}
        </div>
    `;
    
    // Cost optimized results
    costResults.innerHTML = `
        <div class="comparison-summary">
            <div class="comparison-item">
                <span class="comparison-label">Total Distance:</span>
                <span class="comparison-value" style="color: #10b981;">${costRoute.total_distance.toFixed(2)} km</span>
            </div>
            <div class="comparison-item">
                <span class="comparison-label">Total Cost:</span>
                <span class="comparison-value" style="color: #10b981;">₹${costRoute.total_cost.toFixed(2)}</span>
            </div>
            <div class="comparison-item">
                <span class="comparison-label">Stops:</span>
                <span class="comparison-value" style="color: #10b981;">${costRoute.stops}</span>
            </div>
        </div>
        <div class="comparison-path">
            <strong>Route:</strong><br>
            ${costRoute.path.join(' → ')}
        </div>
    `;
    
    // Calculate savings
    const distanceDiff = costRoute.total_distance - distanceRoute.total_distance;
    const costDiff = distanceRoute.total_cost - costRoute.total_cost;
    
    // Add comparison insights
    const insights = document.createElement('div');
    insights.className = 'card-body';
    insights.style.marginTop = '20px';
    insights.style.background = '#f0f9ff';
    insights.style.borderRadius = '8px';
    insights.style.padding = '20px';
    
    insights.innerHTML = `
        <h3 style="margin-bottom: 16px;"><i class="fas fa-lightbulb"></i> Insights</h3>
        <p style="line-height: 1.8; color: #1f2937;">
            ${distanceDiff > 0 ? 
                `<i class="fas fa-check-circle" style="color: #10b981;"></i> 
                The <strong>shortest distance</strong> route saves <strong>${distanceDiff.toFixed(2)} km</strong>.` :
                `<i class="fas fa-info-circle" style="color: #2563eb;"></i> 
                Both routes have similar distances.`
            }
            <br>
            ${costDiff > 0 ? 
                `<i class="fas fa-check-circle" style="color: #10b981;"></i> 
                The <strong>cheapest</strong> route saves <strong>₹${costDiff.toFixed(2)}</strong>.` :
                `<i class="fas fa-info-circle" style="color: #2563eb;"></i> 
                Both routes have similar costs.`
            }
        </p>
    `;
    
    comparison.querySelector('.card-body').appendChild(insights);
    
    // Show comparison card
    comparison.classList.remove('hidden');
}

// Show loading spinner
function showLoading() {
    loading.classList.remove('hidden');
}

// Hide loading spinner
function hideLoading() {
    loading.classList.add('hidden');
}

// Show error message
function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    error.classList.remove('hidden');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        error.classList.add('hidden');
    }, 5000);
}

// Hide all result sections
function hideAllResults() {
    results.classList.add('hidden');
    comparison.classList.add('hidden');
    error.classList.add('hidden');
}