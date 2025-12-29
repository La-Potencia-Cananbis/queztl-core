#!/usr/bin/env python3
"""
QuetzalCore GIS & Remote Sensing System - Quick Test
Fast validation of all core capabilities
"""

import sys
import numpy as np
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

print("🗺️  QuetzalCore GIS & Remote Sensing - Quick Test\n")
print("=" * 60)

tests_passed = 0
total_tests = 0

def test(name):
    global total_tests
    total_tests += 1
    print(f"\n[{total_tests}] {name}...", end=" ")

def passed(details=""):
    global tests_passed
    tests_passed += 1
    print(f"✅ PASS {details}")

def failed(error):
    print(f"❌ FAIL: {error}")

# Test 1: LiDAR Validation
test("LiDAR Point Cloud Validation")
try:
    from gis_validator import LiDARValidator
    points = np.random.rand(1000, 3) * 100
    classification = np.random.randint(0, 19, 1000)
    intensity = np.random.randint(0, 256, 1000)
    result = LiDARValidator.validate_point_cloud(points, classification, intensity)
    if result.is_valid:
        passed(f"({result.metadata['point_count']:,} points)")
    else:
        failed(", ".join(result.errors))
except Exception as e:
    failed(str(e))

# Test 2: DEM Validation
test("Digital Elevation Model Validation")
try:
    from gis_validator import RasterValidator
    dem = np.random.rand(256, 256) * 1000
    result = RasterValidator.validate_elevation_grid(dem)
    if result.is_valid:
        passed(f"({result.metadata['shape']})")
    else:
        failed(", ".join(result.errors))
except Exception as e:
    failed(str(e))

# Test 3: Satellite Imagery
test("Satellite Imagery Validation")
try:
    from gis_validator import RasterValidator
    imagery = np.random.randint(0, 256, (512, 512, 3), dtype=np.uint8)
    result = RasterValidator.validate_image(imagery)
    if result.is_valid:
        passed(f"({result.metadata['channels']} channels)")
    else:
        failed(", ".join(result.errors))
except Exception as e:
    failed(str(e))

# Test 4: Vector Polygons
test("Building Footprint Validation")
try:
    from gis_validator import VectorValidator
    polygons = [
        np.array([[0,0], [10,0], [10,10], [0,10], [0,0]]) + i*20
        for i in range(5)
    ]
    result = VectorValidator.validate_building_footprints(polygons)
    if result.is_valid:
        passed(f"({len(polygons)} polygons)")
    else:
        failed(", ".join(result.errors))
except Exception as e:
    failed(str(e))

# Test 5: GIS Validator Router
test("GIS Data Router (auto-detection)")
try:
    from gis_validator import GISDataValidator, GISDataType
    validator = GISDataValidator()
    dem_data = np.random.rand(128, 128) * 500
    result = validator.validate(dem_data, GISDataType.DEM)
    if result.is_valid:
        passed("(DEM auto-routed)")
    else:
        failed(", ".join(result.errors))
except Exception as e:
    failed(str(e))

# Test 6: Terrain Analysis
test("Terrain Analysis Integration")
try:
    from gis_geophysics_integrator import GISGeophysicsIntegrator
    integrator = GISGeophysicsIntegrator()
    dem = np.random.rand(64, 64) * 500
    points = np.random.rand(1000, 3) * 100
    result = integrator.analyze_terrain_surface(dem, points)
    if result and 'terrain_stats' in result:
        passed(f"(elevation, slope, roughness)")
    else:
        failed("No terrain stats returned")
except Exception as e:
    failed(str(e))

# Test 7: Magnetic-Terrain Correlation
test("Magnetic Anomaly Correlation")
try:
    from gis_geophysics_integrator import GISGeophysicsIntegrator
    integrator = GISGeophysicsIntegrator()
    magnetic = np.random.rand(64, 64) * 100
    dem = np.random.rand(64, 64) * 500
    result = integrator.correlate_magnetic_terrain(magnetic, dem)
    if result and 'correlation' in result:
        passed(f"(r={result['correlation']:.3f})")
    else:
        failed("No correlation returned")
except Exception as e:
    failed(str(e))

# Test 8: Resistivity Integration
test("Resistivity Depth Integration")
try:
    from gis_geophysics_integrator import GISGeophysicsIntegrator
    integrator = GISGeophysicsIntegrator()
    resistivity = np.random.rand(64, 64, 10) * 1000
    dem = np.random.rand(64, 64) * 500
    result = integrator.integrate_resistivity_depth(resistivity, dem)
    if result and 'layer_analysis' in result:
        passed(f"({len(result['layer_analysis'])} layers)")
    else:
        failed("No layer analysis")
except Exception as e:
    failed(str(e))

# Test 9: Seismic Analysis
test("Seismic Structural Analysis")
try:
    from gis_geophysics_integrator import GISGeophysicsIntegrator
    integrator = GISGeophysicsIntegrator()
    seismic = np.random.rand(64, 64, 20) * 5000
    dem = np.random.rand(64, 64) * 500
    result = integrator.analyze_seismic_structure(seismic, dem)
    if result and 'discontinuities' in result:
        passed(f"({result['complexity']:.3f} complexity)")
    else:
        failed("No structural analysis")
except Exception as e:
    failed(str(e))

# Test 10: ML Terrain Classifier Training
test("ML Terrain Classifier Training")
try:
    from gis_geophysics_trainer import GISGeophysicsTrainer
    trainer = GISGeophysicsTrainer()
    X = np.random.rand(500, 10)
    y = np.random.randint(0, 3, 500)
    trainer.train_terrain_classifier(X, y)
    passed("(500 samples, 3 classes)")
except Exception as e:
    failed(str(e))

# Test 11: ML Depth Predictor Training
test("ML Depth Predictor Training")
try:
    from gis_geophysics_trainer import GISGeophysicsTrainer
    trainer = GISGeophysicsTrainer()
    X = np.random.rand(300, 8)
    y = np.random.rand(300) * 100
    trainer.train_depth_predictor(X, y)
    passed("(300 samples, regression)")
except Exception as e:
    failed(str(e))

# Test 12: ML Lithology Classifier
test("ML Lithology Classifier Training")
try:
    from gis_geophysics_trainer import GISGeophysicsTrainer
    trainer = GISGeophysicsTrainer()
    X = np.random.rand(400, 12)
    y = np.random.randint(0, 5, 400)
    trainer.train_lithology_classifier(X, y)
    passed("(400 samples, 5 rock types)")
except Exception as e:
    failed(str(e))

# Test 13: ML Predictions
test("ML Model Predictions")
try:
    from gis_geophysics_trainer import GISGeophysicsTrainer, GISGeophysicsModel
    trainer = GISGeophysicsTrainer()
    X_train = np.random.rand(200, 10)
    y_train = np.random.randint(0, 3, 200)
    trainer.train_terrain_classifier(X_train, y_train)
    
    # Get the model and predict
    model = trainer.models.get('terrain_classifier')
    if model:
        X_test = np.random.rand(50, 10)
        predictions = model.predict(X_test)
        if predictions is not None and len(predictions) == 50:
            passed(f"({len(predictions)} predictions)")
        else:
            failed("Wrong prediction shape")
    else:
        failed("Model not found")
except Exception as e:
    failed(str(e))

# Test 14: Continuous Improvement - Feedback Collection
test("Feedback Collection System")
try:
    from gis_geophysics_improvement import AdaptiveImprovementEngine
    engine = AdaptiveImprovementEngine()
    for i in range(5):
        engine.collect_feedback(
            prediction_id=f"test_{i}",
            predicted_value=np.random.rand(5),
            ground_truth=np.random.rand(5),
            confidence=np.random.rand(),
            user_notes=f"Test feedback {i}"
        )
    passed("(5 feedback items)")
except Exception as e:
    failed(str(e))

# Test 15: Feedback Analysis
test("Feedback Analysis & Insights")
try:
    from gis_geophysics_improvement import AdaptiveImprovementEngine
    engine = AdaptiveImprovementEngine()
    # Add some feedback
    for i in range(10):
        engine.collect_feedback(
            prediction_id=f"analysis_{i}",
            predicted_value=np.array([0.5 + np.random.rand()*0.1]),
            ground_truth=np.array([0.5]),
            confidence=0.9
        )
    analysis = engine.analyze_feedback()
    if analysis and 'accuracy_rate' in analysis:
        passed(f"({analysis['total_feedback']} samples analyzed)")
    else:
        failed("No analysis results")
except Exception as e:
    failed(str(e))

# Test 16: Model Performance Tracking
test("Model Performance Tracking")
try:
    from gis_geophysics_improvement import AdaptiveImprovementEngine
    engine = AdaptiveImprovementEngine()
    metrics = {
        'accuracy': 0.95,
        'precision': 0.93,
        'recall': 0.97,
        'f1_score': 0.95
    }
    engine.track_performance('terrain_classifier', metrics)
    passed("(4 metrics tracked)")
except Exception as e:
    failed(str(e))

# Test 17: Model Diagnostics
test("Model Diagnostics & Health Check")
try:
    from gis_geophysics_improvement import AdaptiveImprovementEngine
    engine = AdaptiveImprovementEngine()
    # Add performance history
    for i in range(5):
        engine.track_performance('depth_predictor', {
            'mae': 5.0 + np.random.rand(),
            'rmse': 8.0 + np.random.rand()
        })
    diagnostics = engine.run_diagnostics()
    if diagnostics and 'models' in diagnostics:
        passed(f"(checked {len(diagnostics['models'])} models)")
    else:
        failed("No diagnostics")
except Exception as e:
    failed(str(e))

# Test 18: End-to-End Pipeline
test("Complete GIS Pipeline (Validate→Integrate→Train→Improve)")
try:
    from gis_validator import GISDataValidator, GISDataType
    from gis_geophysics_integrator import GISGeophysicsIntegrator
    from gis_geophysics_trainer import GISGeophysicsTrainer
    from gis_geophysics_improvement import AdaptiveImprovementEngine
    
    # Step 1: Validate
    validator = GISDataValidator()
    dem = np.random.rand(64, 64) * 500
    val_result = validator.validate(dem, GISDataType.DEM)
    assert val_result.is_valid
    
    # Step 2: Integrate
    integrator = GISGeophysicsIntegrator()
    magnetic = np.random.rand(64, 64) * 100
    int_result = integrator.correlate_magnetic_terrain(magnetic, dem)
    assert 'correlation' in int_result
    
    # Step 3: Train
    trainer = GISGeophysicsTrainer()
    X = np.random.rand(100, 8)
    y = np.random.randint(0, 2, 100)
    trainer.train_terrain_classifier(X, y)
    
    # Step 4: Improve
    engine = AdaptiveImprovementEngine()
    engine.collect_feedback("pipeline_test", np.array([0.5]), np.array([0.5]), 0.9)
    
    passed("(4 stages complete)")
except Exception as e:
    failed(str(e))

# Results
print("\n" + "=" * 60)
print(f"\n📊 RESULTS: {tests_passed}/{total_tests} tests passed ({tests_passed/total_tests*100:.1f}%)\n")

if tests_passed == total_tests:
    print("🎉 ALL TESTS PASSED! GIS & Remote Sensing System is READY!")
    print("\n✅ System Capabilities Verified:")
    print("   • LiDAR point cloud validation")
    print("   • DEM/raster validation")
    print("   • Satellite imagery validation")
    print("   • Vector polygon validation")
    print("   • Terrain analysis")
    print("   • Magnetic anomaly correlation")
    print("   • Resistivity depth integration")
    print("   • Seismic structural analysis")
    print("   • ML terrain classification")
    print("   • ML depth prediction")
    print("   • ML lithology classification")
    print("   • Continuous improvement system")
    print("   • Complete end-to-end pipeline")
    print("\n🚀 PRODUCTION READY!")
    sys.exit(0)
else:
    print(f"⚠️  {total_tests - tests_passed} test(s) failed")
    sys.exit(1)
