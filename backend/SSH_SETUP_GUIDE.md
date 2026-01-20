# SSH Setup Guide for Queztl Cluster

## Current Situation
Your SSH public key is not yet installed on the cluster nodes (Sloth, Beast). This prevents passwordless SSH access needed for distributed execution.

## Quick Fix (Run Once)

### 1. Copy SSH Key to Sloth (Coordinator)
```bash
ssh-copy-id xava@192.168.1.102
# Enter password when prompted
```

### 2. Copy SSH Key to Beast (GPU Node)
First, find Beast's current IP:
```bash
nmap -sn 192.168.1.0/24 | grep -B 2 "beast\|Beast" || nmap -sn 192.168.1.0/24 | grep -B 2 "(192.168.1.105)"
```

Then copy the key:
```bash
ssh-copy-id xava@192.168.1.105   # Or use discovered IP
# Enter password when prompted
```

### 3. Test Connections
```bash
# Test Sloth
ssh xava@192.168.1.102 echo "✅ Sloth connected"

# Test Beast (use actual IP)
ssh xava@192.168.1.105 echo "✅ Beast connected"
```

## Verify Setup

Once SSH keys are installed, run:
```bash
python3 backend/setup_cluster.py
```

You should see:
```
✅ sloth (192.168.1.102) - Connected successfully
✅ beast (192.168.1.XXX) - Connected successfully
```

## Alternative: Password-Based Execution (Not Recommended)

If you can't set up SSH keys, you can use password-based execution by modifying `queztl_exec.py` to use `sshpass` or `paramiko` with password authentication. This is **not recommended** for security reasons.

## Next Steps

After SSH keys are set up:
1. Run `python3 backend/setup_cluster.py` to verify connectivity
2. Test executor: `python3 -c "from queztl_config import config; from queztl_exec import ExecConfig, CommandExecutor; exec_cfg = ExecConfig(mode=config.EXEC_MODE, ssh_user=config.SSH_USER, ssh_host='192.168.1.102', docker_container=config.DOCKER_CONTAINER, remote_cwd=config.REMOTE_CWD); executor = CommandExecutor(exec_cfg); result = executor.run(['echo', 'Hello from Sloth!']); print(f'Exit: {result.returncode}\\nOutput: {result.stdout}')"`
3. Update agent system to use CommandExecutor for distributed tasks

## Troubleshooting

### "Permission denied (publickey)"
- SSH key not installed on remote node
- Run `ssh-copy-id xava@<node-ip>` with password

### "Host key verification failed"
- Host key not in known_hosts
- Run `ssh-keyscan -H <node-ip> >> ~/.ssh/known_hosts`

### "Connection refused" / "No route to host"
- Node IP changed (DHCP)
- Find new IP with `nmap -sn 192.168.1.0/24`
- Update `export QUEZTL_SSH_HOST=<new-ip>`

### Docker container not found
- Verify ray-head container is running: `ssh xava@192.168.1.102 docker ps`
- Start if needed: `ssh xava@192.168.1.102 docker start ray-head`
