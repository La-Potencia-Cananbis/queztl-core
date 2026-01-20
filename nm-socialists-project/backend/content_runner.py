#!/usr/bin/env python3
"""
Dynamic Content Runner - Generates memes, posts to Facebook, manages content
Uses: Beast for image generation, Sloth for storage, Mac for serving
"""

import os
import asyncio
import aiohttp
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import random

# Cluster configuration
BEAST_URL = "http://192.168.1.105:8001"
SLOTH_STORAGE = "http://192.168.1.102:8000"  # Adjust port as needed
LOCAL_CACHE = Path.home() / "queztl-core" / "frontend" / "generated"

# Database on Sloth
SLOTH_DB_PATH = "/mnt/sloth/queztl/members.db"  # Will be mounted via NFS/SMB

# Meme templates and prompts
MEME_TEMPLATES = [
    {
        "theme": "revolutionary",
        "prompts": [
            "Workers unite under red banner, fists raised, socialist realism style",
            "Revolutionary figure addressing crowd, dramatic lighting, propaganda art",
            "Industrial workers building future, constructivist style, bold colors",
            "Unity and strength, diverse workers together, heroic composition"
        ]
    },
    {
        "theme": "tech",
        "prompts": [
            "Futuristic AI brain with circuit patterns, cyberpunk style",
            "Digital revolution, binary code and human hands, neon aesthetic",
            "Machine learning visualization, neural networks, modern tech art",
            "Quantum computing abstract, particles and waves, science fiction"
        ]
    },
    {
        "theme": "nature",
        "prompts": [
            "Majestic eagle soaring over mountains, dramatic sky, photorealistic",
            "Ancient tree with glowing roots, magical realism, mystical atmosphere",
            "Ocean waves crashing, powerful nature, dynamic composition",
            "Desert landscape with stars, cosmic beauty, wide angle"
        ]
    }
]

class ContentRunner:
    def __init__(self):
        self.session = None
        LOCAL_CACHE.mkdir(parents=True, exist_ok=True)
        
    async def init_session(self):
        """Initialize HTTP session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def close_session(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
    
    async def generate_meme(self, theme=None):
        """Generate meme image using Beast"""
        await self.init_session()
        
        # Select theme and prompt
        if not theme:
            theme_data = random.choice(MEME_TEMPLATES)
        else:
            theme_data = next((t for t in MEME_TEMPLATES if t["theme"] == theme), MEME_TEMPLATES[0])
        
        prompt = random.choice(theme_data["prompts"])
        
        print(f"🎨 Generating: {prompt[:50]}...")
        
        try:
            async with self.session.post(
                f"{BEAST_URL}/generate",
                json={
                    "prompt": prompt,
                    "width": 1024,
                    "height": 1024,
                    "steps": 30,
                    "guidance_scale": 7.5
                },
                timeout=aiohttp.ClientTimeout(total=120)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    image_path = data.get("image_path")
                    
                    # Download and save locally with theme prefix
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{theme_data['theme']}_{timestamp}.png"
                    local_path = LOCAL_CACHE / filename
                    
                    # Get image from Beast
                    beast_image_url = f"{BEAST_URL}{image_path}"
                    async with self.session.get(beast_image_url) as img_resp:
                        if img_resp.status == 200:
                            with open(local_path, 'wb') as f:
                                f.write(await img_resp.read())
                            
                            print(f"✅ Saved: {local_path}")
                            
                            # TODO: Upload to Sloth for permanent storage
                            await self.store_on_sloth(local_path, filename)
                            
                            return {
                                "success": True,
                                "path": str(local_path),
                                "url": f"/generated/{filename}",
                                "prompt": prompt,
                                "theme": theme_data["theme"]
                            }
                else:
                    print(f"❌ Beast error: {resp.status}")
                    return {"success": False, "error": f"Beast returned {resp.status}"}
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def store_on_sloth(self, local_path, filename):
        """Upload to Sloth for permanent storage"""
        try:
            # TODO: Implement actual upload to Sloth
            # For now, assume mounted filesystem or rsync
            print(f"📦 Would store {filename} on Sloth")
            # rsync or HTTP upload to Sloth storage
        except Exception as e:
            print(f"⚠️  Sloth storage failed: {e}")
    
    async def post_to_facebook(self, image_path, caption, meta_api_key=None):
        """Post generated content to Facebook"""
        if not meta_api_key:
            print("⚠️  No Meta API key - skipping Facebook post")
            return {"success": False, "reason": "No API key"}
        
        try:
            # Facebook Graph API
            # TODO: Implement when Meta approves application
            print(f"📘 Would post to Facebook: {caption[:50]}...")
            return {"success": True, "posted": True}
        except Exception as e:
            print(f"❌ Facebook post failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_batch(self, count=5):
        """Generate batch of content"""
        results = []
        for i in range(count):
            print(f"\n🔄 Generating {i+1}/{count}...")
            result = await self.generate_meme()
            results.append(result)
            await asyncio.sleep(2)  # Rate limit
        return results

async def run_continuous(interval_minutes=30):
    """Run content generation continuously"""
    runner = ContentRunner()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🎨 DYNAMIC CONTENT RUNNER - STARTED                        ║
╚══════════════════════════════════════════════════════════════╝

📊 Configuration:
• Beast: {BEAST_URL} (Image generation)
• Sloth: {SLOTH_STORAGE} (Permanent storage)
• Local Cache: {LOCAL_CACHE}
• Interval: {interval_minutes} minutes

🚀 Starting continuous generation...
""")
    
    try:
        while True:
            print(f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Generating content batch...")
            results = await runner.generate_batch(count=3)
            
            successful = sum(1 for r in results if r.get("success"))
            print(f"\n✅ Batch complete: {successful}/{len(results)} successful")
            
            # Wait for next interval
            print(f"💤 Sleeping for {interval_minutes} minutes...")
            await asyncio.sleep(interval_minutes * 60)
            
    except KeyboardInterrupt:
        print("\n⏹️  Stopping content runner...")
    finally:
        await runner.close_session()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "once":
        # Generate once and exit
        async def run_once():
            runner = ContentRunner()
            result = await runner.generate_meme()
            await runner.close_session()
            print(json.dumps(result, indent=2))
        
        asyncio.run(run_once())
    else:
        # Run continuously
        asyncio.run(run_continuous(interval_minutes=30))
