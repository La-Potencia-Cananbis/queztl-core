#!/usr/bin/env python3
"""
QUEZTL CLUSTER COORDINATOR
Receives work requests, distributes to nodes, collects results

This is the "brain" - like the Star Trek computer's central processor
"""

import asyncio
from aiohttp import web
import aiohttp
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import logging
from collections import deque

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COORDINATOR_PORT = 9000

class ClusterCoordinator:
    """
    Coordinates work across the cluster
    Nodes connect to this to get work and submit results
    """
    
    def __init__(self):
        self.nodes: Dict[str, Dict] = {}  # node_id -> node_info
        self.pending_tasks: deque = deque()
        self.active_tasks: Dict[str, Dict] = {}  # task_id -> task_info
        self.completed_tasks: List[Dict] = []
        self.stats = {
            "total_tasks_submitted": 0,
            "total_tasks_completed": 0,
            "total_tasks_failed": 0,
            "active_nodes": 0
        }
    
    async def handle_join(self, request):
        """Node joins the cluster"""
        data = await request.json()
        node_id = data.get("node_id")
        
        self.nodes[node_id] = {
            **data,
            "last_seen": time.time(),
            "tasks_completed": 0
        }
        
        self.stats["active_nodes"] = len(self.nodes)
        
        logger.info(f"✅ Node joined: {data.get('node_name')} ({data.get('ip')})")
        logger.info(f"   Capabilities: {data.get('capabilities')}")
        
        return web.json_response({
            "status": "joined",
            "cluster_size": len(self.nodes),
            "pending_work": len(self.pending_tasks)
        })
    
    async def handle_work_request(self, request):
        """Node requests work"""
        data = await request.json()
        node_id = data.get("node_id")
        capabilities = data.get("capabilities", {})
        
        # Update last seen
        if node_id in self.nodes:
            self.nodes[node_id]["last_seen"] = time.time()
        
        # Find suitable task
        for _ in range(len(self.pending_tasks)):
            task = self.pending_tasks.popleft()
            
            # Check if node can handle this task
            required_caps = task.get("required_capabilities", {})
            if self._node_can_handle(capabilities, required_caps):
                task_id = task["task_id"]
                self.active_tasks[task_id] = {
                    **task,
                    "assigned_to": node_id,
                    "assigned_at": time.time()
                }
                
                logger.info(f"📤 Assigned task {task_id} to {self.nodes[node_id].get('node_name')}")
                
                return web.json_response({
                    "status": "work_assigned",
                    "task": task
                })
            else:
                # Put task back if node can't handle it
                self.pending_tasks.append(task)
        
        # No suitable work
        return web.json_response({
            "status": "no_work",
            "message": "No suitable tasks available"
        })
    
    def _node_can_handle(self, node_caps: Dict, required_caps: Dict) -> bool:
        """Check if node has required capabilities"""
        if not required_caps:
            return True
        
        for cap, required_value in required_caps.items():
            if cap not in node_caps:
                return False
            if required_value is True and not node_caps[cap]:
                return False
        
        return True
    
    async def handle_work_complete(self, request):
        """Node submits completed work"""
        result = await request.json()
        task_id = result.get("task_id")
        node_id = result.get("node_id")
        status = result.get("status")
        
        if task_id in self.active_tasks:
            del self.active_tasks[task_id]
        
        if status == "completed":
            self.stats["total_tasks_completed"] += 1
            if node_id in self.nodes:
                self.nodes[node_id]["tasks_completed"] += 1
            logger.info(f"✅ Task {task_id} completed by {self.nodes.get(node_id, {}).get('node_name', node_id)}")
        else:
            self.stats["total_tasks_failed"] += 1
            logger.warning(f"❌ Task {task_id} failed: {result.get('error')}")
        
        self.completed_tasks.append(result)
        
        return web.json_response({"status": "acknowledged"})
    
    async def handle_submit_task(self, request):
        """External client submits work to cluster"""
        task = await request.json()
        
        task_id = f"task_{int(time.time() * 1000)}"
        task["task_id"] = task_id
        task["submitted_at"] = time.time()
        
        self.pending_tasks.append(task)
        self.stats["total_tasks_submitted"] += 1
        
        logger.info(f"📥 New task submitted: {task_id} ({task.get('type')})")
        
        return web.json_response({
            "status": "queued",
            "task_id": task_id,
            "queue_position": len(self.pending_tasks)
        })
    
    async def handle_stats(self, request):
        """Return cluster statistics"""
        return web.json_response({
            "stats": self.stats,
            "nodes": {
                node_id: {
                    "name": info.get("node_name"),
                    "ip": info.get("ip"),
                    "tasks_completed": info.get("tasks_completed", 0),
                    "last_seen": time.time() - info.get("last_seen", 0)
                }
                for node_id, info in self.nodes.items()
            },
            "pending_tasks": len(self.pending_tasks),
            "active_tasks": len(self.active_tasks)
        })
    
    async def cleanup_stale_nodes(self):
        """Remove nodes that haven't been seen in a while"""
        while True:
            await asyncio.sleep(60)
            
            current_time = time.time()
            stale_nodes = []
            
            for node_id, info in self.nodes.items():
                if current_time - info.get("last_seen", 0) > 120:  # 2 minutes
                    stale_nodes.append(node_id)
            
            for node_id in stale_nodes:
                logger.warning(f"⚠️  Removing stale node: {self.nodes[node_id].get('node_name')}")
                del self.nodes[node_id]
            
            if stale_nodes:
                self.stats["active_nodes"] = len(self.nodes)
    
    async def start(self):
        """Start the coordinator server"""
        app = web.Application()
        app.router.add_post('/cluster/join', self.handle_join)
        app.router.add_post('/cluster/work/request', self.handle_work_request)
        app.router.add_post('/cluster/work/complete', self.handle_work_complete)
        app.router.add_post('/cluster/submit', self.handle_submit_task)
        app.router.add_get('/cluster/stats', self.handle_stats)
        
        # Start cleanup task
        asyncio.create_task(self.cleanup_stale_nodes())
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', COORDINATOR_PORT)
        
        logger.info(f"🎯 Cluster Coordinator listening on port {COORDINATOR_PORT}")
        
        await site.start()
        
        # Keep running
        while True:
            await asyncio.sleep(3600)


async def main():
    coordinator = ClusterCoordinator()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🎯 QUEZTL CLUSTER COORDINATOR                              ║
╚══════════════════════════════════════════════════════════════╝

Listening on: 0.0.0.0:{COORDINATOR_PORT}

This is the "brain" of the cluster. Nodes connect here to:
- Announce their presence
- Request work
- Submit results

Star Trek TNG Computer: ONLINE ✨

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Press Ctrl+C to stop.
""")
    
    await coordinator.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️  Coordinator stopped")
