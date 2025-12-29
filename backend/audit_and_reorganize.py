#!/usr/bin/env python3
"""
🔍 AUTONOMOUS AUDIT & REORGANIZATION AGENT
=====================================
This agent will:
1. Find all HTML files and identify duplicates
2. Test all deployed apps and buttons (via API checks)
3. Create git snapshot with version control
4. Categorize public vs private apps
5. Generate comprehensive inventory report
6. Prepare hypervisor architecture plan

NO MANUAL INTERVENTION - Just run and go to lunch!

Usage:
    python3 audit_and_reorganize.py
    python3 audit_and_reorganize.py --quick  # Skip tests, just audit
    python3 audit_and_reorganize.py --full   # Full deep audit with tests
"""

import os
import json
import hashlib
import subprocess
import asyncio
import aiohttp
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Tuple
from datetime import datetime
import difflib

@dataclass
class FileInfo:
    """Information about an HTML file"""
    path: str
    size: int
    hash: str
    has_canvas: bool
    has_webgl: bool
    has_auth: bool
    api_endpoints: List[str]
    title: str
    type: str  # 'benchmark', 'demo', 'dashboard', 'landing', 'auth', 'utility'

@dataclass
class DuplicateGroup:
    """Group of duplicate or similar files"""
    similarity: float
    files: List[str]
    recommendation: str

@dataclass
class AppStatus:
    """Status of a deployed app"""
    name: str
    url: str
    accessible: bool
    has_auth: bool
    buttons_working: bool
    errors: List[str]
    response_time_ms: float

@dataclass
class AuditReport:
    """Complete audit report"""
    timestamp: str
    total_files: int
    duplicate_groups: List[DuplicateGroup]
    file_inventory: Dict[str, FileInfo]
    app_statuses: List[AppStatus]
    public_apps: List[str]
    private_apps: List[str]
    broken_files: List[str]
    recommendations: List[str]

class FileAuditor:
    """Audits all HTML files in the workspace"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.files: Dict[str, FileInfo] = {}
        
    def calculate_file_hash(self, filepath: Path) -> str:
        """Calculate MD5 hash of file content"""
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()
        
    def analyze_file(self, filepath: Path) -> FileInfo:
        """Analyze a single HTML file"""
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        
        # Extract title
        title = "Unknown"
        if '<title>' in content:
            start = content.find('<title>') + 7
            end = content.find('</title>', start)
            if end > start:
                title = content[start:end].strip()
        
        # Check for key features
        has_canvas = 'canvas' in content.lower() or 'getcontext' in content.lower()
        has_webgl = 'webgl' in content.lower()
        has_auth = 'queztl_auth' in content or 'login.html' in content or 'localStorage.getItem' in content
        
        # Extract API endpoints
        api_endpoints = []
        for line in content.split('\n'):
            if '/api/' in line:
                # Extract endpoint
                start = line.find('/api/')
                if start != -1:
                    end = line.find("'", start)
                    if end == -1:
                        end = line.find('"', start)
                    if end > start:
                        endpoint = line[start:end]
                        if endpoint not in api_endpoints:
                            api_endpoints.append(endpoint)
        
        # Determine file type
        file_type = 'utility'
        name_lower = filepath.name.lower()
        if 'login' in name_lower or 'auth' in name_lower:
            file_type = 'auth'
        elif '3dmark' in name_lower or 'benchmark' in name_lower:
            file_type = 'benchmark'
        elif 'demo' in name_lower or '3d' in name_lower:
            file_type = 'demo'
        elif 'dashboard' in name_lower or 'home' in name_lower:
            file_type = 'dashboard'
        elif 'index' in name_lower or 'landing' in name_lower:
            file_type = 'landing'
        elif 'email' in name_lower or 'secret' in name_lower:
            file_type = 'utility'
            
        return FileInfo(
            path=str(filepath.relative_to(self.workspace_root)),
            size=filepath.stat().st_size,
            hash=self.calculate_file_hash(filepath),
            has_canvas=has_canvas,
            has_webgl=has_webgl,
            has_auth=has_auth,
            api_endpoints=api_endpoints,
            title=title,
            type=file_type
        )
        
    def scan_workspace(self):
        """Scan workspace for all HTML files"""
        print("🔍 Scanning workspace for HTML files...")
        
        html_files = list(self.workspace_root.rglob('*.html'))
        print(f"   Found {len(html_files)} HTML files")
        
        for filepath in html_files:
            try:
                file_info = self.analyze_file(filepath)
                self.files[file_info.path] = file_info
            except Exception as e:
                print(f"   ⚠️  Error analyzing {filepath}: {e}")
                
        print(f"✅ Analyzed {len(self.files)} files\n")
        
    def find_duplicates(self) -> List[DuplicateGroup]:
        """Find duplicate and similar files"""
        print("🔎 Finding duplicates and similar files...")
        
        duplicate_groups = []
        processed_hashes: Set[str] = set()
        
        # Group by hash (exact duplicates)
        hash_groups: Dict[str, List[str]] = {}
        for path, info in self.files.items():
            if info.hash not in hash_groups:
                hash_groups[info.hash] = []
            hash_groups[info.hash].append(path)
        
        # Report exact duplicates
        for file_hash, paths in hash_groups.items():
            if len(paths) > 1:
                # Determine which to keep
                deployed = [p for p in paths if '3d-showcase-deploy' in p]
                source = [p for p in paths if 'dashboard/public' in p]
                
                recommendation = "KEEP: "
                if deployed:
                    recommendation += f"{deployed[0]} (deployed), DELETE: " + ", ".join([p for p in paths if p != deployed[0]])
                elif source:
                    recommendation += f"{source[0]} (source), DELETE: " + ", ".join([p for p in paths if p != source[0]])
                else:
                    recommendation += f"{paths[0]}, DELETE: " + ", ".join(paths[1:])
                
                duplicate_groups.append(DuplicateGroup(
                    similarity=1.0,
                    files=paths,
                    recommendation=recommendation
                ))
                processed_hashes.add(file_hash)
        
        print(f"   Found {len(duplicate_groups)} exact duplicate groups")
        
        # Find similar files (>80% similar)
        print("   Checking for similar files (>80% similarity)...")
        file_list = list(self.files.items())
        
        for i in range(len(file_list)):
            for j in range(i + 1, len(file_list)):
                path1, info1 = file_list[i]
                path2, info2 = file_list[j]
                
                # Skip if already in exact duplicate group
                if info1.hash in processed_hashes or info2.hash in processed_hashes:
                    continue
                
                # Only compare files of same type
                if info1.type != info2.type:
                    continue
                
                # Read content and compare
                try:
                    content1 = Path(self.workspace_root / path1).read_text()
                    content2 = Path(self.workspace_root / path2).read_text()
                    
                    similarity = difflib.SequenceMatcher(None, content1, content2).ratio()
                    
                    if similarity > 0.80:
                        recommendation = f"REVIEW: {similarity*100:.0f}% similar - Check if one can be deleted"
                        duplicate_groups.append(DuplicateGroup(
                            similarity=similarity,
                            files=[path1, path2],
                            recommendation=recommendation
                        ))
                except:
                    pass
        
        print(f"✅ Found {len(duplicate_groups)} total duplicate/similar groups\n")
        return duplicate_groups

class AppTester:
    """Tests deployed applications"""
    
    def __init__(self, base_url: str = "https://senasaitech.com"):
        self.base_url = base_url
        self.backend_url = "https://hive-backend.onrender.com"
        
    async def test_app(self, name: str, path: str, has_auth: bool) -> AppStatus:
        """Test a single app"""
        url = f"{self.base_url}/{path}"
        errors = []
        accessible = False
        buttons_working = False
        response_time_ms = 0
        
        try:
            start = asyncio.get_event_loop().time()
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    response_time_ms = (asyncio.get_event_loop().time() - start) * 1000
                    
                    if response.status == 200:
                        accessible = True
                        content = await response.text()
                        
                        # Check for broken links
                        if 'localhost' in content and 'senasaitech.com' not in content:
                            errors.append("Contains localhost references")
                        
                        # Basic button functionality check
                        if 'onclick=' in content or 'addEventListener' in content:
                            buttons_working = True
                    else:
                        errors.append(f"HTTP {response.status}")
        except asyncio.TimeoutError:
            errors.append("Timeout")
        except Exception as e:
            errors.append(str(e))
            
        return AppStatus(
            name=name,
            url=url,
            accessible=accessible,
            has_auth=has_auth,
            buttons_working=buttons_working,
            errors=errors,
            response_time_ms=response_time_ms
        )
        
    async def test_backend(self) -> AppStatus:
        """Test backend API health"""
        return await self.test_app("Backend API", "api/health", False)
        
    async def test_all_apps(self) -> List[AppStatus]:
        """Test all deployed applications"""
        print("🧪 Testing deployed applications...")
        
        apps_to_test = [
            ("Login", "login.html", False),
            ("Home Portal", "home.html", True),
            ("3DMark Demo", "3d-demo.html", True),
            ("Benchmark", "benchmark.html", True),
            ("Email System", "email.html", True),
            ("Secrets Vault", "secrets.html", True),
            ("Demos Hub", "demos.html", True),
        ]
        
        tasks = [self.test_app(name, path, auth) for name, path, auth in apps_to_test]
        results = await asyncio.gather(*tasks)
        
        # Test backend separately
        backend_result = await self.test_backend()
        results.append(backend_result)
        
        # Print results
        for status in results:
            icon = "✅" if status.accessible else "❌"
            print(f"   {icon} {status.name}: {status.response_time_ms:.0f}ms")
            if status.errors:
                for error in status.errors:
                    print(f"      ⚠️  {error}")
        
        print()
        return results

class VersionController:
    """Handles git snapshots and version control"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        
    def create_snapshot(self) -> Tuple[bool, str]:
        """Create git snapshot"""
        print("📸 Creating git snapshot...")
        
        try:
            # Check if there are changes
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.workspace_root,
                capture_output=True,
                text=True
            )
            
            if not result.stdout.strip():
                print("   ℹ️  No changes to commit")
                return True, "No changes"
            
            # Add all files
            subprocess.run(['git', 'add', '-A'], cwd=self.workspace_root, check=True)
            
            # Commit
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            commit_msg = f"🤖 AUTO-SNAPSHOT: Pre-hypervisor audit - {timestamp}"
            
            result = subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                cwd=self.workspace_root,
                capture_output=True,
                text=True
            )
            
            print(f"✅ Snapshot created: {commit_msg}\n")
            return True, commit_msg
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git error: {e}\n")
            return False, str(e)

class HypervisorPlanner:
    """Plans hypervisor architecture"""
    
    def __init__(self, file_inventory: Dict[str, FileInfo]):
        self.file_inventory = file_inventory
        
    def categorize_apps(self) -> Tuple[List[str], List[str]]:
        """Categorize apps as public or private"""
        public_apps = []
        private_apps = []
        
        for path, info in self.file_inventory.items():
            # Public: landing pages, demos without auth requirement
            if info.type in ['landing', 'auth'] or not info.has_auth:
                if '3d-showcase-deploy' in path or 'index.html' in path:
                    public_apps.append(path)
            else:
                # Private: requires authentication
                if '3d-showcase-deploy' in path:
                    private_apps.append(path)
                    
        return public_apps, private_apps
        
    def generate_plan(self) -> Dict[str, any]:
        """Generate hypervisor architecture plan"""
        public, private = self.categorize_apps()
        
        plan = {
            "architecture": "Hypervisor-based Application Router",
            "components": {
                "public_zone": {
                    "description": "No authentication required",
                    "apps": public,
                    "route_pattern": "/public/*"
                },
                "private_zone": {
                    "description": "Requires authentication token",
                    "apps": private,
                    "route_pattern": "/app/*",
                    "auth_check": "localStorage.getItem('queztl_auth')"
                },
                "hypervisor": {
                    "description": "Central routing and permission manager",
                    "features": [
                        "Request routing based on auth status",
                        "Resource allocation and monitoring",
                        "Session management",
                        "API gateway with rate limiting",
                        "Real-time metrics dashboard"
                    ]
                }
            },
            "file_structure": {
                "/hypervisor/": "Core routing logic",
                "/hypervisor/public/": "Public accessible demos",
                "/hypervisor/private/": "Auth-required applications",
                "/hypervisor/dashboard/": "Admin dashboard",
                "/hypervisor/api/": "API gateway"
            },
            "next_steps": [
                "1. Create hypervisor directory structure",
                "2. Implement auth middleware",
                "3. Build routing engine",
                "4. Migrate apps to hypervisor structure",
                "5. Deploy unified dashboard",
                "6. Test all routes and permissions"
            ]
        }
        
        return plan

class AuditOrchestrator:
    """Main orchestrator for audit and reorganization"""
    
    def __init__(self, workspace_root: str, skip_tests: bool = False):
        self.workspace_root = workspace_root
        self.skip_tests = skip_tests
        self.auditor = FileAuditor(workspace_root)
        self.tester = AppTester()
        self.version_controller = VersionController(workspace_root)
        
    async def run_full_audit(self) -> AuditReport:
        """Run complete audit process"""
        print("=" * 80)
        print("🤖 AUTONOMOUS AUDIT & REORGANIZATION AGENT")
        print("=" * 80)
        print(f"Workspace: {self.workspace_root}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80 + "\n")
        
        # 1. Scan files
        self.auditor.scan_workspace()
        
        # 2. Find duplicates
        duplicates = self.auditor.find_duplicates()
        
        # 3. Test apps (if not skipped)
        app_statuses = []
        if not self.skip_tests:
            app_statuses = await self.tester.test_all_apps()
        else:
            print("⏭️  Skipping app tests (--quick mode)\n")
        
        # 4. Create git snapshot
        snapshot_success, snapshot_msg = self.version_controller.create_snapshot()
        
        # 5. Plan hypervisor
        planner = HypervisorPlanner(self.auditor.files)
        public_apps, private_apps = planner.categorize_apps()
        hypervisor_plan = planner.generate_plan()
        
        # 6. Generate recommendations
        recommendations = self.generate_recommendations(
            duplicates, app_statuses, public_apps, private_apps
        )
        
        # 7. Identify broken files
        broken_files = []
        for status in app_statuses:
            if not status.accessible or status.errors:
                broken_files.append(f"{status.name}: {', '.join(status.errors)}")
        
        # Create report
        report = AuditReport(
            timestamp=datetime.now().isoformat(),
            total_files=len(self.auditor.files),
            duplicate_groups=duplicates,
            file_inventory=self.auditor.files,
            app_statuses=app_statuses,
            public_apps=public_apps,
            private_apps=private_apps,
            broken_files=broken_files,
            recommendations=recommendations
        )
        
        # Save reports
        self.save_reports(report, hypervisor_plan)
        
        # Print summary
        self.print_summary(report)
        
        return report
        
    def generate_recommendations(self, duplicates, app_statuses, public_apps, private_apps) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Duplicate recommendations
        exact_dupes = len([d for d in duplicates if d.similarity == 1.0])
        if exact_dupes > 0:
            recommendations.append(f"🗑️  DELETE {exact_dupes} exact duplicate files to clean up workspace")
        
        # App status recommendations
        broken_apps = len([s for s in app_statuses if not s.accessible])
        if broken_apps > 0:
            recommendations.append(f"🔧 FIX {broken_apps} broken/inaccessible apps")
        
        # 3DMark specific
        has_3dmark_text = any('3d-demo.html' in f for f in self.auditor.files.keys() 
                              if not self.auditor.files[f].has_canvas)
        has_3dmark_graphics = any('3dmark-pro.html' in f for f in self.auditor.files.keys())
        
        if has_3dmark_text and has_3dmark_graphics:
            recommendations.append("🎮 REPLACE 3d-demo.html with 3dmark-pro.html (graphics version)")
        
        # Auth recommendations
        public_needs_auth = []
        for path, info in self.auditor.files.items():
            if '3d-showcase-deploy' in path and info.type not in ['landing', 'auth'] and not info.has_auth:
                public_needs_auth.append(path)
        
        if public_needs_auth:
            recommendations.append(f"🔐 ADD authentication to {len(public_needs_auth)} public files")
        
        # Hypervisor recommendation
        recommendations.append("🏗️  IMPLEMENT hypervisor structure for better app organization")
        recommendations.append("📊 CREATE unified dashboard as main entry point")
        recommendations.append("🧹 ARCHIVE or DELETE non-deployed files in dashboard/public")
        
        return recommendations
        
    def save_reports(self, report: AuditReport, hypervisor_plan: Dict):
        """Save audit reports to files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save full audit report
        audit_file = Path(self.workspace_root) / f"AUDIT_REPORT_{timestamp}.json"
        with open(audit_file, 'w') as f:
            # Convert dataclasses to dicts
            report_dict = asdict(report)
            json.dump(report_dict, f, indent=2)
        print(f"💾 Audit report: {audit_file.name}")
        
        # Save hypervisor plan
        plan_file = Path(self.workspace_root) / f"HYPERVISOR_PLAN_{timestamp}.json"
        with open(plan_file, 'w') as f:
            json.dump(hypervisor_plan, f, indent=2)
        print(f"💾 Hypervisor plan: {plan_file.name}")
        
        # Save working versions inventory
        inventory_file = Path(self.workspace_root) / "WORKING_VERSIONS.md"
        with open(inventory_file, 'w') as f:
            f.write("# 🎯 Working Versions Inventory\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 📦 Deployed Apps (Production)\n\n")
            deployed = {k: v for k, v in report.file_inventory.items() if '3d-showcase-deploy' in k}
            for path, info in sorted(deployed.items()):
                icon = "✅" if path in report.public_apps + report.private_apps else "⚠️"
                auth = "🔐 Private" if info.has_auth else "🌐 Public"
                graphics = "🎮 Graphics" if info.has_canvas else "📝 Text"
                f.write(f"- {icon} **{path}**\n")
                f.write(f"  - {auth} | {graphics} | {info.type}\n")
                f.write(f"  - Title: {info.title}\n")
                f.write(f"  - Size: {info.size:,} bytes\n\n")
            
            f.write("## 🔨 Source Files (dashboard/public)\n\n")
            source = {k: v for k, v in report.file_inventory.items() if 'dashboard/public' in k}
            for path, info in sorted(source.items()):
                graphics = "🎮 Graphics" if info.has_canvas else "📝 Text"
                f.write(f"- **{path}**\n")
                f.write(f"  - {graphics} | {info.type}\n")
                f.write(f"  - Title: {info.title}\n\n")
            
            f.write("## 🗑️  Duplicates to Remove\n\n")
            for dup in report.duplicate_groups:
                if dup.similarity == 1.0:
                    f.write(f"- {dup.recommendation}\n")
            
        print(f"💾 Inventory: {inventory_file.name}\n")
        
    def print_summary(self, report: AuditReport):
        """Print executive summary"""
        print("\n" + "=" * 80)
        print("📊 AUDIT SUMMARY")
        print("=" * 80)
        
        print(f"\n📁 Files:")
        print(f"   Total HTML files: {report.total_files}")
        print(f"   Deployed apps: {len(report.public_apps) + len(report.private_apps)}")
        print(f"   🌐 Public: {len(report.public_apps)}")
        print(f"   🔐 Private: {len(report.private_apps)}")
        
        print(f"\n🔍 Duplicates:")
        exact = len([d for d in report.duplicate_groups if d.similarity == 1.0])
        similar = len([d for d in report.duplicate_groups if d.similarity < 1.0])
        print(f"   Exact duplicates: {exact}")
        print(f"   Similar files (>80%): {similar}")
        
        if report.app_statuses:
            print(f"\n🧪 App Testing:")
            accessible = len([s for s in report.app_statuses if s.accessible])
            print(f"   Accessible: {accessible}/{len(report.app_statuses)}")
            print(f"   Broken: {len(report.broken_files)}")
        
        print(f"\n💡 Recommendations:")
        for i, rec in enumerate(report.recommendations, 1):
            print(f"   {i}. {rec}")
        
        print("\n" + "=" * 80)
        print("✅ AUDIT COMPLETE - Reports saved to workspace")
        print("=" * 80 + "\n")

async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Autonomous Audit & Reorganization Agent')
    parser.add_argument('--quick', action='store_true', help='Quick audit without app testing')
    parser.add_argument('--full', action='store_true', help='Full deep audit with all tests')
    parser.add_argument('--workspace', type=str, default=os.getcwd(), help='Workspace root directory')
    
    args = parser.parse_args()
    
    skip_tests = args.quick
    
    orchestrator = AuditOrchestrator(args.workspace, skip_tests=skip_tests)
    report = await orchestrator.run_full_audit()
    
    # Exit code based on findings
    if report.broken_files:
        print(f"⚠️  Found {len(report.broken_files)} issues - review recommended")
        return 1
    else:
        print("✅ No critical issues found")
        return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
