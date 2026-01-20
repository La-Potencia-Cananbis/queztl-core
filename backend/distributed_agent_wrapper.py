"""
Distributed Agent Wrapper for Queztl-Core

This module provides a DistributedAgent class that can execute tasks
on remote cluster nodes using the CommandExecutor infrastructure.

Usage:
    from distributed_agent_wrapper import DistributedAgent
    
    # Create agent on Beast GPU node
    agent = DistributedAgent("TrainerAgent", node='beast', use_docker=True)
    
    # Run Python code remotely
    result = agent.run_python("import torch; print(torch.__version__)")
    
    # Execute commands
    result = agent.execute(['python3', 'train_model.py', '--epochs', '100'])
"""

from typing import List, Optional
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from queztl_config import config
from queztl_exec import ExecConfig, CommandExecutor, ExecMode


class DistributedAgent:
    """
    Agent that can execute tasks on remote cluster nodes.
    
    This wrapper provides a simple interface for distributed execution,
    handling SSH, Docker, and node selection automatically.
    
    Attributes:
        name: Agent identifier
        node: Target node name ('beast', 'sloth', 'optiplex1', etc.)
        use_docker: Whether to execute inside Docker containers
        executor: CommandExecutor instance for this agent
    """
    
    def __init__(
        self,
        name: str,
        node: str = 'beast',
        use_docker: bool = True,
        docker_container: str = 'ray-worker'
    ):
        """
        Create a distributed agent.
        
        Args:
            name: Agent name/identifier
            node: Target node ('beast', 'sloth', 'optiplex1', etc.)
            use_docker: Execute inside Docker container if True
            docker_container: Container name (default: ray-worker)
        """
        self.name = name
        self.node = node
        self.use_docker = use_docker
        self.docker_container = docker_container
        
        # Configure executor based on mode
        if use_docker:
            self.exec_cfg = ExecConfig(
                mode=ExecMode.SSH_DOCKER,
                ssh_user=config.SSH_USER,
                ssh_host=config.get_node_ip(node),
                docker_container=docker_container
            )
        else:
            self.exec_cfg = ExecConfig(
                mode=ExecMode.SSH,
                ssh_user=config.SSH_USER,
                ssh_host=config.get_node_ip(node)
            )
        
        self.executor = CommandExecutor(self.exec_cfg)
    
    def execute(self, command: List[str], timeout: Optional[int] = None):
        """
        Execute a command on the remote node.
        
        Args:
            command: Command and arguments as list
            timeout: Optional timeout in seconds
        
        Returns:
            subprocess.CompletedProcess with stdout, stderr, returncode
        """
        return self.executor.run(command, timeout=timeout)
    
    def run_python(self, code: str, timeout: Optional[int] = None):
        """
        Execute Python code on the remote node.
        
        Args:
            code: Python code to execute
            timeout: Optional timeout in seconds
        
        Returns:
            subprocess.CompletedProcess with stdout, stderr, returncode
        """
        return self.executor.run(['python3', '-c', code], timeout=timeout)
    
    def run_script(self, script_path: str, args: Optional[List[str]] = None, timeout: Optional[int] = None):
        """
        Execute a Python script on the remote node.
        
        Args:
            script_path: Path to Python script (must be accessible on remote)
            args: Optional script arguments
            timeout: Optional timeout in seconds
        
        Returns:
            subprocess.CompletedProcess with stdout, stderr, returncode
        """
        command = ['python3', script_path]
        if args:
            command.extend(args)
        return self.executor.run(command, timeout=timeout)
    
    def check_capabilities(self):
        """
        Check what capabilities are available on this node.
        
        Returns:
            dict with system information
        """
        result = self.run_python("""
import sys, os, platform
import json

info = {
    'os': platform.system(),
    'release': platform.release(),
    'python': sys.version.split()[0],
    'cpu_count': os.cpu_count(),
}

try:
    import torch
    info['pytorch'] = torch.__version__
    info['cuda'] = torch.cuda.is_available()
    info['gpu_count'] = torch.cuda.device_count()
    if torch.cuda.is_available():
        info['gpu_name'] = torch.cuda.get_device_name(0)
except ImportError:
    info['pytorch'] = None

try:
    import ray
    info['ray'] = ray.__version__
except ImportError:
    info['ray'] = None

print(json.dumps(info))
""")
        
        if result.returncode == 0:
            import json
            return json.loads(result.stdout)
        else:
            return {'error': result.stderr}
    
    def __repr__(self):
        mode = "Docker" if self.use_docker else "SSH"
        return f"<DistributedAgent '{self.name}' on {self.node} ({mode})>"


class AgentPool:
    """
    Manage multiple distributed agents as a pool.
    
    Useful for task distribution and load balancing.
    """
    
    def __init__(self):
        self.agents = {}
    
    def add_agent(self, agent: DistributedAgent):
        """Add an agent to the pool"""
        self.agents[agent.name] = agent
    
    def create_agent(self, name: str, node: str = 'beast', use_docker: bool = True):
        """Create and add an agent to the pool"""
        agent = DistributedAgent(name, node, use_docker)
        self.add_agent(agent)
        return agent
    
    def get_agent(self, name: str) -> Optional[DistributedAgent]:
        """Get an agent by name"""
        return self.agents.get(name)
    
    def list_agents(self):
        """List all agents in the pool"""
        return list(self.agents.keys())
    
    def remove_agent(self, name: str):
        """Remove an agent from the pool"""
        if name in self.agents:
            del self.agents[name]
    
    def execute_on_all(self, command: List[str]):
        """Execute a command on all agents in parallel"""
        results = {}
        for name, agent in self.agents.items():
            results[name] = agent.execute(command)
        return results
    
    def __len__(self):
        return len(self.agents)
    
    def __repr__(self):
        return f"<AgentPool with {len(self)} agents>"


# Example usage
if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  Distributed Agent Wrapper - Demo                             ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    
    # Create a distributed agent
    print("Creating agent on Beast...")
    agent = DistributedAgent("TestAgent", node='beast', use_docker=True)
    print(f"✅ {agent}")
    print()
    
    # Check capabilities
    print("Checking node capabilities...")
    caps = agent.check_capabilities()
    for key, value in caps.items():
        print(f"   {key}: {value}")
    print()
    
    # Run a simple task
    print("Running test task...")
    result = agent.run_python("print('Hello from ' + __import__('socket').gethostname())")
    print(f"✅ Output: {result.stdout.strip()}")
    print()
    
    # Create agent pool
    print("Creating agent pool...")
    pool = AgentPool()
    pool.create_agent("Agent1", node='beast', use_docker=True)
    pool.create_agent("Agent2", node='beast', use_docker=False)
    print(f"✅ {pool}")
    print(f"   Agents: {pool.list_agents()}")
    print()
    
    print("╚════════════════════════════════════════════════════════════════╝")
