#!/usr/bin/env python3
"""
Queztl-Core Configuration
Easy-to-edit settings for cluster execution
"""
import os
from typing import Optional

class QueztlConfig:
    """
    Centralized configuration for Queztl-Core cluster execution.
    
    Priority:
    1. Environment variables (highest)
    2. This file's defaults
    3. Hardcoded fallbacks (lowest)
    
    Override via environment:
        export QUEZTL_EXEC_MODE=ssh_docker
        export QUEZTL_SSH_HOST=192.168.1.102
    """
    
    # ===== EXECUTION MODE =====
    # Options: 'local', 'ssh', 'ssh_docker', 'ray'
    EXEC_MODE: str = os.getenv('QUEZTL_EXEC_MODE', 'ssh_docker')
    
    # ===== SSH SETTINGS =====
    SSH_USER: str = os.getenv('QUEZTL_SSH_USER', 'xava')
    SSH_HOST: Optional[str] = os.getenv('QUEZTL_SSH_HOST', None)  # Set via env or discovery
    SSH_KEY: Optional[str] = os.getenv('QUEZTL_SSH_KEY', None)    # None = use default
    SSH_PORT: int = int(os.getenv('QUEZTL_SSH_PORT', '22'))
    
    # ===== DOCKER SETTINGS (for ssh_docker mode) =====
    DOCKER_CONTAINER: str = os.getenv('QUEZTL_DOCKER_CONTAINER', 'ray-head')
    REMOTE_CWD: str = os.getenv('QUEZTL_REMOTE_CWD', '/code/backend')
    
    # ===== NODE DISCOVERY =====
    # Known node hostnames (for SSH config lookup)
    KNOWN_NODES = {
        'beast': {
            'roles': ['gpu', 'image_generation'],
            'capabilities': ['cuda', 'stable_diffusion'],
            'default_ip': '192.168.1.105',  # DHCP - may change
        },
        'sloth': {
            'roles': ['coordinator', 'ray_head'],
            'capabilities': ['orchestration', 'scheduling'],
            'default_ip': '192.168.1.102',  # DHCP - may change
        },
        'optiplex1': {
            'roles': ['worker'],
            'capabilities': ['cpu'],
            'dns': True,  # Uses DNS at remote site
        },
        'optiplex2': {
            'roles': ['worker'],
            'capabilities': ['cpu'],
            'dns': True,
        },
        'optiplex3': {
            'roles': ['worker'],
            'capabilities': ['cpu'],
            'dns': True,
        },
    }
    
    # ===== DEFAULT NODE SELECTION =====
    # Which node to use by default if not specified
    DEFAULT_COORDINATOR: str = os.getenv('QUEZTL_DEFAULT_COORDINATOR', 'sloth')
    DEFAULT_GPU_NODE: str = os.getenv('QUEZTL_DEFAULT_GPU_NODE', 'beast')
    DEFAULT_CPU_WORKERS: list = ['optiplex1', 'optiplex2', 'optiplex3']
    
    # ===== RAY CLUSTER SETTINGS =====
    RAY_HEAD_HOST: Optional[str] = os.getenv('QUEZTL_RAY_HEAD', None)
    RAY_HEAD_PORT: int = int(os.getenv('QUEZTL_RAY_PORT', '6379'))
    
    # ===== WORKSPACE PATHS =====
    LOCAL_WORKSPACE: str = os.path.expanduser(os.getenv('QUEZTL_LOCAL_WORKSPACE', '~/queztl-core'))
    REMOTE_WORKSPACE: str = os.getenv('QUEZTL_REMOTE_WORKSPACE', '/code')
    
    # ===== LOGGING =====
    LOG_LEVEL: str = os.getenv('QUEZTL_LOG_LEVEL', 'INFO')
    LOG_DIR: str = os.path.expanduser(os.getenv('QUEZTL_LOG_DIR', '~/queztl-core/logs'))
    
    # ===== AGENT SETTINGS =====
    AGENT_WORKSPACE: str = os.path.expanduser(os.getenv('QUEZTL_AGENT_WORKSPACE', '~/queztl-core/workspace'))
    MAX_CONCURRENT_AGENTS: int = int(os.getenv('QUEZTL_MAX_AGENTS', '10'))
    
    @classmethod
    def get_node_ip(cls, node_name: str) -> Optional[str]:
        """Get IP for a node (from env, config, or SSH config)"""
        # Check environment override
        env_var = f'QUEZTL_{node_name.upper()}_IP'
        if env_var in os.environ:
            return os.environ[env_var]
        
        # Check known nodes config
        if node_name in cls.KNOWN_NODES:
            node = cls.KNOWN_NODES[node_name]
            if node.get('dns'):
                return node_name  # Use hostname directly (DNS resolution)
            return node.get('default_ip')
        
        return None
    
    @classmethod
    def summary(cls) -> str:
        """Print current configuration"""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║  Queztl-Core Configuration                                   ║
╚══════════════════════════════════════════════════════════════╝

EXECUTION MODE: {cls.EXEC_MODE}

SSH:
  User: {cls.SSH_USER}
  Host: {cls.SSH_HOST or 'auto-discover'}
  Port: {cls.SSH_PORT}
  Container: {cls.DOCKER_CONTAINER} (if ssh_docker mode)
  Remote CWD: {cls.REMOTE_CWD}

DEFAULT NODES:
  Coordinator: {cls.DEFAULT_COORDINATOR} ({cls.get_node_ip(cls.DEFAULT_COORDINATOR)})
  GPU Node: {cls.DEFAULT_GPU_NODE} ({cls.get_node_ip(cls.DEFAULT_GPU_NODE)})
  CPU Workers: {', '.join(cls.DEFAULT_CPU_WORKERS)}

PATHS:
  Local: {cls.LOCAL_WORKSPACE}
  Remote: {cls.REMOTE_WORKSPACE}
  Logs: {cls.LOG_DIR}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
To override any setting:
  export QUEZTL_EXEC_MODE=ssh_docker
  export QUEZTL_SSH_HOST=192.168.1.102
  export QUEZTL_DOCKER_CONTAINER=my-container

Or edit: backend/queztl_config.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


# Convenience: Load config on import
config = QueztlConfig()


if __name__ == "__main__":
    print(QueztlConfig.summary())
