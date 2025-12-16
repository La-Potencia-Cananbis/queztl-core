"""
#  DYNAMIC AUTO-SCALER FOR QUETZALCORE DISTRIBUTED NETWORK
# Automatically scales nodes up/down based on load

# Features:
- Load-based scaling (CPU, memory, task queue depth)
- Predictive scaling (ML-based demand forecasting)
- Cloud provider integration (AWS, GCP, Azure)
- Cost optimization (spot instances, preemptible VMs)
- Geographic distribution (edge computing)
- Health monitoring and auto-healing

================================================================================
# Copyright (c) 2025 QuetzalCore-Core Project
# Patent Pending
================================================================================
"""

# import asyncio
# import time
# import numpy as np
# from typing import Dict, List, Optional, Any, Tuple
# from dataclasses import dataclass, field
# from enum import Enum
# import logging
# from collections import deque

# from .distributed_network import (
#     NodeRegistry, DistributedScheduler, ComputeNode, NodeType,
#     NodeCapabilities, ComputeCapability

# logger = logging.getLogger(__name__)


# ============================================================================
# SCALING POLICIES
# ============================================================================

# class ScalingPolicy(Enum):
    """Auto-scaling policies"""
#     REACTIVE = "reactive"           # React to current load
#     PREDICTIVE = "predictive"       # ML-based forecasting
#     SCHEDULED = "scheduled"         # Time-based scaling
#     COST_OPTIMIZED = "cost_optimized"  # Minimize cost
#     PERFORMANCE = "performance"     # Maximize performance


@dataclass
# class ScalingMetrics:
    """Metrics used for scaling decisions"""
#     timestamp: float = field(default_factory=time.time)
    
    # Task metrics
#     pending_tasks: int = 0
#     active_tasks: int = 0
#     completed_tasks: int = 0
#     failed_tasks: int = 0
#     avg_task_duration: float = 0.0
    
    # Node metrics
#     total_nodes: int = 0
#     available_nodes: int = 0
#     busy_nodes: int = 0
#     offline_nodes: int = 0
    
    # Resource metrics
#     avg_cpu_usage: float = 0.0
#     avg_memory_usage: float = 0.0
#     avg_queue_depth: float = 0.0
    
    # Performance metrics
#     tasks_per_second: float = 0.0
#     avg_response_time: float = 0.0
#     success_rate: float = 1.0


@dataclass
# class ScalingTarget:
    """Desired scaling configuration"""
#     min_nodes: int = 1
#     max_nodes: int = 100
#     target_cpu_utilization: float = 0.70
#     target_queue_depth: int = 10
#     scale_up_threshold: float = 0.85
#     scale_down_threshold: float = 0.30
#     cooldown_seconds: float = 300.0  # 5 minutes between scaling actions


# ============================================================================
# CLOUD PROVIDER INTERFACE
# ============================================================================

# class CloudProvider(Enum):
    """Supported cloud providers"""
#     AWS = "aws"
#     GCP = "gcp"
#     AZURE = "azure"
#     LOCAL = "local"  # Local VMs or bare metal
#     DOCKER = "docker"  # Docker containers


@dataclass
# class NodeTemplate:
    """Template for creating new nodes"""
#     provider: CloudProvider
#     instance_type: str
#     image_id: str
#     region: str
#     zone: Optional[str] = None
    
    # Hardware specs (for estimation)
#     cpu_cores: int = 2
#     ram_gb: float = 8.0
#     gpu_vram_gb: float = 0.0
    
    # Cost (USD per hour)
#     cost_per_hour: float = 0.10
#     spot_instance: bool = False
    
    # Startup script
#     startup_script: Optional[str] = None
    
    # Capabilities
#     node_type: NodeType = NodeType.WORKER_CPU
#     capabilities: List[ComputeCapability] = field(default_factory=list)


# class CloudProviderAdapter:
    """
#     Abstract adapter for cloud provider APIs
#     Implement this for each cloud provider
    """
    
#     async def launch_instance(self, template: NodeTemplate) -> str:
        """
#         Launch a new compute instance
#         Returns: instance_id
        """
#         raise NotImplementedError
    
#     async def terminate_instance(self, instance_id: str):
        """Terminate a compute instance"""
#         raise NotImplementedError
    
#     async def get_instance_status(self, instance_id: str) -> str:
        """Get instance status (running, stopped, etc.)"""
#         raise NotImplementedError
    
#     async def list_instances(self) -> List[Dict[str, Any]]:
        """List all instances"""
#         raise NotImplementedError


# class LocalDockerAdapter(CloudProviderAdapter):
    """
#     Adapter for local Docker containers
#     Fastest for development and testing
    """
    
#     def __init__(self):
#         self.containers: Dict[str, Dict[str, Any]] = {}
    
#     async def launch_instance(self, template: NodeTemplate) -> str:
        """Launch Docker container as worker node"""
#         import uuid
#         instance_id = f"docker-{uuid.uuid4().hex[:8]}"
        
        # In production, would use Docker SDK:
        # import docker
        # client = docker.from_env()
        # container = client.containers.run(
        #     image="quetzalcore-worker:latest",
        #     detach=True,
        #     environment={
        #         "COORDINATOR_URL": "http://master:8000",
        #         "NODE_TYPE": template.node_type.value
        #     }
        # )
        
        # For now, simulate
#         self.containers[instance_id] = {
            "status": "running",
            "template": template,
            "started_at": time.time()
        }
        
#         logger.info(f"Launched Docker container: {instance_id}")
#         return instance_id
    
#     async def terminate_instance(self, instance_id: str):
        """Stop Docker container"""
#         if instance_id in self.containers:
            # In production: container.stop()
#             del self.containers[instance_id]
#             logger.info(f"Terminated Docker container: {instance_id}")
    
#     async def get_instance_status(self, instance_id: str) -> str:
#         if instance_id in self.containers:
#             return self.containers[instance_id]["status"]
#         return "terminated"
    
#     async def list_instances(self) -> List[Dict[str, Any]]:
#         return [
            {"instance_id": iid, **info}
#             for iid, info in self.containers.items()
        ]


# class AWSAdapter(CloudProviderAdapter):
    """
#     Adapter for AWS EC2
    """
    
#     def __init__(self, region: str = "us-east-1"):
#         self.region = region
        # In production: import boto3; self.ec2 = boto3.client('ec2', region_name=region)
    
#     async def launch_instance(self, template: NodeTemplate) -> str:
        """Launch EC2 instance"""
        # In production:
        # response = self.ec2.run_instances(
        #     ImageId=template.image_id,
        #     InstanceType=template.instance_type,
        #     MinCount=1,
        #     MaxCount=1,
        #     UserData=template.startup_script,
        #     InstanceMarketOptions={
        #         'MarketType': 'spot' if template.spot_instance else 'on-demand'
        #     }
        # )
        # return response['Instances'][0]['InstanceId']
        
#         import uuid
#         instance_id = f"i-{uuid.uuid4().hex[:8]}"
#         logger.info(f"Launched AWS EC2 instance: {instance_id}")
#         return instance_id
    
#     async def terminate_instance(self, instance_id: str):
        """Terminate EC2 instance"""
        # In production: self.ec2.terminate_instances(InstanceIds=[instance_id])
#         logger.info(f"Terminated AWS EC2 instance: {instance_id}")
    
#     async def get_instance_status(self, instance_id: str) -> str:
        # In production: self.ec2.describe_instances(InstanceIds=[instance_id])
#         return "running"
    
#     async def list_instances(self) -> List[Dict[str, Any]]:
        # In production: self.ec2.describe_instances()
#         return []


# ============================================================================
# AUTO-SCALER
# ============================================================================

# class AutoScaler:
    """
#     Intelligent auto-scaler for distributed network
#     Monitors load and scales nodes dynamically
    """
    
#     def __init__(
#         self,
#         registry: NodeRegistry,
#         scheduler: DistributedScheduler,
#         policy: ScalingPolicy = ScalingPolicy.REACTIVE,
#         target: ScalingTarget = None
    ):
#         self.registry = registry
#         self.scheduler = scheduler
#         self.policy = policy
#         self.target = target or ScalingTarget()
        
        # Metrics history for ML forecasting
#         self.metrics_history: deque = deque(maxlen=1000)
        
        # Cloud provider adapters
#         self.providers: Dict[CloudProvider, CloudProviderAdapter] = {
#             CloudProvider.LOCAL: LocalDockerAdapter(),
#             CloudProvider.DOCKER: LocalDockerAdapter(),
            # CloudProvider.AWS: AWSAdapter(),
            # Add more as needed
        }
        
        # Managed instances
#         self.managed_instances: Dict[str, Dict[str, Any]] = {}
        
        # Scaling state
#         self.last_scale_action: float = 0.0
#         self.scaling_in_progress: bool = False
        
        # Performance tracking
#         self.scale_up_count: int = 0
#         self.scale_down_count: int = 0
        
#     async def collect_metrics(self) -> ScalingMetrics:
        """Collect current system metrics"""
        # Get scheduler stats
#         sched_stats = self.scheduler.get_stats()
        
        # Get registry stats
#         reg_stats = self.registry.get_stats()
        
        # Calculate averages
#         total_nodes = len(self.registry.nodes)
#         if total_nodes > 0:
#             avg_cpu = np.mean([
#                 node.capabilities.current_load
#                 for node in self.registry.nodes.values()
            ])
#             avg_queue = sched_stats['pending_tasks'] / max(reg_stats['available_nodes'], 1)
#         else:
#             avg_cpu = 0.0
#             avg_queue = float('inf') if sched_stats['pending_tasks'] > 0 else 0.0
        
#         metrics = ScalingMetrics(
#             pending_tasks=sched_stats['pending_tasks'],
#             active_tasks=sched_stats['active_tasks'],
#             completed_tasks=sched_stats['completed_tasks'],
#             total_nodes=total_nodes,
#             available_nodes=reg_stats['available_nodes'],
#             busy_nodes=total_nodes - reg_stats['available_nodes'],
#             avg_cpu_usage=avg_cpu,
#             avg_queue_depth=avg_queue,
#             tasks_per_second=sched_stats.get('tasks_per_second', 0),
#             success_rate=sched_stats.get('success_rate', 1.0)
        
#         self.metrics_history.append(metrics)
#         return metrics
    
#     def should_scale_up(self, metrics: ScalingMetrics) -> Tuple[bool, str]:
        """Determine if we should scale up"""
#         reasons = []
        
        # Check if we're at max capacity
#         if self.target.max_nodes <= metrics.total_nodes:
#             return False, "At maximum node count"
        
        # Check cooldown period
#         if time.time() - self.last_scale_action < self.target.cooldown_seconds:
#             return False, "In cooldown period"
        
        # Check CPU utilization
#         if metrics.avg_cpu_usage > self.target.scale_up_threshold:
#             reasons.append(f"High CPU: {metrics.avg_cpu_usage:.1%}")
        
        # Check queue depth
#         if metrics.avg_queue_depth > self.target.target_queue_depth:
#             reasons.append(f"High queue: {metrics.avg_queue_depth:.0f} tasks/node")
        
        # Check if no available nodes
#         if metrics.available_nodes == 0 and metrics.pending_tasks > 0:
#             reasons.append("No available nodes")
        
#         if reasons:
#             return True, "; ".join(reasons)
        
#         return False, ""
    
#     def should_scale_down(self, metrics: ScalingMetrics) -> Tuple[bool, str]:
        """Determine if we should scale down"""
        # Check if we're at minimum capacity
#         if self.target.min_nodes >= metrics.total_nodes:
#             return False, "At minimum node count"
        
        # Check cooldown period
#         if time.time() - self.last_scale_action < self.target.cooldown_seconds:
#             return False, "In cooldown period"
        
        # Check CPU utilization
#         if metrics.avg_cpu_usage < self.target.scale_down_threshold:
            # Check if we have idle nodes
#             idle_capacity = metrics.available_nodes / max(metrics.total_nodes, 1)
#             if idle_capacity > 0.5:  # More than 50% idle
#                 return True, f"Low CPU: {metrics.avg_cpu_usage:.1%}, {idle_capacity:.0%} idle"
        
#         return False, ""
    
#     def calculate_desired_nodes(self, metrics: ScalingMetrics) -> int:
        """Calculate optimal number of nodes"""
#         if self.policy == ScalingPolicy.REACTIVE:
            # Reactive: based on current load
            
            # Estimate based on CPU utilization
#             cpu_based = int(np.ceil(
#                 metrics.total_nodes * metrics.avg_cpu_usage / self.target.target_cpu_utilization
            ))
            
            # Estimate based on queue depth
#             queue_based = int(np.ceil(
#                 metrics.pending_tasks / self.target.target_queue_depth
            )) + metrics.busy_nodes
            
            # Take the max
#             desired = max(cpu_based, queue_based)
        
#         elif self.policy == ScalingPolicy.PREDICTIVE:
            # Predictive: use ML forecasting
#             desired = self._predict_required_nodes(metrics)
        
#         elif self.policy == ScalingPolicy.COST_OPTIMIZED:
            # Cost-optimized: minimize cost while meeting SLA
#             desired = self._optimize_for_cost(metrics)
        
#         else:
            # Default to current + 1 if overloaded, -1 if underutilized
#             if metrics.avg_cpu_usage > self.target.scale_up_threshold:
#                 desired = metrics.total_nodes + 1
#             elif metrics.avg_cpu_usage < self.target.scale_down_threshold:
#                 desired = metrics.total_nodes - 1
#             else:
#                 desired = metrics.total_nodes
        
        # Clamp to min/max
#         desired = max(self.target.min_nodes, min(self.target.max_nodes, desired))
        
#         return desired
    
#     def _predict_required_nodes(self, current_metrics: ScalingMetrics) -> int:
        """
#         Use ML to predict required nodes based on historical patterns
#         Simple moving average for now, can upgrade to LSTM/Prophet
        """
#         if len(self.metrics_history) < 10:
#             return current_metrics.total_nodes
        
        # Look at task arrival rate trend
#         recent_metrics = list(self.metrics_history)[-10:]
#         task_rates = [m.tasks_per_second for m in recent_metrics]
        
        # Simple linear regression to predict next interval
#         x = np.arange(len(task_rates))
#         coeffs = np.polyfit(x, task_rates, deg=1)
#         predicted_rate = np.polyval(coeffs, len(task_rates))
        
        # Estimate nodes needed
#         avg_tasks_per_node = 10  # Configurable
#         predicted_nodes = int(np.ceil(predicted_rate * 60 / avg_tasks_per_node))
        
        # Add buffer for safety
#         predicted_nodes = int(predicted_nodes * 1.2)
        
#         return max(self.target.min_nodes, predicted_nodes)
    
#     def _optimize_for_cost(self, metrics: ScalingMetrics) -> int:
        """
#         Optimize for minimum cost while meeting SLA
#         Uses spot instances when possible
        """
        # Calculate minimum nodes to meet SLA
#         required_capacity = metrics.pending_tasks + metrics.active_tasks
#         avg_capacity_per_node = 10  # tasks
        
#         min_nodes_for_sla = int(np.ceil(required_capacity / avg_capacity_per_node))
        
        # Use spot instances for extra capacity
        # Keep on-demand for baseline
#         baseline_nodes = self.target.min_nodes
#         spot_nodes = max(0, min_nodes_for_sla - baseline_nodes)
        
#         return baseline_nodes + spot_nodes
    
#     async def scale_up(self, count: int = 1, template: NodeTemplate = None):
        """Add new nodes"""
#         if template is None:
            # Default template
#             template = NodeTemplate(
#                 provider=CloudProvider.DOCKER,
#                 instance_type="standard",
#                 image_id="quetzalcore-worker:latest",
#                 region="local",
#                 cpu_cores=4,
#                 ram_gb=8.0,
#                 node_type=NodeType.WORKER_CPU,
#                 capabilities=[
#                     ComputeCapability.CPU_SIMD,
#                     ComputeCapability.WEBGL,
#                     ComputeCapability.WEBGPU
                ]
        
#         logger.info(f" Scaling UP: Adding {count} nodes...")
        
#         for i in range(count):
#             try:
                # Get cloud provider
#                 provider = self.providers[template.provider]
                
                # Launch instance
#                 instance_id = await provider.launch_instance(template)
                
                # Track instance
#                 self.managed_instances[instance_id] = {
                    "template": template,
                    "launched_at": time.time(),
                    "status": "launching"
                }
                
                # Wait for node to register (in production, would poll)
                # For now, simulate by creating node entry
#                 await asyncio.sleep(2)  # Simulate startup time
                
#                 logger.info(f" Node {instance_id} launched successfully")
                
#             except Exception as e:
#                 logger.error(f" Failed to launch node: {e}")
        
#         self.scale_up_count += count
#         self.last_scale_action = time.time()
    
#     async def scale_down(self, count: int = 1):
        """Remove nodes"""
#         logger.info(f" Scaling DOWN: Removing {count} nodes...")
        
        # Find nodes to remove (prefer idle nodes)
#         available_nodes = await self.registry.get_available_nodes()
        
        # Sort by least loaded
#         available_nodes.sort(key=lambda n: n.capabilities.current_load)
        
#         removed = 0
#         for node in available_nodes[:count]:
            # Don't remove master
#             if node.capabilities.node_type == NodeType.MASTER:
#                 continue
            
            # Find instance ID
#             instance_id = None
#             for iid, info in self.managed_instances.items():
                # Match by node_id or other identifier
#                 instance_id = iid
#                 break
            
#             if instance_id:
#                 try:
                    # Get provider
#                     template = self.managed_instances[instance_id]["template"]
#                     provider = self.providers[template.provider]
                    
                    # Terminate instance
#                     await provider.terminate_instance(instance_id)
                    
                    # Unregister from registry
#                     await self.registry.unregister_node(node.node_id)
                    
                    # Remove from tracking
#                     del self.managed_instances[instance_id]
                    
#                     logger.info(f" Node {instance_id} terminated")
#                     removed += 1
                    
#                 except Exception as e:
#                     logger.error(f" Failed to terminate node: {e}")
        
#         self.scale_down_count += removed
#         self.last_scale_action = time.time()
    
#     async def run_scaling_loop(self):
        """Main auto-scaling loop"""
#         logger.info(" Auto-scaler started")
        
#         while True:
#             try:
                # Collect metrics
#                 metrics = await self.collect_metrics()
                
                # Check if scaling action needed
#                 should_up, up_reason = self.should_scale_up(metrics)
#                 should_down, down_reason = self.should_scale_down(metrics)
                
#                 if should_up:
                    # Calculate how many nodes to add
#                     desired = self.calculate_desired_nodes(metrics)
#                     to_add = desired - metrics.total_nodes
                    
#                     logger.info(f" {up_reason}")
#                     await self.scale_up(to_add)
                
#                 elif should_down:
                    # Calculate how many nodes to remove
#                     desired = self.calculate_desired_nodes(metrics)
#                     to_remove = metrics.total_nodes - desired
                    
#                     logger.info(f" {down_reason}")
#                     await self.scale_down(to_remove)
                
#                 else:
#                     logger.debug(
#                         f" Metrics: {metrics.total_nodes} nodes, "
#                         f"{metrics.avg_cpu_usage:.1%} CPU, "
#                         f"{metrics.pending_tasks} pending tasks"
                
#             except Exception as e:
#                 logger.error(f" Error in scaling loop: {e}")
            
            # Check every 30 seconds
#             await asyncio.sleep(30)
    
#     def get_stats(self) -> Dict[str, Any]:
        """Get auto-scaler statistics"""
#         return {
            "policy": self.policy.value,
            "target": {
                "min_nodes": self.target.min_nodes,
                "max_nodes": self.target.max_nodes,
                "target_cpu": self.target.target_cpu_utilization
            },
            "managed_instances": len(self.managed_instances),
            "scale_up_count": self.scale_up_count,
            "scale_down_count": self.scale_down_count,
            "last_action": time.time() - self.last_scale_action if self.last_scale_action > 0 else None,
            "metrics_history_size": len(self.metrics_history)
        }


# ============================================================================
# GEOGRAPHIC DISTRIBUTION
# ============================================================================

@dataclass
# class GeographicRegion:
    """Geographic region for edge computing"""
#     name: str
#     location: Tuple[float, float]  # (latitude, longitude)
#     provider: CloudProvider
#     available_zones: List[str]
#     latency_to_master_ms: float = 0.0


# class GeoDistributedScaler(AutoScaler):
    """
#     Auto-scaler with geographic distribution
#     Places nodes closer to workload sources
    """
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         self.regions: List[GeographicRegion] = [
#             GeographicRegion("US East", (37.7749, -122.4194), CloudProvider.AWS, ["us-east-1a", "us-east-1b"]),
#             GeographicRegion("US West", (34.0522, -118.2437), CloudProvider.AWS, ["us-west-2a", "us-west-2b"]),
#             GeographicRegion("EU West", (51.5074, -0.1278), CloudProvider.AWS, ["eu-west-1a", "eu-west-1b"]),
#             GeographicRegion("Asia Pacific", (35.6762, 139.6503), CloudProvider.AWS, ["ap-northeast-1a"]),
        ]
        
        # Track workload sources
#         self.workload_origins: Dict[str, int] = {}  # region -> request count
    
#     def select_optimal_region(self) -> GeographicRegion:
        """Select best region based on workload distribution"""
#         if not self.workload_origins:
#             return self.regions[0]  # Default to first region
        
        # Find region with most requests
#         max_requests = max(self.workload_origins.values())
#         for region in self.regions:
#             if self.workload_origins.get(region.name, 0) == max_requests:
#                 return region
        
#         return self.regions[0]
    
#     async def scale_up(self, count: int = 1, template: NodeTemplate = None):
        """Scale up in optimal geographic region"""
#         region = self.select_optimal_region()
        
#         if template is None:
#             template = NodeTemplate(
#                 provider=region.provider,
#                 instance_type="standard",
#                 image_id="quetzalcore-worker:latest",
#                 region=region.name,
#                 zone=region.available_zones[0],
#                 cpu_cores=4,
#                 ram_gb=8.0
#         else:
#             template.region = region.name
#             template.zone = region.available_zones[0]
        
#         logger.info(f" Scaling up in region: {region.name}")
#         await super().scale_up(count, template)
