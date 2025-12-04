# 🚀 Quick Start: Connect Your App to Queztl-Core

Get up and running with Queztl-Core in 5 minutes!

## ⚡ For the Impatient

### Step 1: Start Queztl-Core
```bash
./start.sh
```

### Step 2: Connect Your App
```javascript
const API = 'http://localhost:8000';

// Get metrics
fetch(`${API}/api/metrics`)
  .then(r => r.json())
  .then(console.log);

// Start training
fetch(`${API}/api/training/start`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    difficulty: 'medium', 
    scenario_type: 'load_balancing' 
  })
}).then(r => r.json()).then(console.log);
```

### Step 3: Real-time Updates (Optional)
```javascript
const ws = new WebSocket('ws://localhost:8000/api/ws');
ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

**That's it!** 🎉 You're connected to Queztl-Core.

---

## 📋 Detailed Setup

### Prerequisites
- Docker & Docker Compose (for local development)
- OR Python 3.11+ and Node.js 18+ (for manual setup)

### Option 1: Docker (Recommended)

1. **Clone and start:**
   ```bash
   git clone <your-repo>
   cd hive
   ./start.sh
   ```

2. **Verify it's running:**
   ```bash
   curl http://localhost:8000/api/health
   ```

   You should see:
   ```json
   {
     "service": "Queztl-Core Testing & Monitoring System",
     "status": "running",
     "version": "1.0.0"
   }
   ```

3. **View the dashboard:**
   Open http://localhost:3000

### Option 2: Manual Setup

1. **Start PostgreSQL:**
   ```bash
   createdb queztl_core
   ```

2. **Start Redis:**
   ```bash
   redis-server
   ```

3. **Start Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Start Dashboard:**
   ```bash
   cd dashboard
   npm install
   npm run dev
   ```

---

## 🔌 Integration Examples

### React/Next.js App

Create `hooks/useQueztlCore.ts`:
```typescript
import { useState, useEffect } from 'react';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function useQueztlCore() {
  const [metrics, setMetrics] = useState([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // REST API
    fetch(`${API}/api/metrics`)
      .then(r => r.json())
      .then(setMetrics);

    // WebSocket
    const ws = new WebSocket(`ws://localhost:8000/api/ws`);
    ws.onopen = () => setIsConnected(true);
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.type === 'metrics_update') {
        setMetrics(prev => [...prev, data.data]);
      }
    };
    ws.onerror = () => setIsConnected(false);
    ws.onclose = () => setIsConnected(false);

    return () => ws.close();
  }, []);

  const startTraining = async (difficulty = 'medium', scenarioType = 'load_balancing') => {
    const response = await fetch(`${API}/api/training/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ difficulty, scenario_type: scenarioType })
    });
    return await response.json();
  };

  return { metrics, isConnected, startTraining };
}
```

Use in your component:
```typescript
import { useQueztlCore } from '@/hooks/useQueztlCore';

export default function Dashboard() {
  const { metrics, isConnected, startTraining } = useQueztlCore();

  return (
    <div>
      <h1>My App + Queztl-Core</h1>
      <p>Status: {isConnected ? '🟢' : '🔴'}</p>
      <button onClick={() => startTraining()}>
        Start Training
      </button>
      <div>Metrics: {metrics.length}</div>
    </div>
  );
}
```

### Python App

```python
import requests
import asyncio
import websockets
import json

class QueztlCoreClient:
    def __init__(self, api_url='http://localhost:8000'):
        self.api_url = api_url
        self.ws_url = api_url.replace('http', 'ws')
    
    def get_metrics(self):
        """Get all metrics"""
        response = requests.get(f'{self.api_url}/api/metrics')
        return response.json()
    
    def start_training(self, difficulty='medium', scenario_type='load_balancing'):
        """Start a training session"""
        data = {
            'difficulty': difficulty,
            'scenario_type': scenario_type
        }
        response = requests.post(
            f'{self.api_url}/api/training/start',
            json=data
        )
        return response.json()
    
    def get_training_status(self):
        """Get training status"""
        response = requests.get(f'{self.api_url}/api/training/status')
        return response.json()
    
    async def listen_realtime(self, callback):
        """Listen to real-time updates via WebSocket"""
        uri = f"{self.ws_url}/api/ws"
        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                callback(data)

# Usage
client = QueztlCoreClient()

# Get metrics
metrics = client.get_metrics()
print(f"Total metrics: {len(metrics)}")

# Start training
result = client.start_training(difficulty='hard', scenario_type='fault_tolerance')
print(f"Training started: {result}")

# Listen to real-time updates
async def on_message(data):
    print(f"Received: {data}")

# asyncio.run(client.listen_realtime(on_message))
```

### Node.js/Express Backend

```javascript
const express = require('express');
const axios = require('axios');
const WebSocket = require('ws');

const app = express();
const QUEZTL_API = 'http://localhost:8000';

// Connect to Queztl-Core WebSocket
const ws = new WebSocket('ws://localhost:8000/api/ws');

ws.on('open', () => {
  console.log('Connected to Queztl-Core');
});

ws.on('message', (data) => {
  const message = JSON.parse(data);
  console.log('Received from Queztl-Core:', message);
  // Do something with the data
});

// Proxy endpoint to get metrics
app.get('/metrics', async (req, res) => {
  try {
    const response = await axios.get(`${QUEZTL_API}/api/metrics`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Start training from your app
app.post('/start-training', async (req, res) => {
  try {
    const response = await axios.post(`${QUEZTL_API}/api/training/start`, {
      difficulty: req.body.difficulty || 'medium',
      scenario_type: req.body.scenario_type || 'load_balancing'
    });
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3001, () => {
  console.log('Your app running on port 3001');
  console.log('Connected to Queztl-Core at', QUEZTL_API);
});
```

### Flutter/Dart Mobile App

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';

class QueztlCoreService {
  final String apiUrl;
  final String wsUrl;
  
  QueztlCoreService({
    this.apiUrl = 'http://localhost:8000',
    this.wsUrl = 'ws://localhost:8000',
  });

  Future<List<dynamic>> getMetrics() async {
    final response = await http.get(Uri.parse('$apiUrl/api/metrics'));
    if (response.statusCode == 200) {
      return json.decode(response.body);
    }
    throw Exception('Failed to load metrics');
  }

  Future<Map<String, dynamic>> startTraining({
    String difficulty = 'medium',
    String scenarioType = 'load_balancing',
  }) async {
    final response = await http.post(
      Uri.parse('$apiUrl/api/training/start'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'difficulty': difficulty,
        'scenario_type': scenarioType,
      }),
    );
    return json.decode(response.body);
  }

  WebSocketChannel connectRealtime() {
    return WebSocketChannel.connect(
      Uri.parse('$wsUrl/api/ws'),
    );
  }
}

// Usage in your widget
final queztl = QueztlCoreService();

// Get metrics
final metrics = await queztl.getMetrics();

// Start training
final result = await queztl.startTraining(
  difficulty: 'hard',
  scenarioType: 'concurrent_requests',
);

// Real-time updates
final channel = queztl.connectRealtime();
channel.stream.listen((message) {
  final data = json.decode(message);
  print('Received: $data');
});
```

---

## 🌐 Environment Variables

Add to your `.env` file:

```bash
# For local development
QUEZTL_API_URL=http://localhost:8000
QUEZTL_WS_URL=ws://localhost:8000

# For production (after deploying backend)
# QUEZTL_API_URL=https://your-backend-url.com
# QUEZTL_WS_URL=wss://your-backend-url.com
```

---

## 📡 Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/metrics` | GET | Get all metrics |
| `/api/metrics/recent?limit=10` | GET | Get recent metrics |
| `/api/training/start` | POST | Start training |
| `/api/training/status` | GET | Get status |
| `/api/training/stop` | POST | Stop training |
| `/api/scenarios` | GET | Get scenarios |
| `/api/ws` | WebSocket | Real-time updates |
| `/docs` | GET | API documentation |

---

## 🎯 Scenario Types

Choose from 8 training scenarios:
- `load_balancing` - Test load distribution
- `resource_allocation` - Optimize resources
- `fault_tolerance` - Handle failures
- `data_processing` - Process data efficiently
- `concurrent_requests` - Handle multiple requests
- `network_latency` - Deal with delays
- `memory_optimization` - Optimize memory
- `cache_efficiency` - Improve caching

---

## 🐛 Troubleshooting

### Connection Refused
```bash
# Check if Queztl-Core is running
docker ps

# Restart if needed
./start.sh
```

### CORS Errors
Queztl-Core accepts connections from ANY origin (`*`), so this shouldn't happen. If it does:
1. Check browser console for details
2. Verify the API URL is correct
3. Ensure backend is running

### WebSocket Issues
- Use `ws://` for HTTP and `wss://` for HTTPS
- Check firewall settings
- Verify port 8000 is accessible

---

## 📚 More Resources

- **Full API Docs**: http://localhost:8000/docs
- **Connection Guide**: See `API_CONNECTION_GUIDE.md`
- **Dashboard**: http://localhost:3000
- **Live Demo**: https://senzeni.netlify.app

---

## 🎉 You're Ready!

Your app is now connected to Queztl-Core. Start monitoring performance, running training scenarios, and optimizing your systems!

Need help? Open an issue or check the documentation.
