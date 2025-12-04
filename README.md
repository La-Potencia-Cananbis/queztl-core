# 🦅 Queztl-Core Testing & Monitoring System

A comprehensive real-time testing and monitoring system with dynamic problem generation, adaptive learning, and performance analytics. Connect any app for intelligent performance monitoring and optimization.

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start)
[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://senzeni.netlify.app)

**🌐 Live Demo:** [https://senzeni.netlify.app](https://senzeni.netlify.app)

## 🔥 Quick Connect

Connect any application in seconds:

```javascript
// Any JavaScript/TypeScript app
fetch('http://localhost:8000/api/metrics')
  .then(r => r.json())
  .then(console.log);
```

```python
# Any Python app
import requests
metrics = requests.get('http://localhost:8000/api/metrics').json()
```

**See [CONNECT_YOUR_APP.md](CONNECT_YOUR_APP.md) for complete integration guides** (React, Python, Node.js, Flutter, and more!)

## 💪 Power Testing & Training

**NEW!** Flex and measure Queztl-Core's capabilities:

```bash
# Run the power demo
./demo-power.sh

# Or try directly:
curl -X POST "http://localhost:8000/api/power/stress-test?intensity=medium&duration=15"
```

**Features:**
- 🔥 **Stress Testing** - Light, Medium, Heavy, Extreme (up to 10,000+ ops/sec)
- 📊 **Benchmarking** - Comprehensive performance analysis
- 🧠 **Creative Training** - 8 unique scenarios (Chaos Monkey, Traffic Spikes, Adaptive Adversary, etc.)
- 🏆 **Grading System** - F to S rank based on performance
- 📈 **Real-time Metrics** - CPU, Memory, Disk, Network monitoring

**See [POWER_TRAINING_GUIDE.md](POWER_TRAINING_GUIDE.md) for complete training guide!**

## 🌟 Features

### Performance Dashboard
- **Real-time Metrics Visualization** - Live charts showing response times, throughput, and resource usage
- **WebSocket Integration** - Real-time updates without page refresh
- **Status Cards** - Quick overview of key performance indicators
- **Dark Mode Support** - Modern UI with light/dark theme

### Dynamic Problem Generator
- **Multiple Scenario Types** - Load balancing, resource allocation, fault tolerance, data processing, and more
- **Adaptive Difficulty** - Automatically adjusts based on system performance
- **Realistic Workloads** - Simulates real-world conditions with varying complexity
- **8 Scenario Categories**:
  - Load Balancing
  - Resource Allocation
  - Fault Tolerance
  - Data Processing
  - Concurrent Requests
  - Network Latency
  - Memory Optimization
  - Cache Efficiency

### Training Engine
- **Continuous Training Mode** - Automatically generates and executes scenarios
- **Performance Analytics** - Detailed statistics and recommendations
- **Adaptive Learning** - Difficulty increases with success rate
- **Metrics Collection** - Comprehensive data on all test runs

### Universal Connectivity
- **CORS Enabled for All Origins** - Connect from any domain, any app
- **REST API** - Standard HTTP endpoints for easy integration
- **WebSocket Support** - Real-time updates via WebSocket
- **Multiple Language Support** - Works with JavaScript, Python, Go, Rust, and more
- **No Authentication Required** - Quick setup for development (can be added for production)

### Technology Stack
- **Frontend**: Next.js 14, React, TypeScript, Recharts, TailwindCSS
- **Backend**: Python FastAPI, WebSocket, AsyncIO
- **Database**: PostgreSQL for metrics storage
- **Cache**: Redis for high-performance data access
- **Deployment**: Docker Compose for easy setup

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd hive
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Access the applications**
   - Dashboard: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Local Development

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start PostgreSQL and Redis** (using Docker)
   ```bash
   docker-compose up -d db redis
   ```

5. **Run the backend**
   ```bash
   python -m uvicorn main:app --reload
   ```

#### Dashboard Setup

1. **Navigate to dashboard directory**
   ```bash
   cd dashboard
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```

## 📊 Usage

### Starting Training

1. Open the dashboard at http://localhost:3000
2. Click "Start Continuous Training" to begin automatic scenario generation
3. Watch real-time metrics update on the dashboard
4. View recent problems and their difficulty levels

### Manual Scenario Execution

1. Click "Generate & Execute Scenario" to run a single test
2. View results in the metrics chart
3. Check the training progress panel for statistics

### Monitoring Performance

The dashboard displays:
- **Total Scenarios** - Number of tests completed
- **Average Response Time** - System responsiveness
- **Success Rate** - Percentage of successful completions
- **Total Errors** - Error count across all scenarios

### API Endpoints

#### Health & Status
- `GET /` - Service information
- `GET /api/health` - Health check
- `GET /api/training/status` - Current training status

#### Metrics
- `GET /api/metrics/latest` - Recent performance metrics
- `GET /api/metrics/summary` - Aggregated statistics
- `GET /api/analytics/performance` - Detailed analytics

#### Training
- `POST /api/training/start` - Start continuous training
- `POST /api/training/stop` - Stop training
- `POST /api/scenarios/generate` - Generate new scenario
- `POST /api/scenarios/{id}/execute` - Execute specific scenario

#### WebSocket
- `WS /ws/metrics` - Real-time metrics stream

## 🏗️ Architecture

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Next.js   │ ←────→ │   FastAPI   │ ←────→ │ PostgreSQL  │
│  Dashboard  │ WebSocket│   Backend   │         │  Database   │
└─────────────┘         └─────────────┘         └─────────────┘
                              │
                              ↓
                        ┌─────────────┐
                        │    Redis    │
                        │    Cache    │
                        └─────────────┘
```

### Backend Components

- **`main.py`** - FastAPI application and endpoints
- **`database.py`** - Database models and connection
- **`models.py`** - Pydantic models for validation
- **`problem_generator.py`** - Dynamic scenario generation
- **`training_engine.py`** - Training logic and metrics collection

### Frontend Components

- **`page.tsx`** - Main dashboard page
- **`MetricsChart.tsx`** - Real-time chart component
- **`StatusCard.tsx`** - Metric display cards
- **`TrainingControls.tsx`** - Training control buttons
- **`RecentProblems.tsx`** - Problem history display

## 🎯 Scenario Types Explained

### Load Balancing
Tests the system's ability to distribute requests across multiple nodes efficiently.

### Resource Allocation
Evaluates how well the system allocates limited resources across competing tasks.

### Fault Tolerance
Tests system resilience when nodes fail or become unavailable.

### Data Processing
Measures performance when processing large volumes of data in parallel.

### Concurrent Requests
Tests handling of multiple simultaneous connections and requests.

### Network Latency
Evaluates performance under various network conditions with delays and jitter.

### Memory Optimization
Tests memory management and garbage collection strategies.

### Cache Efficiency
Measures cache hit rates and effectiveness of caching strategies.

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/hive_monitoring
REDIS_URL=redis://localhost:6379
API_HOST=0.0.0.0
API_PORT=8000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Difficulty Levels

The system automatically adjusts difficulty based on performance:
- **Easy** - Basic scenarios, low resource requirements
- **Medium** - Moderate complexity, standard workloads
- **Hard** - High complexity, increased stress
- **Extreme** - Maximum difficulty, edge cases

## 📈 Metrics Collected

- **Response Time** - Time to complete requests (ms)
- **Throughput** - Requests processed per second
- **Error Rate** - Percentage of failed operations
- **CPU Usage** - Processor utilization (%)
- **Memory Usage** - RAM utilization (%)
- **Success Rate** - Overall success percentage

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd dashboard
npm test
```

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild containers
docker-compose up -d --build

# View service status
docker-compose ps
```

## 🛠️ Development

### Adding New Scenario Types

1. Edit `backend/problem_generator.py`
2. Add scenario type to `scenario_types` list
3. Implement parameter generation in `_generate_parameters()`
4. Add description template in `_generate_description()`

### Customizing Metrics

1. Edit `backend/models.py` to add new metric types
2. Update `training_engine.py` to collect new metrics
3. Modify dashboard components to display new metrics

## 📝 API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - feel free to use this project for your own purposes.

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check if database is running
docker-compose ps db

# View database logs
docker-compose logs db
```

### Frontend Not Connecting to Backend
- Ensure `NEXT_PUBLIC_API_URL` is set correctly
- Check CORS settings in `backend/main.py`
- Verify backend is running on port 8000

### WebSocket Connection Failed
- Check browser console for errors
- Ensure WebSocket port is not blocked by firewall
- Verify backend WebSocket endpoint is accessible

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the API documentation
- Review the logs: `docker-compose logs -f`

## 🎉 Acknowledgments

Built with modern web technologies to provide a comprehensive testing and monitoring solution for distributed systems.

---

**Happy Testing! 🐝**
