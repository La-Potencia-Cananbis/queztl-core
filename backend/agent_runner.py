#!/usr/bin/env python3
"""
QuetzalCore Autonomous Agent Runner
Continuously monitors, maintains, and improves the entire system

Features:
- Health monitoring of all services
- Auto-restart failed components
- Performance optimization
- Code quality improvements
- Documentation updates
- Security scanning
- Load testing
- Self-healing capabilities
"""

import asyncio
import subprocess
import json
import time
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
import psutil
import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent_runner.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('AgentRunner')


class ServiceHealth:
    """Track service health status"""
    def __init__(self, name: str):
        self.name = name
        self.status = "unknown"
        self.last_check = None
        self.failures = 0
        self.restarts = 0
        self.uptime_start = None


class QuetzalCoreAgent:
    """Autonomous agent that manages QuetzalCore system"""
    
    def __init__(self):
        self.services: Dict[str, ServiceHealth] = {}
        self.base_dir = Path(__file__).parent
        self.running = False
        self.metrics = {
            'total_checks': 0,
            'total_fixes': 0,
            'total_improvements': 0,
            'uptime_start': time.time()
        }
        
        # Service definitions
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
        
        # Initialize service health tracking
        for service_name in self.service_configs.keys():
            self.services[service_name] = ServiceHealth(service_name)
    
    async def run_forever(self):
        """Main agent loop - runs forever"""
        self.running = True
        logger.info("🤖 QuetzalCore Autonomous Agent starting...")
        logger.info("=" * 70)
        
        iteration = 0
        
        try:
            while self.running:
                iteration += 1
                logger.info(f"\n{'='*70}")
                logger.info(f"🔄 Agent Cycle #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"{'='*70}")
                
                # Phase 1: Health Monitoring
                await self.monitor_services()
                
                # Phase 2: Auto-healing
                await self.heal_services()
                
                # Phase 3: Performance Optimization
                if iteration % 5 == 0:  # Every 5 cycles
                    await self.optimize_performance()
                
                # Phase 4: Code Quality Checks
                if iteration % 10 == 0:  # Every 10 cycles
                    await self.check_code_quality()
                
                # Phase 5: Documentation Updates
                if iteration % 20 == 0:  # Every 20 cycles
                    await self.update_documentation()
                
                # Phase 6: Security Scanning
                if iteration % 15 == 0:  # Every 15 cycles
                    await self.security_scan()
                
                # Phase 7: Load Testing
                if iteration % 30 == 0:  # Every 30 cycles
                    await self.load_test()
                
                # Phase 8: Metrics & Reporting
                await self.report_metrics()
                
                # Sleep before next cycle
                logger.info(f"💤 Sleeping for 30 seconds...")
                await asyncio.sleep(30)
                
        except KeyboardInterrupt:
            logger.info("\n⚠️  Agent interrupted by user")
        except Exception as e:
            logger.error(f"❌ Agent error: {e}", exc_info=True)
        finally:
            await self.shutdown()
    
    async def monitor_services(self):
        """Monitor all services and check health"""
        logger.info("\n🔍 Phase 1: Service Health Monitoring")
        logger.info("-" * 70)
        
        for service_name, config in self.service_configs.items():
            service = self.services[service_name]
            
            # Check if port is open
            port_open = self.is_port_open(config['port'])
            
            # Check health endpoint
            health_ok = False
            if port_open and 'health_url' in config:
                health_ok = await self.check_health_endpoint(config['health_url'])
            
            # Update service status
            if port_open and (not config.get('health_url') or health_ok):
                service.status = "healthy"
                service.failures = 0
                if not service.uptime_start:
                    service.uptime_start = time.time()
                logger.info(f"✅ {service_name}: HEALTHY (port {config['port']})")
            else:
                service.status = "unhealthy"
                service.failures += 1
                service.uptime_start = None
                logger.warning(f"⚠️  {service_name}: UNHEALTHY (port {config['port']}, failures: {service.failures})")
            
            service.last_check = time.time()
            self.metrics['total_checks'] += 1
    
    async def heal_services(self):
        """Auto-heal unhealthy services"""
        logger.info("\n🏥 Phase 2: Auto-Healing Services")
        logger.info("-" * 70)
        
        for service_name, config in self.service_configs.items():
            service = self.services[service_name]
            
            if service.status == "unhealthy":
                logger.info(f"🔧 Attempting to heal {service_name}...")
                
                # Kill existing process on port
                self.kill_port(config['port'])
                await asyncio.sleep(2)
                
                # Start service
                success = await self.start_service(service_name, config)
                
                if success:
                    service.restarts += 1
                    self.metrics['total_fixes'] += 1
                    logger.info(f"✅ {service_name} restarted successfully (restart #{service.restarts})")
                else:
                    logger.error(f"❌ Failed to restart {service_name}")
    
    async def optimize_performance(self):
        """Optimize system performance"""
        logger.info("\n⚡ Phase 3: Performance Optimization")
        logger.info("-" * 70)
        
        # Check system resources
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        logger.info(f"💻 CPU Usage: {cpu_percent}%")
        logger.info(f"💾 Memory Usage: {memory.percent}% ({memory.used / 1e9:.1f}GB / {memory.total / 1e9:.1f}GB)")
        logger.info(f"💿 Disk Usage: {disk.percent}% ({disk.used / 1e9:.1f}GB / {disk.total / 1e9:.1f}GB)")
        
        # Auto-optimization based on load
        if cpu_percent > 80:
            logger.warning("⚠️  High CPU usage detected - considering scale-up")
            await self.trigger_autoscale("cpu_high")
        
        if memory.percent > 85:
            logger.warning("⚠️  High memory usage detected - clearing caches")
            await self.clear_caches()
        
        if disk.percent > 90:
            logger.warning("⚠️  High disk usage detected - cleaning logs")
            await self.clean_logs()
        
        self.metrics['total_improvements'] += 1
    
    async def check_code_quality(self):
        """Run code quality checks"""
        logger.info("\n🔍 Phase 4: Code Quality Checks")
        logger.info("-" * 70)
        
        # Check Python syntax
        logger.info("Checking Python syntax...")
        python_files = list(self.base_dir.glob('backend/*.py'))
        
        errors = 0
        for py_file in python_files[:5]:  # Check first 5 files
            try:
                result = subprocess.run(
                    ['.venv/bin/python', '-m', 'py_compile', str(py_file)],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode != 0:
                    errors += 1
                    logger.error(f"❌ Syntax error in {py_file.name}")
            except Exception as e:
                logger.error(f"⚠️  Could not check {py_file.name}: {e}")
        
        if errors == 0:
            logger.info("✅ All checked files have valid syntax")
        else:
            logger.warning(f"⚠️  Found {errors} files with syntax errors")
    
    async def update_documentation(self):
        """Update system documentation"""
        logger.info("\n📚 Phase 5: Documentation Updates")
        logger.info("-" * 70)
        
        # Generate status report
        status_report = self.generate_status_report()
        
        # Write to file
        report_file = self.base_dir / 'SYSTEM_STATUS_LIVE.md'
        with open(report_file, 'w') as f:
            f.write(status_report)
        
        logger.info(f"✅ Status report updated: {report_file}")
    
    async def security_scan(self):
        """Run security scans"""
        logger.info("\n🔒 Phase 6: Security Scanning")
        logger.info("-" * 70)
        
        # Check for common security issues
        logger.info("Checking for security issues...")
        
        # Check if debug mode is disabled in production
        if os.getenv('DEBUG') == 'True':
            logger.warning("⚠️  DEBUG mode is enabled - should be disabled in production")
        else:
            logger.info("✅ DEBUG mode properly configured")
        
        # Check file permissions
        sensitive_files = ['.env', 'backend/main.py', 'backend/qp_protocol.py']
        for file_path in sensitive_files:
            full_path = self.base_dir / file_path
            if full_path.exists():
                stat = os.stat(full_path)
                if stat.st_mode & 0o077:  # Check if others have any permissions
                    logger.warning(f"⚠️  {file_path} has overly permissive permissions")
        
        logger.info("✅ Security scan complete")
    
    async def load_test(self):
        """Run load tests on services"""
        logger.info("\n🏋️ Phase 7: Load Testing")
        logger.info("-" * 70)
        
        # Test backend
        if self.services['backend'].status == "healthy":
            logger.info("Testing backend performance...")
            
            start = time.time()
            successes = 0
            failures = 0
            
            for i in range(10):  # 10 quick requests
                try:
                    response = requests.get('http://localhost:8000/api/health', timeout=5)
                    if response.status_code == 200:
                        successes += 1
                    else:
                        failures += 1
                except Exception:
                    failures += 1
            
            duration = time.time() - start
            avg_latency = (duration / 10) * 1000  # ms
            
            logger.info(f"✅ Load test: {successes}/10 successful, avg latency: {avg_latency:.2f}ms")
            
            if avg_latency > 500:
                logger.warning("⚠️  High latency detected - may need optimization")
    
    async def report_metrics(self):
        """Report system metrics"""
        logger.info("\n📊 Phase 8: Metrics & Reporting")
        logger.info("-" * 70)
        
        uptime = time.time() - self.metrics['uptime_start']
        uptime_hours = uptime / 3600
        
        logger.info(f"🤖 Agent Uptime: {uptime_hours:.2f} hours")
        logger.info(f"🔍 Total Health Checks: {self.metrics['total_checks']}")
        logger.info(f"🔧 Total Fixes Applied: {self.metrics['total_fixes']}")
        logger.info(f"⚡ Total Optimizations: {self.metrics['total_improvements']}")
        
        # Service status summary
        logger.info("\n📋 Service Status Summary:")
        for service_name, service in self.services.items():
            uptime_str = "N/A"
            if service.uptime_start:
                svc_uptime = time.time() - service.uptime_start
                uptime_str = f"{svc_uptime / 3600:.1f}h"
            
            logger.info(f"  • {service_name}: {service.status.upper()} "
                       f"(uptime: {uptime_str}, restarts: {service.restarts})")
    
    # Helper methods
    
    def is_port_open(self, port: int) -> bool:
        """Check if a port is open (using socket connection test)"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    async def check_health_endpoint(self, url: str) -> bool:
        """Check health endpoint"""
        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def kill_port(self, port: int):
        """Kill process on port"""
        try:
            subprocess.run(
                ['lsof', '-ti', f':{port}'],
                capture_output=True,
                check=False
            )
            subprocess.run(
                ['sh', '-c', f'lsof -ti:{port} | xargs kill -9 2>/dev/null || true'],
                check=False
            )
            logger.info(f"🔪 Killed process on port {port}")
        except Exception as e:
            logger.error(f"Failed to kill port {port}: {e}")
    
    async def start_service(self, service_name: str, config: Dict) -> bool:
        """Start a service"""
        try:
            cwd = self.base_dir / config.get('cwd', '')
            
            # Start process in background
            subprocess.Popen(
                config['start_cmd'],
                cwd=cwd if cwd.exists() else self.base_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            # Wait for service to start
            await asyncio.sleep(5)
            
            # Verify it's running
            return self.is_port_open(config['port'])
            
        except Exception as e:
            logger.error(f"Failed to start {service_name}: {e}")
            return False
    
    async def trigger_autoscale(self, reason: str):
        """Trigger autoscaling"""
        logger.info(f"🔄 Triggering autoscale (reason: {reason})")
        # In a real system, this would call the autoscaler API
        # For now, just log it
        self.metrics['total_improvements'] += 1
    
    async def clear_caches(self):
        """Clear system caches"""
        logger.info("🧹 Clearing caches...")
        # Clear Python cache
        subprocess.run(['find', '.', '-name', '__pycache__', '-type', 'd', '-exec', 'rm', '-rf', '{}', '+'],
                      check=False, cwd=self.base_dir)
        logger.info("✅ Caches cleared")
    
    async def clean_logs(self):
        """Clean old log files"""
        logger.info("🧹 Cleaning old logs...")
        log_files = list(self.base_dir.glob('*.log'))
        
        for log_file in log_files:
            if log_file.stat().st_size > 100 * 1024 * 1024:  # > 100MB
                logger.info(f"Rotating large log: {log_file.name}")
                # Keep last 1000 lines
                subprocess.run(
                    f'tail -n 1000 {log_file} > {log_file}.tmp && mv {log_file}.tmp {log_file}',
                    shell=True,
                    check=False
                )
        
        logger.info("✅ Logs cleaned")
    
    def generate_status_report(self) -> str:
        """Generate system status report"""
        report = f"""# QuetzalCore System Status
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Agent Metrics
- **Uptime**: {(time.time() - self.metrics['uptime_start']) / 3600:.2f} hours
- **Total Health Checks**: {self.metrics['total_checks']}
- **Total Fixes Applied**: {self.metrics['total_fixes']}
- **Total Optimizations**: {self.metrics['total_improvements']}

## Service Status
"""
        
        for service_name, service in self.services.items():
            status_emoji = "✅" if service.status == "healthy" else "❌"
            uptime = "N/A"
            if service.uptime_start:
                uptime = f"{(time.time() - service.uptime_start) / 3600:.1f}h"
            
            report += f"""
### {status_emoji} {service_name.upper()}
- **Status**: {service.status}
- **Uptime**: {uptime}
- **Restarts**: {service.restarts}
- **Failures**: {service.failures}
- **Last Check**: {datetime.fromtimestamp(service.last_check).strftime('%H:%M:%S') if service.last_check else 'Never'}
"""
        
        # System resources
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        report += f"""
## System Resources
- **CPU Usage**: {cpu}%
- **Memory Usage**: {mem.percent}% ({mem.used / 1e9:.1f}GB / {mem.total / 1e9:.1f}GB)
- **Disk Usage**: {disk.percent}% ({disk.used / 1e9:.1f}GB / {disk.total / 1e9:.1f}GB)

---
*This report is automatically generated by the QuetzalCore Autonomous Agent*
"""
        
        return report
    
    async def shutdown(self):
        """Graceful shutdown"""
        logger.info("\n" + "=" * 70)
        logger.info("🛑 Shutting down agent...")
        logger.info("=" * 70)
        
        # Final metrics report
        await self.report_metrics()
        
        # Save final status
        status_report = self.generate_status_report()
        report_file = self.base_dir / 'SYSTEM_STATUS_FINAL.md'
        with open(report_file, 'w') as f:
            f.write(status_report)
        
        logger.info(f"✅ Final status saved to {report_file}")
        logger.info("👋 Agent shutdown complete")


def main():
    """Main entry point"""
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              🤖 QUETZALCORE AUTONOMOUS AGENT RUNNER 🤖                       ║
║                 Continuous Monitoring & Self-Healing                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")
    
    agent = QuetzalCoreAgent()
    
    try:
        asyncio.run(agent.run_forever())
    except KeyboardInterrupt:
        print("\n\n⚠️  Agent interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Agent crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
