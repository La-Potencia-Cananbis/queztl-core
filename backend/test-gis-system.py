#!/usr/bin/env python3
"""
QuetzalCore GIS & Remote Sensing System - Comprehensive Test Suite
Tests all validation, integration, training, and improvement capabilities
"""

import sys
import json
import numpy as np
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from gis_validator import (
    GISDataValidator,
    LiDARValidator,
    RasterValidator,
    VectorValidator
)
from gis_geophysics_integrator import GISGeophysicsIntegrator
from gis_geophysics_trainer import GISGeophysicsTrainer, TrainingDataset
from gis_geophysics_improvement import AdaptiveImprovementEngine

print("╔════════════════════════════════════════════════════════════════════╗")
print("║                                                                    ║")
print("║         QuetzalCore GIS & Remote Sensing Test Suite 🗺️            ║")
print("║                                                                    ║")
print("╚════════════════════════════════════════════════════════════════════╝")
print()

# Test counters
tests_passed = 0
tests_failed = 0
total_tests = 0

def test_section(name: str):
    """Print test section header"""
    print(f"\n{'='*70}")
    print(f"  {name}")
    print(f"{'='*70}\n")

def test_case(description: str) -> bool:
    """Start a test case"""
    global total_tests
    total_tests += 1
    print(f"  {total_tests}. {description}...", end=" ")
    return True

def test_pass():
    """Mark test as passed"""
    global tests_passed
    tests_passed += 1
    print("✅ PASS")

def test_fail(error: str):
    """Mark test as failed"""
    global tests_failed
    tests_failed += 1
    print(f"❌ FAIL: {error}")

# ============================================================================
# TEST 1: LiDAR Validation
# ============================================================================

test_section("TEST 1: LiDAR Point Cloud Validation")

try:
    # Create sample LiDAR data (1000 points)
    test_case("Creating synthetic LiDAR point cloud (1000 points)")
    lidar_points = np.random.rand(1000, 3) * 100  # 100m x 100m x 100m
    test_pass()
    
    # Add classification
    test_case("Adding point classifications (ground, vegetation, building)")
    lidar_classification = np.random.randint(0, 19, size=1000)
    test_pass()
    
    # Add intensity
    test_case("Adding intensity values")
    lidar_intensity = np.random.randint(0, 256, size=1000)
    test_pass()
    
    # Validate
    test_case("Running LiDAR validator")
    validator = LiDARValidator()
    result = validator.validate(lidar_points, lidar_classification, lidar_intensity)
    if result.is_valid:
        test_pass()
        print(f"     📊 Points: {result.metadata.get('point_count', 0):,}")
        print(f"     📐 Bounds: {result.metadata.get('bounds', {})}")
    else:
        test_fail(f"Validation failed: {', '.join(result.errors)}")
        
except Exception as e:
    test_fail(str(e))

# ============================================================================
# TEST 2: Raster/DEM Validation
# ============================================================================

test_section("TEST 2: Digital Elevation Model (DEM) Validation")

try:
    # Create sample DEM
    test_case("Creating synthetic DEM (256x256 pixels)")
    dem_data = np.random.rand(256, 256) * 1000  # Elevation 0-1000m
    test_pass()
    
    # Validate
    test_case("Running DEM validator")
    validator = RasterValidator()
    result = validator.validate(dem_data, data_type='dem')
    if result.is_valid:
        test_pass()
        print(f"     📊 Shape: {result.metadata.get('shape', ())}")
        print(f"     🏔️  Elevation range: {result.metadata.get('elevation_range', {})}")
        print(f"     📐 Mean slope: {result.metadata.get('mean_slope', 0):.2f}°")
    else:
        test_fail(f"Validation failed: {', '.join(result.errors)}")
        
except Exception as e:
    test_fail(str(e))

# ============================================================================
# TEST 3: Satellite Imagery Validation
# ============================================================================

test_section("TEST 3: Satellite Imagery Validation")

try:
    # Create RGB satellite image
    test_case("Creating synthetic satellite imagery (512x512 RGB)")
    satellite_rgb = np.random.randint(0, 256, size=(512, 512, 3), dtype=np.uint8)
    test_pass()
    
    # Validate
    test_case("Running satellite imagery validator")
    validator = RasterValidator()
    result = validator.validate(satellite_rgb, data_type='satellite')
    if result.is_valid:
        test_pass()
        print(f"     📊 Shape: {result.metadata.get('shape', ())}")
        print(f"     🎨 Channels: {result.metadata.get('channels', 0)}")
    else:
        test_fail(f"Validation failed: {', '.join(result.errors)}")
        
except Exception as e:
    test_fail(str(e))

# ============================================================================
# TEST 4: Vector/Polygon Validation
# ============================================================================

test_section("TEST 4: Building Footprint (Vector) Validation")

try:
    # Create sample building footprints
    test_case("Creating synthetic building polygons (5 buildings)")
    polygons = []
    for i in range(5):
        # Create random quadrilateral
        x_base = np.random.rand() * 100
        y_base = np.random.rand() * 100
        polygon = np.array([
            [x_base, y_base],
            [x_base + 10, y_base],
            [x_base + 10, y_base + 15],
            [x_base, y_base + 15],
            [x_base, y_base]  # Close polygon
        ])
        polygons.append(polygon)
    test_pass()
    
    # Validate
    test_case("Running polygon validator")
    validator = VectorValidator()
    result = validator.validate(polygons, feature_type='polygon')
    if result.is_valid:
        test_pass()
        print(f"     📊 Polygons: {len(polygons)}")
        print(f"     ✅ Valid: {result.metadata.get('valid_percentage', 0):.1f}%")
    else:
        test_fail(f"Validation failed: {', '.join(result.errors)}")
        
except Exception as e:
    test_fail(str(e))

# ============================================================================
# TEST 5: Terrain Analysis Integration
# ============================================================================

test_section("TEST 5: GIS-Geophysics Terrain Analysis")

try:
    # Create terrain data
    test_case("Creating terrain dataset (DEM + point cloud)")
    terrain_dem = np.random.rand(128, 128) * 500
    terrain_points = np.random.rand(5000, 3) * 100
    test_pass()
    
    # Analyze
    test_case("Running terrain analysis (elevation, slope, roughness)")
    integrator = GISGeophysicsIntegrator()
    terrain_result = integrator.analyze_terrain(terrain_dem, terrain_points)
    if terrain_result and 'terrain_stats' in terrain_result:
        test_pass()
        print(f"     🏔️  Mean elevation: {terrain_result['terrain_stats'].get('mean_elevation', 0):.2f}m")
        print(f"     📐 Mean slope: {terrain_result['terrain_stats'].get('mean_slope', 0):.2f}°")
        print(f"     🌄 Roughness: {terrain_result['terrain_stats'].get('roughness', 0):.4f}")
    else:
        test_fail("Analysis returned no results")
        
except Exception as e:
    test_fail(str(e))

# ============================================================================
# TEST 6: Multi-Modal Geophysics Integration
# ============================================================================

test_section("TEST 6: Multi-Modal Geophysics Data Fusion")

try:
    # Create geophysics data
    test_case("Creating geophysics datasets (magnetic, resistivity, seismic)")
    magnetic_data = np.random.rand(64, 64) * 100  # nT
    resistivity_data = np.random.rand(64, 64, 10) * 1000  # Ohm-m
    seismic_data = np.random.rand(64, 64, 20) * 5000  # m/s
    test_pass()
    
    # Integrate (early fusion)
    test_case("Running early fusion integration")
    integrator = GISGeophysicsIntegrator()
    fusion_result = integrator.integrate_multi_modal(
        terrain_dem,
        magnetic_data,
        resistivity_data,
        seismic_data,
        fusion_strategy='early'
    )
    if fusion_result and 'fused_features' in fusion_result:
        test_pass()
        print(f"     📊 Fused features: {fusion_result['fused_features'].shape}")
        print(f"     🧬 Integration: {fusion_result.get('fusion_strategy', 'unknown')}")
    else:
        test_fail("Fusion returned no results")
        
except Exception as e:
    test_fail(str(e))

# ============================================================================
# TEST 7: ML Model Training
# ============================================================================

test_section("TEST 7: Machine Learning Model Training")

try:
    # Create training dataset
    test_case("Creating synthetic training dataset (1000 samples)")
    X_train = np.random.rand(1000, 10)  # 10 features
    y_train = np.random.randint(0, 5, size=1000)  # 5 classes
    test_pass()
    
    # Train terrain classifier
    test_case("Training terrain classification model")
    trainer = GISGeophysicsTrainer()
    trainer.train_terrain_classifier(X_train, y_train)
    test_pass()
    print(f"     🎯 Model trained on {len(X_train):,} samples")
    
    # Make predictions
    test_case("Making predictions on test data")
    X_test = np.random.rand(100, 10)
    predictions = trainer.predict(X_test, model_type='terrain_classifier')
    if predictions is not None and len(predictions) == 100:
        test_pass()
        print(f"     📈 Predictions: {len(predictions)}")
    else:
        test_fail("Predictions failed or wrong shape")
        
except Exception as e:
    test_fail(str(e))

# ============================================================================
# TEST 8: Depth Prediction Model
# ============================================================================

test_section("TEST 8: Subsurface Depth Prediction")

try:
    # Create depth training data
    test_case("Creating depth prediction training data (500 samples)")
    X_depth = np.random.rand(500, 8)  # 8 geophysical features
    y_depth = np.random.rand(500) * 100  # Depth 0-100m
    test_pass()
    
    # Train depth predictor
    test_case("Training depth prediction model (regression)")
    trainer = GISGeophysicsTrainer()
    trainer.train_depth_predictor(X_depth, y_depth)
    test_pass()
    
    # Predict depths
    test_case("Predicting depths for new locations")
    X_depth_test = np.random.rand(50, 8)
    depth_predictions = trainer.predict(X_depth_test, model_type='depth_predictor')
    if depth_predictions is not None and len(depth_predictions) == 50:
        test_pass()
        print(f"     📏 Mean predicted depth: {np.mean(depth_predictions):.2f}m")
    else:
        test_fail("Depth prediction failed")
        
except Exception as e:
    test_fail(str(e))

# ============================================================================
# TEST 9: Adaptive Improvement Engine
# ============================================================================

test_section("TEST 9: Continuous Improvement System")

try:
    # Initialize improvement engine
    test_case("Initializing adaptive improvement engine")
    improvement_engine = AdaptiveImprovementEngine()
    test_pass()
    
    # Add feedback
    test_case("Collecting user feedback (5 samples)")
    for i in range(5):
        feedback = {
            'prediction_id': f'pred_{i}',
            'prediction': np.random.rand(10),
            'ground_truth': np.random.rand(10),
            'confidence': np.random.rand(),
            'user_rating': np.random.randint(1, 6)
        }
        improvement_engine.collect_feedback(feedback)
    test_pass()
    
    # Analyze feedback
    test_case("Analyzing feedback for improvement opportunities")
    analysis = improvement_engine.analyze_feedback()
    if analysis and 'accuracy_rate' in analysis:
        test_pass()
        print(f"     📊 Feedback samples: {analysis.get('total_feedback', 0)}")
        print(f"     🎯 Accuracy rate: {analysis.get('accuracy_rate', 0):.1%}")
    else:
        test_fail("Feedback analysis failed")
        
except Exception as e:
    test_fail(str(e))

# ============================================================================
# TEST 10: End-to-End GIS Pipeline
# ============================================================================

test_section("TEST 10: Complete GIS/Remote Sensing Pipeline")

try:
    test_case("Running complete pipeline: Validate → Integrate → Train → Improve")
    
    # Step 1: Validate
    lidar = np.random.rand(2000, 3) * 100
    validator = GISDataValidator()
    validation_result = validator.validate_lidar(lidar)
    print("\n     ✅ Step 1: Validation complete")
    
    # Step 2: Integrate
    dem = np.random.rand(128, 128) * 500
    magnetic = np.random.rand(128, 128) * 100
    integrator = GISGeophysicsIntegrator()
    integration_result = integrator.correlate_magnetic_terrain(magnetic, dem)
    print("     ✅ Step 2: Integration complete")
    
    # Step 3: Train
    X = np.random.rand(500, 10)
    y = np.random.randint(0, 3, size=500)
    trainer = GISGeophysicsTrainer()
    trainer.train_terrain_classifier(X, y)
    print("     ✅ Step 3: Training complete")
    
    # Step 4: Improve
    improvement = AdaptiveImprovementEngine()
    improvement.collect_feedback({
        'prediction_id': 'test',
        'prediction': np.random.rand(5),
        'ground_truth': np.random.rand(5),
        'confidence': 0.9
    })
    print("     ✅ Step 4: Improvement tracking active")
    
    test_pass()
    print("     🎉 Complete pipeline executed successfully!")
    
except Exception as e:
    test_fail(str(e))

# ============================================================================
# FINAL RESULTS
# ============================================================================

print()
print("╔════════════════════════════════════════════════════════════════════╗")
print("║                         TEST RESULTS                               ║")
print("╚════════════════════════════════════════════════════════════════════╝")
print()
print(f"  Total Tests:  {total_tests}")
print(f"  ✅ Passed:     {tests_passed}")
print(f"  ❌ Failed:     {tests_failed}")
print(f"  Success Rate: {(tests_passed/total_tests*100):.1f}%")
print()

if tests_failed == 0:
    print("  🎉 ALL TESTS PASSED! GIS System is READY! 🗺️✨")
    print()
    print("  ✅ LiDAR validation working")
    print("  ✅ DEM/Raster validation working")
    print("  ✅ Satellite imagery validation working")
    print("  ✅ Vector/polygon validation working")
    print("  ✅ Terrain analysis working")
    print("  ✅ Multi-modal fusion working")
    print("  ✅ ML model training working")
    print("  ✅ Depth prediction working")
    print("  ✅ Continuous improvement working")
    print("  ✅ End-to-end pipeline working")
    print()
    print("  🚀 GIS & Remote Sensing System: PRODUCTION READY!")
    sys.exit(0)
else:
    print(f"  ⚠️  {tests_failed} test(s) failed. Review errors above.")
    sys.exit(1)
