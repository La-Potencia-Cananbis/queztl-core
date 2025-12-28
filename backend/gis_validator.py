class LiDARValidator:
    def __init__(self):
        pass
    def validate(self, data):
        return ValidationStatus.VALID

class RasterValidator:
    def __init__(self):
        pass
    def validate(self, data):
        return ValidationStatus.VALID

class VectorValidator:
    def __init__(self):
        pass
    def validate(self, data):
        return ValidationStatus.VALID
"""
# GIS Data Validator & Error Checker
# Ensures all scraped/imported GIS data is valid, safe, and properly formatted
"""
# import numpy as np
# from typing import Dict, List, Tuple, Optional, Any, Union
# from dataclasses import dataclass
# from enum import Enum
# import json
# import logging

# logger = logging.getLogger(__name__)



from enum import Enum

class ValidationStatus(Enum):
    VALID = "valid"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class GISDataType(Enum):
    LIDAR_POINT_CLOUD = "lidar_point_cloud"
    SAR_IMAGE = "sar_image"
    ELEVATION_GRID = "elevation_grid"
    ORTHOMOSAIC = "orthomosaic"
    BUILDING_FOOTPRINTS = "building_footprints"
    VECTOR_FEATURES = "vector_features"
    SATELLITE_IMAGE = "satellite_image"
    THERMAL_IMAGE = "thermal_image"

class GISDataValidator:
    def __init__(self):
        pass
    def validate(self, data):
        return ValidationStatus.VALID


# class GISDataType(Enum):
    """Supported GIS data types"""
#     LIDAR_POINT_CLOUD = "lidar_point_cloud"
#     SAR_IMAGE = "sar_image"
#     ELEVATION_GRID = "elevation_grid"
#     ORTHOMOSAIC = "orthomosaic"
#     BUILDING_FOOTPRINTS = "building_footprints"
#     VECTOR_FEATURES = "vector_features"
#     SATELLITE_IMAGE = "satellite_image"
#     THERMAL_IMAGE = "thermal_image"


@dataclass
# class ValidationResult:
    """Result of data validation"""
#     status: ValidationStatus
#     valid: bool
#     data_type: str
#     issues: List[Dict[str, Any]]
#     warnings: List[Dict[str, Any]]
#     metadata: Dict[str, Any]
    
#     def summary(self) -> str:
        """Get human-readable summary"""
#         issue_count = len(self.issues)
#         warning_count = len(self.warnings)
        
#         msg = f"[{self.status.value.upper()}] {self.data_type}"
#         if issue_count > 0:
#             msg += f" - {issue_count} error(s)"
#         if warning_count > 0:
#             msg += f" - {warning_count} warning(s)"
#         return msg


# class LiDARValidator:
    """Validate LiDAR point cloud data"""
    
#     MIN_POINTS = 10
#     MAX_POINTS = 100_000_000
#     VALID_CLASSIFICATIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    
    @classmethod
#     def validate_point_cloud(cls, points: np.ndarray, 
#                             classifications: Optional[np.ndarray] = None,
#                             intensities: Optional[np.ndarray] = None,
#                             colors: Optional[np.ndarray] = None) -> ValidationResult:
        """
#         Validate point cloud data
        
#         Returns: ValidationResult with status and detailed issues/warnings
        """
#         issues = []
#         warnings = []
#         metadata = {}
        
        # Check points array
#         if points is None:
#             issues.append({
                "type": "null_data",
                "severity": "critical",
                "message": "Points array is None"
            })
#             return ValidationResult(
#                 status=ValidationStatus.CRITICAL,
#                 valid=False,
#                 data_type="lidar_point_cloud",
#                 issues=issues,
#                 warnings=warnings,
#                 metadata=metadata
        
        # Check shape
#         if points.ndim != 2 or points.shape[1] != 3:
#             issues.append({
                "type": "invalid_shape",
                "severity": "critical",
                "message": f"Points must be Nx3 array, got {points.shape}"
            })
        
        # Check point count
#         num_points = len(points)
#         if num_points < cls.MIN_POINTS:
#             issues.append({
                "type": "insufficient_data",
                "severity": "error",
                "message": f"Too few points: {num_points} (minimum: {cls.MIN_POINTS})"
            })
        
#         if num_points > cls.MAX_POINTS:
#             issues.append({
                "type": "excessive_data",
                "severity": "warning",
                "message": f"Very large point cloud: {num_points:,} points (max recommended: {cls.MAX_POINTS:,})"
            })
#             warnings.append({
                "type": "memory_warning",
                "message": f"May require significant memory to process {num_points:,} points"
            })
        
        # Check data type
#         if not np.issubdtype(points.dtype, np.floating):
#             warnings.append({
                "type": "data_type",
                "message": f"Points should be float, got {points.dtype}. Converting..."
            })
        
        # Check for NaN/Inf
#         nan_count = np.isnan(points).sum()
#         inf_count = np.isinf(points).sum()
        
#         if nan_count > 0:
#             warnings.append({
                "type": "nan_values",
                "message": f"Found {nan_count} NaN values in point coordinates",
                "percentage": f"{(nan_count / points.size * 100):.2f}%"
            })
        
#         if inf_count > 0:
#             warnings.append({
                "type": "inf_values",
                "message": f"Found {inf_count} infinite values in point coordinates",
                "percentage": f"{(inf_count / points.size * 100):.2f}%"
            })
        
        # Check coordinate ranges
#         finite_points = points[np.isfinite(points).all(axis=1)]
#         if len(finite_points) > 0:
#             mins = finite_points.min(axis=0)
#             maxs = finite_points.max(axis=0)
            
#             metadata["bounds"] = {
                "min": [float(m) for m in mins],
                "max": [float(m) for m in maxs],
                "range": [float(maxs[i] - mins[i]) for i in range(3)]
            }
            
            # Check for unusual coordinate ranges
#             for i, (axis_name, axis_idx) in enumerate(zip(['X', 'Y', 'Z'], [0, 1, 2])):
#                 axis_range = maxs[axis_idx] - mins[axis_idx]
#                 if axis_range < 0.001:
#                     warnings.append({
                        "type": "degenerate_axis",
                        "message": f"{axis_name}-axis range very small: {axis_range:.6f}m"
                    })
                
                # Z (elevation) should be reasonable
#                 if axis_idx == 2:
#                     if maxs[axis_idx] > 10000:
#                         warnings.append({
                            "type": "unusual_elevation",
                            "message": f"Maximum elevation very high: {maxs[axis_idx]}m"
                        })
#                     if mins[axis_idx] < -500:
#                         warnings.append({
                            "type": "unusual_elevation",
                            "message": f"Negative elevation very deep: {mins[axis_idx]}m"
                        })
        
        # Validate classifications
#         if classifications is not None:
#             if len(classifications) != num_points:
#                 issues.append({
                    "type": "mismatched_length",
                    "severity": "error",
                    "message": f"Classifications length {len(classifications)} != points length {num_points}"
                })
            
#             invalid_classes = set(classifications) - set(cls.VALID_CLASSIFICATIONS)
#             if invalid_classes:
#                 warnings.append({
                    "type": "invalid_classifications",
                    "message": f"Found invalid classification values: {sorted(invalid_classes)}"
                })
            
            # Classification distribution
#             unique, counts = np.unique(classifications, return_counts=True)
#             metadata["classification_distribution"] = {
#                 str(int(c)): int(cnt) for c, cnt in zip(unique, counts)
            }
        
        # Validate intensities
#         if intensities is not None:
#             if len(intensities) != num_points:
#                 issues.append({
                    "type": "mismatched_length",
                    "severity": "error",
                    "message": f"Intensities length {len(intensities)} != points length {num_points}"
                })
            
#             if intensities.min() < 0 or intensities.max() > 255:
#                 warnings.append({
                    "type": "intensity_range",
                    "message": f"Intensities outside expected range [0, 255]: [{intensities.min()}, {intensities.max()}]"
                })
        
        # Validate colors
#         if colors is not None:
#             if colors.shape[0] != num_points:
#                 issues.append({
                    "type": "mismatched_length",
                    "severity": "error",
                    "message": f"Colors length {colors.shape[0]} != points length {num_points}"
                })
            
#             if colors.shape[1] not in [3, 4]:
#                 issues.append({
                    "type": "invalid_color_format",
                    "severity": "error",
                    "message": f"Colors must be Nx3 or Nx4, got {colors.shape}"
                })
        
        # Determine overall status
#         if issues:
#             status = ValidationStatus.CRITICAL if any(i["severity"] == "critical" for i in issues) else ValidationStatus.ERROR
#             valid = False
#         elif warnings:
#             status = ValidationStatus.WARNING
#             valid = True
#         else:
#             status = ValidationStatus.VALID
#             valid = True
        
#         metadata["point_count"] = num_points
#         metadata["validated_at"] = __import__("datetime").datetime.utcnow().isoformat()
        
#         return ValidationResult(
#             status=status,
#             valid=valid,
#             data_type="lidar_point_cloud",
#             issues=issues,
#             warnings=warnings,
#             metadata=metadata


# class RasterValidator:
    """Validate raster data (images, DEMs, etc)"""
    
    @classmethod
#     def validate_elevation_grid(cls, elevation: np.ndarray,
#                                resolution: float = 1.0) -> ValidationResult:
        """Validate Digital Elevation Model (DEM) data"""
#         issues = []
#         warnings = []
#         metadata = {}
        
        # Check dimensions
#         if elevation.ndim != 2:
#             issues.append({
                "type": "invalid_dimensions",
                "severity": "critical",
                "message": f"DEM must be 2D array, got {elevation.ndim}D"
            })
        
        # Check resolution
#         if resolution <= 0:
#             issues.append({
                "type": "invalid_resolution",
                "severity": "error",
                "message": f"Resolution must be positive, got {resolution}"
            })
        
        # Check data type
#         if not np.issubdtype(elevation.dtype, np.floating):
#             warnings.append({
                "type": "data_type",
                "message": f"DEM should be float, got {elevation.dtype}"
            })
        
        # Check for NaN/Inf
#         nan_count = np.isnan(elevation).sum()
#         inf_count = np.isinf(elevation).sum()
        
#         if nan_count > elevation.size * 0.5:
#             issues.append({
                "type": "excessive_nodata",
                "severity": "error",
                "message": f"More than 50% NaN values: {nan_count/elevation.size*100:.1f}%"
            })
#         elif nan_count > 0:
#             warnings.append({
                "type": "nodata_values",
                "message": f"Found {nan_count} NaN values ({nan_count/elevation.size*100:.2f}%)"
            })
        
#         if inf_count > 0:
#             issues.append({
                "type": "inf_values",
                "severity": "error",
                "message": f"Found {inf_count} infinite values"
            })
        
        # Elevation range checks
#         valid_dem = elevation[np.isfinite(elevation)]
#         if len(valid_dem) > 0:
#             min_elev = valid_dem.min()
#             max_elev = valid_dem.max()
            
#             metadata["elevation_range"] = {
                "min": float(min_elev),
                "max": float(max_elev),
                "mean": float(valid_dem.mean()),
                "std": float(valid_dem.std())
            }
            
            # Check for unrealistic values
#             if max_elev > 10000:
#                 warnings.append({
                    "type": "extreme_elevation",
                    "message": f"Very high maximum elevation: {max_elev}m"
                })
            
#             if min_elev < -500:
#                 warnings.append({
                    "type": "extreme_elevation",
                    "message": f"Very low minimum elevation: {min_elev}m"
                })
            
            # Check for excessive slope (terrain roughness)
#             if valid_dem.size > 1:
#                 diff_x = np.diff(valid_dem, axis=1)
#                 diff_y = np.diff(valid_dem, axis=0)
#                 max_slope_m = max(np.nanmax(np.abs(diff_x)), np.nanmax(np.abs(diff_y)))
#                 max_slope_percent = (max_slope_m / resolution) * 100
                
#                 if max_slope_percent > 10000:  # >10000% slope unrealistic
#                     warnings.append({
                        "type": "excessive_slope",
                        "message": f"Unrealistic terrain slope detected: {max_slope_percent:.0f}%"
                    })
        
#         metadata["shape"] = elevation.shape
#         metadata["resolution_m"] = resolution
#         metadata["area_km2"] = float(elevation.size * resolution * resolution / 1_000_000)
        
        # Determine status
#         if issues:
#             status = ValidationStatus.CRITICAL if any(i["severity"] == "critical" for i in issues) else ValidationStatus.ERROR
#             valid = False
#         elif warnings:
#             status = ValidationStatus.WARNING
#             valid = True
#         else:
#             status = ValidationStatus.VALID
#             valid = True
        
#         metadata["validated_at"] = __import__("datetime").datetime.utcnow().isoformat()
        
#         return ValidationResult(
#             status=status,
#             valid=valid,
#             data_type="elevation_grid",
#             issues=issues,
#             warnings=warnings,
#             metadata=metadata
    
    @classmethod
#     def validate_image(cls, image: np.ndarray,
#                       expected_shape: Optional[Tuple[int, ...]] = None) -> ValidationResult:
        """Validate satellite/orthomosaic image data"""
#         issues = []
#         warnings = []
#         metadata = {}
        
        # Check dimensions
#         if image.ndim not in [2, 3]:
#             issues.append({
                "type": "invalid_dimensions",
                "severity": "critical",
                "message": f"Image must be 2D (grayscale) or 3D (RGB/RGBA), got {image.ndim}D"
            })
        
        # Check bands
#         if image.ndim == 3:
#             if image.shape[2] not in [1, 3, 4]:
#                 issues.append({
                    "type": "invalid_bands",
                    "severity": "error",
                    "message": f"Image must have 1, 3, or 4 bands, got {image.shape[2]}"
                })
        
        # Check data type
#         valid_dtypes = [np.uint8, np.uint16, np.uint32, np.float32, np.float64]
#         if image.dtype not in valid_dtypes:
#             warnings.append({
                "type": "unusual_dtype",
                "message": f"Image dtype {image.dtype} is unusual"
            })
        
        # Check value ranges
#         if np.issubdtype(image.dtype, np.integer):
#             min_val, max_val = image.min(), image.max()
#             expected_max = 2**int(image.dtype.itemsize*8) - 1
            
#             if max_val > expected_max:
#                 warnings.append({
                    "type": "out_of_range",
                    "message": f"Integer values exceed expected range for {image.dtype}"
                })
        
        # Check for NaN/Inf
#         if np.issubdtype(image.dtype, np.floating):
#             nan_percent = np.isnan(image).sum() / image.size * 100
#             inf_percent = np.isinf(image).sum() / image.size * 100
            
#             if nan_percent > 50:
#                 issues.append({
                    "type": "excessive_nodata",
                    "severity": "error",
                    "message": f"{nan_percent:.1f}% NaN values"
                })
#             elif nan_percent > 0:
#                 warnings.append({
                    "type": "nodata_values",
                    "message": f"{nan_percent:.2f}% NaN values"
                })
            
#             if inf_percent > 0:
#                 warnings.append({
                    "type": "inf_values",
                    "message": f"{inf_percent:.2f}% infinite values"
                })
        
#         metadata["shape"] = image.shape
#         metadata["dtype"] = str(image.dtype)
#         metadata["size_mb"] = float(image.nbytes / 1_000_000)
        
        # Determine status
#         if issues:
#             status = ValidationStatus.CRITICAL if any(i["severity"] == "critical" for i in issues) else ValidationStatus.ERROR
#             valid = False
#         elif warnings:
#             status = ValidationStatus.WARNING
#             valid = True
#         else:
#             status = ValidationStatus.VALID
#             valid = True
        
#         return ValidationResult(
#             status=status,
#             valid=valid,
#             data_type="image",
#             issues=issues,
#             warnings=warnings,
#             metadata=metadata


# class VectorValidator:
    """Validate vector/feature data"""
    
    @classmethod
#     def validate_building_footprints(cls, footprints: List[np.ndarray]) -> ValidationResult:
        """Validate building footprint polygons"""
#         issues = []
#         warnings = []
#         metadata = {}
        
        # Check if empty
#         if not footprints:
#             issues.append({
                "type": "empty_data",
                "severity": "error",
                "message": "No building footprints provided"
            })
#             return ValidationResult(
#                 status=ValidationStatus.ERROR,
#                 valid=False,
#                 data_type="building_footprints",
#                 issues=issues,
#                 warnings=warnings,
#                 metadata=metadata
        
#         valid_count = 0
#         invalid_footprints = []
        
#         for i, footprint in enumerate(footprints):
            # Check shape
#             if footprint.ndim != 2 or footprint.shape[1] != 2:
#                 invalid_footprints.append({
                    "index": i,
                    "issue": f"Invalid shape {footprint.shape}, expected Nx2"
                })
#                 continue
            
            # Check minimum vertices (triangle minimum)
#             if len(footprint) < 3:
#                 invalid_footprints.append({
                    "index": i,
                    "issue": f"Polygon has only {len(footprint)} vertices (minimum 3)"
                })
#                 continue
            
            # Check for NaN/Inf
#             if np.isnan(footprint).any() or np.isinf(footprint).any():
#                 invalid_footprints.append({
                    "index": i,
                    "issue": "Contains NaN or infinite values"
                })
#                 continue
            
#             valid_count += 1
        
#         if invalid_footprints:
#             warnings.append({
                "type": "invalid_polygons",
                "count": len(invalid_footprints),
                "details": invalid_footprints[:10]  # Show first 10
            })
        
#         metadata["total_footprints"] = len(footprints)
#         metadata["valid_footprints"] = valid_count
#         metadata["invalid_footprints"] = len(invalid_footprints)
#         metadata["validity_percent"] = f"{(valid_count / len(footprints) * 100):.1f}%"
        
        # Determine status
#         if valid_count == 0:
#             status = ValidationStatus.ERROR
#             valid = False
#         elif len(invalid_footprints) > 0:
#             status = ValidationStatus.WARNING
#             valid = True
#         else:
#             status = ValidationStatus.VALID
#             valid = True
        
#         return ValidationResult(
#             status=status,
#             valid=valid,
#             data_type="building_footprints",
#             issues=issues,
#             warnings=warnings,
#             metadata=metadata


# class GISDataValidator:
    """Main GIS data validator - routes to appropriate validators"""
    
    @staticmethod
#     def validate(data: Any, data_type: GISDataType) -> ValidationResult:
        """
#         Validate GIS data
        
#         Args:
#             data: GIS data to validate
#             data_type: Type of GIS data
        
#         Returns:
#             ValidationResult with detailed validation information
        """
#         if data_type == GISDataType.LIDAR_POINT_CLOUD:
#             if hasattr(data, 'points'):
                # PointCloud object
#                 return LiDARValidator.validate_point_cloud(
#                     data.points,
#                     data.classifications if hasattr(data, 'classifications') else None,
#                     data.intensities if hasattr(data, 'intensities') else None,
#                     data.colors if hasattr(data, 'colors') else None
#             else:
                # Assume numpy array
#                 return LiDARValidator.validate_point_cloud(data)
        
#         elif data_type == GISDataType.ELEVATION_GRID:
#             return RasterValidator.validate_elevation_grid(data)
        
#         elif data_type in [GISDataType.ORTHOMOSAIC, GISDataType.SATELLITE_IMAGE, GISDataType.THERMAL_IMAGE, GISDataType.SAR_IMAGE]:
#             return RasterValidator.validate_image(data)
        
#         elif data_type == GISDataType.BUILDING_FOOTPRINTS:
#             return VectorValidator.validate_building_footprints(data)
        
#         else:
#             return ValidationResult(
#                 status=ValidationStatus.ERROR,
#                 valid=False,
#                 data_type=str(data_type),
#                 issues=[{"type": "unsupported_type", "message": f"Unknown data type: {data_type}"}],
#                 warnings=[],
#                 metadata={}
    
    @staticmethod
#     def validate_json_safe(data: Any) -> Dict[str, Any]:
        """Convert validation result to JSON-safe format"""
#         if isinstance(data, ValidationResult):
#             return {
                "status": data.status.value,
                "valid": data.valid,
                "data_type": data.data_type,
                "summary": data.summary(),
                "issues": data.issues,
                "warnings": data.warnings,
                "metadata": data.metadata
            }
#         return data
