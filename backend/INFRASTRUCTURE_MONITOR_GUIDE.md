# 🦅 QuetzalCore Infrastructure Monitor

**Real-time OS Utilization Dashboard - Like Activity Monitor for Your Distributed Infrastructure**

---

## 🚀 Quick Start

### Launch the Monitor
```bash
python3 infrastructure_monitor_web.py
```

**Access in browser:** http://localhost:7070

---

## 📊 What You See

### Main Metrics (Top Cards)
- **CPU Usage**: Current CPU utilization across all cores
- **Memory Usage**: RAM usage in GB and percentage
- **Disk Usage**: Storage utilization
- **Running Processes**: Total number of active processes

### Distributed Infrastructure View
Shows 3 simulated cluster nodes with:
- **CPU & Memory** utilization per node
- **Number of VMs** running on each node
- **GPU count** allocated to each node

### Top Processes
Real-time list of processes consuming most resources:
- PID (Process ID)
- Process Name
- CPU % usage
- Memory % usage

---

## 🎯 Real-time Monitoring

The dashboard **automatically updates every 2 seconds** with:
- Color-coded progress bars (Green → Yellow → Red)
- Live process list
- Dynamic node status
- Timestamp of last update

---

## 📡 API Endpoint

Get metrics as JSON:
```bash
curl http://localhost:7070/api/metrics
```

**Response Example:**
```json
{
  "timestamp": "2025-12-08T15:38:08.904312",
  "cpu": 29.4,
  "cpu_cores": 10,
  "memory": 82.4,
  "memory_total_gb": 16.0,
  "memory_used_gb": 13.2,
  "disk": 12.4,
  "processes": 672,
  "top_processes": [
    {
      "pid": 93399,
      "name": "Python",
      "cpu": 80.3,
      "memory": 0.1
    },
    ...
  ],
  "nodes": [
    {
      "name": "compute-node-1",
      "cpu": 39.4,
      "memory": 87.4,
      "vms": 3,
      "gpus": 2
    },
    ...
  ]
}
```

---

## 💡 Use Cases

### 1. **Monitor Infrastructure Health**
- See overall CPU, memory, disk utilization
- Identify bottlenecks and resource constraints
- Track utilization trends over time

### 2. **Process Monitoring**
- Identify which processes are consuming most CPU/memory
- Kill problematic processes if needed
- Monitor resource-hungry applications

### 3. **Cluster Visibility**
- See distribution of VMs across nodes
- Check GPU utilization across infrastructure
- Monitor node health at a glance

### 4. **Performance Tuning**
- Baseline resource usage
- Identify optimization opportunities
- Track improvements after changes

### 5. **Capacity Planning**
- Monitor utilization trends
- Identify when to add more nodes
- Understand peak usage patterns

---

## 🎨 Dashboard Features

### Color-Coded Indicators
- 🟢 **Green** (<50%): Healthy
- 🟡 **Yellow** (50-75%): Caution
- 🔴 **Red** (>75%): Critical

### Responsive Design
- Works on desktop, tablet, mobile
- Auto-scaling layout
- Touch-friendly on tablets

### Real-time Updates
- JavaScript fetch API
- No page refresh needed
- Smooth transitions and animations

---

## 📈 Performance Metrics

| Metric | Description | Value |
|--------|-------------|-------|
| **Update Frequency** | How often dashboard refreshes | Every 2 seconds |
| **Sample Resolution** | CPU sampling interval | 0.1 seconds |
| **Data Retention** | Historical data points kept | Last 100 readings |
| **API Response Time** | Time to get metrics | <100ms |
| **Dashboard Load Time** | Initial page load | <500ms |

---

## 🔧 Integration with QuetzalCore

### CLI Monitor (Terminal)
```bash
# One-time metrics export
python3 infrastructure_monitor.py --export

# Continuous monitoring (terminal UI)
python3 infrastructure_monitor.py
```

**Output:** Colored terminal dashboard with:
- Progress bars
- Top processes
- Cluster node status
- System information

### Web Monitor (Browser)
```bash
# Start web server
python3 infrastructure_monitor_web.py

# Access at http://localhost:7070
```

**Features:**
- Beautiful web UI
- Real-time updates
- JSON API
- Mobile responsive

---

## 📊 Metrics Explained

### CPU Metrics
- **CPU %**: Instantaneous CPU utilization (0-100%)
- **Cores**: Number of CPU cores available
- **Per-process CPU %**: CPU share used by each process

### Memory Metrics
- **Memory %**: RAM utilization percentage
- **Used/Total**: Actual memory usage in GB
- **Per-process Memory %**: Memory share used by each process

### Disk Metrics
- **Disk %**: Storage utilization percentage
- **Used/Total**: Actual disk usage in GB
- **Free Space**: Available disk space in GB

### Process Metrics
- **PID**: Unique process identifier
- **Name**: Process executable name
- **CPU %**: CPU time allocated to process
- **Memory %**: RAM allocated to process

### Node Metrics (Distributed)
- **CPU %**: Node-wide CPU utilization
- **Memory %**: Node-wide memory utilization
- **VMs**: Number of virtual machines running
- **GPUs**: Number of GPU devices allocated

---

## 🆘 Troubleshooting

### Monitor won't start
**Solution:** Check if port 7070 is available
```bash
lsof -i :7070  # See what's using port 7070
```

### Dashboard shows 0% everywhere
**Solution:** Wait 5 seconds for first metrics to collect

### Missing process information
**Solution:** Some processes require elevated privileges
```bash
sudo python3 infrastructure_monitor_web.py
```

### Slow refresh rate
**Solution:** Check system load and browser performance

---

## 🚀 Advanced Usage

### Monitor Specific Directory
Modify `infrastructure_monitor_web.py` to monitor specific disk:
```python
disk = psutil.disk_usage('/mnt/data')  # Custom path
```

### Filter Top Processes
Change process filtering in `MetricsCollector.collect()`:
```python
if info['cpu_percent'] and info['cpu_percent'] > 0.5:  # Higher threshold
```

### Export to File
```bash
python3 infrastructure_monitor.py --export
# Creates: infrastructure_metrics_TIMESTAMP.json
```

---

## 📱 Mobile Access

Access from any device on your network:

1. **Find your local IP:**
   ```bash
   ifconfig | grep "inet "
   ```

2. **Replace `localhost` with your IP:**
   ```
   http://YOUR_IP:7070
   ```

3. **Access from any device on your network**

---

## 🔒 Security Note

For production use:
- Add authentication (basic auth or OAuth)
- Use HTTPS instead of HTTP
- Restrict access by IP
- Add rate limiting to API
- Monitor API usage

Example with authentication:
```python
# Add to MonitorHandler.do_GET()
auth = request.headers.get('Authorization')
if not auth or not verify_token(auth):
    self.send_response(401)
    return
```

---

## 📝 Summary

You now have a **complete infrastructure monitoring solution** that provides:

✅ **Real-time metrics** - CPU, memory, disk usage  
✅ **Process monitoring** - See resource hogs  
✅ **Distributed view** - Monitor across cluster nodes  
✅ **Beautiful UI** - Web dashboard with live updates  
✅ **API access** - JSON endpoint for integration  
✅ **Terminal version** - For CLI-only environments  

**Use it to understand, monitor, and optimize your QuetzalCore infrastructure!** 🚀
