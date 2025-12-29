# 🦅 QUETZALCORE CLI (qctl) - Quick Reference

**Unix/Linux-style command-line interface for QuetzalCore's unique architecture**

## Installation

```bash
# Make qctl executable
chmod +x /Users/xavasena/hive/qctl

# Optional: Add to PATH
ln -s /Users/xavasena/hive/qctl /usr/local/bin/qctl
```

## Quick Start

```bash
# Show version
qctl --version

# Show help
qctl --help

# Show brain status
qctl brain status

# Show system stats
qctl stats
```

## Command Structure

Like Unix tools (`kubectl`, `docker`, `git`):

```
qctl <resource> <action> [arguments] [flags]
```

## Brain Commands

```bash
# Show brain intelligence status
qctl brain status

# Show learned knowledge base
qctl brain knowledge

# Trigger resource optimization
qctl brain optimize
```

## VM (Virtual Machine) Commands

```bash
# List all VMs
qctl vm list

# Create VM (brain decides resources)
qctl vm create my-vm --purpose "MAG processing"

# Create VM with specific resources
qctl vm create ml-vm --cpu 16 --memory 32768 --gpu 4

# Start a VM
qctl vm start vm-abc123

# Stop a VM
qctl vm stop vm-abc123

# Force stop
qctl vm stop vm-abc123 --force

# Destroy a VM
qctl vm destroy vm-abc123 -y

# View VM console output
qctl vm console vm-abc123

# View last 20 lines
qctl vm console vm-abc123 --lines 20
```

## Node (Cluster) Commands

```bash
# List cluster nodes
qctl node list

# Add a node
qctl node add node-2 --cpu 32 --memory 65536
```

## Task Commands

```bash
# Submit task (brain analyzes and executes)
qctl task submit "Process mining MAG survey"

# Submit with data
qctl task submit "Generate 3D model" --data '{"points":50000}'
```

## Stats & Monitoring

```bash
# Show complete system stats
qctl stats

# Brain status
qctl brain status

# Brain knowledge
qctl brain knowledge

# VM list
qctl vm list

# Node list
qctl node list
```

## Configuration

```bash
# View config
qctl config view

# Set output format
qctl config set output_format json

# Set default namespace
qctl config set default_namespace production
```

## Output Formats

```bash
# Text format (default, human-readable)
qctl vm list

# JSON format (machine-readable)
qctl vm list -o json

# YAML format
qctl vm list -o yaml
```

## Examples

### Example 1: Create Mining VM

```bash
# Let brain decide resources
qctl vm create mining-vm --purpose "MAG magnetometry processing"

# Or specify resources
qctl vm create mining-vm --cpu 4 --memory 8192 --gpu 1
```

### Example 2: Submit ML Training Task

```bash
# Brain analyzes and allocates optimal resources
qctl task submit "Train anomaly detection model" \
  --data '{"epochs":100,"batch_size":32}'
```

### Example 3: Manage Cluster

```bash
# Add nodes
qctl node add node-1 --cpu 16 --memory 32768
qctl node add node-2 --cpu 32 --memory 65536

# List nodes
qctl node list

# Create distributed VM
qctl vm create distributed-vm --cpu 64 --memory 131072
```

### Example 4: Monitor System

```bash
# Show everything
qctl stats

# Watch brain learning
qctl brain knowledge

# Check VMs
qctl vm list

# View specific VM console
qctl vm console vm-abc123 --lines 50
```

### Example 5: JSON Output for Scripts

```bash
# Get VM list as JSON
vms=$(qctl vm list -o json)

# Get brain status as JSON
status=$(qctl brain status -o json)

# Parse with jq
qctl stats -o json | jq '.brain.metrics'
```

## Configuration File

Config stored at: `~/.quetzalcore/config.json`

```json
{
  "brain_endpoint": "local",
  "default_namespace": "default",
  "output_format": "text"
}
```

## Brain Decision Making

When you create a VM without specifying resources:

```bash
qctl vm create my-vm --purpose "3D generation"
```

The brain:
1. Analyzes the purpose ("3D generation")
2. Identifies domain (3D_GEN)
3. Recalls similar past experiences
4. Determines optimal resources
5. Creates VM with calculated specs

This is **autonomous intelligence** - the brain learns what works best!

## vs Traditional Tools

| Traditional | QuetzalCore |
|-------------|--------|
| `docker ps` | `qctl vm list` |
| `docker create` | `qctl vm create` |
| `kubectl get pods` | `qctl vm list` |
| `kubectl apply` | `qctl task submit` |
| Manual resource sizing | **Brain decides** |
| No learning | **Self-improving** |

## Key Differences

### 1. Brain-Powered

```bash
# Traditional: You decide everything
docker run -m 4g --cpus 2 myapp

# QuetzalCore: Brain decides based on learning
qctl task submit "Run myapp"
```

### 2. Self-Learning

Every task teaches the brain:
- What resources work best
- Which approaches succeed
- How to optimize performance

### 3. Unified Interface

One CLI for:
- Brain intelligence
- Hypervisor VMs
- Cluster nodes
- Task submission
- Monitoring

## Advanced Usage

### Scripting

```bash
#!/bin/bash
# Deploy mining analysis cluster

# Add nodes
for i in {1..5}; do
  qctl node add node-$i --cpu 16 --memory 32768
done

# Create VMs
qctl vm create mining-vm-1 --purpose "MAG processing"
qctl vm create mining-vm-2 --purpose "Geophysics analysis"

# Submit tasks
qctl task submit "Process MAG survey" --data '{"survey":"001"}'
qctl task submit "Process MAG survey" --data '{"survey":"002"}'

# Monitor
qctl stats
```

### Monitoring Loop

```bash
#!/bin/bash
# Watch system stats

while true; do
  clear
  echo "=== QUETZALCORE SYSTEM ==="
  qctl stats
  echo ""
  qctl brain knowledge
  sleep 5
done
```

### JSON Parsing

```bash
# Get running VMs count
running=$(qctl stats -o json | jq '.hypervisor.vms.running')

# Get brain confidence
confidence=$(qctl brain status -o json | jq '.confidence_threshold')

# List VM IDs
qctl vm list -o json | jq -r '.vms[].vm_id'
```

## Tips & Tricks

### 1. Trust the Brain

Don't over-specify resources. Let the brain learn and decide:

```bash
# ✅ Good - Brain decides
qctl vm create analysis-vm --purpose "Heavy MAG processing"

# ⚠️ Less optimal - You guess
qctl vm create analysis-vm --cpu 8 --memory 16384
```

### 2. Check Brain Knowledge

Before repeating tasks, check what the brain learned:

```bash
qctl brain knowledge
```

### 3. Use JSON for Automation

```bash
qctl vm list -o json | jq '.vms[] | select(.state=="running")'
```

### 4. View Logs

```bash
# Last 100 lines
qctl vm console vm-abc123 --lines 100

# Full output
qctl vm console vm-abc123
```

## Architecture Flow

```
User Command
    ↓
qctl CLI
    ↓
🧠 Brain Analysis
    ↓
Resource Decision
    ↓
🎛️  Hypervisor Execution
    ↓
🔧 Virtual Hardware Creation
    ↓
🐧 Linux VM Boot
    ↓
Task Execution
    ↓
🧠 Brain Learns
```

## Support

- Documentation: `qctl --help`
- Per-command help: `qctl <command> --help`
- Examples: This file
- Source: `/Users/xavasena/hive/qctl`

---

**Built with 🦅 by QuetzalCore**

*Unix-style interface for next-generation infrastructure*
