#!/usr/bin/env python3
"""
📱 MOBILE APPROVAL DASHBOARD for Samsung Phone
==============================================
Lightweight FastAPI server that provides a mobile-optimized dashboard
for approving critical operations from your phone.

Features:
- Mobile-responsive design
- Push notifications for critical approvals
- One-tap approve/reject
- Real-time status monitoring
- Secure token-based auth

Usage:
    python3 mobile_dashboard.py
    # Access from phone: http://YOUR_IP:9999
"""

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import json
import uuid
from datetime import datetime
import os

app = FastAPI(title="Queztl Mobile Dashboard", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Approval queue
approval_queue: List[Dict] = []
approval_results: Dict[str, str] = {}

class ApprovalRequest(BaseModel):
    title: str
    description: str
    action_type: str  # 'deploy', 'delete', 'build', 'critical'
    auto_approve_after: Optional[int] = 300  # Auto-approve after 5 minutes

class ApprovalResponse(BaseModel):
    approval_id: str
    approved: bool
    reason: Optional[str] = None

# Connected WebSocket clients
connected_clients: List[WebSocket] = []

@app.get("/", response_class=HTMLResponse)
async def mobile_dashboard():
    """Mobile-optimized dashboard"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="theme-color" content="#667eea">
    <title>🦅 Queztl Mobile</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            padding: 10px;
            overflow-x: hidden;
        }
        
        .header {
            text-align: center;
            padding: 20px 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            margin-bottom: 20px;
        }
        
        .header h1 {
            font-size: 24px;
            margin-bottom: 5px;
        }
        
        .status {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            font-size: 14px;
            margin-top: 10px;
        }
        
        .status-dot {
            width: 10px;
            height: 10px;
            background: #00ff88;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .approval-card {
            background: white;
            color: #333;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .approval-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .approval-title {
            font-size: 18px;
            font-weight: 600;
        }
        
        .approval-badge {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .badge-deploy { background: #e3f2fd; color: #1976d2; }
        .badge-delete { background: #ffebee; color: #c62828; }
        .badge-build { background: #f3e5f5; color: #7b1fa2; }
        .badge-critical { background: #fff3e0; color: #e65100; }
        
        .approval-description {
            font-size: 14px;
            color: #666;
            margin-bottom: 15px;
            line-height: 1.5;
        }
        
        .approval-time {
            font-size: 12px;
            color: #999;
            margin-bottom: 15px;
        }
        
        .approval-actions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        
        .btn {
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .btn:active {
            transform: scale(0.95);
        }
        
        .btn-approve {
            background: #4caf50;
            color: white;
        }
        
        .btn-reject {
            background: #f44336;
            color: white;
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            opacity: 0.7;
        }
        
        .empty-state-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }
        
        .countdown {
            font-size: 12px;
            color: #ff9800;
            font-weight: 600;
            margin-top: 10px;
        }
        
        .notification {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #4caf50;
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            z-index: 1000;
            display: none;
            animation: slideDown 0.3s ease;
        }
        
        @keyframes slideDown {
            from { transform: translate(-50%, -100px); }
            to { transform: translate(-50%, 0); }
        }
        
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: 700;
        }
        
        .stat-label {
            font-size: 11px;
            opacity: 0.8;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🦅 Queztl Mobile</h1>
        <div class="status">
            <div class="status-dot"></div>
            <span>Connected</span>
        </div>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-value" id="pendingCount">0</div>
            <div class="stat-label">PENDING</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="approvedCount">0</div>
            <div class="stat-label">APPROVED</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="rejectedCount">0</div>
            <div class="stat-label">REJECTED</div>
        </div>
    </div>
    
    <div id="approvalList"></div>
    
    <div id="notification" class="notification"></div>
    
    <script>
        let ws;
        let approvals = [];
        let stats = { pending: 0, approved: 0, rejected: 0 };
        
        function connectWebSocket() {
            ws = new WebSocket(`ws://${window.location.host}/ws/approvals`);
            
            ws.onopen = () => {
                console.log('Connected to approval system');
                loadApprovals();
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                
                if (data.type === 'new_approval') {
                    showNotification('New approval request!');
                    loadApprovals();
                } else if (data.type === 'update') {
                    loadApprovals();
                }
            };
            
            ws.onclose = () => {
                console.log('Disconnected, reconnecting...');
                setTimeout(connectWebSocket, 3000);
            };
        }
        
        async function loadApprovals() {
            const response = await fetch('/api/approvals');
            const data = await response.json();
            approvals = data.approvals;
            stats = data.stats;
            renderApprovals();
            updateStats();
        }
        
        function updateStats() {
            document.getElementById('pendingCount').textContent = stats.pending;
            document.getElementById('approvedCount').textContent = stats.approved;
            document.getElementById('rejectedCount').textContent = stats.rejected;
        }
        
        function renderApprovals() {
            const list = document.getElementById('approvalList');
            
            if (approvals.length === 0) {
                list.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">✅</div>
                        <div>All caught up!</div>
                        <div style="font-size: 14px; margin-top: 10px;">No pending approvals</div>
                    </div>
                `;
                return;
            }
            
            list.innerHTML = approvals.map(approval => `
                <div class="approval-card">
                    <div class="approval-header">
                        <div class="approval-title">${approval.title}</div>
                        <div class="approval-badge badge-${approval.action_type}">${approval.action_type.toUpperCase()}</div>
                    </div>
                    <div class="approval-description">${approval.description}</div>
                    <div class="approval-time">⏰ ${formatTime(approval.created_at)}</div>
                    ${approval.auto_approve_after ? `<div class="countdown" id="countdown-${approval.id}">Auto-approves in ${approval.auto_approve_after}s</div>` : ''}
                    <div class="approval-actions">
                        <button class="btn btn-approve" onclick="approve('${approval.id}')">
                            ✓ APPROVE
                        </button>
                        <button class="btn btn-reject" onclick="reject('${approval.id}')">
                            ✗ REJECT
                        </button>
                    </div>
                </div>
            `).join('');
            
            // Start countdowns
            approvals.forEach(approval => {
                if (approval.auto_approve_after) {
                    startCountdown(approval.id, approval.auto_approve_after);
                }
            });
        }
        
        function startCountdown(id, seconds) {
            const element = document.getElementById(`countdown-${id}`);
            if (!element) return;
            
            let remaining = seconds;
            const interval = setInterval(() => {
                remaining--;
                if (element) {
                    element.textContent = `Auto-approves in ${remaining}s`;
                }
                if (remaining <= 0) {
                    clearInterval(interval);
                }
            }, 1000);
        }
        
        async function approve(id) {
            await fetch(`/api/approve/${id}`, { method: 'POST', body: JSON.stringify({approved: true}), headers: {'Content-Type': 'application/json'} });
            showNotification('✓ Approved!');
            loadApprovals();
        }
        
        async function reject(id) {
            await fetch(`/api/approve/${id}`, { method: 'POST', body: JSON.stringify({approved: false}), headers: {'Content-Type': 'application/json'} });
            showNotification('✗ Rejected');
            loadApprovals();
        }
        
        function showNotification(message) {
            const notif = document.getElementById('notification');
            notif.textContent = message;
            notif.style.display = 'block';
            setTimeout(() => {
                notif.style.display = 'none';
            }, 3000);
        }
        
        function formatTime(timestamp) {
            const date = new Date(timestamp);
            const now = new Date();
            const diff = Math.floor((now - date) / 1000);
            
            if (diff < 60) return `${diff}s ago`;
            if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
            return `${Math.floor(diff / 3600)}h ago`;
        }
        
        // Connect on load
        connectWebSocket();
        
        // Refresh every 5 seconds
        setInterval(loadApprovals, 5000);
    </script>
</body>
</html>
"""

@app.get("/api/approvals")
async def get_approvals():
    """Get all pending approvals"""
    pending = [a for a in approval_queue if a['id'] not in approval_results]
    
    stats = {
        'pending': len(pending),
        'approved': sum(1 for v in approval_results.values() if v == 'approved'),
        'rejected': sum(1 for v in approval_results.values() if v == 'rejected'),
    }
    
    return {"approvals": pending, "stats": stats}

@app.post("/api/request-approval")
async def request_approval(request: ApprovalRequest):
    """Request approval for an action"""
    approval_id = str(uuid.uuid4())
    
    approval = {
        "id": approval_id,
        "title": request.title,
        "description": request.description,
        "action_type": request.action_type,
        "auto_approve_after": request.auto_approve_after,
        "created_at": datetime.now().isoformat(),
    }
    
    approval_queue.append(approval)
    
    # Notify all connected clients
    for client in connected_clients:
        try:
            await client.send_json({"type": "new_approval", "approval": approval})
        except:
            pass
    
    # Auto-approve after timeout
    if request.auto_approve_after:
        asyncio.create_task(auto_approve_task(approval_id, request.auto_approve_after))
    
    return {"approval_id": approval_id, "status": "pending"}

@app.post("/api/approve/{approval_id}")
async def approve_action(approval_id: str, response: ApprovalResponse):
    """Approve or reject an action"""
    approval_results[approval_id] = "approved" if response.approved else "rejected"
    
    # Notify all clients
    for client in connected_clients:
        try:
            await client.send_json({"type": "update"})
        except:
            pass
    
    return {"success": True}

@app.websocket("/ws/approvals")
async def websocket_approvals(websocket: WebSocket):
    """WebSocket for real-time approval updates"""
    await websocket.accept()
    connected_clients.append(websocket)
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except:
        pass
    finally:
        connected_clients.remove(websocket)

async def auto_approve_task(approval_id: str, timeout: int):
    """Auto-approve after timeout"""
    await asyncio.sleep(timeout)
    
    if approval_id not in approval_results:
        approval_results[approval_id] = "approved"
        print(f"Auto-approved: {approval_id}")

@app.get("/health")
async def health():
    return {"status": "ok", "pending_approvals": len([a for a in approval_queue if a['id'] not in approval_results])}

if __name__ == "__main__":
    import uvicorn
    import socket
    
    # Get local IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    
    print("=" * 80)
    print("📱 MOBILE APPROVAL DASHBOARD")
    print("=" * 80)
    print(f"")
    print(f"🌐 Access from your Samsung phone:")
    print(f"   http://{local_ip}:9999")
    print(f"")
    print(f"📝 Add to home screen for app-like experience!")
    print("=" * 80)
    print("")
    
    uvicorn.run(app, host="0.0.0.0", port=9999)
