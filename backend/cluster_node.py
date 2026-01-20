#!/usr/bin/env python3
"""
QUEZTL CLUSTER NODE - Real Distributed Computing
Every machine (Mac, Beast, Sloth, Optiplexes) runs this to join cluster

Star Trek TNG Computer Vision:
- Self-organizing mesh network
- Instant cluster join/leave
- Work distribution across all nodes
- Real-time resource sharing
"""

import asyncio
import aiohttp
import socket
import psutil
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
import logging

# DHCP-safe discovery / role detection
try:
    from backend.queztl_discovery import seed_nodes, is_command_center
except ImportError:  # pragma: no cover
    from queztl_discovery import seed_nodes, is_command_center


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cluster discovery
CLUSTER_PORT = 9000
COORDINATOR_PORTS = [9001, 9002, 9003]  # Multiple coordinators for HA

class ClusterNode:
    """
    A node in the Queztl cluster
    Can be: Mac, Beast, Sloth, Optiplex - doesn't matter
    All contribute their power to the collective
    """
    
    def __init__(self, node_name: Optional[str] = None):
        self.node_name = node_name or socket.gethostname()
        self.node_id = f"{self.node_name}_{int(time.time())}"
        self.ip = self._get_local_ip()
        self.capabilities = self._detect_capabilities()
        self.peers: Set[str] = set()
        self.workload_queue = asyncio.Queue()
        self.results_queue = asyncio.Queue()
        self.is_running = False
        self.stats = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "cpu_contribution": 0.0,
            "network_bytes_sent": 0,
            "network_bytes_received": 0,
            "uptime_start": datetime.now().isoformat()
        }
    
    def _get_local_ip(self) -> str:
        """Get this machine's IP on local network"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def _detect_capabilities(self) -> Dict:
        """Detect what this node can contribute"""
        cpu_count = psutil.cpu_count(logical=True)
        mem_gb = psutil.virtual_memory().total / (1024**3)
        
        capabilities = {
            "cpu_cores": cpu_count,
            "memory_gb": round(mem_gb, 2),
            "cpu_freq_mhz": psutil.cpu_freq().max if psutil.cpu_freq() else 0,
            "can_compute": not is_command_center(),
            "can_store": True,
            "can_coordinate": True
        }
        
        # Check for GPU
        try:
            import torch
            if torch.cuda.is_available():
                capabilities["gpu"] = "NVIDIA CUDA"
                capabilities["gpu_count"] = torch.cuda.device_count()
            elif torch.backends.mps.is_available():
                capabilities["gpu"] = "Apple Metal"
                capabilities["gpu_count"] = 1
        except:
            pass
        
        # Check for specialized tools
        try:
            import numpy
            capabilities["numpy"] = True
        except:
            pass
        
        try:
            from diffusers import StableDiffusionPipeline
            capabilities["stable_diffusion"] = True
        except:
            pass
        
        return capabilities
    
    async def announce_to_cluster(self):
        """Broadcast presence to cluster using UDP multicast"""
        # Use discovery (env vars or nmap/ssh probing) to find seed nodes.
        known_ips = seed_nodes()
        
        announcement = {
            "node_id": self.node_id,
            "node_name": self.node_name,
            "ip": self.ip,
            "port": CLUSTER_PORT,
            "capabilities": self.capabilities,
            "timestamp": datetime.now().isoformat()
        }
        
        async with aiohttp.ClientSession() as session:
            for ip in known_ips:
                if ip == self.ip:
                    continue
                try:
                    url = f"http://{ip}:{CLUSTER_PORT}/cluster/join"
                    async with session.post(url, json=announcement, timeout=aiohttp.ClientTimeout(total=2)) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            self.peers.add(ip)
                            logger.info(f"✅ Connected to peer: {ip}")
                except Exception as e:
                    logger.debug(f"Could not reach {ip}: {e}")
    
    async def request_work(self) -> Optional[Dict]:
        """Request work from coordinator or peers"""
        # Try all peers
        for peer_ip in self.peers:
            try:
                async with aiohttp.ClientSession() as session:
                    url = f"http://{peer_ip}:{CLUSTER_PORT}/cluster/work/request"
                    async with session.post(url, json={
                        "node_id": self.node_id,
                        "capabilities": self.capabilities
                    }, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                        if resp.status == 200:
                            work = await resp.json()
                            if work.get("task"):
                                logger.info(f"📥 Received work from {peer_ip}: {work['task'].get('type')}")
                                self.stats["network_bytes_received"] += len(json.dumps(work))
                                return work
            except Exception as e:
                logger.debug(f"No work from {peer_ip}: {e}")
        
        return None
    
    async def execute_task(self, task: Dict) -> Dict:
        """Execute a task using this node's resources"""
        task_type = task.get("type")
        task_id = task.get("task_id")
        
        logger.info(f"⚙️  Executing task {task_id}: {task_type}")
        start_time = time.time()
        
        try:
            if not self.capabilities.get("can_compute", True) and task_type in {"compute", "generate_image"}:
                return {"error": "This node is command-center only (no compute).", "task_id": task_id}

            if task_type == "compute":
                result = await self._compute_task(task)
            elif task_type == "generate_image":
                result = await self._generate_image_task(task)
            elif task_type == "generate_content":
                result = await self._generate_content_task(task)
            else:
                result = {"error": f"Unknown task type: {task_type}"}
            
            elapsed = time.time() - start_time
            self.stats["tasks_completed"] += 1
            self.stats["cpu_contribution"] += elapsed
            
            logger.info(f"✅ Task {task_id} completed in {elapsed:.2f}s")
            
            return {
                "task_id": task_id,
                "node_id": self.node_id,
                "status": "completed",
                "result": result,
                "execution_time": elapsed
            }
            
        except Exception as e:
            self.stats["tasks_failed"] += 1
            logger.error(f"❌ Task {task_id} failed: {e}")
            return {
                "task_id": task_id,
                "node_id": self.node_id,
                "status": "failed",
                "error": str(e)
            }
    
    async def _compute_task(self, task: Dict) -> Dict:
        """CPU-intensive computation"""
        import numpy as np
        
        operation = task.get("operation", "matrix_multiply")
        size = task.get("size", 1000)
        
        if operation == "matrix_multiply":
            # Matrix multiplication - uses CPU cores
            a = np.random.rand(size, size)
            b = np.random.rand(size, size)
            result = np.dot(a, b)
            return {
                "operation": "matrix_multiply",
                "size": size,
                "result_shape": result.shape,
                "result_sum": float(result.sum())
            }
        
        elif operation == "prime_generation":
            # Generate prime numbers
            count = task.get("count", 1000)
            primes = []
            num = 2
            while len(primes) < count:
                if all(num % p != 0 for p in primes):
                    primes.append(num)
                num += 1
            return {
                "operation": "prime_generation",
                "count": len(primes),
                "largest_prime": primes[-1]
            }
        
        return {"error": "Unknown computation operation"}
    
    async def _generate_image_task(self, task: Dict) -> Dict:
        """AI image generation"""
        if not self.capabilities.get("stable_diffusion"):
            return {"error": "Stable Diffusion not available on this node"}
        
        from diffusers import StableDiffusionPipeline
        import torch
        
        prompt = task.get("prompt", "revolutionary workers united")
        theme = task.get("theme", "general")
        
        device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16 if device != "cpu" else torch.float32
        )
        pipe = pipe.to(device)
        
        image = pipe(
            prompt=prompt,
            num_inference_steps=20,
            guidance_scale=7.5
        ).images[0]
        
        # Save image
        output_dir = Path.home() / "queztl-core" / "nm-socialists-project" / "frontend" / "generated"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{theme}_{int(time.time())}.png"
        image.save(output_path)
        
        return {
            "operation": "image_generation",
            "theme": theme,
            "output_path": str(output_path),
            "device_used": device
        }
    
    async def _generate_content_task(self, task: Dict) -> Dict:
        """Generate text content"""
        section = task.get("section", "who_we_are")
        
        content_templates = {
            "who_we_are": """
# Who We Are

The New Mexico Socialists are a revolutionary organization fighting for workers' 
power and indigenous liberation in the Land of Enchantment. We stand in solidarity 
with the working class, indigenous peoples, and all oppressed communities.

## Our Mission

We organize for:
- Economic justice and workers' rights
- Indigenous sovereignty and land back
- Housing as a human right
- Abolition of ICE and police reform
- Environmental justice and water rights

## Our History

Founded by workers and activists in New Mexico, we carry forward the legacy of 
labor struggles, indigenous resistance, and revolutionary movements that have 
shaped our state.

Join us in building a better world! ¡La lucha sigue!
            """,
            
            "get_involved": """
# Get Involved

There are many ways to join the struggle for liberation:

## Attend Meetings
We meet monthly to discuss strategy, plan actions, and build community.

## Join a Working Group
- Labor organizing
- Mutual aid
- Political education
- Community defense

## Volunteer
Help with events, outreach, and organizing campaigns.

## Donate
Support our work building working-class power in New Mexico.

Solidarity Forever! ✊
            """,
            
            "resources": """
# Resources

## Study Materials
- Communist Manifesto - Karl Marx & Friedrich Engels
- Pedagogy of the Oppressed - Paulo Freire
- Red Nation Rising - The Red Nation
- A People's History of the United States - Howard Zinn

## Organizations
- Party for Socialism and Liberation (PSL)
- The Red Nation
- Democratic Socialists of America (DSA)
- Liberation News

## Local Support
- Mutual aid networks
- Food banks and community kitchens
- Legal defense funds
- Housing advocacy groups
            """
        }
        
        content = content_templates.get(section, "Content coming soon...")
        
        return {
            "section": section,
            "content": content,
            "generated_at": datetime.now().isoformat()
        }
    
    async def submit_result(self, result: Dict):
        """Send completed work back to coordinator/peers"""
        for peer_ip in self.peers:
            try:
                async with aiohttp.ClientSession() as session:
                    url = f"http://{peer_ip}:{CLUSTER_PORT}/cluster/work/complete"
                    async with session.post(url, json=result, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                        if resp.status == 200:
                            logger.info(f"📤 Result submitted to {peer_ip}")
                            self.stats["network_bytes_sent"] += len(json.dumps(result))
                            return
            except Exception as e:
                logger.debug(f"Could not submit to {peer_ip}: {e}")
    
    async def worker_loop(self):
        """Main worker loop - continuously request and execute work"""
        logger.info(f"🔄 Worker loop started on {self.node_name}")
        
        while self.is_running:
            try:
                # Request work from cluster
                work = await self.request_work()
                
                if work and work.get("task"):
                    # Execute the task
                    result = await self.execute_task(work["task"])
                    
                    # Submit result back
                    await self.submit_result(result)
                else:
                    # No work available, wait a bit
                    await asyncio.sleep(5)
                    
            except Exception as e:
                logger.error(f"Worker loop error: {e}")
                await asyncio.sleep(5)
    
    async def stats_reporter(self):
        """Periodically report stats"""
        while self.is_running:
            logger.info(f"📊 Node Stats: {self.stats['tasks_completed']} completed, "
                       f"{self.stats['cpu_contribution']:.2f}s CPU, "
                       f"{len(self.peers)} peers")
            await asyncio.sleep(30)
    
    async def start(self):
        """Start this node and join the cluster"""
        logger.info(f"🚀 Starting cluster node: {self.node_name}")
        logger.info(f"   IP: {self.ip}")
        logger.info(f"   Capabilities: {self.capabilities}")
        
        self.is_running = True
        
        # Announce to cluster
        await self.announce_to_cluster()
        
        # Start worker tasks
        tasks = [
            asyncio.create_task(self.worker_loop()),
            asyncio.create_task(self.stats_reporter())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logger.info("⏹️  Stopping cluster node...")
            self.is_running = False
            for task in tasks:
                task.cancel()


async def main():
    """Run as cluster node"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Queztl Cluster Node")
    parser.add_argument("--name", type=str, help="Node name (default: hostname)")
    
    args = parser.parse_args()
    
    node = ClusterNode(node_name=args.name)
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🌐 QUEZTL CLUSTER NODE STARTING                            ║
╚══════════════════════════════════════════════════════════════╝

Node: {node.node_name}
IP:   {node.ip}
ID:   {node.node_id}

Capabilities:
""")
    for key, value in node.capabilities.items():
        print(f"  • {key}: {value}")
    
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This machine is now contributing to the Queztl cluster!
Real network traffic and distributed computing happening now.

Press Ctrl+C to stop.
""")
    
    await node.start()


if __name__ == "__main__":
    asyncio.run(main())
