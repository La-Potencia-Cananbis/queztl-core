#!/usr/bin/env python3
"""
🤖 Git Automation System
Monitors repos, triggers builds, manages webhooks, coordinates with cluster
"""
import os
import json
import time
import redis
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import git
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GitAutomation:
    def __init__(self):
        self.gitea_url = os.getenv("GITEA_URL", "http://gitea:3000")
        self.gitea_token = os.getenv("GITEA_TOKEN", "")
        self.beast_url = os.getenv("BEAST_URL", "http://192.168.1.105:8001")
        self.sloth_url = os.getenv("SLOTH_URL", "http://192.168.1.102:9000")
        
        self.redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)
        self.log_dir = Path("/logs")
        self.log_dir.mkdir(exist_ok=True)
        
        self.log("🤖 Git Automation System Starting...")
    
    def log(self, msg: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {msg}"
        print(log_msg)
        
        log_file = self.log_dir / f"git_automation_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, "a") as f:
            f.write(log_msg + "\n")
    
    def get_repos(self) -> List[Dict]:
        """Get all repositories from Gitea"""
        try:
            headers = {"Authorization": f"token {self.gitea_token}"}
            response = requests.get(
                f"{self.gitea_url}/api/v1/user/repos",
                headers=headers,
                timeout=10
            )
            if response.ok:
                return response.json()
            return []
        except Exception as e:
            self.log(f"⚠️ Error fetching repos: {e}")
            return []
    
    def setup_webhooks(self, repo_full_name: str):
        """Setup webhooks for a repository"""
        self.log(f"🪝 Setting up webhooks for {repo_full_name}...")
        
        webhooks = [
            {
                "type": "gitea",
                "config": {
                    "url": f"{self.sloth_url}/git-webhook",
                    "content_type": "json"
                },
                "events": ["push", "pull_request"],
                "active": True
            }
        ]
        
        try:
            headers = {
                "Authorization": f"token {self.gitea_token}",
                "Content-Type": "application/json"
            }
            
            for webhook in webhooks:
                response = requests.post(
                    f"{self.gitea_url}/api/v1/repos/{repo_full_name}/hooks",
                    headers=headers,
                    json=webhook,
                    timeout=10
                )
                if response.ok:
                    self.log(f"✓ Webhook created for {repo_full_name}")
                else:
                    self.log(f"⚠️ Webhook creation failed: {response.text}")
        
        except Exception as e:
            self.log(f"❌ Error setting up webhooks: {e}")
    
    def analyze_commit(self, repo_path: str, commit_sha: str) -> Dict[str, Any]:
        """Analyze a commit for changes"""
        try:
            repo = git.Repo(repo_path)
            commit = repo.commit(commit_sha)
            
            analysis = {
                "sha": commit_sha,
                "author": str(commit.author),
                "message": commit.message,
                "timestamp": commit.committed_datetime.isoformat(),
                "files_changed": [],
                "stats": {},
                "triggers": []
            }
            
            # Get changed files
            if commit.parents:
                diffs = commit.parents[0].diff(commit)
                for diff in diffs:
                    file_path = diff.b_path if diff.b_path else diff.a_path
                    analysis["files_changed"].append({
                        "path": file_path,
                        "change_type": diff.change_type,
                        "additions": diff.b_blob.size if diff.b_blob else 0,
                        "deletions": diff.a_blob.size if diff.a_blob else 0
                    })
            
            # Determine what to trigger
            for file_info in analysis["files_changed"]:
                path = file_info["path"]
                
                if path.startswith("backend/"):
                    analysis["triggers"].append("backend_tests")
                    if "main.py" in path or "api" in path:
                        analysis["triggers"].append("api_restart")
                
                if path.startswith("frontend/"):
                    analysis["triggers"].append("frontend_build")
                
                if "Dockerfile" in path or "docker-compose" in path:
                    analysis["triggers"].append("docker_rebuild")
                
                if path.startswith("infra/"):
                    analysis["triggers"].append("infrastructure_update")
                
                if path.endswith(".md"):
                    analysis["triggers"].append("docs_update")
            
            analysis["triggers"] = list(set(analysis["triggers"]))
            return analysis
        
        except Exception as e:
            self.log(f"❌ Error analyzing commit: {e}")
            return {"error": str(e)}
    
    def trigger_build(self, repo_name: str, branch: str, commit_sha: str):
        """Trigger build on cluster"""
        self.log(f"🔨 Triggering build: {repo_name}@{branch} ({commit_sha[:8]})")
        
        build_job = {
            "id": f"build_{int(time.time())}",
            "type": "git_build",
            "repo": repo_name,
            "branch": branch,
            "commit": commit_sha,
            "timestamp": datetime.now().isoformat(),
            "status": "queued"
        }
        
        # Queue to Redis
        self.redis_client.lpush("build_queue", json.dumps(build_job))
        self.log(f"✓ Build queued: {build_job['id']}")
        
        # Notify orchestrator on Sloth
        try:
            response = requests.post(
                f"{self.sloth_url}/tasks/queue",
                json={
                    "type": "git_build",
                    "params": build_job
                },
                timeout=5
            )
            if response.ok:
                self.log(f"✓ Orchestrator notified")
        except:
            pass
        
        return build_job
    
    def process_webhook(self, webhook_data: Dict[str, Any]):
        """Process incoming webhook"""
        self.log(f"📬 Processing webhook: {webhook_data.get('event', 'unknown')}")
        
        if webhook_data.get("event") == "push":
            repo = webhook_data.get("repository", {})
            repo_name = repo.get("full_name", "")
            branch = webhook_data.get("ref", "").replace("refs/heads/", "")
            commits = webhook_data.get("commits", [])
            
            if commits:
                latest_commit = commits[-1]
                commit_sha = latest_commit.get("id", "")
                
                self.log(f"📝 Push to {repo_name}@{branch}: {commit_sha[:8]}")
                
                # Trigger build
                self.trigger_build(repo_name, branch, commit_sha)
        
        elif webhook_data.get("event") == "pull_request":
            pr = webhook_data.get("pull_request", {})
            pr_number = pr.get("number", "")
            action = webhook_data.get("action", "")
            
            self.log(f"🔀 PR #{pr_number} {action}")
            
            if action in ["opened", "synchronize"]:
                # Trigger PR checks
                self.log(f"✓ Triggering PR checks for #{pr_number}")
    
    def backup_repos(self):
        """Backup all repositories"""
        self.log("💾 Starting repository backup...")
        
        repos = self.get_repos()
        backup_dir = Path("/data/backups") / datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        for repo in repos:
            repo_name = repo.get("full_name", "")
            try:
                # Clone to backup location
                clone_url = repo.get("clone_url", "")
                backup_path = backup_dir / repo_name.replace("/", "_")
                
                self.log(f"  Backing up: {repo_name}")
                git.Repo.clone_from(clone_url, backup_path, bare=True)
                self.log(f"  ✓ {repo_name}")
            
            except Exception as e:
                self.log(f"  ❌ Failed to backup {repo_name}: {e}")
        
        self.log(f"✓ Backup complete: {backup_dir}")
    
    def monitor_loop(self):
        """Main monitoring loop"""
        self.log("👀 Starting monitoring loop...")
        
        cycle_count = 0
        
        while True:
            try:
                cycle_count += 1
                
                # Every 60 seconds
                if cycle_count % 60 == 0:
                    repos = self.get_repos()
                    self.log(f"📊 Monitoring {len(repos)} repositories")
                
                # Every 6 hours - backup
                if cycle_count % (6 * 3600) == 0:
                    self.backup_repos()
                
                # Check build queue
                queued_builds = self.redis_client.llen("build_queue")
                if queued_builds > 0:
                    self.log(f"📋 {queued_builds} builds in queue")
                
                time.sleep(1)
            
            except KeyboardInterrupt:
                self.log("🛑 Shutting down...")
                break
            except Exception as e:
                self.log(f"❌ Error in monitor loop: {e}")
                time.sleep(5)

class RepoChangeHandler(FileSystemEventHandler):
    """Handle filesystem changes in Git repos"""
    
    def __init__(self, automation: GitAutomation):
        self.automation = automation
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".git/HEAD"):
            repo_path = Path(event.src_path).parent.parent
            self.automation.log(f"🔄 Detected change in {repo_path}")

if __name__ == "__main__":
    automation = GitAutomation()
    
    # Start monitoring
    try:
        automation.monitor_loop()
    except KeyboardInterrupt:
        automation.log("👋 Goodbye!")
