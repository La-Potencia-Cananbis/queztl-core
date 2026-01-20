#!/usr/bin/env bash
# Queztl-Core Distributed Execution - Quick Start Guide
# Run this to verify your distributed execution setup

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Queztl-Core Distributed Execution - Quick Start              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo

# Check SSH connectivity
echo "🔍 Checking cluster connectivity..."
echo

if ssh -o BatchMode=yes -o ConnectTimeout=3 xava@192.168.1.105 echo "OK" >/dev/null 2>&1; then
    echo "✅ Beast (192.168.1.105) - Connected"
    BEAST_ONLINE=true
else
    echo "❌ Beast (192.168.1.105) - Not reachable"
    BEAST_ONLINE=false
fi

if ssh -o BatchMode=yes -o ConnectTimeout=3 xava@192.168.1.102 echo "OK" >/dev/null 2>&1; then
    echo "✅ Sloth (192.168.1.102) - Connected"
    SLOTH_ONLINE=true
else
    echo "⚠️  Sloth (192.168.1.102) - No SSH access (needs key setup)"
    SLOTH_ONLINE=false
fi

echo

# Test executor if Beast is online
if [ "$BEAST_ONLINE" = true ]; then
    echo "🚀 Testing CommandExecutor..."
    python3 <<'PYTHON'
from sys import path
path.insert(0, '/Users/xavasena/queztl-core/backend')

from queztl_exec import ExecConfig, CommandExecutor, ExecMode

# Quick test
exec_cfg = ExecConfig(
    mode=ExecMode.SSH,
    ssh_user='xava',
    ssh_host='192.168.1.105'
)

executor = CommandExecutor(exec_cfg)
result = executor.run(['echo', 'Executor operational'])

if result.returncode == 0:
    print(f"✅ {result.stdout.strip()}")
else:
    print("❌ Executor test failed")
PYTHON
    echo
fi

# Show quick usage
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📚 Quick Usage Examples"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

cat <<'EXAMPLES'
# 1. Run command on Beast (SSH mode)
python3 <<EOF
from queztl_exec import ExecConfig, CommandExecutor, ExecMode
exec_cfg = ExecConfig(mode=ExecMode.SSH, ssh_host='192.168.1.105', ssh_user='xava')
executor = CommandExecutor(exec_cfg)
result = executor.run(['python3', 'my_script.py'])
print(result.stdout)
EOF

# 2. Run in Docker container on Beast
python3 <<EOF
from queztl_exec import ExecConfig, CommandExecutor, ExecMode
exec_cfg = ExecConfig(
    mode=ExecMode.SSH_DOCKER,
    ssh_host='192.168.1.105',
    ssh_user='xava',
    docker_container='ray-worker'
)
executor = CommandExecutor(exec_cfg)
result = executor.run(['python3', '-c', 'import torch; print(torch.__version__)'])
print(result.stdout)
EOF

# 3. Use environment variable configuration
export QUEZTL_EXEC_MODE=ssh_docker
export QUEZTL_SSH_HOST=192.168.1.105
export QUEZTL_DOCKER_CONTAINER=ray-worker

python3 -c "
from queztl_exec import CommandExecutor
executor = CommandExecutor()  # Uses env vars
result = executor.run(['echo', 'Hello from cluster!'])
print(result.stdout)
"

EXAMPLES

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 Next Steps:"
echo
echo "  1. Review: backend/INTEGRATION_SUCCESS.md"
echo "  2. Configure: backend/queztl_config.py"
echo "  3. Setup Sloth SSH: backend/setup_ssh_keys.sh"
echo "  4. Integrate with agents: backend/queztl_agents.py"
echo
echo "╚════════════════════════════════════════════════════════════════╝"
