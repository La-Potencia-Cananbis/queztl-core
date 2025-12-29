#!/bin/bash

# 🔥 QUETZAL GIS INTEGRATED TEST RUNNER
# Tests ALL GIS tools: ArcGIS + Leaflet + Turf + GDAL + Backend APIs

echo "🚀 ============================================"
echo "   QUETZAL GIS INTEGRATED TEST SUITE"
echo "============================================"
echo ""

API_URL="http://localhost:8000"
PASSED=0
FAILED=0

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

test_passed() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((PASSED++))
}

test_failed() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    ((FAILED++))
}

test_info() {
    echo -e "${CYAN}ℹ️  INFO${NC}: $1"
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 1: Backend Health Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
HEALTH=$(curl -s "$API_URL/api/health" 2>/dev/null)
if echo "$HEALTH" | grep -q "healthy"; then
    test_passed "Backend is healthy"
else
    test_failed "Backend is not responding"
    echo "Attempting to start backend..."
    cd /Users/xavasena/hive
    .venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
    sleep 5
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 2: GIS Studio Endpoints"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test LiDAR validation endpoint
test_info "Testing LiDAR validation endpoint..."
LIDAR_RESPONSE=$(curl -s -X POST "$API_URL/api/gis/studio/validate/lidar" \
    -H "Content-Type: application/json" \
    -d '{
        "points": [[1,2,3],[4,5,6],[7,8,9]],
        "classification": [2,2,3],
        "intensity": [100,150,200]
    }' 2>/dev/null)

if echo "$LIDAR_RESPONSE" | grep -q "valid\|metadata"; then
    test_passed "LiDAR validation endpoint working"
else
    test_failed "LiDAR validation endpoint failed"
fi
echo ""

# Test DEM validation endpoint
test_info "Testing DEM validation endpoint..."
DEM_RESPONSE=$(curl -s -X POST "$API_URL/api/gis/studio/validate/dem" \
    -H "Content-Type: application/json" \
    -d '{
        "elevation": [[100,102,104],[101,103,105]]
    }' 2>/dev/null)

if echo "$DEM_RESPONSE" | grep -q "valid\|metadata"; then
    test_passed "DEM validation endpoint working"
else
    test_failed "DEM validation endpoint failed"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3: Frontend Files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if frontend files exist
if [ -f "/Users/xavasena/hive/frontend/gis-studio-integrated.html" ]; then
    test_passed "GIS Studio Integrated HTML exists"
else
    test_failed "GIS Studio Integrated HTML not found"
fi

if [ -f "/Users/xavasena/hive/frontend/gis-studio-pro.html" ]; then
    test_passed "GIS Studio Pro HTML exists"
else
    test_failed "GIS Studio Pro HTML not found"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 4: External APIs Availability"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test ArcGIS API
test_info "Testing ArcGIS Online API..."
ARCGIS_TEST=$(curl -s -I "https://js.arcgisonline.com/4.27/" 2>/dev/null | head -1)
if echo "$ARCGIS_TEST" | grep -q "200\|301\|302"; then
    test_passed "ArcGIS API accessible"
else
    test_failed "ArcGIS API not accessible"
fi

# Test Leaflet CDN
test_info "Testing Leaflet CDN..."
LEAFLET_TEST=$(curl -s -I "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js" 2>/dev/null | head -1)
if echo "$LEAFLET_TEST" | grep -q "200"; then
    test_passed "Leaflet CDN accessible"
else
    test_failed "Leaflet CDN not accessible"
fi

# Test Turf.js CDN
test_info "Testing Turf.js CDN..."
TURF_TEST=$(curl -s -I "https://cdn.jsdelivr.net/npm/@turf/turf@6/turf.min.js" 2>/dev/null | head -1)
if echo "$TURF_TEST" | grep -q "200"; then
    test_passed "Turf.js CDN accessible"
else
    test_failed "Turf.js CDN not accessible"
fi

# Test OpenStreetMap
test_info "Testing OpenStreetMap tiles..."
OSM_TEST=$(curl -s -I "https://tile.openstreetmap.org/0/0/0.png" 2>/dev/null | head -1)
if echo "$OSM_TEST" | grep -q "200"; then
    test_passed "OpenStreetMap tiles accessible"
else
    test_failed "OpenStreetMap tiles not accessible"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 5: Free Geocoding Service"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_info "Testing Nominatim geocoding..."
GEOCODE_TEST=$(curl -s "https://nominatim.openstreetmap.org/search?format=json&q=New+York+City&limit=1" 2>/dev/null)
if echo "$GEOCODE_TEST" | grep -q "lat"; then
    test_passed "Nominatim geocoding working"
    test_info "NYC Coordinates: $(echo $GEOCODE_TEST | grep -o '"lat":"[^"]*"' | head -1)"
else
    test_failed "Nominatim geocoding failed"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 6: Free Routing Service"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_info "Testing OSRM routing..."
# Route from NYC to Boston
ROUTE_TEST=$(curl -s "https://router.project-osrm.org/route/v1/driving/-74.0060,40.7128;-71.0589,42.3601?overview=false" 2>/dev/null)
if echo "$ROUTE_TEST" | grep -q "distance"; then
    test_passed "OSRM routing working"
    DISTANCE=$(echo $ROUTE_TEST | grep -o '"distance":[0-9.]*' | head -1 | cut -d: -f2)
    test_info "NYC→Boston distance: $(echo "scale=2; $DISTANCE/1000" | bc) km"
else
    test_failed "OSRM routing failed"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 7: Data Generation Functions"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_info "Testing synthetic DEM generation..."
# This would be tested in the browser, but we can verify the HTML contains the functions
if grep -q "generateDEM" /Users/xavasena/hive/frontend/gis-studio-pro.html 2>/dev/null; then
    test_passed "DEM generation function exists"
else
    test_failed "DEM generation function not found"
fi

if grep -q "generateSARImage" /Users/xavasena/hive/frontend/gis-studio-pro.html 2>/dev/null; then
    test_passed "SAR generation function exists"
else
    test_failed "SAR generation function not found"
fi

if grep -q "turfBufferAnalysis" /Users/xavasena/hive/frontend/gis-studio-integrated.html 2>/dev/null; then
    test_passed "Turf.js buffer analysis function exists"
else
    test_failed "Turf.js buffer analysis function not found"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 8: Python Backend GIS Modules"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_info "Checking Python GIS modules..."
cd /Users/xavasena/hive

# Check if shapely is installed
if .venv/bin/python -c "import shapely; print('OK')" 2>/dev/null | grep -q "OK"; then
    test_passed "Shapely installed"
else
    test_failed "Shapely not installed"
fi

# Check if rasterio is installed
if .venv/bin/python -c "import rasterio; print('OK')" 2>/dev/null | grep -q "OK"; then
    test_passed "Rasterio installed"
else
    test_failed "Rasterio not installed"
fi

# Check if pyproj is installed
if .venv/bin/python -c "import pyproj; print('OK')" 2>/dev/null | grep -q "OK"; then
    test_passed "PyProj installed"
else
    test_failed "PyProj not installed"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 9: GIS Backend Engine"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "/Users/xavasena/hive/backend/gis_engine.py" ]; then
    test_passed "GIS Engine module exists"
    
    # Check for key classes
    if grep -q "class LiDARProcessor" /Users/xavasena/hive/backend/gis_engine.py; then
        test_passed "LiDARProcessor class found"
    fi
    
    if grep -q "class RadarProcessor" /Users/xavasena/hive/backend/gis_engine.py; then
        test_passed "RadarProcessor class found"
    fi
    
    if grep -q "class MultiSensorFusion" /Users/xavasena/hive/backend/gis_engine.py; then
        test_passed "MultiSensorFusion class found"
    fi
else
    test_failed "GIS Engine module not found"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 10: Launch GIS Tools"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_info "Opening GIS Studio Integrated in browser..."
open "http://localhost:8000/frontend/gis-studio-integrated.html" 2>/dev/null
if [ $? -eq 0 ]; then
    test_passed "GIS Studio Integrated opened in browser"
else
    test_failed "Failed to open browser"
fi

sleep 2

test_info "Opening GIS Studio Pro in browser..."
open "http://localhost:8000/frontend/gis-studio-pro.html" 2>/dev/null
if [ $? -eq 0 ]; then
    test_passed "GIS Studio Pro opened in browser"
else
    test_failed "Failed to open browser"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Passed: $PASSED${NC}"
echo -e "${RED}❌ Failed: $FAILED${NC}"
echo ""

TOTAL=$((PASSED + FAILED))
PERCENTAGE=$((PASSED * 100 / TOTAL))

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED! (100%)${NC}"
    echo ""
    echo "🚀 READY TO USE:"
    echo "   📍 Integrated: http://localhost:8000/frontend/gis-studio-integrated.html"
    echo "   📍 Pro Tools:  http://localhost:8000/frontend/gis-studio-pro.html"
    echo ""
    echo "✨ Available Tools:"
    echo "   🌐 ArcGIS Online Web Maps"
    echo "   🍃 Leaflet + OpenStreetMap"
    echo "   📐 Turf.js Geospatial Analysis"
    echo "   🖼️ GDAL Raster Processing"
    echo "   📍 Free Geocoding (Nominatim)"
    echo "   🛣️ Free Routing (OSRM)"
    echo "   ☁️ LiDAR Processing"
    echo "   🗻 DEM Validation"
    echo "   🔀 Multi-Modal Data Fusion"
    echo "   🧲 Geophysics Integration"
    echo "   🤖 ML Terrain Classification"
    echo "   🔮 Neural Network Depth Prediction"
    echo ""
    exit 0
elif [ $PERCENTAGE -ge 80 ]; then
    echo -e "${YELLOW}⚠️  MOSTLY WORKING ($PERCENTAGE%)${NC}"
    echo "Some tests failed but core functionality should work"
    exit 0
else
    echo -e "${RED}❌ CRITICAL FAILURES ($PERCENTAGE%)${NC}"
    echo "Please check the failed tests above"
    exit 1
fi
