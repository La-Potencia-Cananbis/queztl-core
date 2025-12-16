"""
# Real Shap-E Integration for Gen3D
# Uses OpenAI's actual Shap-E models for text-to-3D generation
"""
# import torch
# import numpy as np
# import asyncio
# from concurrent.futures import ThreadPoolExecutor
# from typing import Optional
# import logging

# logger = logging.getLogger(__name__)

# class ShapEGenerator:
    """Real Shap-E text-to-3D generator using OpenAI models"""
    
#     def __init__(self):
#         self.device = "cuda" if torch.cuda.is_available() else "cpu"
#         self.xm = None
#         self.model = None
#         self.diffusion = None
#         self.executor = ThreadPoolExecutor(max_workers=2)
#         logger.info(f"ShapEGenerator initialized on device: {self.device}")
    
#     def _load_models(self):
        """Load Shap-E models from OpenAI (downloads on first run)"""
#         if self.model is not None:
#             return
        
#         try:
#             logger.info("Loading Shap-E models from OpenAI... (first run will download ~1GB)")
#             from shap_e.diffusion.sample import sample_latents
#             from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
#             from shap_e.models.download import load_model, load_config
#             from shap_e.util.notebooks import decode_latent_mesh
            
            # Load models
#             self.xm = load_model('transmitter', device=self.device)
#             self.model = load_model('text300M', device=self.device)
#             self.diffusion = diffusion_from_config(load_config('diffusion'))
            
            # Store functions
#             self.sample_latents = sample_latents
#             self.decode_latent_mesh = decode_latent_mesh
            
#             logger.info(" Shap-E models loaded successfully!")
            
#         except Exception as e:
#             logger.error(f"Failed to load Shap-E models: {e}")
#             raise
    
#     async def generate_from_text(self, prompt: str, guidance_scale: float = 15.0) -> dict:
        """Generate 3D mesh from text prompt using real Shap-E"""
#         try:
            # Load models if needed
#             if self.model is None:
#                 self._load_models()
            
#             logger.info(f"Generating 3D with Shap-E: '{prompt}'")
            
            # Generate in thread to avoid blocking
#             loop = asyncio.get_event_loop()
#             mesh_data = await loop.run_in_executor(
#                 self.executor,
#                 self._run_shap_e,
#                 prompt,
#                 guidance_scale
            
#             return mesh_data
            
#         except Exception as e:
#             logger.error(f"Shap-E generation failed: {e}")
#             raise
    
#     def _run_shap_e(self, prompt: str, guidance_scale: float) -> dict:
        """Run Shap-E generation in thread"""
#         try:
#             batch_size = 1
            
            # Sample latents using diffusion
#             latents = self.sample_latents(
#                 batch_size=batch_size,
#                 model=self.model,
#                 diffusion=self.diffusion,
#                 guidance_scale=guidance_scale,
#                 model_kwargs=dict(texts=[prompt] * batch_size),
#                 progress=False,
#                 clip_denoised=True,
#                 use_fp16=True,
#                 use_karras=True,
#                 karras_steps=64,
#                 sigma_min=1e-3,
#                 sigma_max=160,
#                 s_churn=0,
            
            # Decode latent to mesh
#             latent = latents[0]
#             torch_mesh = self.decode_latent_mesh(self.xm, latent)
#             tri_mesh = torch_mesh.tri_mesh()
            
            # Convert to numpy
#             vertices = tri_mesh.verts.astype(np.float32)
#             faces = tri_mesh.faces.astype(np.int32)
            
            # Compute normals
#             normals = self._compute_normals(vertices, faces)
            
#             return {
                'vertices': vertices,
                'faces': faces.flatten(),
                'normals': normals,
                'vertex_count': len(vertices),
                'face_count': len(faces)
            }
            
#         except Exception as e:
#             logger.error(f"Shap-E execution failed: {e}")
#             raise
    
#     def _compute_normals(self, vertices: np.ndarray, faces: np.ndarray) -> np.ndarray:
        """Compute vertex normals from faces"""
#         normals = np.zeros_like(vertices)
        
#         for face in faces:
#             if len(face) >= 3:
#                 v1, v2, v3 = vertices[face[:3]]
#                 edge1 = v2 - v1
#                 edge2 = v3 - v1
#                 face_normal = np.cross(edge1, edge2)
                
#                 normals[face[0]] += face_normal
#                 normals[face[1]] += face_normal
#                 normals[face[2]] += face_normal
        
        # Normalize
#         norms = np.linalg.norm(normals, axis=1, keepdims=True)
#         norms[norms == 0] = 1
#         normals = normals / norms
        
#         return normals.astype(np.float32)
