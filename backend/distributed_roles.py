#!/usr/bin/env python3
"""
Distributed Role System with Failover
Each node can take on multiple roles with automatic failover
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
import socket
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Role definitions
ROLES = {
    "web_server": {
        "port": 8080,
        "priority": ["sloth", "beast", "mac"],  # Preferred order
        "health_endpoint": "/",
        "start_command": "python3 -m http.server 8080",
        "capabilities": ["serve_static", "host_frontend"]
    },
    "contact_api": {
        "port": 8003,
        "priority": ["sloth", "beast", "mac"],
        "health_endpoint": "/health",
        "start_command": "python3 backend/contact_form_api.py",
        "capabilities": ["handle_forms", "send_email", "database"]
    },
    "image_generator": {
        "port": 8001,
        "priority": ["beast", "sloth"],  # GPU-heavy, prefer Beast
        "health_endpoint": "/health",
        "start_command": "python3 backend/beast_image_generator.py",
        "capabilities": ["generate_images", "stable_diffusion"]
    },
    "content_runner": {
        "port": 8004,
        "priority": ["sloth", "beast", "mac"],
        "health_endpoint": "/health",
        "start_command": "python3 backend/content_runner.py --continuous",
        "capabilities": ["generate_content", "schedule_tasks"]
    },
    "storage_server": {
        "port": 8000,
        "priority": ["sloth", "beast"],  # Large disk space needed
        "health_endpoint": "/health",
        "start_command": "python3 backend/storage_server.py",
        "capabilities": ["file_storage", "database", "backups"]
    },
    "coordinator": {
        "port": 8005,
        "priority": ["sloth", "beast", "mac"],  # Any node can coordinate
        "health_endpoint": "/health",
        "start_command": "python3 backend/distributed_roles.py --coordinator",
        "capabilities": ["health_checks", "failover", "service_discovery"]
    }
}

# Node definitions (these can be discovered dynamically)
NODES = {
    "beast": {
        "ip": "192.168.1.105",
        "hostname": "beast",
        "capabilities": ["gpu", "compute", "storage"],
        "resources": {"ram": "16GB", "cpu": "8 cores", "gpu": "NVIDIA"}
    },
    "sloth": {
        "ip": "192.168.1.102",
        "hostname": "sloth",
        "capabilities": ["storage", "database", "compute"],
        "resources": {"ram": "16GB", "cpu": "8 cores", "disk": "2TB"}
    },
    "mac": {
        "ip": "192.168.1.100",  # Update with actual IP
        "hostname": "mac",
        "capabilities": ["compute", "command_center"],
        "resources": {"ram": "8GB", "cpu": "4 cores"}
    }
}

class DistributedRoleManager:
    """Manages role assignment and failover across cluster nodes"""
    
    def __init__(self, node_name: str):
        self.node_name = node_name
        self.node_info = NODES.get(node_name, {})
        self.active_roles: Set[str] = set()
        self.role_assignments: Dict[str, str] = {}  # role -> node
        self.last_health_check: Dict[str, float] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def check_node_health(self, node_name: str) -> bool:
        """Check if a node is healthy"""
        if node_name not in NODES:
            return False
            
        node = NODES[node_name]
        try:
            async with self.session.get(
                f"http://{node['ip']}:8005/health",
                timeout=aiohttp.ClientTimeout(total=2)
            ) as resp:
                return resp.status == 200
        except:
            return False
    
    async def check_role_health(self, role: str, node_name: str) -> bool:
        """Check if a specific role is healthy on a node"""
        if role not in ROLES or node_name not in NODES:
            return False
            
        role_info = ROLES[role]
        node = NODES[node_name]
        
        try:
            async with self.session.get(
                f"http://{node['ip']}:{role_info['port']}{role_info['health_endpoint']}",
                timeout=aiohttp.ClientTimeout(total=2)
            ) as resp:
                return resp.status == 200
        except:
            return False
    
    async def discover_roles(self) -> Dict[str, str]:
        """Discover which roles are currently running on which nodes"""
        assignments = {}
        
        for role, role_info in ROLES.items():
            for node_name in role_info['priority']:
                if await self.check_role_health(role, node_name):
                    assignments[role] = node_name
                    logger.info(f"✓ {role} found on {node_name}")
                    break
            
            if role not in assignments:
                logger.warning(f"⚠️  {role} not found on any node")
        
        return assignments
    
    async def assign_missing_roles(self):
        """Assign missing roles to available nodes based on priority"""
        current_assignments = await self.discover_roles()
        
        for role, role_info in ROLES.items():
            if role not in current_assignments:
                logger.warning(f"🔍 Role {role} is missing, finding node...")
                
                # Try to assign to highest priority available node
                for node_name in role_info['priority']:
                    if await self.check_node_health(node_name):
                        logger.info(f"📍 Assigning {role} to {node_name}")
                        
                        # If this is our node, start the role
                        if node_name == self.node_name:
                            await self.start_role(role)
                        else:
                            # Request the node to start the role
                            await self.request_role_start(node_name, role)
                        
                        current_assignments[role] = node_name
                        break
                else:
                    logger.error(f"❌ No available node for {role}")
        
        self.role_assignments = current_assignments
        return current_assignments
    
    async def start_role(self, role: str) -> bool:
        """Start a role on this node"""
        if role not in ROLES:
            logger.error(f"Unknown role: {role}")
            return False
        
        role_info = ROLES[role]
        
        # Check if already running
        if await self.check_role_health(role, self.node_name):
            logger.info(f"✓ {role} already running on {self.node_name}")
            self.active_roles.add(role)
            return True
        
        logger.info(f"🚀 Starting {role} on {self.node_name}")
        
        # Start the service (this is simplified - real implementation would use systemd or similar)
        try:
            # This is a placeholder - actual implementation would start the service
            logger.info(f"Command: {role_info['start_command']}")
            self.active_roles.add(role)
            return True
        except Exception as e:
            logger.error(f"Failed to start {role}: {e}")
            return False
    
    async def request_role_start(self, node_name: str, role: str):
        """Request another node to start a role"""
        if node_name not in NODES:
            return
            
        node = NODES[node_name]
        try:
            async with self.session.post(
                f"http://{node['ip']}:8005/start_role",
                json={"role": role},
                timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                if resp.status == 200:
                    logger.info(f"✓ {node_name} accepted {role}")
                else:
                    logger.warning(f"⚠️  {node_name} rejected {role}")
        except Exception as e:
            logger.error(f"Failed to request role from {node_name}: {e}")
    
    async def handle_failover(self, failed_role: str, failed_node: str):
        """Handle failover when a role fails"""
        logger.warning(f"🔄 Handling failover for {failed_role} (was on {failed_node})")
        
        role_info = ROLES[failed_role]
        
        # Find next available node in priority list
        for node_name in role_info['priority']:
            if node_name == failed_node:
                continue  # Skip the failed node
                
            if await self.check_node_health(node_name):
                logger.info(f"📍 Failing over {failed_role} to {node_name}")
                
                if node_name == self.node_name:
                    success = await self.start_role(failed_role)
                    if success:
                        self.role_assignments[failed_role] = node_name
                        return True
                else:
                    await self.request_role_start(node_name, failed_role)
                    # Wait a bit and check if it started
                    await asyncio.sleep(5)
                    if await self.check_role_health(failed_role, node_name):
                        self.role_assignments[failed_role] = node_name
                        return True
        
        logger.error(f"❌ Failed to failover {failed_role}")
        return False
    
    async def monitor_health(self, interval: int = 30):
        """Continuously monitor health and handle failovers"""
        logger.info(f"🔍 Starting health monitor (interval: {interval}s)")
        
        while True:
            try:
                # Check all assigned roles
                for role, node_name in list(self.role_assignments.items()):
                    healthy = await self.check_role_health(role, node_name)
                    
                    if not healthy:
                        logger.error(f"❌ {role} unhealthy on {node_name}")
                        await self.handle_failover(role, node_name)
                    else:
                        # Update last health check time
                        self.last_health_check[f"{role}@{node_name}"] = time.time()
                
                # Check for missing roles
                await self.assign_missing_roles()
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in health monitor: {e}")
                await asyncio.sleep(interval)
    
    async def get_status(self) -> Dict:
        """Get current cluster status"""
        # Discover current state
        current_assignments = await self.discover_roles()
        
        # Check node health
        node_health = {}
        for node_name in NODES:
            node_health[node_name] = await self.check_node_health(node_name)
        
        return {
            "node": self.node_name,
            "active_roles": list(self.active_roles),
            "cluster_roles": current_assignments,
            "node_health": node_health,
            "timestamp": datetime.now().isoformat()
        }

class CoordinatorAPI:
    """FastAPI coordinator service"""
    
    def __init__(self, manager: DistributedRoleManager):
        self.manager = manager
        
        try:
            from fastapi import FastAPI
            from fastapi.middleware.cors import CORSMiddleware
            
            self.app = FastAPI(title="Queztl Coordinator")
            
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            
            # Register routes
            self.app.get("/health")(self.health)
            self.app.get("/status")(self.status)
            self.app.post("/start_role")(self.start_role)
            self.app.post("/stop_role")(self.stop_role)
            self.app.get("/roles")(self.list_roles)
            self.app.get("/nodes")(self.list_nodes)
            
        except ImportError:
            logger.error("FastAPI not installed - coordinator API disabled")
            self.app = None
    
    async def health(self):
        return {"status": "healthy", "node": self.manager.node_name}
    
    async def status(self):
        return await self.manager.get_status()
    
    async def start_role(self, role_request: dict):
        role = role_request.get("role")
        if not role:
            return {"error": "role parameter required"}
        
        success = await self.manager.start_role(role)
        return {"success": success, "role": role, "node": self.manager.node_name}
    
    async def stop_role(self, role_request: dict):
        role = role_request.get("role")
        if not role:
            return {"error": "role parameter required"}
        
        # Simplified - real implementation would stop the service
        if role in self.manager.active_roles:
            self.manager.active_roles.remove(role)
            return {"success": True, "role": role}
        return {"success": False, "error": "role not active"}
    
    async def list_roles(self):
        return {"roles": ROLES}
    
    async def list_nodes(self):
        return {"nodes": NODES}

async def run_coordinator(node_name: str):
    """Run the coordinator service"""
    logger.info(f"🚀 Starting coordinator on {node_name}")
    
    async with DistributedRoleManager(node_name) as manager:
        # Discover current state
        logger.info("🔍 Discovering cluster state...")
        await manager.discover_roles()
        
        # Assign missing roles
        logger.info("📍 Assigning missing roles...")
        await manager.assign_missing_roles()
        
        # Start coordinator API
        coordinator = CoordinatorAPI(manager)
        
        if coordinator.app:
            # Start health monitoring in background
            monitor_task = asyncio.create_task(manager.monitor_health())
            
            # Start FastAPI server
            import uvicorn
            config = uvicorn.Config(
                coordinator.app,
                host="0.0.0.0",
                port=8005,
                log_level="info"
            )
            server = uvicorn.Server(config)
            await server.serve()
        else:
            # Just run health monitoring
            await manager.monitor_health()

async def check_cluster_status():
    """Quick cluster status check"""
    print("╔═══════════════════════════════════════════════════════╗")
    print("║  🦅 QUEZTL CLUSTER STATUS                            ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print()
    
    async with DistributedRoleManager("checker") as manager:
        # Check nodes
        print("🔌 NODES:")
        for node_name, node_info in NODES.items():
            healthy = await manager.check_node_health(node_name)
            status = "✅ ONLINE" if healthy else "❌ OFFLINE"
            print(f"   {node_name.ljust(10)} ({node_info['ip']}) - {status}")
        
        print()
        print("🎭 ROLES:")
        
        # Check roles
        assignments = await manager.discover_roles()
        for role, role_info in ROLES.items():
            if role in assignments:
                node = assignments[role]
                print(f"   ✅ {role.ljust(20)} → {node}")
            else:
                print(f"   ❌ {role.ljust(20)} → NOT RUNNING")
        
        print()
        print("📊 SUMMARY:")
        online_nodes = sum(1 for n in NODES if await manager.check_node_health(n))
        active_roles = len(assignments)
        total_roles = len(ROLES)
        
        print(f"   Nodes:  {online_nodes}/{len(NODES)} online")
        print(f"   Roles:  {active_roles}/{total_roles} active")
        print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--coordinator":
            # Run as coordinator
            node_name = sys.argv[2] if len(sys.argv) > 2 else socket.gethostname()
            asyncio.run(run_coordinator(node_name))
        elif sys.argv[1] == "--status":
            # Just check status
            asyncio.run(check_cluster_status())
        else:
            print("Usage:")
            print("  python3 distributed_roles.py --coordinator [node_name]")
            print("  python3 distributed_roles.py --status")
    else:
        # Default: check status
        asyncio.run(check_cluster_status())
