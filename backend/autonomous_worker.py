#!/usr/bin/env python3
"""
Autonomous Work Session Manager
Runs background tasks, checks in periodically
"""

import time
import subprocess
import requests
from datetime import datetime, timedelta

class AutonomousWorker:
    """Manages autonomous work session"""
    
    def __init__(self, duration_hours: int = 4, checkin_minutes: int = 15):
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(hours=duration_hours)
        self.checkin_interval = timedelta(minutes=checkin_minutes)
        self.next_checkin = self.start_time + self.checkin_interval
        self.tasks_completed = []
        
    def log(self, message: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def check_beast_status(self) -> dict:
        """Check Beast server status"""
        try:
            response = requests.get("http://192.168.1.105:8001/", timeout=5)
            return {"online": True, "data": response.json()}
        except:
            return {"online": False}
    
    def check_job_status(self, job_id: str) -> dict:
        """Check image generation job"""
        try:
            response = requests.get(f"http://192.168.1.105:8001/status/{job_id}", timeout=5)
            return response.json()
        except:
            return {"status": "unknown"}
    
    def generate_image(self, prompt: str, style: str = "propaganda") -> str:
        """Queue image generation"""
        try:
            response = requests.post(
                "http://192.168.1.105:8001/generate",
                json={
                    "prompt": prompt,
                    "style": style,
                    "width": 1024,
                    "height": 1024,
                    "steps": 30,
                    "guidance_scale": 7.5
                },
                timeout=10
            )
            data = response.json()
            return data.get("job_id")
        except Exception as e:
            self.log(f"❌ Image generation failed: {e}")
            return None
    
    def run_training(self, script: str):
        """Run training script"""
        self.log(f"🧠 Starting training: {script}")
        try:
            result = subprocess.run(
                ["python3", script],
                capture_output=True,
                text=True,
                timeout=600
            )
            if result.returncode == 0:
                self.log(f"✅ Training complete: {script}")
                self.tasks_completed.append(script)
            else:
                self.log(f"⚠️  Training had issues: {script}")
        except subprocess.TimeoutExpired:
            self.log(f"⏱️  Training timeout: {script}")
        except Exception as e:
            self.log(f"❌ Training error: {e}")
    
    def checkin(self):
        """Periodic status check-in"""
        elapsed = datetime.now() - self.start_time
        remaining = self.end_time - datetime.now()
        
        print("\n" + "=" * 60)
        print(f"⏰ CHECK-IN - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        print(f"⏱️  Elapsed: {elapsed}")
        print(f"⏳ Remaining: {remaining}")
        print(f"✅ Tasks completed: {len(self.tasks_completed)}")
        
        # Beast status
        beast_status = self.check_beast_status()
        if beast_status["online"]:
            print(f"⚡ Beast: ONLINE")
        else:
            print(f"💤 Beast: OFFLINE")
        
        print("=" * 60 + "\n")
        
        self.next_checkin = datetime.now() + self.checkin_interval
    
    def should_continue(self) -> bool:
        """Check if session should continue"""
        return datetime.now() < self.end_time
    
    def run(self):
        """Main work loop"""
        self.log("🤖 Autonomous session started")
        self.log(f"⏰ Will run until {self.end_time.strftime('%H:%M:%S')}")
        
        # Queue of tasks
        tasks = [
            ("theory", "backend/communist_theory_library.py"),
            ("image1", "Marx revolutionary"),
            ("image2", "Workers united breaking chains"),
            ("image3", "Red star over factory"),
        ]
        
        for task_type, task_data in tasks:
            if not self.should_continue():
                break
            
            # Check-in time?
            if datetime.now() >= self.next_checkin:
                self.checkin()
            
            # Execute task
            if task_type == "theory":
                self.run_training(task_data)
            elif task_type.startswith("image"):
                job_id = self.generate_image(task_data, "propaganda")
                if job_id:
                    self.log(f"🎨 Image queued: {job_id[:8]}...")
                    self.tasks_completed.append(f"image:{task_data}")
            
            # Brief pause
            time.sleep(10)
        
        # Final check-in
        self.checkin()
        self.log("✅ Autonomous session complete")

if __name__ == "__main__":
    worker = AutonomousWorker(duration_hours=4, checkin_minutes=15)
    worker.run()
