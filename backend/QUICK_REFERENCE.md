# 🦅 Queztl-Core - Quick Reference Card

## 🚀 Start & Stop
```bash
./start.sh              # Start all services
docker-compose down     # Stop all services
docker-compose restart  # Restart services
```

## 🌐 URLs
- **Dashboard**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Production**: https://senzeni.netlify.app

## 🔌 Quick Connect

### JavaScript/TypeScript
```javascript
const API = 'http://localhost:8000';

// Get metrics
fetch(`${API}/api/metrics`).then(r => r.json()).then(console.log);

// Start training
fetch(`${API}/api/training/start`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ difficulty: 'medium', scenario_type: 'load_balancing' })
}).then(r => r.json()).then(console.log);

// WebSocket
const ws = new WebSocket('ws://localhost:8000/api/ws');
ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

### Python
```python
import requests

API = 'http://localhost:8000'

# Get metrics
metrics = requests.get(f'{API}/api/metrics').json()

# Start training
result = requests.post(f'{API}/api/training/start', json={
    'difficulty': 'medium',
    'scenario_type': 'load_balancing'
}).json()
```

### cURL
```bash
# Health check
curl http://localhost:8000/api/health

# Get metrics
curl http://localhost:8000/api/metrics

# Start training
curl -X POST http://localhost:8000/api/training/start \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "medium", "scenario_type": "load_balancing"}'
```

## 📡 Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/metrics` | GET | All metrics |
| `/api/metrics/recent?limit=10` | GET | Recent metrics |
| `/api/training/start` | POST | Start training |
| `/api/training/status` | GET | Training status |
| `/api/training/stop` | POST | Stop training |
| `/api/scenarios` | GET | Available scenarios |
| `/api/ws` | WS | Real-time updates |

## 🎯 Scenario Types
- `load_balancing` - Test load distribution
- `resource_allocation` - Optimize resources
- `fault_tolerance` - Handle failures
- `data_processing` - Process data efficiently
- `concurrent_requests` - Handle concurrency
- `network_latency` - Network delays
- `memory_optimization` - Memory usage
- `cache_efficiency` - Caching strategies

## 📊 Difficulty Levels
- `easy` - Basic scenarios
- `medium` - Moderate complexity
- `hard` - Advanced challenges
- `expert` - Maximum difficulty

## 🐳 Docker Commands
```bash
docker ps                          # List running containers
docker-compose logs -f backend     # Follow backend logs
docker-compose logs -f dashboard   # Follow dashboard logs
docker exec -it hive-db-1 psql -U postgres -d queztl_core  # Access DB
docker exec -it hive-redis-1 redis-cli  # Access Redis
```

## 🔍 Debug
```bash
# Check service health
curl http://localhost:8000/api/health

# View backend logs
docker logs hive-backend-1

# View dashboard logs
docker logs hive-dashboard-1

# Restart a service
docker restart hive-backend-1
```

## 📚 Documentation
- `README.md` - Main documentation
- `CONNECT_YOUR_APP.md` - Integration guide
- `API_CONNECTION_GUIDE.md` - API reference
- `REBRANDING_COMPLETE.md` - What changed
- `ARCHITECTURE.md` - System architecture
- `TESTING.md` - Testing guide

## 🔐 Security
**Development:** CORS allows all origins (`*`)  
**Production:** Update CORS to specific domains

## 🆘 Troubleshooting

### Connection Refused
```bash
docker-compose up -d
```

### CORS Error
Already configured to allow all origins

### Database Error
```bash
docker exec -it hive-db-1 psql -U postgres -c "CREATE DATABASE queztl_core;"
docker restart hive-backend-1
```

### Port Already in Use
```bash
# Change ports in docker-compose.yml
# Or kill the process using the port
lsof -ti:8000 | xargs kill -9
```

## ⚡ One-Liners

```bash
# Quick health check
curl http://localhost:8000/api/health | jq

# Count metrics
curl -s http://localhost:8000/api/metrics | jq 'length'

# Start training session
curl -X POST http://localhost:8000/api/training/start \
  -H "Content-Type: application/json" \
  -d '{"difficulty":"hard","scenario_type":"fault_tolerance"}' | jq

# Get training status
curl http://localhost:8000/api/training/status | jq

# View recent problems
curl http://localhost:8000/api/scenarios | jq
```

## 🎨 Environment Variables
```bash
# .env file
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/queztl_core
REDIS_URL=redis://localhost:6379
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

---

**🦅 Queztl-Core** - Universal Testing & Monitoring System  
Connect any app, any language, any platform!
