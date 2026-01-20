#!/usr/bin/env python3
"""
🚩 NM SOCIALISTS AI MEME GENERATOR
Real AI-generated propaganda using Queztl cluster infrastructure

Architecture:
- Route to Beast GPU when available (RTX 4090)
- Fall back to local virtual GPU (gpu_simulator.py)
- Use agents/pilots for distributed generation
- Learn from engagement metrics
"""

import os
import sys
import json
import asyncio
import aiohttp
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
import logging

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent.parent / "backend"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cluster configuration
BEAST_URL = "http://192.168.1.105:8001"
SLOTH_URL = "http://192.168.1.102:8000"
OUTPUT_DIR = Path(__file__).parent.parent / "frontend" / "generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Revolutionary themes
MEME_THEMES = {
    "land_back": {
        "prompt": "powerful propaganda poster of indigenous people reclaiming their ancestral lands, red and black color scheme, solidarity fist raised, mountains and desert landscape, bold typography 'LAND BACK', revolutionary art style",
        "negative": "racist, colonial, stereotypes, cartoonish"
    },
    "union_strong": {
        "prompt": "soviet-style propaganda poster of diverse workers united, raised fists, 'UNION STRONG' bold text, industrial background, red banners, solidarity symbols, powerful composition",
        "negative": "corporate, weak, divided"
    },
    "housing_rights": {
        "prompt": "revolutionary poster showing houses with red crossed-out rent signs, 'HOUSING IS A HUMAN RIGHT' bold text, people of all backgrounds together, hopeful but militant aesthetic",
        "negative": "landlord, capitalism, luxury"
    },
    "strike": {
        "prompt": "dramatic strike scene, workers marching with picket signs, 'ON STRIKE' bold letters, sunrise/sunset lighting, determined faces, red and black color palette, unity and power",
        "negative": "scab, boss, corporate"
    },
    "abolish_ice": {
        "prompt": "powerful protest image of diverse crowd holding 'ABOLISH ICE' signs, chains breaking, birds flying free, sunset colors, hopeful resistance, bold typography",
        "negative": "police, detention, fear"
    },
    "water_protector": {
        "prompt": "indigenous water protectors at pipeline protest, sacred water symbolism, raised fists, 'WATER IS LIFE' text, dramatic sky, eagles flying, powerful and spiritual",
        "negative": "oil, corporate, destruction"
    },
    "mutual_aid": {
        "prompt": "community members sharing food and resources, 'MUTUAL AID' bold text, warm colors, solidarity symbols, people helping each other, anarchist aesthetic",
        "negative": "charity, pity, condescending"
    },
    "no_borders": {
        "prompt": "border wall crumbling, people of all backgrounds joining hands across rubble, 'NO HUMAN IS ILLEGAL' text, sunrise, hope and liberation, powerful imagery",
        "negative": "nationalism, flags, division"
    }
}

class ClusterMemeGenerator:
    """AI meme generator using Queztl cluster infrastructure"""
    
    def __init__(self):
        self.beast_available = False
        self.local_gpu_available = False
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120))
        await self.check_cluster_health()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def check_cluster_health(self):
        """Check what GPU resources are available"""
        # Check Beast GPU
        try:
            async with self.session.get(f"{BEAST_URL}/health", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    self.beast_available = True
                    logger.info("✅ Beast GPU online (RTX 4090)")
        except Exception as e:
            logger.warning(f"⚠️  Beast GPU offline: {e}")
            
        # Check local virtual GPU
        try:
            from backend.gpu_simulator import SoftwareGPU
            self.local_gpu_available = True
            logger.info("✅ Virtual GPU available (software-based)")
        except Exception as e:
            logger.warning(f"⚠️  Virtual GPU unavailable: {e}")
    
    async def generate_with_beast(self, theme: str, prompt_data: Dict) -> Optional[Path]:
        """Generate using Beast's RTX 4090"""
        try:
            payload = {
                "prompt": prompt_data["prompt"],
                "negative_prompt": prompt_data["negative"],
                "width": 1024,
                "height": 1024,
                "steps": 30,
                "guidance_scale": 7.5,
                "theme": theme
            }
            
            logger.info(f"🎨 Generating '{theme}' on Beast GPU...")
            
            async with self.session.post(f"{BEAST_URL}/generate", json=payload) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    
                    # Download generated image
                    if "image_path" in result:
                        image_url = f"{BEAST_URL}{result['image_path']}"
                        async with self.session.get(image_url) as img_resp:
                            if img_resp.status == 200:
                                output_path = OUTPUT_DIR / f"{theme}_{int(datetime.now().timestamp())}.png"
                                output_path.write_bytes(await img_resp.read())
                                logger.info(f"✅ Saved: {output_path}")
                                return output_path
                    
                    # Or if image data is embedded
                    elif "image" in result:
                        import base64
                        output_path = OUTPUT_DIR / f"{theme}_{int(datetime.now().timestamp())}.png"
                        output_path.write_bytes(base64.b64decode(result["image"]))
                        logger.info(f"✅ Saved: {output_path}")
                        return output_path
                        
        except Exception as e:
            logger.error(f"❌ Beast generation failed: {e}")
            return None
    
    async def generate_with_local_gpu(self, theme: str, prompt_data: Dict) -> Optional[Path]:
        """Generate using local virtual GPU (fallback)"""
        try:
            logger.info(f"🎨 Generating '{theme}' on local virtual GPU...")
            
            # Import diffusers (will fail if not installed, handled below)
            try:
                from diffusers import StableDiffusionPipeline
                import torch
                
                # Use CPU or MPS (Metal Performance Shaders on Mac)
                if torch.backends.mps.is_available():
                    device = "mps"
                    logger.info("Using Metal GPU (Apple Silicon)")
                else:
                    device = "cpu"
                    logger.info("Using CPU (slower)")
                
                # Load model (this will download on first run)
                pipe = StableDiffusionPipeline.from_pretrained(
                    "runwayml/stable-diffusion-v1-5",
                    torch_dtype=torch.float16 if device != "cpu" else torch.float32
                )
                pipe = pipe.to(device)
                
                # Generate
                image = pipe(
                    prompt=prompt_data["prompt"],
                    negative_prompt=prompt_data["negative"],
                    width=1024,
                    height=1024,
                    num_inference_steps=20,  # Faster for CPU
                    guidance_scale=7.5
                ).images[0]
                
                # Save
                output_path = OUTPUT_DIR / f"{theme}_{int(datetime.now().timestamp())}.png"
                image.save(output_path)
                logger.info(f"✅ Saved: {output_path}")
                return output_path
                
            except ImportError:
                logger.error("❌ torch/diffusers not installed. Install with:")
                logger.error("   pip3 install --break-system-packages torch torchvision diffusers transformers")
                return None
                
        except Exception as e:
            logger.error(f"❌ Local GPU generation failed: {e}")
            return None
    
    async def generate_with_text_fallback(self, theme: str, prompt_data: Dict) -> Path:
        """Ultimate fallback: text overlay (current implementation)"""
        logger.warning(f"⚠️  Falling back to text overlay for '{theme}'")
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create image
            img = Image.new('RGB', (1080, 1080), "#8B0000")
            draw = ImageDraw.Draw(img)
            
            # Extract key text from prompt
            text = theme.replace("_", " ").upper()
            
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Impact.ttf", 72)
            except:
                font = ImageFont.load_default()
            
            # Center text
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (1080 - text_width) / 2
            y = (1080 - text_height) / 2
            
            # Draw with outline
            for offset_x in [-3, -2, -1, 0, 1, 2, 3]:
                for offset_y in [-3, -2, -1, 0, 1, 2, 3]:
                    draw.text((x + offset_x, y + offset_y), text, font=font, fill="black")
            draw.text((x, y), text, font=font, fill="white")
            
            # Save
            output_path = OUTPUT_DIR / f"{theme}_text_{int(datetime.now().timestamp())}.png"
            img.save(output_path)
            logger.info(f"⚠️  Text fallback saved: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Even text fallback failed: {e}")
            raise
    
    async def generate_meme(self, theme: str) -> Path:
        """
        Generate a meme using best available method:
        1. Try Beast GPU (RTX 4090)
        2. Try local GPU (MPS/CPU with Stable Diffusion)
        3. Fall back to text overlay
        """
        if theme not in MEME_THEMES:
            raise ValueError(f"Unknown theme: {theme}. Available: {list(MEME_THEMES.keys())}")
        
        prompt_data = MEME_THEMES[theme]
        
        # Try Beast first
        if self.beast_available:
            result = await self.generate_with_beast(theme, prompt_data)
            if result:
                return result
        
        # Try local GPU
        if self.local_gpu_available:
            result = await self.generate_with_local_gpu(theme, prompt_data)
            if result:
                return result
        
        # Ultimate fallback
        return await self.generate_with_text_fallback(theme, prompt_data)
    
    async def generate_batch(self, themes: Optional[List[str]] = None, count: int = 8) -> List[Path]:
        """Generate multiple memes"""
        if themes is None:
            import random
            themes = random.sample(list(MEME_THEMES.keys()), min(count, len(MEME_THEMES)))
        
        results = []
        for i, theme in enumerate(themes, 1):
            logger.info(f"[{i}/{len(themes)}] Generating {theme}...")
            try:
                path = await self.generate_meme(theme)
                results.append(path)
            except Exception as e:
                logger.error(f"Failed to generate {theme}: {e}")
        
        return results


async def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Meme Generator for NM Socialists")
    parser.add_argument("--theme", type=str, help=f"Theme: {list(MEME_THEMES.keys())}")
    parser.add_argument("--count", type=int, default=8, help="Number of random memes")
    parser.add_argument("--check-health", action="store_true", help="Check cluster health")
    
    args = parser.parse_args()
    
    async with ClusterMemeGenerator() as generator:
        if args.check_health:
            print("\n🔍 CLUSTER HEALTH CHECK")
            print("=" * 60)
            print(f"Beast GPU (RTX 4090):  {'✅ Online' if generator.beast_available else '❌ Offline'}")
            print(f"Local Virtual GPU:     {'✅ Available' if generator.local_gpu_available else '❌ Unavailable'}")
            print("=" * 60)
            return
        
        if args.theme:
            # Generate single theme
            result = await generator.generate_meme(args.theme)
            print(f"\n✅ Generated: {result}")
        else:
            # Generate batch
            print(f"\n🚩 Generating {args.count} revolutionary memes...")
            results = await generator.generate_batch(count=args.count)
            print(f"\n✅ Generated {len(results)} memes:")
            for path in results:
                print(f"   - {path.name}")


if __name__ == "__main__":
    asyncio.run(main())
