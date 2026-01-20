#!/usr/bin/env python3
"""
Mac Cluster Node - Adds Mac as compute node to Beast/Sloth cluster
Provides dynamic content generation for website
"""

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
from datetime import datetime
from pathlib import Path
import json
import os
import socket
import psutil
import platform

# DHCP-safe cluster host resolution
try:
    from backend.queztl_discovery import resolve_cluster_hosts
except ImportError:  # pragma: no cover
    from queztl_discovery import resolve_cluster_hosts

app = FastAPI(title="Mac Command Center", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
MAC_IP = socket.gethostbyname(socket.gethostname())

# Allow explicit override; otherwise resolve via env/nmap/ssh probing
BEAST_URL = os.environ.get("QUEZTL_BEAST_URL")
SLOTH_URL = os.environ.get("QUEZTL_SLOTH_URL")
if not (BEAST_URL and SLOTH_URL):
    hosts = resolve_cluster_hosts()
    if not BEAST_URL and hosts.beast:
        BEAST_URL = f"http://{hosts.beast}:8001"
    if not SLOTH_URL and hosts.sloth:
        SLOTH_URL = f"http://{hosts.sloth}:8000"

OUTPUT_DIR = Path("output/mac_generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# System info
SYSTEM_INFO = {
    "hostname": socket.gethostname(),
    "platform": platform.system(),
    "processor": platform.processor(),
    "ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
    "cpu_count": psutil.cpu_count(),
    "role": "command_center_only"
}

@app.get("/")
async def root():
    """Mac node status"""
    return {
        "status": "online",
        "node": "mac_command_center",
        "system": SYSTEM_INFO,
        "timestamp": datetime.now().isoformat(),
        "cluster_members": await get_cluster_status()
    }

@app.get("/health")
async def health():
    """Health check"""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    
    return {
        "status": "healthy" if cpu < 90 and ram < 90 else "degraded",
        "cpu_usage": cpu,
        "ram_usage": ram,
        "uptime": datetime.now().isoformat()
    }

async def get_cluster_status():
    """Check all cluster nodes"""
    nodes = {}
    
    # Check Beast
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(f"{BEAST_URL}/health")
            nodes["beast"] = resp.json() if resp.status_code == 200 else {"status": "error"}
    except:
        nodes["beast"] = {"status": "offline"}
    
    # Check Sloth
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(f"{SLOTH_URL}/health")
            nodes["sloth"] = resp.json() if resp.status_code == 200 else {"status": "error"}
    except:
        nodes["sloth"] = {"status": "offline"}
    
    return nodes

@app.post("/generate/content")
async def generate_content(content_type: str, params: dict, background_tasks: BackgroundTasks):
    """
    Generate dynamic content for website
    Routes to appropriate cluster node
    """
    
    if content_type == "meme":
        # Route to Beast for image generation
        return await generate_meme_on_beast(params)
    
    elif content_type == "theory":
        # Generate theory content locally
        return generate_theory_snippet(params)
    
    elif content_type == "stats":
        # Generate live stats
        return await get_cluster_stats()
    
    else:
        raise HTTPException(status_code=400, detail="Unknown content type")

async def generate_meme_on_beast(params: dict):
    """Send meme generation to Beast"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(f"{BEAST_URL}/generate", json=params)
            
            if resp.status_code == 200:
                result = resp.json()
                return {
                    "status": "success",
                    "generated_by": "beast",
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                raise HTTPException(status_code=500, detail="Beast generation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Beast offline: {str(e)}")

def generate_theory_snippet(params: dict):
    """Generate theory content snippet"""
    topic = params.get("topic", "revolution")
    
    snippets = {
        "revolution": "The history of all hitherto existing society is the history of class struggles.",
        "labor": "Workers of the world, unite! You have nothing to lose but your chains.",
        "capitalism": "Capital is dead labor, which, vampire-like, lives only by sucking living labor.",
        "solidarity": "An injury to one is an injury to all.",
        "liberation": "The emancipation of the working class must be the work of the workers themselves."
    }
    
    return {
        "status": "success",
        "topic": topic,
        "content": snippets.get(topic, snippets["solidarity"]),
        "source": "mac_local",
        "timestamp": datetime.now().isoformat()
    }

async def get_cluster_stats():
    """Get real-time cluster statistics"""
    cluster = await get_cluster_status()
    
    return {
        "cluster": {
            "total_nodes": len([n for n in cluster.values() if n.get("status") != "offline"]),
            "online_nodes": len([n for n in cluster.values() if n.get("status") == "healthy"]),
            "nodes": cluster
        },
        "mac": {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/test/beast")
async def test_beast_connection():
    """Test Beast image generation"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            test_prompt = {
                "prompt": "Red star symbol, revolutionary fist, minimal design",
                "width": 512,
                "height": 512,
                "steps": 20
            }
            resp = await client.post(f"{BEAST_URL}/generate", json=test_prompt)
            
            return {
                "status": "success" if resp.status_code == 200 else "failed",
                "response": resp.json() if resp.status_code == 200 else resp.text
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  💻 MAC CLUSTER NODE STARTING                               ║
║  Command Center + Compute Node                              ║
╚══════════════════════════════════════════════════════════════╝

System: {SYSTEM_INFO['processor']}
RAM: {SYSTEM_INFO['ram_gb']} GB
CPUs: {SYSTEM_INFO['cpu_count']}

Starting on: http://localhost:8002
""")
    
    uvicorn.run(app, host="0.0.0.0", port=8002)
