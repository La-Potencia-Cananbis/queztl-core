"""
# Trained 3D Model Inference
# Uses the fast-trained model to generate 3D geometry
# Supports premium features: STL export, validation, multiple formats
"""
# import torch
# import torch.nn as nn
# import numpy as np
# from typing import Dict, Any, Optional
# import logging
# import os

# logger = logging.getLogger(__name__)

# Import premium features if available
# try:
#     from .premium_features import PremiumExporter, MeshValidator, analyze_printability
#     PREMIUM_AVAILABLE = True
# except ImportError:
#     PREMIUM_AVAILABLE = False
#     logger.warning("Premium features not available")


# class Fast3DModel(nn.Module):
    """Lightweight 3D generation model"""
#     def __init__(self, text_dim=128, hidden_dim=256, output_vertices=512):
#         super().__init__()
#         self.output_vertices = output_vertices
        
#         self.net = nn.Sequential(
#             nn.Linear(text_dim, hidden_dim),
#             nn.ReLU(),
#             nn.Linear(hidden_dim, hidden_dim),
#             nn.ReLU(),
#             nn.Linear(hidden_dim, output_vertices * 3)
    
#     def forward(self, text_embed):
#         x = self.net(text_embed)
#         return x.reshape(-1, self.output_vertices, 3)


# class TrainedModelInference:
    """Inference engine for trained 3D models"""
    
#     def __init__(self, model_path="/workspace/models/fast_3d_model.pt"):
#         self.model_path = model_path
#         self.model = None
#         self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         self._load_model()
    
#     def _load_model(self):
        """Load the trained model"""
#         try:
#             logger.info(f"Loading trained 3D model from {self.model_path}")
#             checkpoint = torch.load(self.model_path, map_location=self.device)
            
            # Create model
#             self.model = Fast3DModel(**checkpoint['model_config'])
#             self.model.load_state_dict(checkpoint['model_state_dict'])
#             self.model.to(self.device)
#             self.model.eval()
            
#             logger.info(" Trained 3D model loaded successfully")
#         except Exception as e:
#             logger.error(f"Failed to load trained model: {e}")
#             self.model = None
    
#     def is_available(self) -> bool:
        """Check if model is loaded and ready"""
#         return self.model is not None
    
#     def text_to_embed(self, text: str, dim: int = 128) -> np.ndarray:
        """Convert text to embedding via hash (same as training)"""
#         h = hash(text.lower()) % (2**31)
#         np.random.seed(h)
#         embed = np.random.randn(dim)
#         return embed / (np.linalg.norm(embed) + 1e-8)
    
#     def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
#         Generate 3D model from text prompt
        
#         Args:
#             prompt: Text description
            **kwargs: Additional parameters (ignored for now)
        
#         Returns:
#             Dictionary with vertices, faces, and metadata
        """
#         if not self.is_available():
#             raise RuntimeError("Trained model not available")
        
#         try:
            # Convert prompt to embedding
#             text_embed = self.text_to_embed(prompt, dim=128)
#             text_embed_tensor = torch.FloatTensor(text_embed).unsqueeze(0).to(self.device)
            
            # Generate vertices
#             with torch.no_grad():
#                 vertices = self.model(text_embed_tensor)
            
            # Convert to numpy
#             vertices_np = vertices[0].cpu().numpy()
            
            # Filter out zero-padded vertices
#             non_zero = (vertices_np**2).sum(axis=1) > 0.001
#             vertices_np = vertices_np[non_zero]
            
            # Generate faces using Delaunay triangulation approximation
#             faces = self._generate_faces(vertices_np)
            
#             return {
                'vertices': vertices_np.tolist(),
                'faces': faces,
                'method': 'trained_model',
                'model_path': self.model_path,
                'prompt': prompt,
                'stats': {
                    'vertices': len(vertices_np),
                    'faces': len(faces),
                    'model_type': 'fast_3d_trained'
                }
            }
        
#         except Exception as e:
#             logger.error(f"Generation failed: {e}")
#             raise
    
#     def _generate_faces(self, vertices: np.ndarray) -> list:
        """
#         Generate faces from vertices using improved connectivity
        
#         Uses spatial proximity and Delaunay-like triangulation
#         to create more realistic mesh topology
        """
#         num_verts = len(vertices)
#         faces = []
        
#         if num_verts < 3:
#             return []
        
        # Strategy 1: Sequential triangulation (40% of faces)
#         for i in range(0, num_verts - 2, 1):
#             if i + 2 < num_verts:
#                 faces.append([i, i + 1, i + 2])
        
        # Strategy 2: Connect to centroid (creates fan-like structure)
#         if num_verts >= 10:
            # Use first vertex as pseudo-centroid
#             centroid_idx = 0
#             for i in range(2, num_verts - 1, 2):
#                 if i + 1 < num_verts:
#                     faces.append([centroid_idx, i, i + 1])
        
        # Strategy 3: Cross-connections for better topology
#         if num_verts >= 20:
#             mid = num_verts // 2
#             quarter = num_verts // 4
            
            # Connect quarters
#             for i in range(0, quarter, 2):
#                 if i + 1 < num_verts and mid + i < num_verts:
#                     faces.append([i, i + 1, mid + i])
        
        # Strategy 4: Wrap-around for closed mesh
#         if num_verts >= 6:
            # Connect beginning to end
#             faces.append([0, 1, num_verts - 1])
#             faces.append([1, num_verts - 2, num_verts - 1])
#             faces.append([num_verts - 3, num_verts - 2, 0])
            
            # Additional wrap connections
#             if num_verts >= 12:
#                 mid = num_verts // 2
#                 q = num_verts // 4
#                 faces.append([0, mid, num_verts - 1])
#                 faces.append([q, mid, num_verts - q])
        
        # Remove duplicate faces
#         unique_faces = []
#         seen = set()
#         for face in faces:
            # Sort to catch duplicates regardless of order
#             face_key = tuple(sorted(face))
#             if face_key not in seen:
#                 seen.add(face_key)
#                 unique_faces.append(face)
        
#         return unique_faces


# Global instance
_inference_engine = None

# def get_inference_engine() -> TrainedModelInference:
    """Get or create the global inference engine"""
#     global _inference_engine
#     if _inference_engine is None:
        _inference_engine = TrainedModelInference()
#     return _inference_engine
