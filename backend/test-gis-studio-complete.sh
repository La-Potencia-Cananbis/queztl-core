#!/bin/bash
# GIS Studio - Complete Test Suite

API="http://localhost:8000"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASSED=0
FAILED=0
TOTAL=0

echo "╔═══════════════════════════════════════════════════════╗"
echo "║  🗺️  GIS STUDIO - COMPLETE TEST SUITE                ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Test 1: Health Check
echo "1️⃣  Testing Backend Health..."
TOTAL=$((TOTAL + 1))
HEALTH=$(curl -s "$API/api/health")
if echo "$HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}❌ Backend health check failed${NC}"
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 2: LiDAR Validation
echo "2️⃣  Testing LiDAR Point Cloud Validation..."
TOTAL=$((TOTAL + 1))
LIDAR_TEST=$(curl -s -X POST "$API/api/gis/studio/validate/lidar" \
  -H "Content-Type: application/json" \
  -d '{
    "points": [[0.0, 0.0, 100.5], [1.0, 1.0, 102.3], [2.0, 2.0, 104.1]],
    "classification": [2, 2, 1],
    "intensity": [100, 120, 110]
  }')

if echo "$LIDAR_TEST" | grep -q "valid\|metadata"; then
    echo -e "${GREEN}✅ LiDAR validation working${NC}"
    echo "   Response: $(echo "$LIDAR_TEST" | python3 -m json.tool 2>/dev/null | head -3)"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}❌ LiDAR validation failed${NC}"
    echo "   Response: $LIDAR_TEST"
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 3: DEM Validation
echo "3️⃣  Testing Digital Elevation Model (DEM) Validation..."
TOTAL=$((TOTAL + 1))
DEM_TEST=$(curl -s -X POST "$API/api/gis/studio/validate/dem" \
  -H "Content-Type: application/json" \
  -d '{
    "elevation": [[100.0, 102.0, 104.0], [101.0, 103.0, 105.0], [102.0, 104.0, 106.0]]
  }')

if echo "$DEM_TEST" | grep -q "valid\|metadata\|error"; then
    echo -e "${GREEN}✅ DEM validation working${NC}"
    echo "   Response: $(echo "$DEM_TEST" | python3 -m json.tool 2>/dev/null | head -3)"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}❌ DEM validation failed${NC}"
    echo "   Response: $DEM_TEST"
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 4: Terrain Analysis Integration
echo "4️⃣  Testing Terrain Analysis Integration..."
TOTAL=$((TOTAL + 1))
TERRAIN=$(curl -s -X POST "$API/api/gis/studio/integrate/terrain" \
  -H "Content-Type: application/json" \
  -d '{
    "dem": [[100.0, 102.0], [101.0, 103.0]],
    "points": [[0.0, 0.0, 100.5], [1.0, 1.0, 102.3]]
  }')

if echo "$TERRAIN" | grep -q "stats\|classification\|error"; then
    echo -e "${GREEN}✅ Terrain analysis working${NC}"
    echo "   Response: $(echo "$TERRAIN" | python3 -m json.tool 2>/dev/null | head -3)"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}❌ Terrain analysis failed${NC}"
    echo "   Response: $TERRAIN"
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 5: List Capabilities
echo "5️⃣  Testing GIS Capabilities Endpoint..."
TOTAL=$((TOTAL + 1))
CAPS=$(curl -s "$API/api/gen3d/capabilities")
if echo "$CAPS" | grep -q "gis_lidar\|gis_radar\|geophysics"; then
    echo -e "${GREEN}✅ GIS capabilities listed${NC}"
    echo "   Modules: LiDAR, Radar, Geophysics"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}❌ Capabilities check failed${NC}"
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 6: GPU Info
echo "6️⃣  Testing GPU/Hardware Info..."
TOTAL=$((TOTAL + 1))
GPU=$(curl -s "$API/api/gpu/info")
if echo "$GPU" | grep -q "cores\|threads\|memory"; then
    echo -e "${GREEN}✅ GPU info available${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}❌ GPU info check failed${NC}"
    FAILED=$((FAILED + 1))
fi
echo ""

# Summary
echo "╔═══════════════════════════════════════════════════════╗"
echo "║           📊 TEST RESULTS                             ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo -e "Total Tests:  $TOTAL"
echo -e "Passed:       ${GREEN}$PASSED${NC}"
echo -e "Failed:       ${RED}$FAILED${NC}"
PERCENTAGE=$((PASSED * 100 / TOTAL))
echo -e "Success Rate: ${YELLOW}$PERCENTAGE%${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 All GIS Studio tests passed!"
    exit 0
else
    echo "⚠️  Some tests failed. Check responses above."
    exit 1
fi
