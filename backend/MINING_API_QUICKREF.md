# Mining Magnetometry API - Quick Reference

## 🎯 Overview
Complete mining magnetometry processing system with:
- MAG survey data import (CSV, XYZ, Geosoft)
- IGRF background field removal
- Mineral discrimination (Fe, Cu, Au, Ni)
- Drill target recommendations
- Cost-effectiveness analysis

---

## 📡 API Endpoints

### 1. Upload & Process MAG Survey
**`POST /api/mining/mag-survey`**

Upload magnetometry survey file and get complete analysis.

**Form Data:**
- `file`: Survey file (CSV, XYZ, or Geosoft format)
- `file_format`: "csv" | "xyz" | "geosoft" (default: "csv")
- `latitude`: Optional survey latitude (for IGRF)
- `longitude`: Optional survey longitude (for IGRF)
- `date`: Optional survey date

**CSV Format:**
```csv
latitude,longitude,elevation,magnetic_field
-30.5,138.6,250,52400
-30.5,138.7,245,52600
...
```

**Response:**
```json
{
  "survey_info": {
    "num_stations": 100,
    "file_format": "csv",
    "igrf_corrected": true,
    "survey_stats": {
      "mean_anomaly_nT": 150.5,
      "max_anomaly_nT": 1200.0,
      "min_anomaly_nT": -50.0
    }
  },
  "mineral_discrimination": {
    "num_target_types": 3,
    "all_targets": [...],
    "high_priority_targets": [...]
  },
  "drill_targets": [
    {
      "mineral_type": "iron_magnetite",
      "confidence": "high",
      "drill_priority": 1,
      "locations": [[138.6, -30.5, 250], ...]
    }
  ]
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/mining/mag-survey \
  -F "file=@my_survey.csv" \
  -F "file_format=csv" \
  -F "latitude=-30.5" \
  -F "longitude=138.6"
```

---

### 2. Discriminate Minerals
**`POST /api/mining/discriminate`**

Identify mineral types from magnetic data.

**Request:**
```json
{
  "magnetic_data": [150.5, 890.2, 450.1, ...],
  "locations": [[138.6, -30.5, 250], [138.7, -30.5, 245], ...],
  "target_minerals": ["iron", "gold", "copper"]  // optional
}
```

**Response:**
```json
{
  "discrimination_results": {
    "survey_stats": {
      "total_stations": 100,
      "mean_anomaly_nT": 150.5,
      "max_anomaly_nT": 1200.0
    },
    "targets": [
      {
        "mineral_type": "iron_magnetite",
        "confidence": "high",
        "num_targets": 15,
        "max_anomaly": 1200.0,
        "description": "Strong positive anomaly - likely magnetite or Fe-rich deposit",
        "drill_priority": 1,
        "locations": [[138.6, -30.5, 250], ...]
      },
      {
        "mineral_type": "copper_gold_association",
        "confidence": "medium",
        "num_targets": 8,
        "max_anomaly": 450.0,
        "description": "Moderate positive anomaly - possible Cu-Au with magnetic alteration",
        "drill_priority": 2,
        "locations": [[138.8, -30.6, 240], ...]
      }
    ]
  }
}
```

**Mineral Types Detected:**
- `iron_magnetite` - Strong anomalies (>500nT), Fe-rich deposits
- `copper_gold_association` - Moderate anomalies (100-400nT), Cu-Au alteration
- `ultramafic_nickel` - Clustered moderate anomalies, Ni potential
- `non_magnetic_sedimentary` - Negative anomalies, sediment basins

---

### 3. Get Drill Targets
**`POST /api/mining/target-drills`**

Ranked drill location recommendations.

**Request:**
```json
{
  "magnetic_data": [150.5, 890.2, 450.1, ...],
  "locations": [[138.6, -30.5, 250], ...],
  "min_anomaly": 100.0,  // Minimum nT to consider
  "top_n": 10           // Number of targets to return
}
```

**Response:**
```json
{
  "drill_targets": [
    {
      "location": [138.6, -30.5, 250],
      "mineral_type": "iron_magnetite",
      "confidence": "high",
      "priority": 1,
      "anomaly_nT": 1200.0
    },
    {
      "location": [138.7, -30.6, 245],
      "mineral_type": "copper_gold_association",
      "confidence": "medium",
      "priority": 2,
      "anomaly_nT": 450.0
    }
  ],
  "parameters": {
    "min_anomaly_nt": 100.0,
    "top_n": 10,
    "num_stations": 100
  }
}
```

---

### 4. Cost Analysis
**`GET /api/mining/survey-cost`**

Compare MAG survey vs drilling costs.

**Query Parameters:**
- `area_km2` - Survey area in km² (required)
- `line_spacing_m` - Distance between lines (default: 100m)
- `station_spacing_m` - Distance between stations (default: 25m)
- `cost_per_station` - Cost per MAG station in $ (default: $50)
- `cost_per_drill` - Cost per drill hole in $ (default: $100,000)

**Response:**
```json
{
  "survey_design": {
    "area_km2": 10.0,
    "num_lines": 100,
    "stations_per_line": 400,
    "total_stations": 40000,
    "line_spacing_m": 100,
    "station_spacing_m": 25
  },
  "cost_analysis": {
    "mag_survey_cost_usd": 2000000,
    "blind_drilling_cost_usd": 10000000,
    "targeted_drilling_cost_usd": 2000000,
    "total_cost_with_mag_usd": 4000000,
    "savings_usd": 6000000,
    "roi_percent": 300,
    "drills_avoided": 8
  },
  "recommendations": {
    "use_mag_survey": true,
    "optimal_strategy": "MAG + Targeted Drilling",
    "confidence": "high"
  }
}
```

**cURL Example:**
```bash
curl "http://localhost:8000/api/mining/survey-cost?area_km2=10&cost_per_station=50&cost_per_drill=100000"
```

---

## 🚀 Quick Start

### 1. Start Backend
```bash
cd /Users/xavasena/hive
.venv/bin/python -m backend.main
```

### 2. Test APIs
```bash
chmod +x test_mining_api.py
.venv/bin/python test_mining_api.py
```

### 3. Upload Your MAG Survey
```python
import requests

with open('my_mag_survey.csv', 'rb') as f:
    files = {'file': f}
    data = {
        'file_format': 'csv',
        'latitude': -30.5,
        'longitude': 138.6
    }
    
    response = requests.post(
        'http://localhost:8000/api/mining/mag-survey',
        files=files,
        data=data
    )
    
    results = response.json()
    print(f"Found {len(results['drill_targets'])} drill targets!")
    
    for target in results['drill_targets'][:5]:
        print(f"- {target['mineral_type']}: {target['locations'][0]}")
```

---

## 📊 Data Formats

### CSV Format
```csv
latitude,longitude,elevation,magnetic_field
-30.5000,138.6000,250.0,52400.5
-30.5000,138.7000,245.0,52600.2
-30.5000,138.8000,240.0,51800.7
```

### XYZ Format
```
138.6000 -30.5000 250.0 52400.5
138.7000 -30.5000 245.0 52600.2
138.8000 -30.5000 240.0 51800.7
```

### Geosoft GDB Format
Binary Geosoft database format (auto-detected)

---

## 🎯 Typical Workflow

1. **Upload Survey** → `/api/mining/mag-survey`
   - Get complete analysis with anomalies and targets

2. **Review Targets** → Check drill recommendations
   - High-priority iron deposits
   - Medium-priority Cu-Au zones
   - Ultramafic Ni potential

3. **Cost Analysis** → `/api/mining/survey-cost`
   - Validate survey design
   - Calculate ROI

4. **Refine Targets** → `/api/mining/target-drills`
   - Filter by anomaly strength
   - Get top N recommendations

5. **Export for Drilling** → Use target coordinates
   - Format: [longitude, latitude, elevation]
   - Ready for drill planning software

---

## 🔬 Technical Details

### IGRF Correction
- Uses IGRF-13 model for Earth's magnetic field
- Removes background to reveal anomalies
- Date/location used for accuracy

### Mineral Discrimination Algorithm
- Statistical analysis (mean, std dev)
- Threshold-based classification
- Pattern recognition (clustering, elongation)
- Magnetic signature matching

### Anomaly Detection
- 2-sigma thresholds for outliers
- Clustering for target grouping
- Gradient analysis for boundaries

---

## 💡 Best Practices

1. **Survey Design**
   - Line spacing: 50-200m (depending on target size)
   - Station spacing: 10-50m (depending on resolution)
   - Coverage: Extend beyond known mineralization

2. **Data Quality**
   - Remove diurnal variations
   - Level flight lines
   - Apply terrain corrections

3. **Interpretation**
   - High confidence → Drill first
   - Medium confidence → Follow-up geophysics
   - Low confidence → Monitor, low priority

4. **Cost Optimization**
   - Use MAG to reduce drilling by 80%
   - Typical ROI: 200-500%
   - Best for large areas (>5 km²)

---

## 📞 Support

For mining project questions or custom features:
- API docs: http://localhost:8000/docs
- Test suite: `python test_mining_api.py`
- Backend logs: Check terminal output

**Ready for your mining project! 🧲⛏️**
