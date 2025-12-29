#!/usr/bin/env python3

"""
QuetzalCore BETA 1 - Production Health Checker
Validates that all systems are ready for production
"""

import subprocess
import json
import sys
import time
from datetime import datetime
import os
from pathlib import Path

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

class HealthChecker:
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.checks_warning = 0
        self.results = []
        
    def log_pass(self, check, message=""):
        self.checks_passed += 1
        msg = f"✅ {check}"
        if message:
            msg += f" - {message}"
        print(f"{GREEN}{msg}{RESET}")
        self.results.append({"check": check, "status": "pass", "message": message})
        
    def log_fail(self, check, message=""):
        self.checks_failed += 1
        msg = f"❌ {check}"
        if message:
            msg += f" - {message}"
        print(f"{RED}{msg}{RESET}")
        self.results.append({"check": check, "status": "fail", "message": message})
        
    def log_warn(self, check, message=""):
        self.checks_warning += 1
        msg = f"⚠️  {check}"
        if message:
            msg += f" - {message}"
        print(f"{YELLOW}{msg}{RESET}")
        self.results.append({"check": check, "status": "warning", "message": message})
        
    def run_command(self, cmd, description=""):
        """Run a command and return True if successful"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    # =========================================================================
    # System Checks
    # =========================================================================
    
    def check_project_structure(self):
        """Check that all required files exist"""
        print(f"\n{BOLD}{BLUE}📁 PROJECT STRUCTURE{RESET}")
        
        required_files = [
            "backend/main.py",
            "backend/models.py",
            "backend/database.py",
            "backend/requirements.txt",
            "dashboard/package.json",
            "docker-compose.yml",
            ".env",
            "BETA_1_PRODUCTION_READY.md",
        ]
        
        for file in required_files:
            if Path(file).exists():
                self.log_pass(f"File exists: {file}")
            else:
                self.log_fail(f"File missing: {file}")
    
    def check_dependencies(self):
        """Check that required tools are installed"""
        print(f"\n{BOLD}{BLUE}🔧 DEPENDENCIES{RESET}")
        
        tools = [
            ("docker", "Docker"),
            ("python3", "Python 3"),
            ("node", "Node.js"),
            ("npm", "npm"),
            ("git", "Git"),
        ]
        
        for cmd, name in tools:
            success, stdout, stderr = self.run_command(f"which {cmd}")
            if success:
                version_cmd = f"{cmd} --version"
                version_success, version, _ = self.run_command(version_cmd)
                if version_success:
                    self.log_pass(f"{name} installed", version.split('\n')[0][:50])
                else:
                    self.log_pass(f"{name} installed")
            else:
                self.log_fail(f"{name} not found")
    
    def check_python_environment(self):
        """Check Python environment"""
        print(f"\n{BOLD}{BLUE}🐍 PYTHON ENVIRONMENT{RESET}")
        
        # Check Python version
        success, stdout, _ = self.run_command("python3 --version")
        if success:
            self.log_pass("Python version", stdout)
        else:
            self.log_fail("Python version check")
            return
        
        # Check virtual environment
        if Path(".venv").exists() or "VIRTUAL_ENV" in os.environ:
            self.log_pass("Virtual environment", "Found")
        else:
            self.log_warn("Virtual environment", "Not detected (optional)")
        
        # Check pip packages
        packages = [
            "fastapi",
            "uvicorn",
            "sqlalchemy",
            "psutil",
            "torch",
            "numpy",
        ]
        
        for pkg in packages:
            success, _, _ = self.run_command(f"python3 -c 'import {pkg.split('-')[0].replace('-', '_')}'")
            if success:
                self.log_pass(f"Package installed: {pkg}")
            else:
                self.log_warn(f"Package missing: {pkg} (may not be critical)")
    
    def check_docker_setup(self):
        """Check Docker configuration"""
        print(f"\n{BOLD}{BLUE}🐳 DOCKER SETUP{RESET}")
        
        # Check Docker daemon
        success, _, _ = self.run_command("docker ps")
        if success:
            self.log_pass("Docker daemon running")
        else:
            self.log_fail("Docker daemon not accessible")
            return
        
        # Check docker-compose version
        success, version, _ = self.run_command("docker-compose --version")
        if success:
            self.log_pass("Docker Compose", version)
        else:
            self.log_fail("Docker Compose not found")
        
        # Check if containers are running
        success, containers, _ = self.run_command("docker-compose ps --services 2>/dev/null || echo ''")
        if success and containers:
            num_services = len(containers.strip().split('\n'))
            self.log_pass(f"Services defined", f"{num_services} services")
        else:
            self.log_warn("Docker Compose services", "Not yet started")
    
    # =========================================================================
    # API Checks
    # =========================================================================
    
    def check_api_health(self):
        """Check if API is running and healthy"""
        print(f"\n{BOLD}{BLUE}🔌 API HEALTH{RESET}")
        
        endpoints = [
            ("http://localhost:8000/api/health", "Health endpoint"),
            ("http://localhost:8000/docs", "API documentation"),
            ("http://localhost:8000/api/mining", "Mining API"),
        ]
        
        for url, description in endpoints:
            success, _, _ = self.run_command(f"curl -s {url} > /dev/null 2>&1")
            if success:
                self.log_pass(description, f"{url}")
            else:
                self.log_warn(description, f"Not responding (services may not be started)")
    
    def check_database(self):
        """Check database configuration"""
        print(f"\n{BOLD}{BLUE}🗄️  DATABASE{RESET}")
        
        # Check DATABASE_URL in .env
        success, _, _ = self.run_command("grep -q DATABASE_URL .env")
        if success:
            self.log_pass("DATABASE_URL configured in .env")
        else:
            self.log_fail("DATABASE_URL not found in .env")
        
        # Check REDIS_URL
        success, _, _ = self.run_command("grep -q REDIS_URL .env")
        if success:
            self.log_pass("REDIS_URL configured in .env")
        else:
            self.log_warn("REDIS_URL not configured (optional)")
    
    # =========================================================================
    # Security Checks
    # =========================================================================
    
    def check_security(self):
        """Check security configurations"""
        print(f"\n{BOLD}{BLUE}🔒 SECURITY{RESET}")
        
        # Check .env in gitignore
        success, _, _ = self.run_command("grep -q '\\.env' .gitignore")
        if success:
            self.log_pass(".env in gitignore")
        else:
            self.log_warn(".env may be tracked by git")
        
        # Check for hardcoded secrets
        success, output, _ = self.run_command(
            "grep -r 'password.*=' backend/ 2>/dev/null | grep -v test | grep -v '#' | wc -l"
        )
        if success and output.strip() == "0":
            self.log_pass("No obvious hardcoded secrets found")
        else:
            self.log_warn(f"Potential hardcoded secrets found ({output.strip()} lines)")
        
        # Check SSL/TLS setup
        if Path("ssl_certs").exists():
            self.log_pass("SSL certificates directory exists")
        else:
            self.log_warn("SSL certificates not yet configured (production requirement)")
    
    # =========================================================================
    # Code Quality Checks
    # =========================================================================
    
    def check_code_quality(self):
        """Check code quality"""
        print(f"\n{BOLD}{BLUE}📝 CODE QUALITY{RESET}")
        
        # Check Python syntax
        success, _, _ = self.run_command("python3 -m py_compile backend/main.py")
        if success:
            self.log_pass("Python syntax valid (main.py)")
        else:
            self.log_fail("Python syntax error in main.py")
        
        # Check for test files
        if Path("tests").exists():
            success, output, _ = self.run_command("find tests -name 'test_*.py' | wc -l")
            if success and int(output.strip()) > 0:
                self.log_pass(f"Test files found", f"{output.strip()} test files")
            else:
                self.log_warn("No test files found")
        else:
            self.log_warn("Tests directory not found")
    
    # =========================================================================
    # Deployment Checks
    # =========================================================================
    
    def check_deployment_readiness(self):
        """Check deployment readiness"""
        print(f"\n{BOLD}{BLUE}🚀 DEPLOYMENT READINESS{RESET}")
        
        deployment_files = [
            ("deploy-beta-1-production.sh", "Production deployment script"),
            ("quick-launch-beta-1.sh", "Quick launch script"),
            ("docker-compose.yml", "Docker Compose configuration"),
            ("Procfile", "Process file for cloud deployment"),
        ]
        
        for file, description in deployment_files:
            if Path(file).exists():
                self.log_pass(f"{description}: {file}")
            else:
                self.log_warn(f"{description}: Missing ({file})")
    
    def check_documentation(self):
        """Check documentation"""
        print(f"\n{BOLD}{BLUE}📚 DOCUMENTATION{RESET}")
        
        docs = [
            ("BETA_1_PRODUCTION_READY.md", "Production checklist"),
            ("FINAL_SUMMARY.md", "Project summary"),
            ("PROJECT_SUMMARY.md", "Architecture documentation"),
            ("API_CONNECTION_GUIDE.md", "API connection guide"),
            ("DEPLOYMENT.md", "Deployment guide"),
        ]
        
        found_docs = 0
        for file, description in docs:
            if Path(file).exists():
                self.log_pass(f"{description}: {file}")
                found_docs += 1
            else:
                self.log_warn(f"{description}: Missing ({file})")
        
        if found_docs >= 3:
            self.log_pass(f"Documentation coverage: {found_docs}/{len(docs)} files")
    
    # =========================================================================
    # Summary
    # =========================================================================
    
    def print_summary(self):
        """Print health check summary"""
        total = self.checks_passed + self.checks_failed + self.checks_warning
        
        print(f"\n{BOLD}{BLUE}{'=' * 60}{RESET}")
        print(f"{BOLD}{BLUE}HEALTH CHECK SUMMARY{RESET}")
        print(f"{BOLD}{BLUE}{'=' * 60}{RESET}")
        print()
        print(f"  {GREEN}✅ Passed:  {self.checks_passed}{RESET}")
        print(f"  {YELLOW}⚠️  Warnings: {self.checks_warning}{RESET}")
        print(f"  {RED}❌ Failed:  {self.checks_failed}{RESET}")
        print(f"  {BLUE}━━━━━━━━━━━━━━━━{RESET}")
        print(f"  {BLUE}Total: {total}{RESET}")
        print()
        
        # Recommendation
        if self.checks_failed == 0:
            if self.checks_warning == 0:
                print(f"{GREEN}{BOLD}🎉 PRODUCTION READY!{RESET}")
                print(f"{GREEN}All checks passed. Your system is ready for production deployment.{RESET}")
            else:
                print(f"{YELLOW}{BOLD}✅ READY (with warnings){RESET}")
                print(f"{YELLOW}Address warnings above before production deployment.{RESET}")
            return 0
        else:
            print(f"{RED}{BOLD}⚠️  NOT READY{RESET}")
            print(f"{RED}Fix the failures above before deploying to production.{RESET}")
            return 1
    
    def run_all_checks(self):
        """Run all health checks"""
        print(f"{BOLD}{BLUE}")
        print("╔════════════════════════════════════════════════════════╗")
        print("║  QuetzalCore BETA 1 - Production Health Checker       ║")
        print(f"║  {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<50} ║")
        print("╚════════════════════════════════════════════════════════╝")
        print(f"{RESET}\n")
        
        self.check_project_structure()
        self.check_dependencies()
        self.check_python_environment()
        self.check_docker_setup()
        self.check_api_health()
        self.check_database()
        self.check_security()
        self.check_code_quality()
        self.check_deployment_readiness()
        self.check_documentation()
        
        return self.print_summary()

if __name__ == "__main__":
    checker = HealthChecker()
    exit_code = checker.run_all_checks()
    sys.exit(exit_code)
