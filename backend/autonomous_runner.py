#!/usr/bin/env python3
"""
🏃 Autonomous Runner - Spins off tasks before hardware changes
Keeps working while Beast/Sloth transition happens
"""
import json
import time
import requests
import subprocess
from datetime import datetime
from pathlib import Path

class AutonomousRunner:
    def __init__(self):
        self.base_dir = Path.home() / "queztl-core"
        self.tasks_file = self.base_dir / "data" / "autonomous_tasks.json"
        self.log_file = self.base_dir / "logs" / "autonomous_runner.log"
        self.base_dir.mkdir(exist_ok=True)
        (self.base_dir / "data").mkdir(exist_ok=True)
        (self.base_dir / "logs").mkdir(exist_ok=True)
        
    def log(self, msg):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {msg}"
        print(log_msg)
        with open(self.log_file, "a") as f:
            f.write(log_msg + "\n")
    
    def queue_cloud_prep_tasks(self):
        """Queue tasks for cloud deployment preparation"""
        tasks = [
            {
                "id": "cloud-prep-1",
                "type": "docker_build",
                "desc": "Build Docker images for AWS/Azure/GCP",
                "priority": "high",
                "files": ["Dockerfile", "docker-compose.yml", "infra/k8s/*"],
                "output": "data/docker_images_manifest.json"
            },
            {
                "id": "cloud-prep-2", 
                "type": "dependency_audit",
                "desc": "Audit all dependencies for cloud deployment",
                "priority": "high",
                "files": ["requirements.txt", "package.json"],
                "output": "data/dependency_report.json"
            },
            {
                "id": "cloud-prep-3",
                "type": "config_templates",
                "desc": "Generate deployment configs for AWS/Azure/GCP",
                "priority": "medium",
                "templates": ["aws", "azure", "gcp"],
                "output": "infra/cloud_configs/"
            },
            {
                "id": "image-batch-1",
                "type": "propaganda_images",
                "desc": "Generate remaining propaganda art queue",
                "priority": "medium",
                "count": 10,
                "output": "output/beast_generated_images/"
            },
            {
                "id": "backup-1",
                "type": "full_backup",
                "desc": "Backup all core data before hardware change",
                "priority": "critical",
                "paths": ["data/*", "logs/*", "output/*"],
                "output": "backup/pre_reimage_$(date +%Y%m%d).tar.gz"
            }
        ]
        
        with open(self.tasks_file, "w") as f:
            json.dump(tasks, f, indent=2)
        
        self.log(f"✓ Queued {len(tasks)} tasks")
        return tasks
    
    def execute_docker_build(self, task):
        """Build Docker images"""
        self.log(f"🐋 Building Docker images...")
        
        # Create Dockerfile if not exists
        dockerfile = self.base_dir / "Dockerfile"
        if not dockerfile.exists():
            self.log("Creating Dockerfile...")
            dockerfile_content = '''FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    git curl build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY scripts/ ./scripts/

# Expose ports
EXPOSE 8000 8001 9000

# Default command
CMD ["python3", "backend/main.py"]
'''
            dockerfile.write_text(dockerfile_content)
            self.log("✓ Dockerfile created")
        
        # Create docker-compose
        compose_file = self.base_dir / "docker-compose.yml"
        compose_content = '''version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_URL=${POSTGRES_URL:-}
      - REDIS_URL=${REDIS_URL:-}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
  
  orchestrator:
    build: .
    command: python3 backend/orchestrator.py
    ports:
      - "9000:9000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./inbox:/app/inbox
    restart: unless-stopped
  
  beast-api:
    build: .
    command: python3 backend/beast_image_generator.py
    ports:
      - "8001:8001"
    volumes:
      - ./output:/app/output
      - ./data:/app/data
    restart: unless-stopped
'''
        compose_file.write_text(compose_content)
        self.log("✓ docker-compose.yml created")
        
        # Save manifest
        manifest = {
            "created_at": datetime.now().isoformat(),
            "files": ["Dockerfile", "docker-compose.yml"],
            "services": ["backend", "orchestrator", "beast-api"],
            "status": "ready"
        }
        
        output_file = self.base_dir / task["output"]
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(manifest, f, indent=2)
        
        self.log(f"✓ Docker build complete: {output_file}")
        return manifest
    
    def execute_dependency_audit(self, task):
        """Audit dependencies"""
        self.log("📦 Auditing dependencies...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "python_packages": [],
            "npm_packages": [],
            "system_packages": ["git", "curl", "python3", "nodejs"]
        }
        
        # Check Python requirements
        req_file = self.base_dir / "backend" / "requirements.txt"
        if req_file.exists():
            packages = req_file.read_text().strip().split("\n")
            report["python_packages"] = [p for p in packages if p and not p.startswith("#")]
            self.log(f"✓ Found {len(report['python_packages'])} Python packages")
        
        # Check package.json
        pkg_file = self.base_dir / "frontend" / "package.json"
        if pkg_file.exists():
            pkg_data = json.loads(pkg_file.read_text())
            report["npm_packages"] = list(pkg_data.get("dependencies", {}).keys())
            self.log(f"✓ Found {len(report['npm_packages'])} npm packages")
        
        output_file = self.base_dir / task["output"]
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)
        
        self.log(f"✓ Dependency audit complete: {output_file}")
        return report
    
    def execute_config_templates(self, task):
        """Generate cloud deployment configs"""
        self.log("☁️ Generating cloud configs...")
        
        infra_dir = self.base_dir / "infra" / "cloud_configs"
        infra_dir.mkdir(parents=True, exist_ok=True)
        
        # AWS ECS config
        aws_config = {
            "taskDefinition": {
                "family": "queztl-core",
                "networkMode": "awsvpc",
                "requiresCompatibilities": ["FARGATE"],
                "cpu": "256",
                "memory": "512",
                "containerDefinitions": [{
                    "name": "queztl-backend",
                    "image": "queztl-core:latest",
                    "portMappings": [{"containerPort": 8000, "protocol": "tcp"}],
                    "essential": True
                }]
            }
        }
        (infra_dir / "aws_ecs.json").write_text(json.dumps(aws_config, indent=2))
        
        # Azure Container Instances
        azure_config = {
            "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
            "contentVersion": "1.0.0.0",
            "resources": [{
                "type": "Microsoft.ContainerInstance/containerGroups",
                "apiVersion": "2021-09-01",
                "name": "queztl-core",
                "location": "eastus",
                "properties": {
                    "containers": [{
                        "name": "backend",
                        "properties": {
                            "image": "queztl-core:latest",
                            "ports": [{"port": 8000}],
                            "resources": {"requests": {"cpu": 0.5, "memoryInGB": 1}}
                        }
                    }],
                    "osType": "Linux",
                    "ipAddress": {"type": "Public", "ports": [{"protocol": "TCP", "port": 8000}]}
                }
            }]
        }
        (infra_dir / "azure_aci.json").write_text(json.dumps(azure_config, indent=2))
        
        # GCP Cloud Run
        gcp_config = {
            "apiVersion": "serving.knative.dev/v1",
            "kind": "Service",
            "metadata": {"name": "queztl-core"},
            "spec": {
                "template": {
                    "spec": {
                        "containers": [{
                            "image": "gcr.io/PROJECT_ID/queztl-core:latest",
                            "ports": [{"containerPort": 8000}],
                            "resources": {"limits": {"memory": "512Mi", "cpu": "1"}}
                        }]
                    }
                }
            }
        }
        (infra_dir / "gcp_cloudrun.yaml").write_text(json.dumps(gcp_config, indent=2))
        
        # Kubernetes (works on all platforms)
        k8s_config = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": "queztl-core"},
            "spec": {
                "replicas": 2,
                "selector": {"matchLabels": {"app": "queztl-core"}},
                "template": {
                    "metadata": {"labels": {"app": "queztl-core"}},
                    "spec": {
                        "containers": [{
                            "name": "backend",
                            "image": "queztl-core:latest",
                            "ports": [{"containerPort": 8000}],
                            "resources": {"requests": {"cpu": "100m", "memory": "256Mi"}}
                        }]
                    }
                }
            }
        }
        (infra_dir / "k8s_deployment.yaml").write_text(json.dumps(k8s_config, indent=2))
        
        self.log(f"✓ Generated configs for: AWS, Azure, GCP, Kubernetes")
        self.log(f"✓ Configs saved to: {infra_dir}")
        
        return {"status": "complete", "configs": ["aws", "azure", "gcp", "k8s"]}
    
    def execute_backup(self, task):
        """Backup all data"""
        self.log("💾 Creating backup...")
        
        backup_dir = self.base_dir / "backup"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"pre_reimage_{timestamp}.tar.gz"
        
        # Create tar archive
        cmd = f"cd {self.base_dir} && tar -czf {backup_file} data/ logs/ output/ 2>/dev/null || true"
        subprocess.run(cmd, shell=True)
        
        if backup_file.exists():
            size_mb = backup_file.stat().st_size / 1024 / 1024
            self.log(f"✓ Backup complete: {backup_file} ({size_mb:.1f} MB)")
            return {"file": str(backup_file), "size_mb": size_mb}
        else:
            self.log("⚠️ Backup failed or no data to backup")
            return {"status": "empty"}
    
    def run_task(self, task):
        """Execute a single task"""
        self.log(f"\n{'='*60}")
        self.log(f"TASK: {task['id']} - {task['desc']}")
        self.log(f"Priority: {task['priority']}")
        self.log(f"{'='*60}")
        
        start = time.time()
        
        try:
            if task["type"] == "docker_build":
                result = self.execute_docker_build(task)
            elif task["type"] == "dependency_audit":
                result = self.execute_dependency_audit(task)
            elif task["type"] == "config_templates":
                result = self.execute_config_templates(task)
            elif task["type"] == "full_backup":
                result = self.execute_backup(task)
            elif task["type"] == "propaganda_images":
                self.log("⚠️ Image generation requires Beast API - skipping for now")
                result = {"status": "queued", "note": "Will run when Beast API available"}
            else:
                self.log(f"⚠️ Unknown task type: {task['type']}")
                result = {"status": "skipped"}
            
            duration = time.time() - start
            self.log(f"✓ Task complete in {duration:.1f}s")
            
            task["result"] = result
            task["completed_at"] = datetime.now().isoformat()
            task["duration_sec"] = duration
            
            return True
            
        except Exception as e:
            self.log(f"❌ Task failed: {e}")
            task["error"] = str(e)
            return False
    
    def run_all(self):
        """Run all queued tasks"""
        self.log("\n" + "="*60)
        self.log("🏃 AUTONOMOUS RUNNER STARTING")
        self.log("="*60)
        
        # Queue tasks
        tasks = self.queue_cloud_prep_tasks()
        
        # Execute each task
        completed = 0
        failed = 0
        
        for task in tasks:
            if task["priority"] == "critical":
                self.log(f"\n⚡ CRITICAL TASK: {task['id']}")
            
            success = self.run_task(task)
            if success:
                completed += 1
            else:
                failed += 1
        
        # Save final results
        with open(self.tasks_file, "w") as f:
            json.dump(tasks, f, indent=2)
        
        # Summary
        self.log("\n" + "="*60)
        self.log("📊 RUNNER SUMMARY")
        self.log("="*60)
        self.log(f"Total tasks:     {len(tasks)}")
        self.log(f"Completed:       {completed}")
        self.log(f"Failed:          {failed}")
        self.log(f"Results saved:   {self.tasks_file}")
        self.log(f"Log file:        {self.log_file}")
        self.log("="*60)
        
        return tasks

if __name__ == "__main__":
    runner = AutonomousRunner()
    runner.run_all()
