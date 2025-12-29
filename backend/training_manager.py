#!/usr/bin/env python3
"""
Queztl Training Manager (QTM)
A unified training orchestration system similar to apt/yum for managing ML model training.

Commands:
  qtm list                    - List all available training modules
  qtm status                  - Show status of all training jobs
  qtm install <module>        - Train/install a specific module
  qtm upgrade <module>        - Retrain/upgrade a module with new data
  qtm upgrade-all             - Retrain all modules
  qtm remove <module>         - Remove a trained model
  qtm info <module>           - Show detailed info about a module
  qtm search <keyword>        - Search for training modules
  qtm check-deps              - Check dependencies for training
  qtm clean                   - Clean old training logs and artifacts
"""

import os
import sys
import json
import time
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Training module registry
TRAINING_MODULES = {
    "image-to-3d": {
        "name": "Image-to-3D Generator",
        "description": "Converts photos to 3D models (competes with Hexa3D)",
        "script": "train_image_to_3d.py",
        "model_path": "/workspace/models/image_to_3d_model.pt",
        "epochs": 150,
        "estimated_time": "60 minutes",
        "dependencies": ["torch", "torchvision", "PIL"],
        "category": "3D Generation",
        "priority": "high",
        "gpu_required": True,
        "memory_gb": 4
    },
    "enhanced-3d": {
        "name": "Enhanced 3D Model",
        "description": "High-quality 3D generation (1024 vertices)",
        "script": "enhanced_training.py",
        "model_path": "/workspace/models/enhanced_3d_model.pt",
        "epochs": 150,
        "estimated_time": "40 minutes",
        "dependencies": ["torch"],
        "category": "3D Generation",
        "priority": "high",
        "gpu_required": True,
        "memory_gb": 3
    },
    "gis-lidar": {
        "name": "GIS LiDAR Classifier",
        "description": "Point cloud classification and building extraction",
        "script": "train_gis_geophysics.py",
        "function": "train_lidar_classifier",
        "model_path": "/workspace/models/lidar_classifier.pt",
        "epochs": 100,
        "estimated_time": "30 minutes",
        "dependencies": ["torch", "numpy", "scipy"],
        "category": "GIS",
        "priority": "high",
        "gpu_required": True,
        "memory_gb": 4
    },
    "gis-buildings": {
        "name": "Building Extractor",
        "description": "Automatic building extraction from LiDAR",
        "script": "train_gis_geophysics.py",
        "function": "train_building_extractor",
        "model_path": "/workspace/models/building_extractor.pt",
        "epochs": 80,
        "estimated_time": "25 minutes",
        "dependencies": ["torch", "numpy"],
        "category": "GIS",
        "priority": "medium",
        "gpu_required": True,
        "memory_gb": 3
    },
    "geophysics-magnetic": {
        "name": "Magnetic Anomaly Interpreter",
        "description": "Magnetic survey interpretation (competes with Geosoft)",
        "script": "train_gis_geophysics.py",
        "function": "train_magnetic_interpreter",
        "model_path": "/workspace/models/magnetic_interpreter.pt",
        "epochs": 150,
        "estimated_time": "35 minutes",
        "dependencies": ["torch", "numpy"],
        "category": "Geophysics",
        "priority": "high",
        "gpu_required": True,
        "memory_gb": 3
    },
    "geophysics-resistivity": {
        "name": "Resistivity Inverter",
        "description": "Fast resistivity inversion (replaces commercial software)",
        "script": "train_gis_geophysics.py",
        "function": "train_resistivity_inverter",
        "model_path": "/workspace/models/resistivity_inverter.pt",
        "epochs": 120,
        "estimated_time": "30 minutes",
        "dependencies": ["torch", "numpy"],
        "category": "Geophysics",
        "priority": "medium",
        "gpu_required": True,
        "memory_gb": 3
    },
    "geophysics-seismic": {
        "name": "Seismic Velocity Analyzer",
        "description": "Seismic velocity analysis and interpretation",
        "script": "train_gis_geophysics.py",
        "function": "train_seismic_analyzer",
        "model_path": "/workspace/models/seismic_analyzer.pt",
        "epochs": 100,
        "estimated_time": "25 minutes",
        "dependencies": ["torch", "numpy"],
        "category": "Geophysics",
        "priority": "low",
        "gpu_required": True,
        "memory_gb": 2
    },
    "text-to-3d": {
        "name": "Text-to-3D Generator",
        "description": "Generate 3D models from text descriptions",
        "script": "train_text_to_3d.py",
        "model_path": "/workspace/models/text_to_3d_model.pt",
        "epochs": 200,
        "estimated_time": "80 minutes",
        "dependencies": ["torch", "transformers"],
        "category": "3D Generation",
        "priority": "medium",
        "gpu_required": True,
        "memory_gb": 6
    }
}

class TrainingManager:
    """Main training orchestration class"""
    
    def __init__(self, workspace: str = "/workspace"):
        self.workspace = Path(workspace)
        self.models_dir = self.workspace / "models"
        self.logs_dir = self.workspace / "training_logs"
        self.status_file = self.workspace / "training_status.json"
        self.logs_dir.mkdir(exist_ok=True)
        
    def load_status(self) -> Dict:
        """Load training status from disk"""
        if self.status_file.exists():
            with open(self.status_file) as f:
                return json.load(f)
        return {}
    
    def save_status(self, status: Dict):
        """Save training status to disk"""
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)
    
    def list_modules(self, category: Optional[str] = None):
        """List all available training modules"""
        print("\n" + "="*80)
        print("QUEZTL TRAINING MODULES")
        print("="*80)
        
        status = self.load_status()
        categories = {}
        
        # Group by category
        for module_id, info in TRAINING_MODULES.items():
            cat = info['category']
            if category and cat.lower() != category.lower():
                continue
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((module_id, info))
        
        # Print by category
        for cat, modules in sorted(categories.items()):
            print(f"\n📦 {cat}")
            print("-" * 80)
            for module_id, info in modules:
                mod_status = status.get(module_id, {})
                installed = "✅" if mod_status.get("installed") else "⬜"
                priority = info['priority'].upper()
                
                print(f"{installed} {module_id:25s} {info['name']}")
                print(f"   └─ {info['description']}")
                print(f"      Priority: {priority} | Est. Time: {info['estimated_time']} | "
                      f"GPU: {'Yes' if info['gpu_required'] else 'No'} | "
                      f"RAM: {info['memory_gb']}GB")
        
        print("\n" + "="*80)
        print(f"Total modules: {len(TRAINING_MODULES)} | Use 'qtm info <module>' for details")
        print("="*80 + "\n")
    
    def show_status(self):
        """Show status of all training jobs"""
        print("\n" + "="*80)
        print("TRAINING STATUS")
        print("="*80)
        
        status = self.load_status()
        
        # Summary stats
        installed = sum(1 for s in status.values() if s.get("installed"))
        training = sum(1 for s in status.values() if s.get("status") == "training")
        failed = sum(1 for s in status.values() if s.get("status") == "failed")
        
        print(f"\n📊 Summary: {installed}/{len(TRAINING_MODULES)} installed | "
              f"{training} training | {failed} failed\n")
        
        # Detailed status
        for module_id, info in sorted(TRAINING_MODULES.items(), 
                                     key=lambda x: x[1]['priority'] != 'high'):
            mod_status = status.get(module_id, {})
            
            if mod_status.get("installed"):
                icon = "✅"
                state = "INSTALLED"
            elif mod_status.get("status") == "training":
                icon = "🔄"
                state = "TRAINING"
            elif mod_status.get("status") == "failed":
                icon = "❌"
                state = "FAILED"
            else:
                icon = "⬜"
                state = "NOT INSTALLED"
            
            print(f"{icon} {module_id:25s} [{state}]")
            
            if mod_status.get("last_trained"):
                print(f"   Last trained: {mod_status['last_trained']}")
            if mod_status.get("accuracy"):
                print(f"   Accuracy: {mod_status['accuracy']:.2%}")
            if mod_status.get("loss"):
                print(f"   Loss: {mod_status['loss']:.6f}")
            if mod_status.get("epoch"):
                print(f"   Epoch: {mod_status['epoch']}/{info['epochs']}")
        
        print("\n" + "="*80 + "\n")
    
    def install_module(self, module_id: str, force: bool = False):
        """Train/install a specific module"""
        if module_id not in TRAINING_MODULES:
            print(f"❌ Error: Module '{module_id}' not found")
            print(f"   Use 'qtm list' to see available modules")
            return False
        
        info = TRAINING_MODULES[module_id]
        status = self.load_status()
        mod_status = status.get(module_id, {})
        
        # Check if already installed
        if mod_status.get("installed") and not force:
            print(f"⚠️  Module '{module_id}' is already installed")
            print(f"   Use 'qtm upgrade {module_id}' to retrain")
            return True
        
        print(f"\n{'='*80}")
        print(f"📦 Installing: {info['name']}")
        print(f"{'='*80}")
        print(f"Description: {info['description']}")
        print(f"Estimated time: {info['estimated_time']}")
        print(f"Epochs: {info['epochs']}")
        print(f"GPU required: {'Yes' if info['gpu_required'] else 'No'}")
        print(f"Memory required: {info['memory_gb']}GB")
        print(f"{'='*80}\n")
        
        # Check dependencies
        print("🔍 Checking dependencies...")
        if not self.check_dependencies(info['dependencies']):
            print("❌ Dependency check failed")
            return False
        
        print("✅ All dependencies satisfied\n")
        
        # Start training
        print(f"🚀 Starting training for {module_id}...")
        log_file = self.logs_dir / f"{module_id}_training.log"
        
        # Update status
        mod_status.update({
            "status": "training",
            "started_at": datetime.now().isoformat(),
            "log_file": str(log_file)
        })
        status[module_id] = mod_status
        self.save_status(status)
        
        # Build training command
        script_path = self.workspace / info['script']
        
        if 'function' in info:
            # Module with specific training function
            cmd = f"cd {self.workspace} && python3 -c 'from {info['script'].replace('.py', '')} import {info['function']}; {info['function']}()'"
        else:
            # Standalone training script
            cmd = f"cd {self.workspace} && python3 {info['script']}"
        
        # Run training
        print(f"📝 Logging to: {log_file}")
        print(f"⏳ Training in progress...\n")
        
        try:
            with open(log_file, 'w') as log:
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
                
                # Stream output
                for line in process.stdout:
                    print(line, end='')
                    log.write(line)
                    log.flush()
                
                process.wait()
                
                if process.returncode == 0:
                    print(f"\n✅ Training completed successfully!")
                    mod_status.update({
                        "status": "completed",
                        "installed": True,
                        "completed_at": datetime.now().isoformat(),
                        "last_trained": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    status[module_id] = mod_status
                    self.save_status(status)
                    return True
                else:
                    raise subprocess.CalledProcessError(process.returncode, cmd)
                    
        except Exception as e:
            print(f"\n❌ Training failed: {e}")
            mod_status.update({
                "status": "failed",
                "error": str(e),
                "failed_at": datetime.now().isoformat()
            })
            status[module_id] = mod_status
            self.save_status(status)
            return False
    
    def upgrade_module(self, module_id: str):
        """Retrain/upgrade a module"""
        return self.install_module(module_id, force=True)
    
    def upgrade_all(self):
        """Retrain all modules"""
        print("\n🔄 Upgrading all training modules...\n")
        
        # Sort by priority
        modules = sorted(TRAINING_MODULES.keys(), 
                        key=lambda x: (TRAINING_MODULES[x]['priority'] != 'high',
                                      TRAINING_MODULES[x]['priority'] != 'medium'))
        
        results = {"success": [], "failed": []}
        
        for module_id in modules:
            if self.install_module(module_id, force=True):
                results["success"].append(module_id)
            else:
                results["failed"].append(module_id)
        
        print(f"\n{'='*80}")
        print("UPGRADE SUMMARY")
        print(f"{'='*80}")
        print(f"✅ Successful: {len(results['success'])}")
        print(f"❌ Failed: {len(results['failed'])}")
        if results['failed']:
            print(f"\nFailed modules: {', '.join(results['failed'])}")
        print(f"{'='*80}\n")
    
    def remove_module(self, module_id: str):
        """Remove a trained model"""
        if module_id not in TRAINING_MODULES:
            print(f"❌ Error: Module '{module_id}' not found")
            return False
        
        info = TRAINING_MODULES[module_id]
        model_path = Path(info['model_path'])
        
        if model_path.exists():
            model_path.unlink()
            print(f"✅ Removed model: {model_path}")
        
        status = self.load_status()
        if module_id in status:
            del status[module_id]
            self.save_status(status)
        
        print(f"✅ Module '{module_id}' removed")
        return True
    
    def show_info(self, module_id: str):
        """Show detailed info about a module"""
        if module_id not in TRAINING_MODULES:
            print(f"❌ Error: Module '{module_id}' not found")
            return
        
        info = TRAINING_MODULES[module_id]
        status = self.load_status()
        mod_status = status.get(module_id, {})
        
        print(f"\n{'='*80}")
        print(f"📦 {info['name']}")
        print(f"{'='*80}")
        print(f"ID: {module_id}")
        print(f"Description: {info['description']}")
        print(f"Category: {info['category']}")
        print(f"Priority: {info['priority'].upper()}")
        print(f"\n📊 Training Parameters:")
        print(f"  - Script: {info['script']}")
        if 'function' in info:
            print(f"  - Function: {info['function']}()")
        print(f"  - Epochs: {info['epochs']}")
        print(f"  - Estimated time: {info['estimated_time']}")
        print(f"  - GPU required: {'Yes' if info['gpu_required'] else 'No'}")
        print(f"  - Memory required: {info['memory_gb']}GB")
        print(f"\n🔧 Dependencies:")
        for dep in info['dependencies']:
            print(f"  - {dep}")
        print(f"\n💾 Model:")
        print(f"  - Path: {info['model_path']}")
        print(f"  - Installed: {'Yes' if mod_status.get('installed') else 'No'}")
        
        if mod_status.get("last_trained"):
            print(f"\n📅 Last Training:")
            print(f"  - Date: {mod_status['last_trained']}")
            if mod_status.get("accuracy"):
                print(f"  - Accuracy: {mod_status['accuracy']:.2%}")
            if mod_status.get("loss"):
                print(f"  - Loss: {mod_status['loss']:.6f}")
        
        print(f"{'='*80}\n")
    
    def search_modules(self, keyword: str):
        """Search for training modules"""
        keyword = keyword.lower()
        results = []
        
        for module_id, info in TRAINING_MODULES.items():
            if (keyword in module_id.lower() or 
                keyword in info['name'].lower() or 
                keyword in info['description'].lower() or
                keyword in info['category'].lower()):
                results.append((module_id, info))
        
        if not results:
            print(f"❌ No modules found matching '{keyword}'")
            return
        
        print(f"\n🔍 Found {len(results)} module(s) matching '{keyword}':\n")
        for module_id, info in results:
            print(f"📦 {module_id} - {info['name']}")
            print(f"   {info['description']}")
            print(f"   Category: {info['category']} | Priority: {info['priority']}\n")
    
    def check_dependencies(self, deps: List[str]) -> bool:
        """Check if dependencies are installed"""
        missing = []
        for dep in deps:
            try:
                __import__(dep)
            except ImportError:
                missing.append(dep)
        
        if missing:
            print(f"❌ Missing dependencies: {', '.join(missing)}")
            print(f"   Install with: pip install {' '.join(missing)}")
            return False
        return True
    
    def check_all_deps(self):
        """Check dependencies for all modules"""
        print("\n🔍 Checking dependencies for all modules...\n")
        
        all_deps = set()
        for info in TRAINING_MODULES.values():
            all_deps.update(info['dependencies'])
        
        missing = []
        installed = []
        
        for dep in sorted(all_deps):
            try:
                __import__(dep)
                installed.append(dep)
                print(f"✅ {dep}")
            except ImportError:
                missing.append(dep)
                print(f"❌ {dep} (NOT INSTALLED)")
        
        print(f"\n{'='*80}")
        print(f"📊 Dependencies: {len(installed)}/{len(all_deps)} installed")
        if missing:
            print(f"\n⚠️  Missing: {', '.join(missing)}")
            print(f"Install with: pip install {' '.join(missing)}")
        else:
            print("\n✅ All dependencies satisfied!")
        print(f"{'='*80}\n")
    
    def clean(self):
        """Clean old training logs and artifacts"""
        print("\n🧹 Cleaning training artifacts...\n")
        
        cleaned = 0
        
        # Clean old logs (keep last 5)
        log_files = sorted(self.logs_dir.glob("*.log"), key=os.path.getmtime, reverse=True)
        for log_file in log_files[5:]:
            print(f"  Removing: {log_file.name}")
            log_file.unlink()
            cleaned += 1
        
        # Clean __pycache__
        for pycache in self.workspace.rglob("__pycache__"):
            print(f"  Removing: {pycache}")
            for file in pycache.iterdir():
                file.unlink()
            pycache.rmdir()
            cleaned += 1
        
        print(f"\n✅ Cleaned {cleaned} item(s)\n")


def main():
    parser = argparse.ArgumentParser(
        description="Queztl Training Manager - Unified ML training orchestration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  qtm list                    List all modules
  qtm list --category=GIS     List GIS modules only
  qtm status                  Show training status
  qtm install image-to-3d     Train image-to-3D model
  qtm upgrade gis-lidar       Retrain LiDAR classifier
  qtm upgrade-all             Retrain all modules
  qtm info geophysics-magnetic  Show module details
  qtm search magnetic         Search for magnetic modules
  qtm check-deps              Check all dependencies
  qtm clean                   Clean old logs
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available modules')
    list_parser.add_argument('--category', help='Filter by category')
    
    # Status command
    subparsers.add_parser('status', help='Show training status')
    
    # Install command
    install_parser = subparsers.add_parser('install', help='Train/install a module')
    install_parser.add_argument('module', help='Module ID to install')
    install_parser.add_argument('--force', action='store_true', help='Force reinstall')
    
    # Upgrade command
    upgrade_parser = subparsers.add_parser('upgrade', help='Retrain/upgrade a module')
    upgrade_parser.add_argument('module', help='Module ID to upgrade')
    
    # Upgrade-all command
    subparsers.add_parser('upgrade-all', help='Retrain all modules')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a trained model')
    remove_parser.add_argument('module', help='Module ID to remove')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show module details')
    info_parser.add_argument('module', help='Module ID')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for modules')
    search_parser.add_argument('keyword', help='Search keyword')
    
    # Check-deps command
    subparsers.add_parser('check-deps', help='Check all dependencies')
    
    # Clean command
    subparsers.add_parser('clean', help='Clean old logs and artifacts')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = TrainingManager()
    
    if args.command == 'list':
        manager.list_modules(args.category if hasattr(args, 'category') else None)
    elif args.command == 'status':
        manager.show_status()
    elif args.command == 'install':
        manager.install_module(args.module, args.force if hasattr(args, 'force') else False)
    elif args.command == 'upgrade':
        manager.upgrade_module(args.module)
    elif args.command == 'upgrade-all':
        manager.upgrade_all()
    elif args.command == 'remove':
        manager.remove_module(args.module)
    elif args.command == 'info':
        manager.show_info(args.module)
    elif args.command == 'search':
        manager.search_modules(args.keyword)
    elif args.command == 'check-deps':
        manager.check_all_deps()
    elif args.command == 'clean':
        manager.clean()


if __name__ == "__main__":
    main()
