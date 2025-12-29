# 🔌 Queztl-Core API Connection Guide

Connect any application to Queztl-Core for real-time performance monitoring and adaptive learning.

## 🌐 API Endpoints

### Base URL (Production)
```
https://your-backend-url.com
```

### Base URL (Local Development)
```
http://localhost:8000
```

## 📡 Available Endpoints

### 1. Health Check
```http
GET /api/health
```
Returns system status.

### 2. Get Metrics
```http
GET /api/metrics
```
Returns all performance metrics.

### 3. Get Recent Metrics
```http
GET /api/metrics/recent?limit=10
```
Returns recent metrics (default: 10).

### 4. Start Training Session
```http
POST /api/training/start
Content-Type: application/json

{
    "difficulty": "medium",
    "scenario_type": "load_balancing"
}
```

### 5. Get Training Status
```http
GET /api/training/status
```
Returns current training session status.

### 6. Stop Training
```http
POST /api/training/stop
```
Stops the current training session.

### 7. WebSocket Connection (Real-time Updates)
```javascript
const ws = new WebSocket('ws://localhost:8000/api/ws');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

## 🔐 CORS Configuration

Queztl-Core accepts connections from **ANY origin** (`*`), making it easy to connect from:
- Web applications
- Mobile apps
- Desktop applications
- IoT devices
- Microservices

## 📦 Quick Integration Examples

### JavaScript/TypeScript (Fetch API)
```javascript
const QUEZTL_API = 'http://localhost:8000';

// Get metrics
async function getMetrics() {
    const response = await fetch(`${QUEZTL_API}/api/metrics`);
    return await response.json();
}

// Start training
async function startTraining(difficulty = 'medium', scenarioType = 'load_balancing') {
    const response = await fetch(`${QUEZTL_API}/api/training/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ difficulty, scenario_type: scenarioType })
    });
    return await response.json();
}

// WebSocket connection
const ws = new WebSocket(`ws://localhost:8000/api/ws`);
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Real-time update:', data);
};
```

### Python (requests)
```python
import requests
import json

QUEZTL_API = 'http://localhost:8000'

# Get metrics
response = requests.get(f'{QUEZTL_API}/api/metrics')
metrics = response.json()

# Start training
training_data = {
    'difficulty': 'medium',
    'scenario_type': 'load_balancing'
}
response = requests.post(
    f'{QUEZTL_API}/api/training/start',
    json=training_data
)
result = response.json()
```

### Python (WebSocket)
```python
import asyncio
import websockets
import json

async def connect_to_queztl():
    uri = "ws://localhost:8000/api/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Received: {data}")

asyncio.run(connect_to_queztl())
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

# Get training status
curl http://localhost:8000/api/training/status
```

### React/Next.js Example
```typescript
import { useEffect, useState } from 'react';

const QUEZTL_API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function QueztlDashboard() {
    const [metrics, setMetrics] = useState([]);
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        // REST API: Fetch metrics
        fetch(`${QUEZTL_API}/api/metrics`)
            .then(res => res.json())
            .then(data => setMetrics(data));

        // WebSocket: Real-time updates
        const ws = new WebSocket(`ws://localhost:8000/api/ws`);
        
        ws.onopen = () => setIsConnected(true);
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'metrics_update') {
                setMetrics(prev => [...prev, data.data]);
            }
        };
        ws.onerror = () => setIsConnected(false);
        ws.onclose = () => setIsConnected(false);

        return () => ws.close();
    }, []);

    const startTraining = async () => {
        const response = await fetch(`${QUEZTL_API}/api/training/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                difficulty: 'medium',
                scenario_type: 'load_balancing'
            })
        });
        const result = await response.json();
        console.log('Training started:', result);
    };

    return (
        <div>
            <h1>Queztl-Core Dashboard</h1>
            <p>Status: {isConnected ? '🟢 Connected' : '🔴 Disconnected'}</p>
            <button onClick={startTraining}>Start Training</button>
            <div>
                {metrics.map((metric, i) => (
                    <div key={i}>{JSON.stringify(metric)}</div>
                ))}
            </div>
        </div>
    );
}
```

## 🎯 Scenario Types

Choose from 8 different training scenarios:
- `load_balancing` - Test load distribution
- `resource_allocation` - Optimize resource usage
- `fault_tolerance` - Handle failures gracefully
- `data_processing` - Process data efficiently
- `concurrent_requests` - Handle multiple requests
- `network_latency` - Deal with network delays
- `memory_optimization` - Optimize memory usage
- `cache_efficiency` - Improve caching strategies

## 📊 Difficulty Levels

- `easy` - Basic scenarios
- `medium` - Moderate complexity
- `hard` - Advanced challenges
- `expert` - Maximum difficulty

## 🔄 Real-time Event Types

WebSocket messages include:
- `metrics_update` - New performance metrics
- `training_started` - Training session began
- `training_stopped` - Training session ended
- `scenario_completed` - A scenario finished
- `system_status` - System health update

## 🚀 Environment Variables

For your application, set:
```bash
# .env file
QUEZTL_API_URL=http://localhost:8000  # or production URL
QUEZTL_WS_URL=ws://localhost:8000
```

## 📱 Mobile Apps (React Native)
```javascript
import { useState, useEffect } from 'react';

const QUEZTL_API = 'http://your-backend-url.com';

export function useQueztlCore() {
    const [metrics, setMetrics] = useState([]);

    const getMetrics = async () => {
        const response = await fetch(`${QUEZTL_API}/api/metrics`);
        const data = await response.json();
        setMetrics(data);
    };

    const startTraining = async (difficulty, scenarioType) => {
        const response = await fetch(`${QUEZTL_API}/api/training/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                difficulty,
                scenario_type: scenarioType
            })
        });
        return await response.json();
    };

    return { metrics, getMetrics, startTraining };
}
```

## 🛡️ Security Notes

- The API currently accepts all origins (`*`) for development ease
- For production, consider implementing API keys or JWT authentication
- Rate limiting can be added via middleware
- For sensitive deployments, update CORS to specific origins

## 📚 Response Format

All responses are JSON:
```json
{
    "success": true,
    "data": {},
    "message": "Operation completed"
}
```

## 🐛 Troubleshooting

### Connection Refused
- Ensure backend is running: `docker-compose up` or `./start.sh`
- Check firewall settings
- Verify correct port (8000)

### WebSocket Connection Failed
- Use `ws://` for HTTP and `wss://` for HTTPS
- Check browser console for errors
- Verify WebSocket support in your environment

### CORS Errors
- Should not occur as we allow all origins
- If issues persist, check browser console for specifics

## 📖 Complete API Documentation

Visit `/docs` on your backend URL for interactive API documentation (Swagger UI):
```
http://localhost:8000/docs
```

---

**Need help?** Check the main README or open an issue on GitHub.
