#!/usr/bin/env python3
"""
Beast GPU Workload Runner - Actually uses the RTX 4090!
Generates images continuously to keep GPU busy
"""

import asyncio
import aiohttp
import time
from datetime import datetime
from pathlib import Path
import random

BEAST_URL = "http://192.168.1.105:8001"
OUTPUT_DIR = Path.home() / "queztl-core" / "frontend" / "generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPTS = [
    "Futuristic cyberpunk cityscape at night, neon lights, flying cars, detailed",
    "Mountain landscape with aurora borealis, stars, photorealistic",
    "Abstract geometric patterns, vibrant colors, digital art",
    "Steampunk mechanical clockwork, brass gears, intricate details",
    "Ocean waves crashing on rocks, dramatic sunset, high resolution",
    "Space station orbiting earth, realistic, detailed",
    "Dense forest with sunlight filtering through trees, mystical atmosphere",
    "Desert sand dunes under starry night sky, long exposure effect",
]

async def generate_image(session, prompt_id):
    """Generate one image using Beast GPU"""
    prompt = random.choice(PROMPTS)
    
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🎨 Generating image {prompt_id}...")
        print(f"   Prompt: {prompt[:60]}...")
        
        start_time = time.time()
        
        async with session.post(
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
                elapsed = time.time() - start_time
                
                # Download image
                image_path = data.get("image_path")
                if image_path:
                    async with session.get(f"{BEAST_URL}{image_path}") as img_resp:
                        if img_resp.status == 200:
                            filename = f"workload_{prompt_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                            output_path = OUTPUT_DIR / filename
                            
                            with open(output_path, 'wb') as f:
                                f.write(await img_resp.read())
                            
                            print(f"   ✅ Done in {elapsed:.1f}s - saved to {filename}")
                            return True
            else:
                print(f"   ❌ Beast error: {resp.status}")
                return False
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

async def continuous_workload(batch_size=5, delay_between_batches=10):
    """
    Run continuous GPU workload
    batch_size: number of images to generate in parallel
    delay_between_batches: seconds to wait between batches
    """
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🔥 BEAST GPU WORKLOAD RUNNER                               ║
║  RTX 4090 Continuous Processing                             ║
╚══════════════════════════════════════════════════════════════╝

Configuration:
• Batch Size: {batch_size} parallel generations
• Delay: {delay_between_batches}s between batches
• Output: {OUTPUT_DIR}

Press Ctrl+C to stop
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    
    async with aiohttp.ClientSession() as session:
        batch_num = 0
        total_generated = 0
        
        try:
            while True:
                batch_num += 1
                print(f"\n🚀 BATCH {batch_num} - Generating {batch_size} images in parallel...")
                
                # Generate images in parallel
                tasks = [
                    generate_image(session, f"B{batch_num}_{i+1}")
                    for i in range(batch_size)
                ]
                
                results = await asyncio.gather(*tasks)
                success_count = sum(1 for r in results if r)
                total_generated += success_count
                
                print(f"\n📊 Batch {batch_num} complete: {success_count}/{batch_size} successful")
                print(f"   Total generated: {total_generated}")
                print(f"\n⏳ Waiting {delay_between_batches}s before next batch...")
                
                await asyncio.sleep(delay_between_batches)
                
        except KeyboardInterrupt:
            print(f"\n\n✋ Stopped by user")
            print(f"📊 Final stats: {total_generated} images generated")

async def stress_test(duration_minutes=5):
    """
    Maximum stress test - generate as fast as possible
    """
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  ⚡ BEAST GPU STRESS TEST                                   ║
║  Maximum load for {duration_minutes} minutes                         ║
╚══════════════════════════════════════════════════════════════╝

This will max out the RTX 4090!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        generated = 0
        
        while time.time() < end_time:
            success = await generate_image(session, f"STRESS_{generated+1}")
            if success:
                generated += 1
            
            remaining = int((end_time - time.time()) / 60)
            print(f"   📊 {generated} images | {remaining}min remaining\n")
        
        elapsed = (time.time() - start_time) / 60
        rate = generated / elapsed
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║  📊 STRESS TEST COMPLETE                                    ║
╚══════════════════════════════════════════════════════════════╝

Duration:  {elapsed:.1f} minutes
Generated: {generated} images
Rate:      {rate:.1f} images/min
Output:    {OUTPUT_DIR}
""")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "stress":
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        asyncio.run(stress_test(duration))
    else:
        batch_size = int(sys.argv[1]) if len(sys.argv) > 1 else 3
        delay = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        asyncio.run(continuous_workload(batch_size, delay))
