#!/usr/bin/env python3
"""
🦅 QUETZALCORE OS - AUTONOMOUS SCRUM MONITOR
Real-time dashboard for Agile development with auto-refresh
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import subprocess
import psutil

app = FastAPI(title="QuetzalCore OS Scrum Dashboard")

# Sprint configuration
CURRENT_SPRINT = {
    "number": 1,
    "name": "Hello QuetzalCore",
    "start_date": "2025-12-07",
    "end_date": "2025-12-20",
    "goal": "Bootable kernel with console output",
    "total_points": 10
}

STORIES = [
    {"id": "US-1", "title": "Boot QuetzalCore OS", "points": 5, "status": "in-progress"},
    {"id": "US-2", "title": "Serial console", "points": 3, "status": "todo"},
    {"id": "US-4", "title": "Version info", "points": 2, "status": "todo"},
]

def get_build_status():
    """Check if kernel builds successfully"""
    try:
        result = subprocess.run(
            ["cargo", "build", "--release", "--manifest-path", "quetzalcore-kernel/Cargo.toml"],
            capture_output=True,
            timeout=60,
            cwd="/Users/xavasena/hive"
        )
        return {
            "success": result.returncode == 0,
            "time": datetime.now().isoformat(),
            "output": result.stderr.decode()[:500]
        }
    except Exception as e:
        return {"success": False, "error": str(e), "time": datetime.now().isoformat()}

def get_git_stats():
    """Get today's commits"""
    try:
        result = subprocess.run(
            ["git", "log", "--since=today", "--oneline"],
            capture_output=True,
            cwd="/Users/xavasena/hive"
        )
        commits = result.stdout.decode().strip().split('\n')
        return {"count": len([c for c in commits if c]), "commits": commits[:5]}
    except:
        return {"count": 0, "commits": []}

def get_system_metrics():
    """Get system performance"""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
    }

def calculate_sprint_progress():
    """Calculate completed story points"""
    completed = sum(s["points"] for s in STORIES if s["status"] == "done")
    in_progress = sum(s["points"] for s in STORIES if s["status"] == "in-progress")
    total = CURRENT_SPRINT["total_points"]
    return {
        "completed": completed,
        "in_progress": in_progress,
        "remaining": total - completed - in_progress,
        "total": total,
        "percent": int((completed / total) * 100) if total > 0 else 0
    }

@app.get("/")
async def dashboard():
    """Main Scrum dashboard"""
    progress = calculate_sprint_progress()
    build = get_build_status()
    git = get_git_stats()
    metrics = get_system_metrics()
    
    # Calculate days remaining
    from datetime import datetime
    start = datetime.fromisoformat(CURRENT_SPRINT["start_date"])
    end = datetime.fromisoformat(CURRENT_SPRINT["end_date"])
    now = datetime.now()
    days_remaining = (end - now).days
    
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🦅 QuetzalCore OS - Scrum Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Courier New', monospace;
                background: linear-gradient(135deg, #000000 0%, #1a1a2e 100%);
                color: #00ff00;
                padding: 20px;
                min-height: 100vh;
            }}
            .container {{
                max-width: 1400px;
                margin: 0 auto;
            }}
            h1 {{
                text-align: center;
                font-size: 2.5em;
                margin-bottom: 30px;
                text-shadow: 0 0 10px #00ff00;
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.7; }}
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }}
            .card {{
                background: rgba(0, 255, 0, 0.05);
                border: 2px solid #00ff00;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
            }}
            .card h2 {{
                color: #00ff00;
                font-size: 1.5em;
                margin-bottom: 15px;
                border-bottom: 1px solid #00ff00;
                padding-bottom: 10px;
            }}
            .progress-bar {{
                background: rgba(0, 255, 0, 0.1);
                border: 1px solid #00ff00;
                height: 30px;
                border-radius: 5px;
                overflow: hidden;
                margin: 10px 0;
            }}
            .progress-fill {{
                background: linear-gradient(90deg, #00ff00, #00aa00);
                height: 100%;
                transition: width 0.5s;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
            }}
            .stat {{
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px dotted #00ff0040;
            }}
            .stat:last-child {{
                border-bottom: none;
            }}
            .status-badge {{
                display: inline-block;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 0.85em;
                font-weight: bold;
            }}
            .status-done {{ background: #00ff00; color: #000; }}
            .status-progress {{ background: #ffaa00; color: #000; }}
            .status-todo {{ background: #ff0000; color: #fff; }}
            .build-success {{ color: #00ff00; }}
            .build-fail {{ color: #ff0000; }}
            ul {{
                list-style: none;
                padding-left: 0;
            }}
            li {{
                padding: 8px 0;
                border-bottom: 1px dotted #00ff0040;
            }}
            li:last-child {{
                border-bottom: none;
            }}
            .metric {{
                font-size: 2em;
                text-align: center;
                margin: 10px 0;
            }}
            .refresh-info {{
                text-align: center;
                color: #00aa00;
                font-style: italic;
                margin-top: 20px;
            }}
        </style>
        <script>
            // Auto-refresh every 30 seconds
            setTimeout(() => location.reload(), 30000);
            
            // Update timestamp
            setInterval(() => {{
                document.getElementById('timestamp').textContent = new Date().toLocaleTimeString();
            }}, 1000);
        </script>
    </head>
    <body>
        <div class="container">
            <h1>🦅 QUETZALCORE OS - SPRINT DASHBOARD</h1>
            
            <div class="grid">
                <div class="card">
                    <h2>📅 Current Sprint</h2>
                    <div class="stat">
                        <span>Sprint:</span>
                        <span><strong>#{CURRENT_SPRINT['number']} "{CURRENT_SPRINT['name']}"</strong></span>
                    </div>
                    <div class="stat">
                        <span>Goal:</span>
                        <span>{CURRENT_SPRINT['goal']}</span>
                    </div>
                    <div class="stat">
                        <span>Days Remaining:</span>
                        <span><strong>{days_remaining} days</strong></span>
                    </div>
                    <div class="stat">
                        <span>Story Points:</span>
                        <span><strong>{progress['completed']}/{progress['total']} complete</strong></span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {progress['percent']}%">
                            {progress['percent']}%
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h2>🏗️ Build Status</h2>
                    <div class="stat">
                        <span>Last Build:</span>
                        <span class="{'build-success' if build['success'] else 'build-fail'}">
                            <strong>{'✅ PASSED' if build['success'] else '❌ FAILED'}</strong>
                        </span>
                    </div>
                    <div class="stat">
                        <span>Time:</span>
                        <span>{datetime.now().strftime('%H:%M:%S')}</span>
                    </div>
                    <div class="stat">
                        <span>Commits Today:</span>
                        <span><strong>{git['count']}</strong></span>
                    </div>
                </div>
                
                <div class="card">
                    <h2>💻 System Metrics</h2>
                    <div class="stat">
                        <span>CPU Usage:</span>
                        <span><strong>{metrics['cpu_percent']:.1f}%</strong></span>
                    </div>
                    <div class="stat">
                        <span>Memory:</span>
                        <span><strong>{metrics['memory_percent']:.1f}%</strong></span>
                    </div>
                    <div class="stat">
                        <span>Disk:</span>
                        <span><strong>{metrics['disk_percent']:.1f}%</strong></span>
                    </div>
                </div>
            </div>
            
            <div class="grid">
                <div class="card">
                    <h2>📋 User Stories</h2>
                    <ul>
                        {''.join(f'''
                        <li>
                            <span class="status-badge status-{s['status'].replace('-', '')}">{s['status'].upper()}</span>
                            <strong>{s['id']}</strong>: {s['title']} ({s['points']} pts)
                        </li>
                        ''' for s in STORIES)}
                    </ul>
                </div>
                
                <div class="card">
                    <h2>🎯 Today's Commits</h2>
                    <ul>
                        {''.join(f'<li>{commit}</li>' for commit in git['commits']) if git['commits'][0] else '<li>No commits yet today</li>'}
                    </ul>
                </div>
                
                <div class="card">
                    <h2>🚧 Blockers</h2>
                    <ul>
                        <li style="color: #00ff00;">✅ None! Team is unblocked 🎉</li>
                    </ul>
                </div>
            </div>
            
            <div class="refresh-info">
                <p>🔄 Auto-refreshes every 30 seconds | Current time: <span id="timestamp">{datetime.now().strftime('%H:%M:%S')}</span></p>
                <p>🦅 QuetzalCore OS - Building the future of cloud desktops</p>
            </div>
        </div>
    </body>
    </html>
    """)

@app.get("/api/status")
async def api_status():
    """JSON API for status"""
    return {
        "sprint": CURRENT_SPRINT,
        "progress": calculate_sprint_progress(),
        "build": get_build_status(),
        "git": get_git_stats(),
        "metrics": get_system_metrics()
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await websocket.accept()
    try:
        while True:
            data = {
                "progress": calculate_sprint_progress(),
                "metrics": get_system_metrics(),
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except:
        pass

if __name__ == "__main__":
    import uvicorn
    print("🦅 Starting QuetzalCore OS Scrum Dashboard...")
    print("📊 Dashboard: http://localhost:9998")
    print("🔌 API: http://localhost:9998/api/status")
    uvicorn.run(app, host="0.0.0.0", port=9998)
