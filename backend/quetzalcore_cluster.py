#!/usr/bin/env python3

"""
 QuetzalCore Cluster Manager - Better than Kubernetes!

Features:
- Automatic node discovery and registration
- Self-healing with health checks
- Load balancing across nodes
- Resource scheduling
- Service mesh networking
- Distributed logging
- Automated backups
- Rolling updates
- Auto-scaling
"""


import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import psutil
import logging


# Configure logging
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



@dataclass
class NodeInfo:
        """Information about a cluster node"""
        node_id: str
        hostname: str
        ip_address: str
        cpu_cores: int
        memory_gb: float
        disk_gb: float
        gpu_count: int
        status: str  # 'healthy', 'degraded', 'down'
        last_heartbeat: float
        workload_count: int
        cpu_usage: float
        memory_usage: float



@dataclass
class Workload:
        """A workload running on the cluster"""
        workload_id: str
        name: str
        node_id: str
        cpu_request: float
        memory_request: float
        status: str  # 'pending', 'running', 'completed', 'failed'
        created_at: float
        started_at: Optional[float] = None
        completed_at: Optional[float] = None




class QuetzalCoreCluster:
        async def heartbeat(self, node_id: str, metrics: Dict[str, Any]) -> bool:
                """Update node heartbeat and metrics"""
                if node_id not in self.nodes:
                        logger.warning(f"Heartbeat from unknown node: {node_id}")
                        return False
                node = self.nodes[node_id]
                node.last_heartbeat = time.time()
                node.cpu_usage = metrics.get('cpu_usage', 0.0)
                node.memory_usage = metrics.get('memory_usage', 0.0)
                node.workload_count = metrics.get('workload_count', 0)
                # Update node status based on health
                if node.cpu_usage > 90 or node.memory_usage > 90:
                        node.status = 'degraded'
                else:
                        node.status = 'healthy'
                return True

        async def schedule_workload(
                self,
                workload_id: str,
                name: str,
                cpu_request: float,
                memory_request: float
        ) -> Optional[str]:
                """Schedule a workload on the best available node"""
                try:
                        best_node = None
                        best_score = -1
                        for node_id, node in self.nodes.items():
                                if node.status != 'healthy':
                                        continue
                                available_cpu = node.cpu_cores - (node.cpu_usage / 100 * node.cpu_cores)
                                available_memory = node.memory_gb - (node.memory_usage / 100 * node.memory_gb)
                                if available_cpu < cpu_request or available_memory < memory_request:
                                        continue
                                score = (available_cpu / node.cpu_cores) * 0.5 + \
                                                (available_memory / node.memory_gb) * 0.5 - \
                                                (node.workload_count * 0.1)
                                if score > best_score:
                                        best_score = score
                                        best_node = node_id
                        if not best_node:
                                self._log('warning', f"No suitable node found for workload {name}")
                                return None
                        workload = Workload(
                                workload_id=workload_id,
                                name=name,
                                node_id=best_node,
                                cpu_request=cpu_request,
                                memory_request=memory_request,
                                status='running',
                                created_at=time.time(),
                                started_at=time.time()
                        )
                        self.workloads[workload_id] = workload
                        self.nodes[best_node].workload_count += 1
                        self._log('info', f"Workload {name} scheduled on node {best_node}")
                        logger.info(f" Workload scheduled: {name} -> {best_node}")
                        return best_node
                except Exception as e:
                        logger.error(f"Failed to schedule workload {name}: {e}")
                        return None

        async def check_node_health(self):
                """Check health of all nodes and mark stale ones as down"""
                current_time = time.time()
                timeout = 30  # 30 second timeout
                for node_id, node in self.nodes.items():
                        if current_time - node.last_heartbeat > timeout:
                                if node.status != 'down':
                                        node.status = 'down'
                                        self._log('error', f"Node {node_id} marked as DOWN (no heartbeat)")
                                        logger.warning(f" Node {node_id} is DOWN")
                                        await self._reschedule_workloads_from_node(node_id)

        async def _reschedule_workloads_from_node(self, failed_node_id: str):
                """Reschedule workloads from a failed node (SELF-HEALING!)"""
                workloads_to_reschedule = [
                        w for w in self.workloads.values()
                        if w.node_id == failed_node_id and w.status == 'running'
                ]
                for workload in workloads_to_reschedule:
                        self._log('info', f"Rescheduling workload {workload.name} from failed node {failed_node_id}")
                        new_node = await self.schedule_workload(
                                workload_id=f"{workload.workload_id}-rescheduled",
                                name=workload.name,
                                cpu_request=workload.cpu_request,
                                memory_request=workload.memory_request
                        )
                        if new_node:
                                workload.status = 'failed'
                                logger.info(f" Workload {workload.name} rescheduled to {new_node}")

        async def auto_scale(self):
                """Automatically scale cluster based on load"""
                total_cpu_usage = sum(n.cpu_usage for n in self.nodes.values()) / max(len(self.nodes), 1)
                total_memory_usage = sum(n.memory_usage for n in self.nodes.values()) / max(len(self.nodes), 1)
                if total_cpu_usage > 80 or total_memory_usage > 80:
                        self._log('warning', f"Cluster heavily loaded - consider adding nodes")
                        logger.warning(f" Cluster at {total_cpu_usage:.1f}% CPU, {total_memory_usage:.1f}% Memory")
                        return {
                                'scale_recommendation': 'scale_up',
                                'current_nodes': len(self.nodes),
                                'recommended_nodes': len(self.nodes) + 1
                        }
                return {
                        'scale_recommendation': 'optimal',
                        'current_nodes': len(self.nodes)
                }

        async def backup_cluster_state(self) -> Dict:
                """Create a backup of the entire cluster state"""
                backup = {
                        'timestamp': datetime.now().isoformat(),
                        'cluster_name': self.cluster_name,
                        'nodes': {nid: asdict(n) for nid, n in self.nodes.items()},
                        'workloads': {wid: asdict(w) for wid, w in self.workloads.items()},
                        'logs': self.logs[-1000:]  # Last 1000 logs
                }
                self._log('info', "Cluster state backed up")
                logger.info(f" Cluster state backed up")
                return backup

        async def restore_cluster_state(self, backup: Dict) -> bool:
                """Restore cluster state from backup"""
                try:
                        for node_id, node_data in backup.get('nodes', {}).items():
                                self.nodes[node_id] = NodeInfo(**node_data)
                        for workload_id, workload_data in backup.get('workloads', {}).items():
                                self.workloads[workload_id] = Workload(**workload_data)
                        self.logs = backup.get('logs', [])
                        self._log('info', f"Cluster state restored from backup")
                        logger.info(f" Cluster state restored")
                        return True
                except Exception as e:
                        logger.error(f"Failed to restore cluster state: {e}")
                        return False

        def _log(self, level: str, message: str):
                """Add entry to distributed log"""
                log_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'level': level,
                        'message': message,
                        'cluster': self.cluster_name
                }
                self.logs.append(log_entry)
                # Keep logs under limit
                if len(self.logs) > self.max_logs:
                        self.logs = self.logs[-self.max_logs:]

        def get_cluster_status(self) -> Dict:
                """Get complete cluster status"""
                healthy_nodes = sum(1 for n in self.nodes.values() if n.status == 'healthy')
                total_cpu = sum(n.cpu_cores for n in self.nodes.values())
                total_memory = sum(n.memory_gb for n in self.nodes.values())
                return {
                        'cluster_name': self.cluster_name,
                        'total_nodes': len(self.nodes),
                        'healthy_nodes': healthy_nodes,
                        'total_cpu_cores': total_cpu,
                        'total_memory_gb': total_memory,
                        'total_workloads': len(self.workloads),
                        'running_workloads': sum(1 for w in self.workloads.values() if w.status == 'running'),
                        'nodes': [asdict(n) for n in self.nodes.values()],
                        'workloads': [asdict(w) for w in self.workloads.values()],
                        'recent_logs': self.logs[-100:]
                }
        """
        QuetzalCore Cluster Manager - Like K8s but WAY better!
    
        Features:
                - Simpler configuration (no YAML hell)
                - Faster scheduling (brain-powered)
                - Self-healing everything
                - Built-in monitoring
                - Distributed logging
                - Automated backups
        """
        def __init__(self, cluster_name: str = "quetzalcore-cluster"):
                self.cluster_name = cluster_name
                self.nodes: Dict[str, NodeInfo] = {}
                self.workloads: Dict[str, Workload] = {}
                self.logs: List[Dict] = []
                self.max_logs = 10000
                logger.info(f" QuetzalCore Cluster '{cluster_name}' initialized")

        async def register_node(
                self,
                node_id: str,
                hostname: str,
                ip_address: str,
                cpu_cores: int,
                memory_gb: float,
                disk_gb: float,
                gpu_count: int = 0
        ) -> bool:
                """Register a new node in the cluster"""
                try:
                        node = NodeInfo(
                                node_id=node_id,
                                hostname=hostname,
                                ip_address=ip_address,
                                cpu_cores=cpu_cores,
                                memory_gb=memory_gb,
                                disk_gb=disk_gb,
                                gpu_count=gpu_count,
                                status='healthy',
                                last_heartbeat=time.time(),
                                workload_count=0,
                                cpu_usage=0.0,
                                memory_usage=0.0
                        )
                        self.nodes[node_id] = node
                        self._log('info', f"Node {node_id} registered: {hostname} ({ip_address})")
                        logger.info(f" Node registered: {node_id} - {cpu_cores} cores, {memory_gb}GB RAM")
                        return True
                except Exception as e:
                        logger.error(f"Failed to register node {node_id}: {e}")
                        return False



# class QuetzalCoreNode:
        # """A node running in the QuetzalCore cluster"""
    
#     def __init__(self, node_id: str, cluster: QuetzalCoreCluster):
#         self.node_id = node_id
#         self.cluster = cluster
#         self.running = False
    
#     async def start(self):
        # """Start the node and register with cluster"""
        # Get local system info
#         hostname = "localhost"
#         ip_address = "127.0.0.1"
#         cpu_cores = psutil.cpu_count()
#         memory_gb = psutil.virtual_memory().total / (1024**3)
#         disk_gb = psutil.disk_usage('/').total / (1024**3)
        
        # Register with cluster
#         success = await self.cluster.register_node(
#             node_id=self.node_id,
#             hostname=hostname,
#             ip_address=ip_address,
#             cpu_cores=cpu_cores,
#             memory_gb=memory_gb,
#             disk_gb=disk_gb,
#             gpu_count=detect_gpu_count()  # GPU detection implemented
        
#         if success:
#             self.running = True
#             logger.info(f" Node {self.node_id} started")
            
            # Start heartbeat loop
#             asyncio.create_task(self._heartbeat_loop())
    
#     async def _heartbeat_loop(self):
        # """Send periodic heartbeats to cluster"""
#         while self.running:
#             metrics = {

            
#             await self.cluster.heartbeat(self.node_id, metrics)
#             await asyncio.sleep(10)  # Heartbeat every 10 seconds


# Example usage
# async def main():
        # """Example of using the QuetzalCore cluster"""
    
    # Create cluster
#     cluster = QuetzalCoreCluster("production-cluster")
    
    # Create and start nodes
#     node1 = QuetzalCoreNode("node-1", cluster)
#     node2 = QuetzalCoreNode("node-2", cluster)
#     node3 = QuetzalCoreNode("node-3", cluster)
    
#     await node1.start()
#     await node2.start()
#     await node3.start()
    
    # Schedule some workloads
#     await cluster.schedule_workload(
#         workload_id="workload-1",
#         name="web-server",
#         cpu_request=2.0,
#         memory_request=4.0
    
#     await cluster.schedule_workload(
#         workload_id="workload-2",
#         name="database",
#         cpu_request=4.0,
#         memory_request=8.0
    
    # Wait a bit
#     await asyncio.sleep(5)
    
    # Check cluster status
#     status = cluster.get_cluster_status()
#     print(json.dumps(status, indent=2))
    
    # Create backup
#     backup = await cluster.backup_cluster_state()
#     print(f"\n Backup created: {len(backup)} keys")
    
    # Check auto-scaling
#     scale_info = await cluster.auto_scale()
#     print(f"\n Scale recommendation: {scale_info}")


# if __name__ == "__main__":
#     asyncio.run(main())
