#!/usr/bin/env python3
"""
📡 RGIS DATA SERVER
Simple file server for exposing MAG survey data from RGIS.com

Deploy this on RGIS.com to serve survey data to your master coordinator.
"""

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from typing import List, Dict, Any
import hashlib
from datetime import datetime

app = FastAPI(title="RGIS Survey Data Server", version="1.0")

# CORS for cross-domain access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CONFIGURATION
SURVEY_DATA_DIR = os.getenv("SURVEY_DATA_DIR", "/data/surveys")
RESULTS_DIR = os.getenv("RESULTS_DIR", "/data/results")

# Ensure directories exist
Path(SURVEY_DATA_DIR).mkdir(parents=True, exist_ok=True)
Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)


def get_file_hash(filepath: str) -> str:
    """Calculate file hash for integrity"""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


@app.get("/")
async def root():
    return {
        "service": "RGIS Survey Data Server",
        "version": "1.0",
        "survey_directory": SURVEY_DATA_DIR,
        "endpoints": {
            "list_surveys": "/api/surveys/list",
            "download": "/api/surveys/download/{survey_id}",
            "upload_results": "/api/surveys/{survey_id}/results"
        }
    }


@app.get("/api/surveys/list")
async def list_surveys():
    """List all available MAG surveys"""
    surveys = []
    survey_dir = Path(SURVEY_DATA_DIR)
    
    for file_path in survey_dir.glob("**/*"):
        if file_path.is_file() and file_path.suffix.lower() in ['.csv', '.xyz', '.gdb', '.dat']:
            # Get file info
            stat = file_path.stat()
            
            # Generate survey ID from filename
            survey_id = hashlib.md5(str(file_path.relative_to(survey_dir)).encode()).hexdigest()[:16]
            
            surveys.append({
                "id": survey_id,
                "name": file_path.name,
                "path": str(file_path.relative_to(survey_dir)),
                "format": file_path.suffix.lstrip('.').lower(),
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "hash": get_file_hash(str(file_path))
            })
    
    return {
        "surveys": surveys,
        "total": len(surveys),
        "data_directory": SURVEY_DATA_DIR
    }


@app.get("/api/surveys/download/{survey_id}")
async def download_survey(survey_id: str):
    """Download a specific survey file"""
    survey_dir = Path(SURVEY_DATA_DIR)
    
    # Find file by ID
    for file_path in survey_dir.glob("**/*"):
        if file_path.is_file():
            file_id = hashlib.md5(str(file_path.relative_to(survey_dir)).encode()).hexdigest()[:16]
            if file_id == survey_id:
                return FileResponse(
                    path=str(file_path),
                    filename=file_path.name,
                    media_type="application/octet-stream"
                )
    
    raise HTTPException(status_code=404, detail=f"Survey {survey_id} not found")


@app.post("/api/surveys/{survey_id}/results")
async def upload_results(survey_id: str, results: Dict[str, Any]):
    """Receive processing results from master"""
    results_dir = Path(RESULTS_DIR)
    results_file = results_dir / f"{survey_id}_results.json"
    
    # Add metadata
    results['uploaded_at'] = datetime.now().isoformat()
    results['survey_id'] = survey_id
    
    # Save results
    import json
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    return {
        "status": "success",
        "survey_id": survey_id,
        "results_file": str(results_file),
        "drill_targets": len(results.get('drill_targets', [])),
        "message": "Results saved successfully"
    }


@app.get("/api/surveys/{survey_id}/results")
async def get_results(survey_id: str):
    """Retrieve processing results"""
    results_file = Path(RESULTS_DIR) / f"{survey_id}_results.json"
    
    if not results_file.exists():
        raise HTTPException(status_code=404, detail="Results not found")
    
    import json
    with open(results_file) as f:
        results = json.load(f)
    
    return results


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "survey_directory": SURVEY_DATA_DIR,
        "results_directory": RESULTS_DIR,
        "surveys_available": len(list(Path(SURVEY_DATA_DIR).glob("**/*.[csv|xyz|gdb|dat]")))
    }


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("📡 RGIS SURVEY DATA SERVER")
    print("=" * 60)
    print(f"Survey Data: {SURVEY_DATA_DIR}")
    print(f"Results: {RESULTS_DIR}")
    print()
    print("Starting server on http://0.0.0.0:8000")
    print("=" * 60)
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
