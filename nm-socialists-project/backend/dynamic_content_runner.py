#!/usr/bin/env python3
"""
Dynamic Content Runner - Auto-generates content for website
Memes, theory snippets, stats - all live and fresh
"""

import asyncio
import httpx
import json
from datetime import datetime
from pathlib import Path
import random

# Content generation rules
MEME_PROMPTS = [
    {
        "prompt": "Workers united raising fists, red banners, soviet propaganda style",
        "style": "propaganda"
    },
    {
        "prompt": "Solidarity forever, hands clasped together, constructivist design",
        "style": "constructivist"
    },
    {
        "prompt": "An injury to one is an injury to all, industrial workers, vintage poster",
        "style": "vintage"
    },
    {
        "prompt": "Break the chains of capitalism, revolutionary imagery, bold colors",
        "style": "propaganda"
    },
    {
        "prompt": "The people united will never be defeated, crowd scene, powerful",
        "style": "propaganda"
    }
]

THEORY_SNIPPETS = [
    {
        "title": "On Class Struggle",
        "quote": "The history of all hitherto existing society is the history of class struggles.",
        "author": "Karl Marx",
        "source": "Communist Manifesto"
    },
    {
        "title": "Workers Unity",
        "quote": "Workers of the world, unite! You have nothing to lose but your chains.",
        "author": "Karl Marx",
        "source": "Communist Manifesto"
    },
    {
        "title": "On Capital",
        "quote": "Capital is dead labor, which, vampire-like, lives only by sucking living labor.",
        "author": "Karl Marx",
        "source": "Das Kapital"
    },
    {
        "title": "Solidarity",
        "quote": "An injury to one is an injury to all.",
        "author": "IWW Slogan",
        "source": "Labor Movement"
    },
    {
        "title": "Self-Emancipation",
        "quote": "The emancipation of the working class must be the work of the workers themselves.",
        "author": "Karl Marx",
        "source": "International Workingmen's Association"
    }
]

class ContentRunner:
    def __init__(self):
        self.output_dir = Path("frontend/dynamic_content")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.beast_url = "http://192.168.1.105:8001"
        self.mac_url = "http://localhost:8002"
        
        self.generation_log = []
    
    async def check_beast_health(self):
        """Check if Beast is online"""
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.get(f"{self.beast_url}/health")
                return resp.status_code == 200
        except:
            return False
    
    async def generate_meme(self):
        """Generate a meme using Beast"""
        if not await self.check_beast_health():
            print("⚠️  Beast offline - skipping meme generation")
            return None
        
        prompt_data = random.choice(MEME_PROMPTS)
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                payload = {
                    "prompt": prompt_data["prompt"],
                    "style": prompt_data["style"],
                    "width": 1024,
                    "height": 1024,
                    "steps": 30,
                    "guidance_scale": 7.5
                }
                
                print(f"🎨 Generating: {prompt_data['prompt'][:50]}...")
                resp = await client.post(f"{self.beast_url}/generate", json=payload)
                
                if resp.status_code == 200:
                    result = resp.json()
                    
                    # Save metadata
                    meme_data = {
                        "timestamp": datetime.now().isoformat(),
                        "prompt": prompt_data["prompt"],
                        "style": prompt_data["style"],
                        "result": result
                    }
                    
                    filename = f"meme_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(self.output_dir / filename, 'w') as f:
                        json.dump(meme_data, f, indent=2)
                    
                    print(f"✅ Meme generated: {filename}")
                    return meme_data
                else:
                    print(f"❌ Generation failed: {resp.status_code}")
                    return None
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def generate_theory_content(self):
        """Generate theory snippet"""
        snippet = random.choice(THEORY_SNIPPETS)
        
        content = {
            "type": "theory",
            "timestamp": datetime.now().isoformat(),
            **snippet
        }
        
        filename = f"theory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(self.output_dir / filename, 'w') as f:
            json.dump(content, f, indent=2)
        
        print(f"✅ Theory content: {snippet['title']}")
        return content
    
    def generate_stats_widget(self):
        """Generate stats for website"""
        stats = {
            "type": "stats",
            "timestamp": datetime.now().isoformat(),
            "members": random.randint(150, 200),  # Will be replaced with real DB count
            "active_campaigns": random.randint(3, 8),
            "events_this_month": random.randint(5, 12),
            "theory_articles": 47
        }
        
        with open(self.output_dir / "stats.json", 'w') as f:
            json.dump(stats, f, indent=2)
        
        print(f"✅ Stats updated: {stats['members']} members")
        return stats
    
    def create_content_feed(self):
        """Create a feed of all recent content"""
        feed = []
        
        for file in sorted(self.output_dir.glob("*.json"), reverse=True)[:10]:
            with open(file) as f:
                data = json.load(f)
                feed.append(data)
        
        with open(self.output_dir / "feed.json", 'w') as f:
            json.dump(feed, f, indent=2)
        
        print(f"✅ Content feed updated: {len(feed)} items")
        return feed
    
    async def run_generation_cycle(self):
        """Run one cycle of content generation"""
        print("\n╔══════════════════════════════════════════════════════════════╗")
        print("║  🔄 DYNAMIC CONTENT GENERATION CYCLE                        ║")
        print("╚══════════════════════════════════════════════════════════════╝\n")
        
        # Generate meme (if Beast is up)
        await self.generate_meme()
        
        # Generate theory content
        self.generate_theory_content()
        
        # Update stats
        self.generate_stats_widget()
        
        # Update feed
        self.create_content_feed()
        
        print("\n✅ Generation cycle complete!\n")
    
    async def run_continuous(self, interval_minutes=30):
        """Run continuously"""
        print(f"🚀 Starting continuous generation (every {interval_minutes} minutes)\n")
        
        while True:
            await self.run_generation_cycle()
            await asyncio.sleep(interval_minutes * 60)

async def main():
    runner = ContentRunner()
    
    # Run one cycle immediately
    await runner.run_generation_cycle()
    
    # Ask if continuous
    print("Run continuously? (y/n): ", end='')
    # For automation, just run once
    # Uncomment below for continuous:
    # await runner.run_continuous(interval_minutes=30)

if __name__ == "__main__":
    asyncio.run(main())
