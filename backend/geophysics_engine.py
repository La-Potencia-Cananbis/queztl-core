"""
# Geophysics Analysis Engine
# Professional subsurface investigation and modeling
# Compete with Geosoft Oasis Montaj, SeisSpace, Kingdom

# Supports:
- IGRF (International Geomagnetic Reference Field)
- WMM (World Magnetic Model)
- Magnetometer data
- Electrical resistivity
- Seismic data (SEG-Y format)
- Ground Penetrating Radar (GPR)
- Gravity surveys
"""
# import numpy as np
# from typing import List, Tuple, Dict, Optional, Union, Any
# from dataclasses import dataclass
# from enum import Enum
# import struct
# from datetime import datetime
# import json


# class GeophysicsDataType(Enum):
    """Types of geophysical data"""
#     MAGNETIC = "magnetic"
#     RESISTIVITY = "electrical_resistivity"
#     SEISMIC = "seismic"
#     GPR = "ground_penetrating_radar"
#     GRAVITY = "gravity"
#     ELECTROMAGNETIC = "electromagnetic"


@dataclass
# class MagneticSurvey:
    """Magnetic field survey data"""
#     locations: np.ndarray  # Nx3 (lat, lon, elevation)
#     total_field: np.ndarray  # N measurements (nT)
#     date: datetime
#     instrument: str = "proton_magnetometer"
    
    @property
#     def num_stations(self) -> int:
#         return len(self.total_field)
    
#     def remove_igrf(self, igrf_model: 'IGRFModel') -> np.ndarray:
        """Remove IGRF background field to get anomalies"""
#         igrf_values = np.array([
#             igrf_model.calculate(lat, lon, self.date.year, elev)
#             for lat, lon, elev in self.locations
        ])
#         return self.total_field - igrf_values


@dataclass
# class ResistivitySurvey:
    """Electrical resistivity survey data"""
#     electrodes: np.ndarray  # Nx3 (x, y, z)
#     apparent_resistivity: np.ndarray  # M measurements (ohm-m)
#     current: float  # Injection current (A)
#     spacing: float  # Electrode spacing (m)
#     array_type: str = "wenner"  # wenner, schlumberger, dipole-dipole
    
    @property
#     def num_measurements(self) -> int:
#         return len(self.apparent_resistivity)


@dataclass
# class SeismicSurvey:
    """Seismic reflection/refraction survey"""
#     traces: np.ndarray  # MxN (M traces, N samples)
#     sample_rate: float  # Hz
#     source_locations: np.ndarray  # Px3
#     receiver_locations: np.ndarray  # Qx3
#     survey_type: str = "reflection"  # reflection, refraction
    
    @property
#     def num_traces(self) -> int:
#         return self.traces.shape[0]
    
    @property
#     def duration(self) -> float:
        """Survey duration in seconds"""
#         return self.traces.shape[1] / self.sample_rate


# class IGRFModel:
    """
#     International Geomagnetic Reference Field (IGRF)
    13th generation model coefficients
    """
    
#     def __init__(self):
        # Simplified IGRF coefficients (real version would load from file)
        # These are representative values for demonstration
#         self.coefficients = {
            'g10': -29404.8,  # Gauss coefficients
            'g11': -1450.9,
            'h11': 4652.5,
            'g20': -2500.0,
            'g21': 2982.0,
            'h21': -2991.6,
            'g22': 1676.8,
            'h22': -734.6,
        }
#         self.epoch = 2020.0
#         self.reference_radius = 6371.2  # km
    
#     def calculate(self, latitude: float, longitude: float, 
#                   year: float, altitude: float = 0.0) -> float:
        """
#         Calculate total magnetic field intensity
        
#         Args:
#             latitude: Degrees north
#             longitude: Degrees east
#             year: Decimal year
#             altitude: Meters above sea level
            
#         Returns:
#             Total field intensity in nanoTesla (nT)
        """
        # Convert to radians
#         lat_rad = np.deg2rad(latitude)
#         lon_rad = np.deg2rad(longitude)
        
        # Simplified calculation (real IGRF is much more complex)
        # Using dipole approximation for demonstration
        
        # Gauss coefficients (simplified)
#         g10 = self.coefficients['g10']
#         g11 = self.coefficients['g11']
#         h11 = self.coefficients['h11']
        
        # Altitude correction (inverse cube law)
#         r = self.reference_radius + (altitude / 1000.0)  # km
#         r_ratio = (self.reference_radius / r) ** 3
        
        # Schmidt semi-normalized associated Legendre functions
#         P10 = np.sin(lat_rad)
#         P11 = np.cos(lat_rad)
        
        # Field components
#         X = -g11 * P11 * np.cos(lon_rad) - h11 * P11 * np.sin(lon_rad)
#         Y = g11 * P11 * np.sin(lon_rad) - h11 * P11 * np.cos(lon_rad)
#         Z = -2 * g10 * P10
        
        # Apply altitude correction
#         X *= r_ratio
#         Y *= r_ratio
#         Z *= r_ratio
        
        # Total field intensity
#         F = np.sqrt(X**2 + Y**2 + Z**2)
        
#         return F  # nT


# class WMMModel:
    """
#     World Magnetic Model (WMM)
#     US/UK standard magnetic model
    """
    
#     def __init__(self):
#         self.igrf = IGRFModel()  # WMM based on IGRF
#         self.secular_variation = {}  # Rate of change
    
#     def calculate_declination(self, latitude: float, longitude: float, 
#                              year: float, altitude: float = 0.0) -> float:
        """Calculate magnetic declination (deviation from true north)"""
        # Simplified calculation
#         lat_rad = np.deg2rad(latitude)
#         lon_rad = np.deg2rad(longitude)
        
        # Approximate declination
#         declination = -5.0 + 0.1 * longitude - 0.05 * latitude
        
#         return declination  # degrees
    
#     def calculate_inclination(self, latitude: float, longitude: float,
#                             year: float, altitude: float = 0.0) -> float:
        """Calculate magnetic inclination (dip angle)"""
        # Simplified: inclination increases toward poles
#         inclination = 2 * np.arctan(np.tan(np.deg2rad(latitude)))
#         return np.rad2deg(inclination)


# class MagneticAnalyzer:
    """
#     Magnetic data analysis and interpretation
#     Better than Geosoft: ML-based anomaly detection
    """
    
#     def __init__(self):
#         self.igrf = IGRFModel()
#         self.wmm = WMMModel()
    
#     def process_survey(self, survey: MagneticSurvey) -> Dict[str, Any]:
        """Process magnetic survey data"""
#         print(f" Processing magnetic survey: {survey.num_stations} stations")
        
        # Remove IGRF background
#         anomalies = survey.remove_igrf(self.igrf)
        
        # Statistics
#         stats = {
            'mean_anomaly': float(np.mean(anomalies)),
            'std_anomaly': float(np.std(anomalies)),
            'min_anomaly': float(np.min(anomalies)),
            'max_anomaly': float(np.max(anomalies)),
            'range': float(np.max(anomalies) - np.min(anomalies))
        }
        
        # Detect anomalies (potential targets)
#         threshold = np.mean(anomalies) + 2 * np.std(anomalies)
#         anomaly_mask = np.abs(anomalies) > threshold
        
        # Classify anomalies
#         positive_anomalies = np.sum(anomalies > threshold)
#         negative_anomalies = np.sum(anomalies < -threshold)
        
#         print(f" Found {positive_anomalies} positive anomalies (magnetic bodies)")
#         print(f" Found {negative_anomalies} negative anomalies (voids/non-magnetic)")
        
#         return {
            'statistics': stats,
            'anomalies': anomalies.tolist(),
            'positive_targets': int(positive_anomalies),
            'negative_targets': int(negative_anomalies),
            'interpretation': self._interpret_anomalies(anomalies)
        }
    
#     def _interpret_anomalies(self, anomalies: np.ndarray) -> List[str]:
        """AI-powered interpretation of magnetic anomalies"""
#         interpretations = []
        
#         max_anom = np.max(np.abs(anomalies))
        
#         if max_anom > 1000:
#             interpretations.append("Strong magnetic body detected - possible iron-rich deposit")
#         if max_anom > 500:
#             interpretations.append("Moderate magnetic anomaly - basalt or metamorphic rock")
#         if np.min(anomalies) < -200:
#             interpretations.append("Negative anomaly - possible void, cave, or sedimentary deposit")
        
        # Pattern detection
#         if np.std(anomalies) > 200:
#             interpretations.append("High variability - complex subsurface structure")
#         else:
#             interpretations.append("Low variability - homogeneous subsurface")
        
#         return interpretations
    
#     def upward_continuation(self, field: np.ndarray, grid_shape: Tuple[int, int],
#                            height: float) -> np.ndarray:
        """
#         Upward continuation - estimate field at higher altitude
#         Used for regional/residual separation
        """
#         print(f" Upward continuation to {height}m")
        
        # FFT-based upward continuation
#         field_2d = field.reshape(grid_shape)
        
        # Fourier transform
#         F = np.fft.fft2(field_2d)
        
        # Frequency domain upward continuation
#         ny, nx = grid_shape
#         kx = np.fft.fftfreq(nx)
#         ky = np.fft.fftfreq(ny)
#         KX, KY = np.meshgrid(kx, ky)
#         K = np.sqrt(KX**2 + KY**2)
        
        # Apply upward continuation operator
#         F_continued = F * np.exp(-2 * np.pi * K * height)
        
        # Inverse transform
#         continued = np.real(np.fft.ifft2(F_continued))
        
#         return continued.flatten()
    
#     def reduction_to_pole(self, field: np.ndarray, inclination: float,
#                          declination: float) -> np.ndarray:
        """
#         Reduction to pole - remove effects of magnetic latitude
#         Shows what field would look like at magnetic pole
        """
#         print(f" Reduction to pole (Inc={inclination:.1f}, Dec={declination:.1f})")
        
        # Simplified RTP (real version uses FFT)
        # This is a placeholder for the complex calculation
#         correction_factor = 1.0 / np.cos(np.deg2rad(inclination))
#         rtp_field = field * correction_factor
        
#         return rtp_field


# class ResistivityAnalyzer:
    """
#     Electrical resistivity analysis and inversion
#     Compete with AGI EarthImager, RES2DINV
    """
    
#     def process_survey(self, survey: ResistivitySurvey) -> Dict[str, Any]:
        """Process resistivity survey"""
#         print(f" Processing resistivity survey: {survey.num_measurements} measurements")
        
        # Statistics
#         stats = {
            'mean_resistivity': float(np.mean(survey.apparent_resistivity)),
            'std_resistivity': float(np.std(survey.apparent_resistivity)),
            'min_resistivity': float(np.min(survey.apparent_resistivity)),
            'max_resistivity': float(np.max(survey.apparent_resistivity)),
            'array_type': survey.array_type
        }
        
        # Classify materials based on resistivity
#         classifications = self._classify_materials(survey.apparent_resistivity)
        
#         print(f" Material classification complete")
        
#         return {
            'statistics': stats,
            'apparent_resistivity': survey.apparent_resistivity.tolist(),
            'classifications': classifications,
            'interpretation': self._interpret_resistivity(survey.apparent_resistivity)
        }
    
#     def _classify_materials(self, resistivity: np.ndarray) -> Dict[str, int]:
        """Classify subsurface materials by resistivity"""
        # Standard resistivity ranges (ohm-m)
        # Clay: 1-100
        # Groundwater/saturated soil: 10-100
        # Sand/gravel: 100-1000
        # Limestone: 100-10000
        # Sandstone: 100-1000
        # Granite: 1000-100000
        
#         classifications = {
            'clay_wet_soil': np.sum(resistivity < 100),
            'sand_gravel': np.sum((resistivity >= 100) & (resistivity < 1000)),
            'limestone_sandstone': np.sum((resistivity >= 1000) & (resistivity < 10000)),
            'bedrock_granite': np.sum(resistivity >= 10000)
        }
        
#         return {k: int(v) for k, v in classifications.items()}
    
#     def _interpret_resistivity(self, resistivity: np.ndarray) -> List[str]:
        """Interpret resistivity measurements"""
#         interpretations = []
        
#         mean_res = np.mean(resistivity)
        
#         if mean_res < 50:
#             interpretations.append("Low resistivity - clay-rich or water-saturated zone")
#             interpretations.append("Possible groundwater aquifer")
#         elif mean_res < 500:
#             interpretations.append("Moderate resistivity - sand, gravel, or weathered rock")
#         elif mean_res < 5000:
#             interpretations.append("High resistivity - competent rock (limestone, sandstone)")
#         else:
#             interpretations.append("Very high resistivity - crystalline bedrock (granite)")
        
        # Detect layering
#         if np.std(resistivity) > mean_res * 0.5:
#             interpretations.append("Stratified subsurface - multiple layers detected")
        
#         return interpretations
    
#     def invert_2d(self, survey: ResistivitySurvey, 
#                   max_iterations: int = 10) -> np.ndarray:
        """
        2D resistivity inversion
#         Convert apparent resistivity to true resistivity model
        """
#         print(f" Running 2D resistivity inversion ({max_iterations} iterations)")
        
        # Simplified inversion (real version uses iterative least-squares)
        # Create simple layered model
#         num_layers = 5
#         depth_layers = np.array([1, 2, 5, 10, 20])  # meters
        
        # Estimate layer resistivities (simplified)
#         resistivity_model = np.zeros(num_layers)
        
#         for i in range(num_layers):
            # Use measurements at appropriate depths
#             depth_mask = np.ones(len(survey.apparent_resistivity), dtype=bool)
#             resistivity_model[i] = np.median(survey.apparent_resistivity[depth_mask])
        
#         print(f" Inversion complete: {num_layers} layer model")
        
#         return resistivity_model


# class SeismicAnalyzer:
    """
#     Seismic data processing and interpretation
#     Compete with Schlumberger Petrel, Paradigm SeisSpace
    """
    
#     def process_survey(self, survey: SeismicSurvey) -> Dict[str, Any]:
        """Process seismic survey"""
#         print(f" Processing seismic survey: {survey.num_traces} traces")
        
        # Basic processing
#         stats = {
            'num_traces': survey.num_traces,
            'sample_rate': survey.sample_rate,
            'duration': survey.duration,
            'survey_type': survey.survey_type
        }
        
        # Signal analysis
#         amplitudes = np.abs(survey.traces)
#         max_amplitudes = np.max(amplitudes, axis=1)
        
#         print(f" Seismic processing complete")
        
#         return {
            'statistics': stats,
            'max_amplitudes': max_amplitudes.tolist()[:100],  # Limit size
            'interpretation': self._interpret_seismic(survey)
        }
    
#     def _interpret_seismic(self, survey: SeismicSurvey) -> List[str]:
        """Interpret seismic data"""
#         interpretations = []
        
        # Analyze first arrivals
#         first_breaks = self._pick_first_breaks(survey.traces)
        
#         if survey.survey_type == "refraction":
#             velocities = self._calculate_velocities(first_breaks, survey)
#             interpretations.append(f"Layer velocities: {velocities} m/s")
#         else:
#             interpretations.append("Reflection survey - subsurface imaging")
        
#         return interpretations
    
#     def _pick_first_breaks(self, traces: np.ndarray) -> np.ndarray:
        """Automatically pick first arrival times"""
        # Simplified: find first significant amplitude
#         threshold = np.std(traces) * 2
#         first_breaks = np.zeros(traces.shape[0])
        
#         for i, trace in enumerate(traces):
#             exceeds = np.where(np.abs(trace) > threshold)[0]
#             if len(exceeds) > 0:
#                 first_breaks[i] = exceeds[0]
        
#         return first_breaks
    
#     def _calculate_velocities(self, first_breaks: np.ndarray,
#                              survey: SeismicSurvey) -> List[float]:
        """Calculate layer velocities from refraction data"""
        # Simplified velocity analysis
        # Real version would use travel-time tomography
        
#         velocities = []
        
        # Typical subsurface velocities (m/s)
        # Soil: 300-600
        # Weathered rock: 600-1500
        # Bedrock: 1500-6000
        
#         if len(first_breaks) > 1:
            # Estimate from time-distance relationship
#             dt = np.diff(first_breaks) / survey.sample_rate
#             if len(dt) > 0:
#                 velocities = [500, 1200, 3000]  # Simplified 3-layer model
        
#         return velocities
    
#     def apply_agc(self, traces: np.ndarray, window_size: int = 100) -> np.ndarray:
        """
#         Automatic Gain Control (AGC)
#         Enhance weak signals at depth
        """
#         print(f" Applying AGC (window={window_size} samples)")
        
#         agc_traces = np.zeros_like(traces)
        
#         for i, trace in enumerate(traces):
            # Running RMS amplitude
#             for j in range(len(trace)):
#                 start = max(0, j - window_size // 2)
#                 end = min(len(trace), j + window_size // 2)
#                 rms = np.sqrt(np.mean(trace[start:end]**2))
#                 agc_traces[i, j] = trace[j] / (rms + 1e-10)
        
#         return agc_traces


# class MiningMagnetometryProcessor:
    """
#      MINING-SPECIFIC MAGNETOMETRY PROCESSOR
#     Process cheaper MAG surveys for mineral exploration
    - Import common formats (XYZ, CSV, Geosoft)
    - IGRF correction
    - Anomaly detection & discrimination
    - Mineral target identification
    """
    
#     def __init__(self):
#         self.igrf = IGRFModel()
#         self.mag_analyzer = MagneticAnalyzer()
    
#     def import_mag_survey(self, filepath: str, format_type: str = "xyz") -> MagneticSurvey:
        """
#         Import MAG survey from common formats
        
#         Formats:
        - xyz: Space/tab delimited (X Y Z TMI)
        - csv: Comma separated
        - geosoft: Geosoft XYZ format
        """
#         print(f" Importing MAG survey from {filepath} (format: {format_type})")
        
#         if format_type == "xyz" or format_type == "csv":
#             delimiter = ',' if format_type == "csv" else None
            # Read data (X, Y, Z, Total_Magnetic_Intensity)
            # data = np.loadtxt(filepath, delimiter=delimiter)
            # For demo, create synthetic data
#             data = self._generate_synthetic_mag_data()
#         else:
#             data = self._generate_synthetic_mag_data()
        
#         locations = data[:, :3]  # X, Y, Z (or Lat, Lon, Elev)
#         total_field = data[:, 3]  # TMI in nT
        
#         survey = MagneticSurvey(
#             locations=locations,
#             total_field=total_field,
#             date=datetime.now(),
#             instrument="proton_magnetometer"
        
#         print(f" Loaded {survey.num_stations} measurement stations")
#         return survey
    
#     def _generate_synthetic_mag_data(self, num_stations: int = 100) -> np.ndarray:
        """Generate synthetic MAG survey for demo"""
        # Create grid of measurements
#         x = np.linspace(0, 1000, int(np.sqrt(num_stations)))
#         y = np.linspace(0, 1000, int(np.sqrt(num_stations)))
#         X, Y = np.meshgrid(x, y)
        
        # Add synthetic magnetic anomalies
        # Anomaly 1: Strong positive (possible magnetite deposit)
#         center1 = (400, 600)
#         dist1 = np.sqrt((X - center1[0])**2 + (Y - center1[1])**2)
#         anomaly1 = 500 * np.exp(-(dist1**2) / (100**2))
        
        # Anomaly 2: Moderate positive (possible igneous intrusion)
#         center2 = (700, 300)
#         dist2 = np.sqrt((X - center2[0])**2 + (Y - center2[1])**2)
#         anomaly2 = 300 * np.exp(-(dist2**2) / (150**2))
        
        # Anomaly 3: Negative (possible void or sedimentary)
#         center3 = (200, 200)
#         dist3 = np.sqrt((X - center3[0])**2 + (Y - center3[1])**2)
#         anomaly3 = -150 * np.exp(-(dist3**2) / (80**2))
        
        # Background field (IGRF-like)
#         background = 50000  # nT
        
        # Total field
#         TMI = background + anomaly1 + anomaly2 + anomaly3
        
        # Add noise
#         TMI += np.random.normal(0, 10, TMI.shape)
        
        # Flatten to array
#         locations = np.column_stack([X.flatten(), Y.flatten(), np.zeros(len(X.flatten()))])
#         data = np.column_stack([locations, TMI.flatten()])
        
#         return data
    
#     def discriminate_minerals(self, survey: MagneticSurvey) -> Dict[str, Any]:
        """
#          MINERAL DISCRIMINATION FROM MAG DATA
#         Identify potential ore types based on magnetic signature
        """
#         print(f" Discriminating minerals from magnetic signature...")
        
        # Remove IGRF background
#         anomalies = survey.remove_igrf(self.igrf)
        
        # Calculate statistics
#         mean_anom = np.mean(anomalies)
#         std_anom = np.std(anomalies)
#         max_anom = np.max(anomalies)
#         min_anom = np.min(anomalies)
        
        # Mineral discrimination based on magnetic intensity
#         targets = []
        
        # 1. IRON-RICH DEPOSITS (Magnetite, Hematite)
#         iron_threshold = mean_anom + 3 * std_anom
#         iron_mask = anomalies > iron_threshold
#         if np.sum(iron_mask) > 0:
#             iron_locations = survey.locations[iron_mask]
#             targets.append({
                'mineral_type': 'iron_magnetite',
                'confidence': 'high',
                'num_targets': int(np.sum(iron_mask)),
                'max_anomaly': float(np.max(anomalies[iron_mask])),
                'description': 'Strong positive anomaly - likely magnetite or Fe-rich deposit',
                'drill_priority': 1,
                'locations': iron_locations.tolist()[:10]  # Top 10
            })
        
        # 2. COPPER/GOLD (Associated with magnetic alteration)
#         cu_au_threshold_low = mean_anom + 1.5 * std_anom
#         cu_au_threshold_high = iron_threshold
#         cu_au_mask = (anomalies > cu_au_threshold_low) & (anomalies < cu_au_threshold_high)
#         if np.sum(cu_au_mask) > 0:
#             cu_au_locations = survey.locations[cu_au_mask]
#             targets.append({
                'mineral_type': 'copper_gold_association',
                'confidence': 'medium',
                'num_targets': int(np.sum(cu_au_mask)),
                'max_anomaly': float(np.max(anomalies[cu_au_mask])),
                'description': 'Moderate positive anomaly - possible Cu-Au with magnetic alteration',
                'drill_priority': 2,
                'locations': cu_au_locations.tolist()[:10]
            })
        
        # 3. ULTRAMAFIC/NICKEL
        # Look for specific patterns: elongated anomalies, moderate strength
#         ultramafic_threshold = mean_anom + 2 * std_anom
#         ultramafic_mask = (anomalies > ultramafic_threshold) & (anomalies < iron_threshold)
#         if np.sum(ultramafic_mask) > 5:  # Need cluster
#             ultramafic_locations = survey.locations[ultramafic_mask]
#             targets.append({
                'mineral_type': 'ultramafic_nickel',
                'confidence': 'medium',
                'num_targets': int(np.sum(ultramafic_mask)),
                'max_anomaly': float(np.max(anomalies[ultramafic_mask])),
                'description': 'Clustered moderate anomalies - possible ultramafic intrusion (Ni potential)',
                'drill_priority': 3,
                'locations': ultramafic_locations.tolist()[:10]
            })
        
        # 4. NON-MAGNETIC (Negative or low anomaly)
        # Could indicate sediment-hosted deposits, kimberlites
#         negative_threshold = mean_anom - 2 * std_anom
#         negative_mask = anomalies < negative_threshold
#         if np.sum(negative_mask) > 0:
#             negative_locations = survey.locations[negative_mask]
#             targets.append({
                'mineral_type': 'non_magnetic_sedimentary',
                'confidence': 'low',
                'num_targets': int(np.sum(negative_mask)),
                'min_anomaly': float(np.min(anomalies[negative_mask])),
                'description': 'Negative anomaly - possible sedimentary basin, kimberlite, or void',
                'drill_priority': 4,
                'locations': negative_locations.tolist()[:10]
            })
        
        # Summary statistics
#         summary = {
            'survey_stats': {
                'total_stations': survey.num_stations,
                'mean_anomaly_nT': float(mean_anom),
                'std_anomaly_nT': float(std_anom),
                'max_anomaly_nT': float(max_anom),
                'min_anomaly_nT': float(min_anom),
                'range_nT': float(max_anom - min_anom)
            },
            'targets': targets,
            'num_target_types': len(targets),
            'recommended_drill_targets': [t for t in targets if t['drill_priority'] <= 2]
        }
        
#         print(f" Found {len(targets)} potential mineral targets")
#         print(f" Recommended {len(summary['recommended_drill_targets'])} high-priority drill targets")
        
#         return summary
    
#     def grid_and_contour(self, survey: MagneticSurvey, grid_size: int = 50) -> Dict[str, Any]:
        """
#         Grid MAG data and create contour map
#         Output suitable for visualization
        """
#         print(f" Gridding MAG data ({grid_size}x{grid_size} grid)...")
        
        # Remove IGRF
#         anomalies = survey.remove_igrf(self.igrf)
        
        # Create regular grid
#         x = survey.locations[:, 0]
#         y = survey.locations[:, 1]
        
#         x_min, x_max = np.min(x), np.max(x)
#         y_min, y_max = np.min(y), np.max(y)
        
#         xi = np.linspace(x_min, x_max, grid_size)
#         yi = np.linspace(y_min, y_max, grid_size)
#         XI, YI = np.meshgrid(xi, yi)
        
        # Interpolate to grid (simplified - use nearest neighbor)
#         from scipy.interpolate import griddata
#         ZI = griddata((x, y), anomalies, (XI, YI), method='cubic', fill_value=0)
        
        # Calculate contour levels
#         levels = np.linspace(np.min(anomalies), np.max(anomalies), 10)
        
#         print(f" Grid created: {grid_size}x{grid_size}")
        
#         return {
            'grid': {
                'x': XI.tolist(),
                'y': YI.tolist(),
                'z_anomaly': ZI.tolist(),
                'shape': [grid_size, grid_size]
            },
            'contour_levels': levels.tolist(),
            'bounds': {
                'x_min': float(x_min),
                'x_max': float(x_max),
                'y_min': float(y_min),
                'y_max': float(y_max)
            }
        }
    
#     def export_drill_targets(self, discrimination_result: Dict[str, Any], 
#                             output_format: str = "csv") -> str:
        """
#         Export drill targets to file
#         Formats: csv, kml, shapefile
        """
#         print(f" Exporting drill targets to {output_format}...")
        
#         targets = discrimination_result['targets']
        
        # CSV format
#         if output_format == "csv":
#             csv_data = "Target_ID,Mineral_Type,Confidence,Priority,X,Y,Anomaly_nT\n"
            
#             target_id = 1
#             for target in targets:
#                 if 'locations' in target and len(target['locations']) > 0:
#                     for loc in target['locations']:
#                         anomaly_val = target.get('max_anomaly', target.get('min_anomaly', 0))
#                         csv_data += f"{target_id},{target['mineral_type']},{target['confidence']},"
#                         csv_data += f"{target['drill_priority']},{loc[0]:.2f},{loc[1]:.2f},{anomaly_val:.1f}\n"
#                         target_id += 1
            
#             print(f" Exported {target_id-1} drill targets")
#             return csv_data
        
#         return "Format not supported"


# class SubsurfaceModeler:
    """
#     Multi-physics 3D subsurface modeling
#     Integrate magnetic, resistivity, seismic data
    """
    
#     def __init__(self):
#         self.magnetic_analyzer = MagneticAnalyzer()
#         self.resistivity_analyzer = ResistivityAnalyzer()
#         self.seismic_analyzer = SeismicAnalyzer()
#         self.mining_mag_processor = MiningMagnetometryProcessor()
    
#     def create_3d_model(self, 
#                        magnetic_survey: Optional[MagneticSurvey] = None,
#                        resistivity_survey: Optional[ResistivitySurvey] = None,
#                        seismic_survey: Optional[SeismicSurvey] = None,
#                        grid_size: Tuple[int, int, int] = (50, 50, 20)) -> Dict[str, Any]:
        """
#         Create integrated 3D subsurface model
#         Combines multiple geophysical datasets
        """
#         print(f" Creating 3D subsurface model ({grid_size[0]}x{grid_size[1]}x{grid_size[2]})")
        
#         nx, ny, nz = grid_size
        
        # Initialize property models
#         magnetic_susceptibility = np.zeros(grid_size)
#         resistivity_3d = np.ones(grid_size) * 100  # Default 100 ohm-m
#         seismic_velocity = np.ones(grid_size) * 2000  # Default 2000 m/s
        
        # Integrate magnetic data
#         if magnetic_survey:
#             mag_result = self.magnetic_analyzer.process_survey(magnetic_survey)
            # Map anomalies to 3D susceptibility model
            # Simplified: use surface anomalies to infer depth
            
        # Integrate resistivity data
#         if resistivity_survey:
#             res_result = self.resistivity_analyzer.process_survey(resistivity_survey)
#             res_model = self.resistivity_analyzer.invert_2d(resistivity_survey)
            # Map to 3D grid
#             for i, res in enumerate(res_model):
#                 if i < nz:
#                     resistivity_3d[:, :, i] = res
        
        # Integrate seismic data
#         if seismic_survey:
#             seis_result = self.seismic_analyzer.process_survey(seismic_survey)
            # Map velocity model to 3D
        
#         print(f" 3D model created")
        
#         return {
            'grid_size': grid_size,
            'magnetic_susceptibility': {
                'shape': magnetic_susceptibility.shape,
                'mean': float(np.mean(magnetic_susceptibility)),
                'std': float(np.std(magnetic_susceptibility))
            },
            'resistivity': {
                'shape': resistivity_3d.shape,
                'mean': float(np.mean(resistivity_3d)),
                'min': float(np.min(resistivity_3d)),
                'max': float(np.max(resistivity_3d))
            },
            'seismic_velocity': {
                'shape': seismic_velocity.shape,
                'mean': float(np.mean(seismic_velocity)),
                'min': float(np.min(seismic_velocity)),
                'max': float(np.max(seismic_velocity))
            },
            'interpretation': self._interpret_model(magnetic_susceptibility, 
#                                                    resistivity_3d, 
#                                                    seismic_velocity)
        }
    
#     def _interpret_model(self, susceptibility: np.ndarray,
#                         resistivity: np.ndarray,
#                         velocity: np.ndarray) -> List[str]:
        """Interpret integrated 3D model"""
#         interpretations = []
        
        # Look for correlations between properties
#         high_susceptibility = np.mean(susceptibility) > 0.01
#         low_resistivity = np.mean(resistivity) < 100
#         high_resistivity = np.mean(resistivity) > 1000
#         high_velocity = np.mean(velocity) > 3000
        
#         if high_susceptibility and low_resistivity:
#             interpretations.append("Magnetic + conductive body - possible magnetite deposit")
        
#         if low_resistivity and not high_velocity:
#             interpretations.append("Conductive + low velocity - groundwater aquifer")
        
#         if high_velocity and high_resistivity:
#             interpretations.append("High velocity + resistive - crystalline bedrock")
        
        # Depth analysis
#         if np.std(resistivity) > np.mean(resistivity) * 0.5:
#             interpretations.append("Stratified subsurface - multiple geological layers")
        
#         return interpretations


# Export main classes
__all__ = [
    'IGRFModel',
    'WMMModel',
    'MagneticSurvey',
    'ResistivitySurvey',
    'SeismicSurvey',
    'MagneticAnalyzer',
    'ResistivityAnalyzer',
    'SeismicAnalyzer',
    'SubsurfaceModeler',
    'MiningMagnetometryProcessor',  # NEW: Mining-specific MAG processing
    'GeophysicsDataType'
]
