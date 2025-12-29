#!/usr/bin/env python3
"""
🦅 QuetzalCore Web-Based Infrastructure Monitor
Real-time OS utilization dashboard - like Activity Monitor in a web browser!
"""

import asyncio
import time
import psutil
import json
from datetime import datetime
from typing import Dict, List
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import os


class MetricsCollector:
    """Collect real-time metrics from OS"""
    
    def __init__(self):
        self.history = []
        self.current_metrics = None
        
    def collect(self) -> Dict:
        """Collect current metrics"""
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get top processes
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
                if info['cpu_percent'] and info['cpu_percent'] > 0.1:
                    processes.append({
                        'pid': info['pid'],
                        'name': info['name'][:30],
                        'cpu': round(info['cpu_percent'], 1),
                        'memory': round(info['memory_percent'], 1)
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        processes.sort(key=lambda p: p['cpu'] + p['memory'], reverse=True)
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu': round(cpu, 1),
            'cpu_cores': psutil.cpu_count(),
            'memory': round(memory.percent, 1),
            'memory_total_gb': round(memory.total / (1024**3), 1),
            'memory_used_gb': round((memory.total - memory.available) / (1024**3), 1),
            'disk': round(disk.percent, 1),
            'disk_total_gb': round(disk.total / (1024**3), 1),
            'disk_used_gb': round((disk.total - disk.free) / (1024**3), 1),
            'processes': len(psutil.pids()),
            'top_processes': processes[:10],
            'nodes': self._simulate_nodes(cpu, memory.percent)
        }
        
        self.current_metrics = metrics
        self.history.append(metrics)
        if len(self.history) > 100:
            self.history.pop(0)
        
        return metrics
    
    def _simulate_nodes(self, base_cpu: float, base_mem: float) -> List[Dict]:
        """Simulate cluster nodes"""
        return [
            {
                'name': 'compute-node-1',
                'cpu': min(100, base_cpu + 10),
                'memory': min(100, base_mem + 5),
                'vms': 3,
                'gpus': 2
            },
            {
                'name': 'compute-node-2',
                'cpu': min(100, base_cpu - 5),
                'memory': min(100, base_mem - 10),
                'vms': 2,
                'gpus': 1
            },
            {
                'name': 'compute-node-3',
                'cpu': min(100, base_cpu + 5),
                'memory': min(100, base_mem + 15),
                'vms': 4,
                'gpus': 2
            }
        ]


class MonitorHandler(BaseHTTPRequestHandler):
    """HTTP handler for metrics API and web interface"""
    
    collector = None
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_html().encode())
        
        elif self.path == '/api/metrics':
            metrics = self.collector.collect()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(metrics).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        return
    
    @staticmethod
    def get_html() -> str:
        """Return HTML dashboard"""
        return '''
<!DOCTYPE html>
<html>
<head>
    <title>🦅 QuetzalCore Infrastructure Monitor</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #00d4ff;
        }
        h1 {
            font-size: 28px;
            margin-bottom: 5px;
            background: linear-gradient(90deg, #00d4ff, #0099ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .timestamp {
            color: #aaa;
            font-size: 12px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: rgba(255,255,255, 0.05);
            border: 1px solid rgba(0,212,255, 0.2);
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0;
            color: #00d4ff;
        }
        .metric-label {
            color: #aaa;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .progress-bar {
            width: 100%;
            height: 6px;
            background: rgba(0,212,255, 0.1);
            border-radius: 3px;
            margin-top: 10px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00ff00, #ffff00, #ff0000);
            border-radius: 3px;
            transition: width 0.3s ease;
        }
        .sub-metric {
            color: #aaa;
            font-size: 12px;
            margin-top: 5px;
        }
        .nodes-section {
            margin-top: 30px;
        }
        .nodes-title {
            font-size: 20px;
            margin-bottom: 15px;
            color: #00d4ff;
            font-weight: bold;
        }
        .node-card {
            background: rgba(255,255,255, 0.03);
            border-left: 4px solid #00d4ff;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        .node-name {
            font-weight: bold;
            margin-bottom: 10px;
        }
        .node-metrics {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            font-size: 12px;
        }
        .processes-section {
            margin-top: 30px;
        }
        .processes-title {
            font-size: 20px;
            margin-bottom: 15px;
            color: #00d4ff;
            font-weight: bold;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th {
            text-align: left;
            padding: 10px;
            border-bottom: 1px solid rgba(0,212,255, 0.2);
            color: #00d4ff;
            font-size: 12px;
            text-transform: uppercase;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid rgba(0,212,255, 0.1);
            font-size: 13px;
        }
        tr:hover {
            background: rgba(0,212,255, 0.05);
        }
        .refresh-note {
            text-align: center;
            color: #aaa;
            font-size: 12px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🦅 QuetzalCore Infrastructure Monitor</h1>
            <p>Real-time OS Utilization Dashboard</p>
            <p class="timestamp" id="timestamp">Loading...</p>
        </header>

        <div class="grid">
            <div class="card">
                <div class="metric-label">CPU Usage</div>
                <div class="metric-value" id="cpu">--</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="cpu-bar" style="width: 0%"></div>
                </div>
                <div class="sub-metric" id="cpu-info"></div>
            </div>

            <div class="card">
                <div class="metric-label">Memory Usage</div>
                <div class="metric-value" id="memory">--</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="memory-bar" style="width: 0%"></div>
                </div>
                <div class="sub-metric" id="memory-info"></div>
            </div>

            <div class="card">
                <div class="metric-label">Disk Usage</div>
                <div class="metric-value" id="disk">--</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="disk-bar" style="width: 0%"></div>
                </div>
                <div class="sub-metric" id="disk-info"></div>
            </div>

            <div class="card">
                <div class="metric-label">Running Processes</div>
                <div class="metric-value" id="processes">--</div>
            </div>
        </div>

        <div class="nodes-section">
            <div class="nodes-title">🖥️ Distributed Infrastructure (3 Nodes)</div>
            <div id="nodes-container"></div>
        </div>

        <div class="processes-section">
            <div class="processes-title">🔝 Top Processes</div>
            <table>
                <thead>
                    <tr>
                        <th>PID</th>
                        <th>Process Name</th>
                        <th>CPU %</th>
                        <th>Memory %</th>
                    </tr>
                </thead>
                <tbody id="processes-tbody">
                </tbody>
            </table>
        </div>

        <div class="refresh-note">
            ⏱️ Auto-refreshing every 2 seconds...
        </div>
    </div>

    <script>
        async function updateMetrics() {
            try {
                const response = await fetch('/api/metrics');
                const data = await response.json();

                // Update timestamp
                document.getElementById('timestamp').textContent = 
                    'Updated: ' + new Date(data.timestamp).toLocaleTimeString();

                // Update main metrics
                document.getElementById('cpu').textContent = data.cpu + '%';
                document.getElementById('cpu-bar').style.width = data.cpu + '%';
                document.getElementById('cpu-info').textContent = data.cpu_cores + ' cores';

                document.getElementById('memory').textContent = data.memory + '%';
                document.getElementById('memory-bar').style.width = data.memory + '%';
                document.getElementById('memory-info').textContent = 
                    data.memory_used_gb + 'GB / ' + data.memory_total_gb + 'GB';

                document.getElementById('disk').textContent = data.disk + '%';
                document.getElementById('disk-bar').style.width = data.disk + '%';
                document.getElementById('disk-info').textContent = 
                    data.disk_used_gb + 'GB / ' + data.disk_total_gb + 'GB';

                document.getElementById('processes').textContent = data.processes;

                // Update nodes
                let nodesHTML = '';
                for (const node of data.nodes) {
                    nodesHTML += `
                        <div class="node-card">
                            <div class="node-name">${node.name}</div>
                            <div class="node-metrics">
                                <div>CPU: ${node.cpu.toFixed(1)}%</div>
                                <div>Memory: ${node.memory.toFixed(1)}%</div>
                                <div>VMs: ${node.vms}</div>
                                <div>GPUs: ${node.gpus}</div>
                            </div>
                        </div>
                    `;
                }
                document.getElementById('nodes-container').innerHTML = nodesHTML;

                // Update processes table
                let processesHTML = '';
                for (const proc of data.top_processes) {
                    processesHTML += `
                        <tr>
                            <td>${proc.pid}</td>
                            <td>${proc.name}</td>
                            <td>${proc.cpu}%</td>
                            <td>${proc.memory}%</td>
                        </tr>
                    `;
                }
                document.getElementById('processes-tbody').innerHTML = processesHTML;

            } catch (error) {
                console.error('Error fetching metrics:', error);
            }
        }

        // Update immediately and then every 2 seconds
        updateMetrics();
        setInterval(updateMetrics, 2000);
    </script>
</body>
</html>
        '''


def run_server():
    """Start the monitoring server"""
    collector = MetricsCollector()
    MonitorHandler.collector = collector
    
    server = HTTPServer(('localhost', 7070), MonitorHandler)
    print("\n" + "="*70)
    print("🦅 QuetzalCore Infrastructure Monitor")
    print("="*70)
    print("\n✅ Monitor running at: http://localhost:7070")
    print("\n📊 Features:")
    print("   • Real-time CPU, Memory, Disk usage")
    print("   • Top processes listing")
    print("   • Simulated distributed cluster view (3 nodes)")
    print("   • Auto-updating every 2 seconds")
    print("   • JSON API at: http://localhost:7070/api/metrics")
    print("\n💡 Use this to:")
    print("   • Monitor OS resource utilization")
    print("   • See process CPU/Memory usage")
    print("   • Track infrastructure metrics")
    print("   • Identify resource bottlenecks")
    print("\n🛑 Press Ctrl+C to stop\n")
    print("="*70 + "\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Monitor stopped")
        server.shutdown()


if __name__ == "__main__":
    run_server()
