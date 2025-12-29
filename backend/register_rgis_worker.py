#!/usr/bin/env python3
"""
🌐 RGIS.com Worker Node Registration
Connect RGIS.com infrastructure to QuetzalCore distributed network

Deploy this script on RGIS.com servers to add them as compute nodes.
"""

import asyncio
import aiohttp
import argparse
import socket
import platform
import psutil
import hashlib
import time
import sys
from typing import Dict, Any


class RGISWorkerNode:
    """Worker node that registers with QuetzalCore master"""
    
    def __init__(self, master_url: str, rgis_domain: str = "RGIS.com", port: int = 8001):
        self.master_url = master_url.rstrip('/')
        self.rgis_domain = rgis_domain
        self.port = port
        self.node_id = None
        self.running = False
        
    def get_node_info(self) -> Dict[str, Any]:
        """Gather node information for registration"""
        hostname = socket.gethostname()
        
        # Add RGIS domain identifier
        full_hostname = f"{hostname}.{self.rgis_domain}"
        
        # Create unique node ID
        self.node_id = hashlib.sha256(full_hostname.encode()).hexdigest()[:16]
        
        # Detect GPU
        has_cuda = False
        gpu_model = None
        gpu_vram_gb = 0.0
        
        try:
            import torch
            if torch.cuda.is_available():
                has_cuda = True
                gpu_model = torch.cuda.get_device_name(0)
                gpu_vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        except:
            pass
        
        # Determine node type
        if has_cuda:
            node_type = "worker_gpu"
            capabilities = ["cuda", "webgl", "webgpu", "cpu_simd"]
        elif platform.system() == "Darwin" and platform.machine() in ["arm64", "aarch64"]:
            node_type = "worker_ane"
            capabilities = ["metal", "ane_ml", "webgl", "webgpu", "cpu_simd"]
        else:
            node_type = "worker_cpu"
            capabilities = ["webgl", "webgpu", "cpu_simd"]
        
        # Get IP address
        try:
            ip_address = socket.gethostbyname(socket.gethostname())
        except:
            ip_address = "127.0.0.1"
        
        return {
            "node_id": self.node_id,
            "hostname": full_hostname,
            "ip_address": ip_address,
            "port": self.port,
            "capabilities": {
                "node_type": node_type,
                "compute_apis": capabilities,
                "cpu_cores": psutil.cpu_count(logical=False),
                "cpu_threads": psutil.cpu_count(logical=True),
                "ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "gpu_vram_gb": round(gpu_vram_gb, 2),
                "gpu_model": gpu_model,
                "os": platform.system(),
                "arch": platform.machine(),
                "has_ane": (node_type == "worker_ane"),
                "max_concurrent_tasks": psutil.cpu_count(logical=True)
            }
        }
    
    async def register(self) -> bool:
        """Register this node with the master coordinator"""
        node_info = self.get_node_info()
        
        print(f"🌐 Registering RGIS worker: {node_info['hostname']}")
        print(f"   Node ID: {node_info['node_id']}")
        print(f"   Type: {node_info['capabilities']['node_type']}")
        print(f"   CPUs: {node_info['capabilities']['cpu_cores']} cores, {node_info['capabilities']['cpu_threads']} threads")
        print(f"   RAM: {node_info['capabilities']['ram_gb']} GB")
        if node_info['capabilities']['gpu_model']:
            print(f"   GPU: {node_info['capabilities']['gpu_model']} ({node_info['capabilities']['gpu_vram_gb']} GB)")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.master_url}/api/v1.2/nodes/register",
                    json=node_info,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"✅ Registration successful!")
                        print(f"   Network has {result.get('total_nodes', '?')} nodes")
                        return True
                    else:
                        error = await response.text()
                        print(f"❌ Registration failed: {error}")
                        return False
        except Exception as e:
            print(f"❌ Could not connect to master: {e}")
            return False
    
    async def send_heartbeat(self) -> bool:
        """Send heartbeat to master"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.master_url}/api/v1.2/nodes/{self.node_id}/heartbeat",
                    json={
                        "load": psutil.cpu_percent() / 100.0,
                        "active_tasks": 0,  # TODO: Track actual tasks
                        "available": True
                    },
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    return response.status == 200
        except:
            return False
    
    async def heartbeat_loop(self):
        """Send periodic heartbeats"""
        while self.running:
            success = await self.send_heartbeat()
            if not success:
                print("⚠️ Heartbeat failed")
            await asyncio.sleep(10)
    
    async def run(self):
        """Run the worker node"""
        # Register with master
        if not await self.register():
            print("❌ Could not register with master. Exiting.")
            return
        
        # Start heartbeat
        self.running = True
        print(f"\n💓 Worker running. Sending heartbeats every 10s...")
        print(f"   Press Ctrl+C to stop\n")
        
        try:
            await self.heartbeat_loop()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down worker...")
            self.running = False


async def main():
    parser = argparse.ArgumentParser(
        description="Register RGIS.com server as QuetzalCore worker node"
    )
    parser.add_argument(
        "master_url",
        help="URL of QuetzalCore master coordinator (e.g., http://localhost:8000)"
    )
    parser.add_argument(
        "--domain",
        default="RGIS.com",
        help="RGIS domain identifier (default: RGIS.com)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        help="Local port for this worker (default: 8001)"
    )
    
    args = parser.parse_args()
    
    # Create and run worker
    worker = RGISWorkerNode(
        master_url=args.master_url,
        rgis_domain=args.domain,
        port=args.port
    )
    
    await worker.run()


if __name__ == "__main__":
    print("=" * 70)
    print("🌐 RGIS.COM WORKER NODE")
    print("   Connecting to QuetzalCore Distributed Network")
    print("=" * 70)
    print()
    
    asyncio.run(main())
