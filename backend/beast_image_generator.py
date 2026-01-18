#!/usr/bin/env python3
"""
Beast Image Generator - Stable Diffusion XL on Beast
Generate high-quality socialist propaganda images using open-source AI
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from typing import Optional, List
import uuid
import json
from datetime import datetime
import subprocess
import os

app = FastAPI(title="BeastQC Image Generator", version="1.0.0")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OUTPUT_DIR = Path("output/beast_generated_images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

QUEUE_FILE = Path("output/generation_queue.json")
RESULTS_FILE = Path("output/generation_results.json")


class ImagePrompt(BaseModel):
    """Image generation request"""
    prompt: str
    negative_prompt: Optional[str] = "low quality, blurry, distorted, watermark, text"
    width: int = 1024
    height: int = 1024
    steps: int = 30
    guidance_scale: float = 7.5
    seed: Optional[int] = None
    style: Optional[str] = "propaganda"  # propaganda, constructivist, vintage, modern


class GenerationResult(BaseModel):
    """Generation result"""
    job_id: str
    status: str  # queued, processing, complete, failed
    prompt: str
    image_path: Optional[str] = None
    error: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None


# Preset styles matching your aesthetic
STYLE_PRESETS = {
    "propaganda": {
        "prompt_suffix": ", bold propaganda poster style, high contrast, red and black colors, revolutionary aesthetic, dramatic lighting, socialist realism",
        "negative": "cartoon, anime, photo, modern, digital art, low quality"
    },
    "constructivist": {
        "prompt_suffix": ", soviet constructivist style, geometric shapes, bold typography, red black and white, avant-garde, 1920s design",
        "negative": "detailed, realistic, modern, cartoon, low quality"
    },
    "vintage": {
        "prompt_suffix": ", vintage propaganda poster, aged paper texture, 1940s style, weathered, historical, muted colors",
        "negative": "modern, digital, cartoon, anime, low quality"
    },
    "modern": {
        "prompt_suffix": ", modern political art, digital illustration, bold colors, clean design, contemporary",
        "negative": "vintage, old, blurry, low quality"
    }
}


def load_queue():
    """Load generation queue"""
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE) as f:
            return json.load(f)
    return []


def save_queue(queue):
    """Save generation queue"""
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)


def load_results():
    """Load generation results"""
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE) as f:
            return json.load(f)
    return {}


def save_results(results):
    """Save generation results"""
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)


def enhance_prompt_with_style(prompt: str, style: str) -> str:
    """Enhance prompt with style preset"""
    if style in STYLE_PRESETS:
        preset = STYLE_PRESETS[style]
        return prompt + preset["prompt_suffix"]
    return prompt


def get_style_negative_prompt(style: str, user_negative: str) -> str:
    """Get negative prompt for style"""
    if style in STYLE_PRESETS:
        preset = STYLE_PRESETS[style]
        return f"{user_negative}, {preset['negative']}"
    return user_negative


@app.get("/")
async def root():
    """API info"""
    return {
        "name": "BeastQC Image Generator",
        "version": "1.0.0",
        "status": "online",
        "backend": "Stable Diffusion XL",
        "styles": list(STYLE_PRESETS.keys())
    }


@app.post("/generate", response_model=GenerationResult)
async def generate_image(request: ImagePrompt, background_tasks: BackgroundTasks):
    """Queue image generation"""
    job_id = str(uuid.uuid4())
    
    # Enhance prompt with style
    enhanced_prompt = enhance_prompt_with_style(request.prompt, request.style or "propaganda")
    enhanced_negative = get_style_negative_prompt(
        request.style or "propaganda",
        request.negative_prompt
    )
    
    # Create job
    job = {
        "job_id": job_id,
        "status": "queued",
        "prompt": request.prompt,
        "enhanced_prompt": enhanced_prompt,
        "negative_prompt": enhanced_negative,
        "width": request.width,
        "height": request.height,
        "steps": request.steps,
        "guidance_scale": request.guidance_scale,
        "seed": request.seed,
        "style": request.style,
        "created_at": datetime.now().isoformat()
    }
    
    # Add to queue
    queue = load_queue()
    queue.append(job)
    save_queue(queue)
    
    # Add to results
    results = load_results()
    results[job_id] = job
    save_results(results)
    
    # Start processing in background
    background_tasks.add_task(process_generation, job_id)
    
    return GenerationResult(
        job_id=job_id,
        status="queued",
        prompt=request.prompt,
        created_at=job["created_at"]
    )


@app.get("/status/{job_id}", response_model=GenerationResult)
async def get_status(job_id: str):
    """Get generation status"""
    results = load_results()
    
    if job_id not in results:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = results[job_id]
    
    return GenerationResult(
        job_id=job_id,
        status=job["status"],
        prompt=job["prompt"],
        image_path=job.get("image_path"),
        error=job.get("error"),
        created_at=job["created_at"],
        completed_at=job.get("completed_at")
    )


@app.get("/image/{job_id}")
async def get_image(job_id: str):
    """Download generated image"""
    results = load_results()
    
    if job_id not in results:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = results[job_id]
    
    if job["status"] != "complete":
        raise HTTPException(status_code=400, detail="Image not ready")
    
    if not job.get("image_path"):
        raise HTTPException(status_code=404, detail="Image not found")
    
    image_path = Path(job["image_path"])
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image file not found")
    
    return FileResponse(image_path, media_type="image/png")


@app.get("/queue")
async def get_queue():
    """Get current queue"""
    queue = load_queue()
    return {"queue": queue, "count": len(queue)}


@app.get("/recent")
async def get_recent(limit: int = 10):
    """Get recent generations"""
    results = load_results()
    
    # Sort by created_at
    sorted_results = sorted(
        results.values(),
        key=lambda x: x["created_at"],
        reverse=True
    )
    
    return {"results": sorted_results[:limit], "total": len(results)}


@app.delete("/job/{job_id}")
async def cancel_job(job_id: str):
    """Cancel job"""
    results = load_results()
    
    if job_id not in results:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = results[job_id]
    
    if job["status"] == "processing":
        raise HTTPException(status_code=400, detail="Cannot cancel job in progress")
    
    # Remove from queue
    queue = load_queue()
    queue = [j for j in queue if j["job_id"] != job_id]
    save_queue(queue)
    
    # Mark as cancelled
    job["status"] = "cancelled"
    results[job_id] = job
    save_results(results)
    
    return {"message": "Job cancelled"}


def process_generation(job_id: str):
    """Process image generation using Stable Diffusion"""
    results = load_results()
    job = results[job_id]
    
    try:
        # Update status
        job["status"] = "processing"
        results[job_id] = job
        save_results(results)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"beast_gen_{timestamp}_{job_id[:8]}.png"
        output_path = OUTPUT_DIR / filename
        
        # Check if diffusers is installed
        try:
            import torch
            from diffusers import DiffusionPipeline
            
            # Load Stable Diffusion XL
            print(f"🎨 Loading Stable Diffusion XL for job {job_id[:8]}...")
            
            pipe = DiffusionPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=torch.float16,
                use_safetensors=True,
                variant="fp16"
            )
            
            # Use CPU if no GPU
            device = "cuda" if torch.cuda.is_available() else "cpu"
            pipe = pipe.to(device)
            
            print(f"🔥 Generating: {job['enhanced_prompt'][:80]}...")
            
            # Generate image
            image = pipe(
                prompt=job["enhanced_prompt"],
                negative_prompt=job["negative_prompt"],
                width=job["width"],
                height=job["height"],
                num_inference_steps=job["steps"],
                guidance_scale=job["guidance_scale"],
                generator=torch.Generator(device=device).manual_seed(job["seed"]) if job["seed"] else None
            ).images[0]
            
            # Save image
            image.save(output_path)
            
            print(f"✓ Generated: {filename}")
            
            # Update results
            job["status"] = "complete"
            job["image_path"] = str(output_path)
            job["completed_at"] = datetime.now().isoformat()
            
        except ImportError:
            # Diffusers not installed - use fallback or placeholder
            print(f"⚠️  Stable Diffusion not installed, creating placeholder")
            
            # Create a placeholder with the prompt text
            from PIL import Image, ImageDraw, ImageFont
            
            img = Image.new('RGB', (job["width"], job["height"]), (40, 40, 40))
            draw = ImageDraw.Draw(img)
            
            # Add prompt text
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
            except:
                font = ImageFont.load_default()
            
            text = f"PLACEHOLDER\n\n{job['prompt']}\n\nInstall Stable Diffusion:\npip install diffusers transformers accelerate"
            
            # Wrap text
            words = text.split()
            lines = []
            line = []
            for word in words:
                test = ' '.join(line + [word])
                bbox = draw.textbbox((0, 0), test, font=font)
                if bbox[2] - bbox[0] <= job["width"] - 100:
                    line.append(word)
                else:
                    lines.append(' '.join(line))
                    line = [word]
            lines.append(' '.join(line))
            
            y = 100
            for line_text in lines:
                draw.text((50, y), line_text, font=font, fill=(200, 200, 200))
                y += 50
            
            img.save(output_path)
            
            job["status"] = "complete"
            job["image_path"] = str(output_path)
            job["completed_at"] = datetime.now().isoformat()
            job["note"] = "Placeholder - Stable Diffusion not installed"
        
    except Exception as e:
        print(f"✗ Error generating {job_id}: {e}")
        job["status"] = "failed"
        job["error"] = str(e)
        job["completed_at"] = datetime.now().isoformat()
    
    # Save final results
    results[job_id] = job
    save_results(results)
    
    # Remove from queue
    queue = load_queue()
    queue = [j for j in queue if j["job_id"] != job_id]
    save_queue(queue)


if __name__ == "__main__":
    import uvicorn
    
    print("🚩 BeastQC Image Generator")
    print("=" * 50)
    print("")
    print("Starting FastAPI server...")
    print("API will be available at: http://0.0.0.0:8001")
    print("")
    print("📖 Endpoints:")
    print("  POST /generate    - Generate image")
    print("  GET  /status/{id} - Check status")
    print("  GET  /image/{id}  - Download image")
    print("  GET  /queue       - View queue")
    print("  GET  /recent      - Recent generations")
    print("")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
