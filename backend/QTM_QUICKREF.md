# Queztl Training Manager (QTM) - Quick Reference

## 🚀 Quick Start

```bash
# List all available training modules
./qtm list

# Check training status
./qtm status

# Install a specific module
./qtm install gis-lidar

# Install all high-priority modules
./qtm install image-to-3d
./qtm install enhanced-3d
./qtm install gis-lidar
./qtm install geophysics-magnetic

# Or upgrade everything at once
./qtm upgrade-all
```

## 📦 Available Modules

### 3D Generation
- **image-to-3d** - Converts photos to 3D models (competes with Hexa3D)
- **enhanced-3d** - High-quality 3D generation (1024 vertices)
- **text-to-3d** - Generate 3D models from text descriptions

### GIS
- **gis-lidar** - Point cloud classification and building extraction
- **gis-buildings** - Automatic building extraction from LiDAR

### Geophysics
- **geophysics-magnetic** - Magnetic survey interpretation (competes with Geosoft)
- **geophysics-resistivity** - Fast resistivity inversion
- **geophysics-seismic** - Seismic velocity analysis

## 🔧 Common Commands

```bash
# List modules by category
./qtm list --category=GIS
./qtm list --category=Geophysics
./qtm list --category="3D Generation"

# Get detailed info about a module
./qtm info gis-lidar
./qtm info geophysics-magnetic

# Search for modules
./qtm search magnetic
./qtm search 3d

# Check dependencies
./qtm check-deps

# Remove a trained model
./qtm remove gis-lidar

# Clean old logs
./qtm clean

# Retrain a module
./qtm upgrade image-to-3d

# Retrain all modules
./qtm upgrade-all
```

## 📊 Training Priority

**HIGH Priority** (Train first):
1. `image-to-3d` - Core photo-to-3D capability
2. `enhanced-3d` - High-quality 3D generation
3. `gis-lidar` - GIS point cloud processing
4. `geophysics-magnetic` - Geophysics interpretation

**MEDIUM Priority**:
5. `text-to-3d` - Text-based generation
6. `gis-buildings` - Building extraction
7. `geophysics-resistivity` - Resistivity inversion

**LOW Priority**:
8. `geophysics-seismic` - Seismic analysis

## ⚡ Automated Training Pipeline

Train all high-priority modules in sequence:

```bash
#!/bin/bash
# Install high-priority modules
for module in image-to-3d enhanced-3d gis-lidar geophysics-magnetic; do
    echo "Training $module..."
    ./qtm install $module
done

# Check final status
./qtm status
```

## 🐛 Troubleshooting

```bash
# Check dependencies
./qtm check-deps

# View training logs
docker exec hive-backend-1 tail -f /workspace/training_logs/gis-lidar_training.log

# Check if training is running
docker exec hive-backend-1 ps aux | grep python

# Clean and restart
./qtm clean
./qtm upgrade <module>
```

## 📈 Training Status

```bash
# Real-time status monitoring
watch -n 5 ./qtm status

# View specific module status
./qtm info gis-lidar
```

## 🎯 Example Workflows

### Fresh Installation
```bash
# 1. Check environment
./qtm check-deps

# 2. Install all modules
./qtm upgrade-all

# 3. Monitor progress
./qtm status
```

### Update Specific Module
```bash
# 1. Get module info
./qtm info gis-lidar

# 2. Retrain with new data
./qtm upgrade gis-lidar

# 3. Verify installation
./qtm status
```

### Clean Installation
```bash
# 1. Remove old models
./qtm remove image-to-3d
./qtm remove gis-lidar

# 2. Clean artifacts
./qtm clean

# 3. Reinstall
./qtm install image-to-3d
./qtm install gis-lidar
```

## 💡 Tips

- Use `./qtm list` to see what's available
- Use `./qtm status` to track progress
- Training runs in background - you can continue working
- Logs are saved in `/workspace/training_logs/`
- Models are saved in `/workspace/models/`
- Each module tracks its own training history
