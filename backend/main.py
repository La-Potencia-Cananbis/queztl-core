"""
Main FastAPI application for Queztl-Core Testing & Monitoring System
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from typing import List
import json
from datetime import datetime

from database import init_db, get_db
from models import PerformanceMetric, TestScenario
from problem_generator import ProblemGenerator
from training_engine import TrainingEngine
from power_meter import PowerMeter, CreativeTrainer

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()
problem_generator = ProblemGenerator()
training_engine = TrainingEngine()
power_meter = PowerMeter()
creative_trainer = CreativeTrainer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    print("✅ Database initialized")
    yield
    # Shutdown
    print("👋 Shutting down...")

app = FastAPI(
    title="Queztl-Core Testing & Monitoring System",
    description="Real-time performance monitoring and dynamic training system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - Allow connections from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for maximum compatibility
    allow_credentials=False,  # Set to False when using wildcard origins
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "service": "Queztl-Core Testing & Monitoring System",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/metrics/latest")
async def get_latest_metrics():
    """Get the latest performance metrics"""
    metrics = await training_engine.get_latest_metrics(limit=100)
    return {"metrics": metrics}

@app.get("/api/metrics/summary")
async def get_metrics_summary():
    """Get aggregated metrics summary"""
    summary = await training_engine.get_metrics_summary()
    return summary

@app.post("/api/scenarios/generate")
async def generate_scenario():
    """Generate a new training scenario"""
    scenario = await problem_generator.generate_scenario()
    return scenario

@app.post("/api/scenarios/{scenario_id}/execute")
async def execute_scenario(scenario_id: str):
    """Execute a training scenario and collect metrics"""
    result = await training_engine.execute_scenario(scenario_id)
    
    # Broadcast results to all connected clients
    await manager.broadcast({
        "type": "scenario_completed",
        "data": result
    })
    
    return result

@app.get("/api/training/status")
async def get_training_status():
    """Get current training status and progress"""
    status = await training_engine.get_status()
    return status

@app.post("/api/training/start")
async def start_training():
    """Start continuous training with dynamic problems"""
    asyncio.create_task(training_engine.start_continuous_training(manager))
    return {"status": "training_started"}

@app.post("/api/training/stop")
async def stop_training():
    """Stop continuous training"""
    await training_engine.stop_training()
    return {"status": "training_stopped"}

@app.websocket("/ws/metrics")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics streaming"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and receive any client messages
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/problems/recent")
async def get_recent_problems():
    """Get recently generated problems"""
    problems = await problem_generator.get_recent_problems(limit=20)
    return {"problems": problems}

@app.get("/api/analytics/performance")
async def get_performance_analytics():
    """Get detailed performance analytics"""
    analytics = await training_engine.get_performance_analytics()
    return analytics

# Power Measurement & Benchmarking Endpoints
@app.get("/api/power/measure")
async def measure_system_power():
    """Measure current system power and capabilities"""
    measurement = await power_meter.measure_power()
    
    # Broadcast to connected clients
    await manager.broadcast({
        "type": "power_measurement",
        "data": measurement
    })
    
    return measurement

@app.post("/api/power/stress-test")
async def run_stress_test(duration: int = 10, intensity: str = 'medium'):
    """
    Run a stress test to measure maximum capacity
    
    - duration: Test duration in seconds (default: 10)
    - intensity: light, medium, heavy, or extreme (default: medium)
    """
    result = await power_meter.run_stress_test(duration, intensity)
    
    await manager.broadcast({
        "type": "stress_test_complete",
        "data": result
    })
    
    return result

@app.post("/api/power/benchmark")
async def run_benchmark_suite():
    """Run comprehensive benchmark suite"""
    results = await power_meter.run_benchmark_suite()
    
    await manager.broadcast({
        "type": "benchmark_complete",
        "data": results
    })
    
    return results

@app.get("/api/power/report")
async def get_power_report():
    """Get comprehensive power report"""
    report = power_meter.get_power_report()
    return report

# Creative Training Scenarios
@app.post("/api/training/creative")
async def start_creative_training(mode: str = None):
    """
    Start a creative training scenario
    
    Modes: chaos_monkey, resource_starving, cascade_failure, 
           traffic_spike, adaptive_adversary
    """
    scenario = await creative_trainer.generate_creative_scenario(mode)
    
    await manager.broadcast({
        "type": "creative_scenario_started",
        "data": scenario
    })
    
    return scenario

@app.get("/api/training/creative/modes")
async def get_creative_modes():
    """Get available creative training modes"""
    return {
        "modes": creative_trainer.creativity_modes,
        "descriptions": {
            "chaos_monkey": "Random failures and disruptions",
            "resource_starving": "Limited resources challenge",
            "cascade_failure": "One failure triggers others",
            "traffic_spike": "Sudden massive traffic increase",
            "data_corruption": "Handle corrupted or invalid data",
            "time_pressure": "Critical time-constrained scenarios",
            "multi_attack": "Multiple simultaneous challenges",
            "adaptive_adversary": "Intelligent opponent that learns"
        }
    }

@app.get("/api/power/leaderboard")
async def get_power_leaderboard():
    """Get power measurement leaderboard"""
    if not power_meter.stress_test_results:
        return {"message": "No stress tests completed yet"}
    
    # Sort by operations per second
    sorted_results = sorted(
        power_meter.stress_test_results.items(),
        key=lambda x: x[1].get('operations_per_second', 0),
        reverse=True
    )
    
    leaderboard = []
    for timestamp, result in sorted_results[:10]:  # Top 10
        leaderboard.append({
            'timestamp': timestamp,
            'ops_per_second': result.get('operations_per_second', 0),
            'grade': result.get('grade', 'N/A'),
            'intensity': result.get('intensity', 'unknown'),
            'error_rate': result.get('error_rate', 0)
        })
    
    return {
        "leaderboard": leaderboard,
        "total_tests": len(power_meter.stress_test_results)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
