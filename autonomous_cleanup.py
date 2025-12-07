#!/usr/bin/env python3
"""
🤖 AUTONOMOUS CLEANUP & DEPLOYMENT RUNNER
=========================================
Handles all workspace cleanup autonomously:
1. Deletes duplicate files
2. Fixes broken apps (deploys missing files)
3. Deploys dashboard
4. Tests everything

NO INTERACTION NEEDED - Just run and walk away!

Usage:
    python3 autonomous_cleanup.py
    python3 autonomous_cleanup.py --dry-run  # Preview only
"""

import os
import json
import shutil
import subprocess
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Tuple
import sys

class AutonomousCleanup:
    """Autonomous workspace cleanup and deployment"""
    
    def __init__(self, workspace_root: str, dry_run: bool = False):
        self.workspace_root = Path(workspace_root)
        self.dry_run = dry_run
        self.actions_taken = []
        self.errors = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        icon = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}.get(level, "📝")
        print(f"[{timestamp}] {icon} {message}")
        self.actions_taken.append({"time": timestamp, "level": level, "message": message})
        
    def load_audit_report(self) -> dict:
        """Load the audit report"""
        self.log("Loading audit report...")
        
        # Find most recent audit report
        audit_files = list(self.workspace_root.glob("AUDIT_REPORT_*.json"))
        if not audit_files:
            self.log("No audit report found!", "ERROR")
            return {}
        
        latest_audit = max(audit_files, key=lambda p: p.stat().st_mtime)
        self.log(f"Found audit report: {latest_audit.name}", "SUCCESS")
        
        with open(latest_audit, 'r') as f:
            return json.load(f)
    
    def delete_duplicates(self, audit_report: dict):
        """Delete duplicate files based on audit recommendations"""
        self.log("🗑️  Step 1: Deleting duplicate files...")
        
        duplicate_groups = audit_report.get('duplicate_groups', [])
        deleted_count = 0
        
        for group in duplicate_groups:
            if group['similarity'] != 1.0:
                continue  # Only delete exact duplicates
            
            recommendation = group['recommendation']
            
            # Parse recommendation to find files to delete
            if 'DELETE:' in recommendation:
                keep_part, delete_part = recommendation.split('DELETE:')
                files_to_delete = [f.strip() for f in delete_part.split(',')]
                
                for file_path in files_to_delete:
                    full_path = self.workspace_root / file_path
                    
                    if full_path.exists():
                        if self.dry_run:
                            self.log(f"Would delete: {file_path}", "INFO")
                        else:
                            try:
                                full_path.unlink()
                                self.log(f"Deleted: {file_path}", "SUCCESS")
                                deleted_count += 1
                            except Exception as e:
                                self.log(f"Failed to delete {file_path}: {e}", "ERROR")
                                self.errors.append(str(e))
        
        self.log(f"Deleted {deleted_count} duplicate files", "SUCCESS" if deleted_count > 0 else "INFO")
        
    def fix_3dmark(self):
        """Replace text-only 3DMark with graphics version"""
        self.log("🎮 Step 2: Fixing 3DMark (replacing with graphics version)...")
        
        source = self.workspace_root / "dashboard/public/3dmark-pro.html"
        dest = self.workspace_root / "3d-showcase-deploy/3d-demo.html"
        
        if not source.exists():
            self.log("Source 3dmark-pro.html not found!", "WARNING")
            return
        
        if self.dry_run:
            self.log(f"Would copy {source.name} → {dest.name}", "INFO")
            return
        
        try:
            # Backup existing
            if dest.exists():
                backup = dest.with_suffix('.html.old')
                shutil.copy2(dest, backup)
                self.log(f"Backed up original to {backup.name}", "INFO")
            
            # Copy new version
            shutil.copy2(source, dest)
            self.log("Replaced 3d-demo.html with graphics version", "SUCCESS")
            
            # Add auth check if missing
            content = dest.read_text()
            if 'queztl_auth' not in content:
                # Add auth check at the beginning
                auth_check = """
    <script>
        // Check authentication
        window.addEventListener('DOMContentLoaded', () => {
            const token = localStorage.getItem('queztl_auth');
            if (!token) {
                window.location.href = 'login.html';
            }
        });
    </script>
"""
                # Insert after <head>
                content = content.replace('<head>', '<head>' + auth_check, 1)
                dest.write_text(content)
                self.log("Added authentication check", "SUCCESS")
                
        except Exception as e:
            self.log(f"Failed to fix 3DMark: {e}", "ERROR")
            self.errors.append(str(e))
    
    def deploy_dashboard(self):
        """Deploy the dashboard to Netlify"""
        self.log("🚀 Step 3: Deploying dashboard to Netlify...")
        
        deploy_dir = self.workspace_root / "3d-showcase-deploy"
        
        if not deploy_dir.exists():
            self.log("Deploy directory not found!", "ERROR")
            return
        
        if self.dry_run:
            self.log("Would run: netlify deploy --prod", "INFO")
            return
        
        try:
            # Check if home.html exists
            home_file = deploy_dir / "home.html"
            if not home_file.exists():
                self.log("home.html not found in deploy directory!", "WARNING")
            
            self.log("Running netlify deploy --prod...", "INFO")
            result = subprocess.run(
                ['netlify', 'deploy', '--prod'],
                cwd=deploy_dir,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                self.log("Deployment successful!", "SUCCESS")
                # Extract URL from output
                for line in result.stdout.split('\n'):
                    if 'https://' in line and 'senasaitech.com' in line:
                        self.log(f"Live at: {line.strip()}", "SUCCESS")
            else:
                self.log(f"Deployment failed: {result.stderr}", "ERROR")
                self.errors.append(result.stderr)
                
        except subprocess.TimeoutExpired:
            self.log("Deployment timed out after 5 minutes", "ERROR")
            self.errors.append("Deployment timeout")
        except FileNotFoundError:
            self.log("netlify CLI not found! Install with: npm install -g netlify-cli", "ERROR")
            self.errors.append("netlify CLI missing")
        except Exception as e:
            self.log(f"Deployment error: {e}", "ERROR")
            self.errors.append(str(e))
    
    def test_deployment(self):
        """Test deployed apps"""
        self.log("🧪 Step 4: Testing deployed applications...")
        
        if self.dry_run:
            self.log("Would test all deployed apps", "INFO")
            return
        
        apps_to_test = [
            ("Login", "https://senasaitech.com/login.html"),
            ("Dashboard", "https://senasaitech.com/home.html"),
            ("3DMark", "https://senasaitech.com/3d-demo.html"),
            ("Email", "https://senasaitech.com/email.html"),
        ]
        
        try:
            import requests
            success_count = 0
            
            for name, url in apps_to_test:
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        self.log(f"✓ {name}: OK ({response.elapsed.total_seconds():.2f}s)", "SUCCESS")
                        success_count += 1
                    else:
                        self.log(f"✗ {name}: HTTP {response.status_code}", "WARNING")
                except Exception as e:
                    self.log(f"✗ {name}: {str(e)[:50]}", "WARNING")
            
            self.log(f"Tests passed: {success_count}/{len(apps_to_test)}", "INFO")
            
        except ImportError:
            self.log("requests library not available, skipping tests", "WARNING")
    
    def create_backup(self):
        """Create git commit backup"""
        self.log("📸 Creating git backup...")
        
        if self.dry_run:
            self.log("Would create git commit", "INFO")
            return
        
        try:
            # Check if there are changes
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.workspace_root,
                capture_output=True,
                text=True
            )
            
            if result.stdout.strip():
                subprocess.run(['git', 'add', '-A'], cwd=self.workspace_root, check=True)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                commit_msg = f"🤖 AUTO-CLEANUP: Workspace cleanup and deployment - {timestamp}"
                
                subprocess.run(
                    ['git', 'commit', '-m', commit_msg],
                    cwd=self.workspace_root,
                    check=True
                )
                
                self.log(f"Backup created: {commit_msg}", "SUCCESS")
            else:
                self.log("No changes to commit", "INFO")
                
        except Exception as e:
            self.log(f"Git backup failed: {e}", "WARNING")
    
    def save_report(self):
        """Save cleanup report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.workspace_root / f"CLEANUP_REPORT_{timestamp}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": self.dry_run,
            "actions_taken": self.actions_taken,
            "errors": self.errors,
            "success": len(self.errors) == 0
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log(f"Report saved: {report_file.name}", "SUCCESS")
        
        # Also save markdown summary
        md_file = self.workspace_root / f"CLEANUP_SUMMARY_{timestamp}.md"
        with open(md_file, 'w') as f:
            f.write(f"# 🤖 Autonomous Cleanup Report\n\n")
            f.write(f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'DRY RUN' if self.dry_run else 'LIVE'}\n\n")
            
            f.write(f"## Actions Taken\n\n")
            for action in self.actions_taken:
                f.write(f"- [{action['time']}] {action['level']}: {action['message']}\n")
            
            if self.errors:
                f.write(f"\n## Errors\n\n")
                for error in self.errors:
                    f.write(f"- {error}\n")
            
            f.write(f"\n**Status:** {'❌ FAILED' if self.errors else '✅ SUCCESS'}\n")
        
        self.log(f"Summary saved: {md_file.name}", "SUCCESS")
    
    def run(self):
        """Run the complete cleanup process"""
        print("=" * 80)
        print("🤖 AUTONOMOUS CLEANUP & DEPLOYMENT RUNNER")
        print("=" * 80)
        print(f"Mode: {'DRY RUN (preview only)' if self.dry_run else 'LIVE'}")
        print(f"Workspace: {self.workspace_root}")
        print("=" * 80)
        print()
        
        try:
            # Load audit data
            audit_report = self.load_audit_report()
            
            if not audit_report:
                self.log("Cannot proceed without audit report", "ERROR")
                return False
            
            # Step 1: Delete duplicates
            self.delete_duplicates(audit_report)
            
            # Step 2: Fix 3DMark
            self.fix_3dmark()
            
            # Step 3: Deploy
            self.deploy_dashboard()
            
            # Step 4: Test
            self.test_deployment()
            
            # Step 5: Backup
            self.create_backup()
            
            # Save report
            self.save_report()
            
            print()
            print("=" * 80)
            if self.errors:
                print(f"⚠️  COMPLETED WITH {len(self.errors)} ERRORS")
            else:
                print("✅ CLEANUP COMPLETE - ALL SYSTEMS GO!")
            print("=" * 80)
            
            return len(self.errors) == 0
            
        except Exception as e:
            self.log(f"Fatal error: {e}", "ERROR")
            self.errors.append(str(e))
            return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Autonomous Cleanup & Deployment Runner')
    parser.add_argument('--dry-run', action='store_true', help='Preview actions without making changes')
    parser.add_argument('--workspace', type=str, default=os.getcwd(), help='Workspace root directory')
    
    args = parser.parse_args()
    
    runner = AutonomousCleanup(args.workspace, dry_run=args.dry_run)
    success = runner.run()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
