# 🤖 QuetzalCore Autonomous Agent Runner

## Overview

The **Autonomous Agent Runner** is a self-managing system that continuously monitors, maintains, and improves the entire QuetzalCore infrastructure. It runs 24/7, automatically detecting and fixing issues, optimizing performance, and ensuring system reliability.

## Features

### 🔍 **Continuous Monitoring**
- Health checks every 30 seconds
- Service availability monitoring
- Port and process tracking
- Resource usage monitoring (CPU, Memory, Disk)

### 🏥 **Self-Healing**
- Auto-restart crashed services
- Automatic port cleanup
- Service recovery with retry logic
- Failure tracking and logging

### ⚡ **Performance Optimization**
- CPU usage monitoring and auto-scaling triggers
- Memory cache clearing when needed
- Log rotation for disk space management
- Load balancing recommendations

### 🔍 **Code Quality**
- Python syntax validation
- File structure checks
- Import verification
- Performance profiling

### 📚 **Documentation**
- Auto-generated status reports
- Real-time system metrics
- Service uptime tracking
- Historical performance data

### 🔒 **Security**
- File permission checks
- Debug mode verification
- Vulnerability scanning
- Access control validation

### 🏋️ **Load Testing**
- Periodic performance tests
- Latency measurement
- Throughput validation
- Stress testing

---

## Quick Start

### Start the Agent

```bash
./start-agent.sh
```

The agent will start in the background and immediately begin monitoring.

### Stop the Agent

```bash
./stop-agent.sh
```

Graceful shutdown with final status report.

### View Live Status

```bash
# Real-time logs
tail -f agent_runner.log

# Current status report
cat SYSTEM_STATUS_LIVE.md

# Watch status updates
watch -n 5 cat SYSTEM_STATUS_LIVE.md
```

---

## Agent Cycles

The agent runs in continuous cycles (every 30 seconds), performing these phases:

### Phase 1: Health Monitoring (Every cycle - 30s)
- Check backend service (port 8000)
- Check frontend service (port 8080)
- Verify health endpoints
- Update service status

### Phase 2: Auto-Healing (Every cycle - 30s)
- Detect failed services
- Kill stuck processes
- Restart failed services
- Track restart attempts

### Phase 3: Performance Optimization (Every 5 cycles - 2.5min)
- Monitor CPU usage
- Check memory consumption
- Verify disk space
- Trigger auto-scaling if needed
- Clear caches if memory is high
- Rotate logs if disk is full

### Phase 4: Code Quality (Every 10 cycles - 5min)
- Validate Python syntax
- Check for import errors
- Verify file structure
- Report issues

### Phase 5: Documentation (Every 20 cycles - 10min)
- Generate status report
- Update SYSTEM_STATUS_LIVE.md
- Archive historical data
- Create metrics snapshots

### Phase 6: Security Scanning (Every 15 cycles - 7.5min)
- Check debug mode settings
- Validate file permissions
- Scan for common vulnerabilities
- Report security issues

### Phase 7: Load Testing (Every 30 cycles - 15min)
- Send test requests to backend
- Measure response times
- Calculate average latency
- Detect performance degradation

### Phase 8: Metrics & Reporting (Every cycle - 30s)
- Update agent uptime
- Count health checks
- Track fixes applied
- Report service status

---

## Monitored Services

### Backend Service
- **Port**: 8000
- **Health URL**: `http://localhost:8000/api/health`
- **Critical**: Yes (auto-restart immediately)
- **Start Command**: `.venv/bin/python -m uvicorn backend.main:app --port 8000`

### Frontend Service
- **Port**: 8080
- **Health URL**: `http://localhost:8080/quetzal-browser.html`
- **Critical**: No (restart with lower priority)
- **Start Command**: `python3 -m http.server 8080`
- **Working Directory**: `frontend/`

---

## Configuration

The agent is configured in `agent_runner.py`:

```python
self.service_configs = {
    'backend': {
        'port': 8000,
        'health_url': 'http://localhost:8000/api/health',
        'start_cmd': ['.venv/bin/python', '-m', 'uvicorn', 'backend.main:app', '--port', '8000'],
        'critical': True
    },
    'frontend': {
        'port': 8080,
        'health_url': 'http://localhost:8080/quetzal-browser.html',
        'start_cmd': ['python3', '-m', 'http.server', '8080'],
        'cwd': 'frontend',
        'critical': False
    }
}
```

### Adding New Services

To monitor additional services, add them to `service_configs`:

```python
'new_service': {
    'port': 9000,
    'health_url': 'http://localhost:9000/health',
    'start_cmd': ['path/to/service'],
    'cwd': 'service_directory',  # Optional
    'critical': True  # Auto-restart immediately
}
```

---

## Thresholds

The agent uses these thresholds for auto-actions:

| Metric | Threshold | Action |
|--------|-----------|--------|
| CPU Usage | > 80% | Trigger auto-scaling alert |
| Memory Usage | > 85% | Clear caches |
| Disk Usage | > 90% | Rotate logs |
| Service Failures | > 3 consecutive | Alert (but keep retrying) |
| Response Latency | > 500ms | Performance warning |
| Log File Size | > 100MB | Auto-rotate |

---

## Logs

### Agent Log
- **File**: `agent_runner.log`
- **Format**: Timestamped with log levels
- **Rotation**: Automatic when > 100MB
- **Contents**: All agent activities, health checks, fixes

### Startup Log
- **File**: `agent_runner_startup.log`
- **Contents**: Initial startup output and early errors

### Service Logs
Services may have their own logs in `/tmp/` or service directories.

---

## Metrics Tracked

### Agent Metrics
- **Uptime**: How long the agent has been running
- **Total Checks**: Number of health checks performed
- **Total Fixes**: Number of services restarted
- **Total Optimizations**: Performance improvements applied

### Service Metrics (per service)
- **Status**: healthy/unhealthy
- **Uptime**: Time since last restart
- **Restarts**: Number of times restarted
- **Failures**: Consecutive failures
- **Last Check**: Timestamp of last health check

### System Metrics
- **CPU Usage**: Percentage
- **Memory Usage**: Percentage and absolute
- **Disk Usage**: Percentage and absolute
- **Process Count**: Active processes

---

## Status Reports

### Live Status
- **File**: `SYSTEM_STATUS_LIVE.md`
- **Update Frequency**: Every 10 minutes
- **Contents**: Current system state, service status, resources

### Final Status
- **File**: `SYSTEM_STATUS_FINAL.md`
- **Created**: When agent stops
- **Contents**: Complete session summary, total metrics

---

## Troubleshooting

### Agent Won't Start

```bash
# Check for errors
cat agent_runner_startup.log

# Verify Python environment
.venv/bin/python --version

# Install missing dependencies
.venv/bin/pip install psutil requests
```

### Services Keep Failing

```bash
# View agent log
tail -f agent_runner.log

# Check service-specific logs
ls -lh /tmp/*backend*.log

# Manual service test
.venv/bin/python -m uvicorn backend.main:app --port 8000
```

### High Resource Usage

```bash
# Check what agent is doing
cat SYSTEM_STATUS_LIVE.md

# Temporarily stop agent
./stop-agent.sh

# Investigate system resources
htop
```

### Agent Not Healing Services

Check if:
1. Port is actually blocked: `lsof -i :8000`
2. Permissions are correct: `ls -la start-agent.sh`
3. Service command is valid: test manually
4. Virtual environment is activated

---

## Integration with Other Scripts

### With QuetzalCore Browser

```bash
# Start everything with agent monitoring
./start-agent.sh
./start-quetzal-browser.sh
```

The agent will monitor both backend and frontend.

### With Manual Operations

The agent detects and works around manual operations:
- If you manually start/stop services, agent adapts
- If you manually fix issues, agent detects and logs
- Agent won't fight with manual interventions

---

## Advanced Usage

### Custom Monitoring

Edit `agent_runner.py` to add custom checks:

```python
async def custom_check(self):
    """Your custom monitoring logic"""
    # Check something specific
    if condition:
        logger.warning("Custom alert!")
        await self.custom_fix()
```

Add to main loop:

```python
if iteration % 25 == 0:  # Every 25 cycles
    await self.custom_check()
```

### Alerting Integration

Add webhook calls for critical alerts:

```python
import requests

async def send_alert(self, message: str):
    """Send alert to external system"""
    try:
        requests.post('https://your-webhook.com/alert', 
                     json={'message': message})
    except Exception as e:
        logger.error(f"Failed to send alert: {e}")
```

### Metrics Export

Export metrics to external systems:

```python
async def export_metrics(self):
    """Export to Prometheus/Grafana/etc"""
    metrics = {
        'agent_uptime': time.time() - self.metrics['uptime_start'],
        'total_checks': self.metrics['total_checks'],
        'total_fixes': self.metrics['total_fixes']
    }
    # Send to your monitoring system
```

---

## Best Practices

1. **Let the Agent Run**: Don't interfere unless necessary
2. **Monitor the Logs**: `tail -f agent_runner.log`
3. **Check Status Regularly**: `cat SYSTEM_STATUS_LIVE.md`
4. **Graceful Shutdowns**: Use `./stop-agent.sh` not `kill -9`
5. **Review Final Reports**: Check `SYSTEM_STATUS_FINAL.md` after stops
6. **Adjust Thresholds**: Tune based on your system
7. **Add Custom Checks**: Extend for your specific needs

---

## Performance Impact

The agent is designed to be lightweight:

- **CPU Usage**: < 1% average
- **Memory Usage**: ~50-100MB
- **Disk I/O**: Minimal (mostly logging)
- **Network**: Only health check requests

Typical overhead per cycle:
- Health checks: ~10ms per service
- Resource monitoring: ~50ms
- Auto-healing (when needed): ~2-5 seconds
- Everything else: < 100ms

**Total**: < 200ms every 30 seconds = 0.67% time overhead

---

## Future Enhancements

Planned features:

- [ ] Machine learning for failure prediction
- [ ] Automatic performance tuning
- [ ] Distributed agent deployment
- [ ] Advanced anomaly detection
- [ ] Auto-scaling cluster management
- [ ] Integration with cloud providers
- [ ] Slack/Discord notifications
- [ ] Web dashboard for agent status
- [ ] Historical trends and analytics
- [ ] Predictive maintenance

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                Autonomous Agent Runner                   │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Main Loop (every 30 seconds)                      │ │
│  │                                                     │ │
│  │  Phase 1: Health Monitoring                        │ │
│  │  Phase 2: Auto-Healing                             │ │
│  │  Phase 3: Performance Optimization (2.5min)        │ │
│  │  Phase 4: Code Quality (5min)                      │ │
│  │  Phase 5: Documentation (10min)                    │ │
│  │  Phase 6: Security (7.5min)                        │ │
│  │  Phase 7: Load Testing (15min)                     │ │
│  │  Phase 8: Metrics & Reporting                      │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Backend    │  │   Frontend   │  │   Future     │ │
│  │   Service    │  │   Service    │  │   Services   │ │
│  │   (8000)     │  │   (8080)     │  │              │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│         ▲                ▲                    ▲         │
│         │                │                    │         │
│         └────────────────┴────────────────────┘         │
│                  Health Checks                          │
│                  Auto-Restart                           │
│                  Performance                            │
└─────────────────────────────────────────────────────────┘
```

---

## Support

For issues or questions:

- Check logs: `agent_runner.log`
- View status: `SYSTEM_STATUS_LIVE.md`
- Run diagnostic: `./diagnose-routing.sh`
- Test routes: `./test-api-routes.py`

---

**Built with ❤️ for autonomous operations**

**Dale! Let the agent work for you! 🤖**
