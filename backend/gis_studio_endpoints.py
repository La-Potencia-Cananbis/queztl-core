"""
GIS Studio REST API Endpoints for QuetzalCore
Complete validation, integration, training, and improvement endpoints
Add these to backend/main.py after the geophysics endpoints
"""

# After line 3250 in main.py, add these imports at the top with other imports:
# from .gis_geophysics_integrator import GISGeophysicsIntegrator
# from .gis_geophysics_trainer import GISGeophysicsTrainer, TrainingDataset
# from .gis_geophysics_improvement import AdaptiveImprovementEngine

# Then add these global initializers after gis_validator:
# gis_integrator = GISGeophysicsIntegrator()
# gis_trainer = GISGeophysicsTrainer()
# gis_improvement = AdaptiveImprovementEngine()

# Add these endpoints before the @app.get("/info") endpoint:

# =============================================================================
# 🗺️ GIS STUDIO API ENDPOINTS - Complete Validation & Analysis
# =============================================================================

@app.post("/api/gis/studio/validate/lidar")
async def validate_lidar_data(
    points: List[List[float]],
    classification: Optional[List[int]] = None,
    intensity: Optional[List[int]] = None
):
    """
    Validate LiDAR point cloud data
    - Points: Nx3 array (x, y, z coordinates)
    - Classification: Optional point classifications (0-18)
    - Intensity: Optional intensity values (0-255)
    """
    try:
        import numpy as np
        points_array = np.array(points)
        
        result = LiDARValidator.validate_point_cloud(
            points_array,
            np.array(classification) if classification else None,
            np.array(intensity) if intensity else None
        )
        
        return {
            "valid": result.valid,
            "status": result.status.value,
            "data_type": result.data_type,
            "metadata": result.metadata,
            "issues": result.issues,
            "warnings": result.warnings,
            "summary": result.summary()
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"LiDAR validation failed: {str(e)}"}
        )


@app.post("/api/gis/studio/validate/dem")
async def validate_dem_data(elevation: List[List[float]]):
    """
    Validate Digital Elevation Model (DEM) data
    - Elevation: 2D grid of elevation values
    """
    try:
        import numpy as np
        elevation_array = np.array(elevation)
        
        result = RasterValidator.validate_elevation_grid(elevation_array)
        
        return {
            "valid": result.valid,
            "status": result.status.value,
            "metadata": result.metadata,
            "issues": result.issues,
            "warnings": result.warnings
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"DEM validation failed: {str(e)}"}
        )


@app.post("/api/gis/studio/validate/imagery")
async def validate_satellite_imagery(file: UploadFile = File(...)):
    """
    Validate satellite imagery
    Supports: RGB, RGBA, multispectral
    """
    try:
        from PIL import Image
        import numpy as np
        import io
        
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_array = np.array(image)
        
        result = RasterValidator.validate_image(image_array)
        
        return {
            "valid": result.valid,
            "status": result.status.value,
            "metadata": result.metadata,
            "issues": result.issues,
            "warnings": result.warnings
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Imagery validation failed: {str(e)}"}
        )


@app.post("/api/gis/studio/validate/footprints")
async def validate_building_footprints(polygons: List[List[List[float]]]):
    """
    Validate building footprint polygons
    - Polygons: List of polygon coordinates [[x,y], [x,y], ...]
    """
    try:
        import numpy as np
        polygon_arrays = [np.array(poly) for poly in polygons]
        
        result = VectorValidator.validate_building_footprints(polygon_arrays)
        
        return {
            "valid": result.valid,
            "status": result.status.value,
            "metadata": result.metadata,
            "issues": result.issues,
            "warnings": result.warnings
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Footprint validation failed: {str(e)}"}
        )


@app.post("/api/gis/studio/integrate/terrain")
async def analyze_terrain(
    dem: List[List[float]],
    points: Optional[List[List[float]]] = None
):
    """
    Analyze terrain surface characteristics
    - DEM: Digital Elevation Model (2D grid)
    - Points: Optional LiDAR point cloud
    """
    try:
        import numpy as np
        dem_array = np.array(dem)
        points_array = np.array(points) if points else None
        
        result = gis_integrator.analyze_terrain_surface(dem_array, points_array)
        
        return {
            "terrain_stats": result.get("terrain_stats", {}),
            "classification": result.get("terrain_classification", {}),
            "analysis_complete": True
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Terrain analysis failed: {str(e)}"}
        )


@app.post("/api/gis/studio/integrate/magnetic")
async def correlate_magnetic_terrain(
    magnetic_data: List[List[float]],
    dem_data: List[List[float]]
):
    """
    Correlate magnetic anomalies with terrain
    - Magnetic data: 2D grid of magnetic field values (nT)
    - DEM data: Digital Elevation Model
    """
    try:
        import numpy as np
        magnetic_array = np.array(magnetic_data)
        dem_array = np.array(dem_data)
        
        result = gis_integrator.correlate_magnetic_terrain(magnetic_array, dem_array)
        
        return {
            "correlation": result.get("correlation", 0.0),
            "anomalies": result.get("anomalies", []),
            "subsurface_inference": result.get("subsurface_inference", {})
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Magnetic correlation failed: {str(e)}"}
        )


@app.post("/api/gis/studio/integrate/resistivity")
async def integrate_resistivity_depth(
    resistivity_data: List[List[List[float]]],
    dem_data: List[List[float]]
):
    """
    Integrate resistivity depth profiles with surface topography
    - Resistivity data: 3D array (x, y, depth)
    - DEM data: Digital Elevation Model
    """
    try:
        import numpy as np
        resistivity_array = np.array(resistivity_data)
        dem_array = np.array(dem_data)
        
        result = gis_integrator.integrate_resistivity_depth(resistivity_array, dem_array)
        
        return {
            "layer_analysis": result.get("layer_analysis", []),
            "conductive_zones": result.get("conductive_zones", []),
            "depth_profile": result.get("depth_profile", {})
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Resistivity integration failed: {str(e)}"}
        )


@app.post("/api/gis/studio/integrate/seismic")
async def analyze_seismic_structure(
    seismic_data: List[List[List[float]]],
    dem_data: List[List[float]]
):
    """
    Analyze seismic structural features
    - Seismic data: 3D array of seismic velocities
    - DEM data: Digital Elevation Model
    """
    try:
        import numpy as np
        seismic_array = np.array(seismic_data)
        dem_array = np.array(dem_data)
        
        result = gis_integrator.analyze_seismic_structure(seismic_array, dem_array)
        
        return {
            "discontinuities": result.get("discontinuities", []),
            "faults": result.get("faults", []),
            "complexity": result.get("complexity", 0.0),
            "structural_interpretation": result.get("structural_interpretation", {})
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Seismic analysis failed: {str(e)}"}
        )


@app.post("/api/gis/studio/train/terrain")
async def train_terrain_classifier(
    features: List[List[float]],
    labels: List[int]
):
    """
    Train terrain classification model
    - Features: Training feature vectors
    - Labels: Terrain class labels
    """
    try:
        import numpy as np
        X = np.array(features)
        y = np.array(labels)
        
        gis_trainer.train_terrain_classifier(X, y)
        
        return {
            "model_trained": True,
            "samples": len(X),
            "classes": len(np.unique(y)),
            "model_type": "terrain_classifier"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Terrain classifier training failed: {str(e)}"}
        )


@app.post("/api/gis/studio/train/depth")
async def train_depth_predictor(
    features: List[List[float]],
    depths: List[float]
):
    """
    Train subsurface depth prediction model
    - Features: Geophysical feature vectors
    - Depths: Target depth values (meters)
    """
    try:
        import numpy as np
        X = np.array(features)
        y = np.array(depths)
        
        gis_trainer.train_depth_predictor(X, y)
        
        return {
            "model_trained": True,
            "samples": len(X),
            "depth_range": {
                "min": float(y.min()),
                "max": float(y.max()),
                "mean": float(y.mean())
            },
            "model_type": "depth_predictor"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Depth predictor training failed: {str(e)}"}
        )


@app.post("/api/gis/studio/train/lithology")
async def train_lithology_classifier(
    features: List[List[float]],
    rock_types: List[int]
):
    """
    Train lithology (rock type) classification model
    - Features: Multi-modal geophysical features
    - Rock types: Lithology class labels
    """
    try:
        import numpy as np
        X = np.array(features)
        y = np.array(rock_types)
        
        gis_trainer.train_lithology_classifier(X, y)
        
        return {
            "model_trained": True,
            "samples": len(X),
            "rock_types": len(np.unique(y)),
            "model_type": "lithology_classifier"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Lithology classifier training failed: {str(e)}"}
        )


@app.post("/api/gis/studio/predict")
async def make_prediction(
    model_type: str,
    features: List[List[float]]
):
    """
    Make predictions using trained models
    - model_type: terrain_classifier, depth_predictor, or lithology_classifier
    - features: Feature vectors for prediction
    """
    try:
        import numpy as np
        X = np.array(features)
        
        model = gis_trainer.models.get(model_type)
        if not model:
            return JSONResponse(
                status_code=404,
                content={"error": f"Model '{model_type}' not found. Train it first."}
            )
        
        predictions = model.predict(X)
        
        return {
            "model_type": model_type,
            "num_predictions": len(predictions),
            "predictions": predictions.tolist()
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Prediction failed: {str(e)}"}
        )


@app.post("/api/gis/studio/improve/feedback")
async def submit_feedback(
    prediction_id: str,
    predicted_value: List[float],
    ground_truth: List[float],
    confidence: float,
    user_notes: str = ""
):
    """
    Submit feedback for continuous improvement
    - prediction_id: Unique identifier for the prediction
    - predicted_value: Model's prediction
    - ground_truth: Actual correct value
    - confidence: Model confidence (0-1)
    - user_notes: Optional feedback notes
    """
    try:
        import numpy as np
        
        gis_improvement.collect_feedback(
            prediction_id=prediction_id,
            predicted_value=np.array(predicted_value),
            ground_truth=np.array(ground_truth),
            confidence=confidence,
            user_notes=user_notes
        )
        
        return {
            "feedback_recorded": True,
            "prediction_id": prediction_id
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Feedback submission failed: {str(e)}"}
        )


@app.get("/api/gis/studio/improve/analysis")
async def get_feedback_analysis(lookback_hours: int = 24):
    """
    Get feedback analysis and improvement insights
    - lookback_hours: Hours to look back for analysis
    """
    try:
        analysis = gis_improvement.analyze_feedback(lookback_hours=lookback_hours)
        
        return {
            "analysis": analysis,
            "lookback_hours": lookback_hours
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Analysis failed: {str(e)}"}
        )


@app.get("/api/gis/studio/improve/diagnostics")
async def run_model_diagnostics():
    """
    Run comprehensive model diagnostics
    """
    try:
        diagnostics = gis_improvement.run_diagnostics()
        
        return {
            "diagnostics": diagnostics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Diagnostics failed: {str(e)}"}
        )


@app.get("/api/gis/studio/status")
async def get_gis_studio_status():
    """
    Get complete GIS Studio system status
    """
    try:
        return {
            "gis_studio": {
                "status": "operational",
                "version": "1.0.0",
                "modules": {
                    "validator": {
                        "status": "ready",
                        "capabilities": ["lidar", "dem", "imagery", "footprints"]
                    },
                    "integrator": {
                        "status": "ready",
                        "capabilities": ["terrain", "magnetic", "resistivity", "seismic", "multi-modal"]
                    },
                    "trainer": {
                        "status": "ready",
                        "models_loaded": list(gis_trainer.models.keys()),
                        "capabilities": ["terrain_classification", "depth_prediction", "lithology_classification"]
                    },
                    "improvement": {
                        "status": "ready",
                        "feedback_count": len(gis_improvement.feedback_history),
                        "capabilities": ["feedback_collection", "performance_tracking", "model_diagnostics"]
                    }
                },
                "endpoints": {
                    "validation": 4,
                    "integration": 4,
                    "training": 4,
                    "improvement": 3,
                    "total": 15
                }
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Status check failed: {str(e)}"}
        )
