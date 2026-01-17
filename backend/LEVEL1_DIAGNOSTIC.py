#!/usr/bin/env python3
"""
LEVEL 1 DIAGNOSTIC - Agent System Readiness Check
==================================================
Verifies all systems before spinning up agents.
"""

import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def check(name: str) -> None:
    """Print check header."""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}🔍 {name}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")

def ok(msg: str) -> None:
    """Print success."""
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def fail(msg: str) -> None:
    """Print failure."""
    print(f"{Colors.RED}✗{Colors.END} {msg}")

def warn(msg: str) -> None:
    """Print warning."""
    print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")

def run_cmd(cmd: List[str]) -> Tuple[int, str, str]:
    """Run command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

def check_python():
    """Check Python version and installation."""
    check("Python Environment")
    
    code, stdout, stderr = run_cmd([sys.executable, "--version"])
    if code == 0:
        version = stdout.split()[1]
        ok(f"Python {version} ({sys.executable})")
        
        # Check if we're in a virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            ok(f"Virtual environment active: {sys.prefix}")
        else:
            warn("No virtual environment detected (recommended)")
        
        return True
    else:
        fail(f"Python check failed: {stderr}")
        return False

def check_python_packages():
    """Check required Python packages."""
    check("Python Dependencies")
    
    required = {
        'torch': 'PyTorch (ML training)',
        'torchvision': 'PyTorch vision models',
        'PIL': 'Pillow (image processing)',
        'flask': 'Flask (dashboard)',
        'fastapi': 'FastAPI (API server)',
        'uvicorn': 'Uvicorn (ASGI server)',
        'websockets': 'WebSocket support',
        'redis': 'Redis client',
        'psycopg2': 'PostgreSQL client',
        'sqlalchemy': 'SQLAlchemy ORM',
    }
    
    missing = []
    
    for package, description in required.items():
        try:
            __import__(package.replace('-', '_'))
            ok(f"{package:15s} - {description}")
        except ImportError:
            fail(f"{package:15s} - {description}")
            missing.append(package)
    
    if missing:
        warn(f"\nMissing {len(missing)} packages. Install with:")
        print(f"\n    pip3 install {' '.join(missing)}")
        print(f"\n    OR use requirements.txt:")
        print(f"    pip3 install -r backend/requirements.txt\n")
        return False
    
    return True

def check_agent_code():
    """Check if agent code files exist."""
    check("Agent System Files")
    
    repo_root = Path.cwd()
    required_files = [
        'backend/queztl_agents.py',
        'backend/simple_trainer.py',
        'backend/training_dashboard.py',
        'backend/requirements.txt',
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = repo_root / file_path
        if full_path.exists():
            ok(f"{file_path} ({full_path.stat().st_size:,} bytes)")
        else:
            fail(f"{file_path} (not found)")
            all_exist = False
    
    return all_exist

def check_docker():
    """Check Docker availability."""
    check("Docker Services")
    
    # Check Docker
    code, stdout, stderr = run_cmd(['docker', '--version'])
    if code == 0:
        ok(f"Docker installed: {stdout}")
    else:
        fail("Docker not installed or not in PATH")
        return False
    
    # Check Docker daemon
    code, stdout, stderr = run_cmd(['docker', 'ps'])
    if code == 0:
        ok("Docker daemon running")
    else:
        fail("Docker daemon not running")
        warn("Start Docker Desktop or run: open -a Docker")
        return False
    
    # Check Docker Compose
    code, stdout, stderr = run_cmd(['docker-compose', '--version'])
    if code == 0:
        ok(f"Docker Compose installed: {stdout}")
    else:
        warn("docker-compose not found (might use 'docker compose' instead)")
    
    return True

def check_docker_services():
    """Check if required Docker services are running."""
    check("Docker Container Status")
    
    required_services = ['postgres', 'redis']
    
    code, stdout, stderr = run_cmd(['docker', 'ps', '--format', '{{.Names}}'])
    if code != 0:
        fail("Cannot list Docker containers")
        return False
    
    running = stdout.split('\n')
    
    for service in required_services:
        matching = [c for c in running if service in c.lower()]
        if matching:
            ok(f"{service.capitalize()} container: {matching[0]}")
        else:
            warn(f"{service.capitalize()} container not running")
    
    return len([c for s in required_services for c in running if s in c.lower()]) > 0

def check_workspace():
    """Check workspace directories."""
    check("Workspace Structure")
    
    workspace = Path('/tmp/queztl_agents')
    if workspace.exists():
        ok(f"Agent workspace exists: {workspace}")
        
        # Count agent directories
        agents = list(workspace.rglob('dna.json'))
        if agents:
            ok(f"Found {len(agents)} existing agent(s)")
            for agent_dna in agents[:5]:  # Show first 5
                print(f"     - {agent_dna.parent.name}")
        else:
            warn("No existing agents found")
    else:
        warn(f"Agent workspace not initialized: {workspace}")
        print(f"     Will be created on first agent spawn")
    
    return True

def check_simple_trainer():
    """Check if simple trainer can initialize."""
    check("Simple Trainer Initialization")
    
    try:
        # Try to import the trainer module
        sys.path.insert(0, str(Path.cwd() / 'backend'))
        from simple_trainer import SimpleTrainer, OBJECTS
        
        ok(f"Module imported successfully")
        ok(f"Training objects: {', '.join(OBJECTS)}")
        ok(f"Ready to train on {len(OBJECTS)} classes")
        return True
    except ImportError as e:
        fail(f"Cannot import simple_trainer: {e}")
        return False
    except Exception as e:
        fail(f"Trainer initialization error: {e}")
        return False

def test_agent_spawn():
    """Test spawning a simple agent."""
    check("Agent Spawn Test")
    
    try:
        sys.path.insert(0, str(Path.cwd() / 'backend'))
        from queztl_agents import AgentNode, AgentType, Path as AgentPath
        
        ok("Agent module imported")
        
        # Try to create a node
        test_workspace = Path('/tmp/queztl_diagnostic')
        test_workspace.mkdir(exist_ok=True)
        
        node = AgentNode('diagnostic_node', test_workspace)
        ok(f"Node created: {node.node_id}")
        
        # Try to spawn a simple runner agent
        agent = node.spawn_agent(AgentType.RUNNER, 'diagnostic_runner')
        ok(f"Agent spawned: {agent.dna.agent_id}")
        ok(f"Agent type: {agent.dna.agent_type.value}")
        ok(f"Agent workspace: {agent.workspace}")
        
        # Verify agent can log
        agent.log("Diagnostic test message")
        ok(f"Agent logging functional")
        
        # Check DNA file
        dna_path = agent.workspace / 'dna.json'
        if dna_path.exists():
            ok(f"DNA file created: {dna_path.stat().st_size} bytes")
        else:
            warn("DNA file not created")
        
        return True
        
    except Exception as e:
        fail(f"Agent spawn failed: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def main():
    """Run all diagnostics."""
    print(f"\n{Colors.BOLD}{'='*60}")
    print("🔬 QUEZTL AGENT SYSTEM - LEVEL 1 DIAGNOSTIC")
    print(f"{'='*60}{Colors.END}\n")
    print(f"Date: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}")
    print(f"Host: {subprocess.run(['hostname'], capture_output=True, text=True).stdout.strip()}")
    
    results = {
        'Python Environment': check_python(),
        'Python Dependencies': check_python_packages(),
        'Agent Code Files': check_agent_code(),
        'Workspace Structure': check_workspace(),
        'Docker Services': check_docker(),
    }
    
    # Only run these if basics pass
    if results['Python Dependencies'] and results['Agent Code Files']:
        results['Simple Trainer'] = check_simple_trainer()
        results['Agent Spawn Test'] = test_agent_spawn()
    
    # Summary
    print(f"\n{Colors.BOLD}{'='*60}")
    print("📊 DIAGNOSTIC SUMMARY")
    print(f"{'='*60}{Colors.END}\n")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, status in results.items():
        status_str = f"{Colors.GREEN}PASS{Colors.END}" if status else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  {status_str}  {name}")
    
    print(f"\n{Colors.BOLD}Result: {passed}/{total} checks passed{Colors.END}\n")
    
    # Recommendations
    if passed == total:
        print(f"{Colors.GREEN}{'='*60}")
        print("✅ ALL SYSTEMS GO - Ready to spin up agents!")
        print(f"{'='*60}{Colors.END}\n")
        print("Next steps:")
        print("  1. Run agent demo:")
        print("     python3 backend/queztl_agents.py --demo")
        print("\n  2. Start dashboard (if Flask installed):")
        print("     python3 backend/training_dashboard.py")
        print("\n  3. Spawn specific agent:")
        print("     python3 backend/queztl_agents.py --spawn trainer")
    else:
        print(f"{Colors.YELLOW}{'='*60}")
        print("⚠️  SOME SYSTEMS NEED ATTENTION")
        print(f"{'='*60}{Colors.END}\n")
        
        if not results['Python Dependencies']:
            print("🔧 Fix: Install Python dependencies")
            print("   pip3 install -r backend/requirements.txt\n")
        
        if not results.get('Docker Services', True):
            print("🔧 Fix: Start Docker")
            print("   open -a Docker\n")
            print("   Then run: docker-compose up -d\n")
    
    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
