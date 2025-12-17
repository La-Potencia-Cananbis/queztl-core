import numpy as np
from datetime import datetime
from typing import Any, Dict, List, Tuple

class IGRFModel:
    """Stub for IGRFModel with minimal coefficients and reference radius."""
    def __init__(self):
        self.coefficients = {'g10': 0, 'g11': 0, 'h11': 0}
        self.reference_radius = 6371.2

class MagneticSurvey:
    """Stub for MagneticSurvey with required attributes and methods."""
    def __init__(self, locations=None, total_field=None, date=None, instrument=None):
        self.locations = locations if locations is not None else np.zeros((10,3))
        self.total_field = total_field if total_field is not None else np.zeros(10)
        self.date = date if date is not None else datetime.now()
        self.instrument = instrument if instrument is not None else "unknown"
        self.num_stations = self.locations.shape[0]
    def remove_igrf(self, igrf_model):
        # Dummy: just subtract mean for demo
        return self.total_field - np.mean(self.total_field)

class ResistivitySurvey:
    """Stub for ResistivitySurvey with required attributes."""
    def __init__(self):
        self.apparent_resistivity = np.ones(10) * 100
        self.array_type = "Wenner"
        self.num_measurements = 10

class SeismicSurvey:
    """Stub for SeismicSurvey with required attributes."""
    def __init__(self):
        self.num_traces = 10
        self.sample_rate = 1000
        self.duration = 10.0
        self.survey_type = "refraction"
        self.traces = np.random.randn(10, 1000)

class GeophysicsDataType:
    pass

class WMMModel:
    pass

class MagneticAnalyzer:
    pass

class ResistivityAnalyzer:
    pass

class MiningMagnetometryProcessor:
    pass

class SubsurfaceModeler:
    pass

class SeismicAnalyzer:
    pass

__all__ = [
    "IGRFModel",
    "WMMModel",
    "MagneticSurvey",
    "ResistivitySurvey",
    "SeismicSurvey",
    "MagneticAnalyzer",
    "ResistivityAnalyzer",
    "SeismicAnalyzer",
    "SubsurfaceModeler",
    "MiningMagnetometryProcessor",
    "GeophysicsDataType"
]
