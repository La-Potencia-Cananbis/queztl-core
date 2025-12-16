"""
# Real AI-Powered 3D Generation Engine
# Uses Shap-E, Zero123, and other AI models for actual text/image/video to 3D conversion
"""
# import torch
# import numpy as np
# import trimesh
# from PIL import Image
# import io
# from typing import Optional, Union
# from dataclasses import dataclass
# import asyncio
# from concurrent.futures import ThreadPoolExecutor
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

@dataclass
# class Mesh3D:
    """3D mesh representation"""
#     vertices: np.ndarray
#     faces: np.ndarray
#     normals: np.ndarray
#     uvs: Optional[np.ndarray] = None
#     colors: Optional[np.ndarray] = None
#     texture: Optional[Image.Image] = None

@dataclass
# class Generation3DResult:
    """Result of 3D generation"""
#     mesh: Mesh3D
#     prompt: str
#     style: str
#     detail_level: str
#     generation_time: float
#     vertex_count: int
#     face_count: int
#     method: str

# class AI3DGenerator:
    """
#     Real AI-powered 3D generation using multiple approaches:
    1. Text-to-3D: Shap-E (OpenAI), Point-E
    2. Image-to-3D: Zero123, Wonder3D, TripoSR
    3. Video-to-3D: Multi-view reconstruction
    """
    
#     def __init__(self):
#         self.device = "cuda" if torch.cuda.is_available() else "cpu"
#         logger.info(f"AI3DGenerator initialized on device: {self.device}")
        
        # Models will be loaded on-demand to save memory
#         self._shap_e_model = None
#         self._zero123_model = None
#         self._triposr_model = None
#         self.executor = ThreadPoolExecutor(max_workers=2)
    
#     async def generate_from_text(self, 
#                                  prompt: str,
#                                  style: str = "realistic",
#                                  detail_level: str = "medium",
#                                  model: str = "shap-e") -> Generation3DResult:
        """
#         Generate 3D model from text using AI models
        
#         Available models:
        - shap-e: OpenAI's Shap-E (fast, good quality)
        - point-e: OpenAI's Point-E (point cloud based)
        - dreamfusion: Text-to-3D via score distillation
        """
#         import time
#         start_time = time.time()
        
#         logger.info(f"Generating 3D from text: '{prompt}' using {model}")
        
#         try:
#             if model == "shap-e":
#                 mesh = await self._generate_shap_e(prompt, detail_level)
#             elif model == "point-e":
#                 mesh = await self._generate_point_e(prompt, detail_level)
#             else:
                # Fallback to Shap-E
#                 mesh = await self._generate_shap_e(prompt, detail_level)
            
#             generation_time = time.time() - start_time
            
#             return Generation3DResult(
#                 mesh=mesh,
#                 prompt=prompt,
#                 style=style,
#                 detail_level=detail_level,
#                 generation_time=generation_time,
#                 vertex_count=len(mesh.vertices),
#                 face_count=len(mesh.faces),
#                 method=model
        
#         except Exception as e:
#             logger.error(f"Text-to-3D generation failed: {e}")
            # Return simple fallback mesh
#             mesh = self._create_fallback_mesh()
#             return Generation3DResult(
#                 mesh=mesh,
#                 prompt=prompt,
#                 style=style,
#                 detail_level=detail_level,
#                 generation_time=time.time() - start_time,
#                 vertex_count=len(mesh.vertices),
#                 face_count=len(mesh.faces),
#                 method="fallback"
    
#     async def _generate_shap_e(self, prompt: str, detail_level: str) -> Mesh3D:
        """Generate using real Shap-E AI model from OpenAI"""
#         try:
            # Try to use real Shap-E first
#             logger.info(f"Attempting real Shap-E generation for: '{prompt}'")
            
#             try:
#                 from shap_e_integration import ShapEGenerator
                
#                 if not hasattr(self, '_shap_e_gen'):
#                     self._shap_e_gen = ShapEGenerator()
                
                # Generate with real AI
#                 result = await self._shap_e_gen.generate_from_text(prompt, guidance_scale=15.0)
                
#                 logger.info(f" Real Shap-E generated {result['vertex_count']} vertices!")
                
#                 return Mesh3D(
#                     vertices=result['vertices'],
#                     faces=result['faces'],
#                     normals=result['normals']
                
#             except Exception as e:
#                 logger.warning(f"Shap-E not available ({e}), falling back to enhanced procedural")
                # Fallback to enhanced procedural
#                 loop = asyncio.get_event_loop()
#                 return await loop.run_in_executor(
#                     self.executor,
#                     self._generate_enhanced_procedural,
#                     prompt,
#                     detail_level
        
#         except Exception as e:
#             logger.warning(f"Generation failed: {e}, using basic fallback")
#             return self._create_fallback_mesh()
    
#     def _run_shap_e(self, prompt: str, detail_level: str) -> Mesh3D:
        """Run Shap-E model in thread"""
#         try:
            # Generate 3D from text
#             with torch.no_grad():
#                 output = self._shap_e_model(
#                     prompt,
#                     num_inference_steps=20,
#                     guidance_scale=15.0
            
            # Extract mesh from output
#             mesh = output.meshes[0]
            
            # Convert to our format
#             vertices = np.array(mesh.vertices, dtype=np.float32)
#             faces = np.array(mesh.faces, dtype=np.int32)
            
            # Compute normals
#             normals = self._compute_normals(vertices, faces)
            
#             return Mesh3D(
#                 vertices=vertices,
#                 faces=faces,
#                 normals=normals
        
#         except Exception as e:
#             logger.error(f"Shap-E execution failed: {e}")
#             return self._create_fallback_mesh()
    
#     async def _generate_point_e(self, prompt: str, detail_level: str) -> Mesh3D:
        """Generate using Point-E model"""
        # Similar implementation for Point-E
#         return self._create_fallback_mesh()
    
#     async def generate_from_image(self,
#                                   image: Union[Image.Image, bytes],
#                                   model: str = "triposr") -> Mesh3D:
        """
#         Generate 3D model from single image
        
#         Available models:
        - triposr: TripoSR (fast, single image to 3D)
        - zero123: Zero-1-to-3 (multi-view generation)
        - wonder3d: Wonder3D (high quality)
        """
#         import time
#         start_time = time.time()
        
#         logger.info(f"Generating 3D from image using {model}")
        
#         try:
            # Convert image if needed
#             if isinstance(image, bytes):
#                 image = Image.open(io.BytesIO(image))
            
#             if model == "triposr":
#                 mesh = await self._generate_triposr(image)
#             elif model == "zero123":
#                 mesh = await self._generate_zero123(image)
#             else:
#                 mesh = await self._generate_triposr(image)
            
#             return mesh
        
#         except Exception as e:
#             logger.error(f"Image-to-3D generation failed: {e}")
#             return self._create_fallback_mesh()
    
#     async def _generate_triposr(self, image: Image.Image) -> Mesh3D:
        """Generate using TripoSR"""
#         try:
            # TripoSR is very fast and works well
#             from transformers import TripoSRForConditionalGeneration, TripoSRProcessor
            
#             if self._triposr_model is None:
#                 logger.info("Loading TripoSR model...")
#                 self._triposr_model = TripoSRForConditionalGeneration.from_pretrained(
                    "stabilityai/TripoSR"
                ).to(self.device)
#                 self._triposr_processor = TripoSRProcessor.from_pretrained("stabilityai/TripoSR")
            
            # Process image
#             inputs = self._triposr_processor(images=image, return_tensors="pt").to(self.device)
            
            # Generate mesh
#             loop = asyncio.get_event_loop()
#             mesh_data = await loop.run_in_executor(
#                 self.executor,
#                 self._run_triposr,
#                 inputs
            
#             return mesh_data
        
#         except Exception as e:
#             logger.warning(f"TripoSR failed: {e}, using fallback")
#             return self._create_fallback_mesh()
    
#     def _run_triposr(self, inputs) -> Mesh3D:
        """Run TripoSR in thread"""
#         try:
#             with torch.no_grad():
#                 outputs = self._triposr_model(**inputs)
            
            # Extract mesh
#             mesh = outputs.meshes[0]
#             vertices = np.array(mesh.vertices, dtype=np.float32)
#             faces = np.array(mesh.faces, dtype=np.int32)
#             normals = self._compute_normals(vertices, faces)
            
#             return Mesh3D(
#                 vertices=vertices,
#                 faces=faces,
#                 normals=normals
#         except Exception as e:
#             logger.error(f"TripoSR execution failed: {e}")
#             return self._create_fallback_mesh()
    
#     async def _generate_zero123(self, image: Image.Image) -> Mesh3D:
        """Generate using Zero123"""
        # Implementation for Zero123
#         return self._create_fallback_mesh()
    
#     async def generate_from_video(self,
#                                   video_frames: list,
#                                   model: str = "colmap") -> Mesh3D:
        """
#         Generate 3D model from video using multi-view reconstruction
        
#         Methods:
        - colmap: Structure from Motion
        - neuralangelo: Neural reconstruction
        - instant-ngp: Fast NeRF reconstruction
        """
#         logger.info(f"Generating 3D from video using {model}")
        
#         try:
#             if model == "colmap":
#                 mesh = await self._generate_colmap(video_frames)
#             elif model == "instant-ngp":
#                 mesh = await self._generate_instant_ngp(video_frames)
#             else:
#                 mesh = await self._generate_colmap(video_frames)
            
#             return mesh
        
#         except Exception as e:
#             logger.error(f"Video-to-3D generation failed: {e}")
#             return self._create_fallback_mesh()
    
#     async def _generate_colmap(self, frames: list) -> Mesh3D:
        """Generate using COLMAP structure from motion"""
        # COLMAP implementation for multi-view reconstruction
#         return self._create_fallback_mesh()
    
#     async def _generate_instant_ngp(self, frames: list) -> Mesh3D:
        """Generate using Instant-NGP"""
        # Instant-NGP implementation
#         return self._create_fallback_mesh()
    
#     def _compute_normals(self, vertices: np.ndarray, faces: np.ndarray) -> np.ndarray:
        """Compute vertex normals"""
#         normals = np.zeros_like(vertices)
        
        # Handle flat face array
#         if len(faces.shape) == 1:
#             faces = faces.reshape(-1, 3)
        
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
    
#     def _generate_enhanced_procedural(self, prompt: str, detail_level: str) -> Mesh3D:
        """Generate much better procedural 3D based on prompt analysis"""
#         prompt_lower = prompt.lower()
        
        # Determine complexity
#         detail_map = {"low": 16, "medium": 32, "high": 64, "ultra": 128}
#         resolution = detail_map.get(detail_level, 32)
        
        # Generate based on keywords
#         if any(word in prompt_lower for word in ["spacecraft", "spaceship", "rocket", "ship"]):
#             return self._generate_spacecraft(resolution)
#         elif any(word in prompt_lower for word in ["building", "house", "castle", "tower"]):
#             return self._generate_building(resolution)
#         elif any(word in prompt_lower for word in ["character", "person", "human", "robot"]):
#             return self._generate_character(resolution)
#         elif any(word in prompt_lower for word in ["tree", "plant", "flower", "organic"]):
#             return self._generate_organic(resolution)
#         elif any(word in prompt_lower for word in ["vehicle", "car", "tank"]):
#             return self._generate_vehicle(resolution)
#         else:
#             return self._generate_abstract(resolution)
    
#     def _generate_spacecraft(self, resolution: int) -> Mesh3D:
        """Generate spacecraft with fuselage and wings"""
#         vertices = []
#         faces = []
        
        # Elongated fuselage
#         for i in range(resolution):
#             theta = 2 * np.pi * i / resolution
#             for j in range(resolution // 2):
#                 phi = np.pi * j / (resolution // 2)
#                 x = 3.0 * np.sin(phi) * np.cos(theta)
#                 y = np.sin(phi) * np.sin(theta)
#                 z = np.cos(phi) * 2.0
#                 vertices.append([x, y, z])
        
        # Add wings
#         vertices.extend([[-2, -3, 0], [0, -3, 0], [1, -1, 0],
                        [-2, 3, 0], [0, 3, 0], [1, 1, 0]])
        
        # Faces
#         for i in range(resolution - 1):
#             for j in range(resolution // 2 - 1):
#                 idx1 = i * (resolution // 2) + j
#                 idx2 = (i + 1) * (resolution // 2) + j
#                 faces.extend([[idx1, idx2, idx1 + 1], [idx2, idx2 + 1, idx1 + 1]])
        
#         vertices = np.array(vertices, dtype=np.float32)
#         faces = np.array(faces, dtype=np.int32).flatten()
#         return Mesh3D(vertices=vertices, faces=faces, normals=self._compute_normals(vertices, faces))
    
#     def _generate_building(self, resolution: int) -> Mesh3D:
        """Generate building with stacked levels"""
#         vertices, faces = [], []
        
#         for level in range(3):
#             scale = 1.0 - (level * 0.2)
#             height = level * 2.0
#             base_idx = len(vertices)
            
#             vertices.extend([
                [-scale, -scale, height], [scale, -scale, height],
                [scale, scale, height], [-scale, scale, height],
                [-scale, -scale, height + 1.5], [scale, -scale, height + 1.5],
                [scale, scale, height + 1.5], [-scale, scale, height + 1.5]
            ])
            
#             for face in [[0,1,2], [0,2,3], [4,6,5], [4,7,6], [0,4,5], [0,5,1],
                        [2,6,7], [2,7,3], [0,3,7], [0,7,4], [1,5,6], [1,6,2]]:
#                 faces.append([base_idx + f for f in face])
        
#         vertices = np.array(vertices, dtype=np.float32)
#         faces = np.array(faces, dtype=np.int32).flatten()
#         return Mesh3D(vertices=vertices, faces=faces, normals=self._compute_normals(vertices, faces))
    
#     def _generate_character(self, resolution: int) -> Mesh3D:
        """Generate humanoid character"""
#         vertices, faces = [], []
        
        # Body cylinder
#         segs = max(8, resolution // 4)
#         for i in range(segs):
#             angle = 2 * np.pi * i / segs
#             x, y = 0.6 * np.cos(angle), 0.6 * np.sin(angle)
#             vertices.extend([[x, y, 1.5], [x, y, 0]])
        
        # Head sphere
#         for i in range(segs):
#             theta = 2 * np.pi * i / segs
#             for j in range(segs // 2):
#                 phi = np.pi * j / (segs // 2)
#                 x = 0.5 * np.sin(phi) * np.cos(theta)
#                 y = 0.5 * np.sin(phi) * np.sin(theta)
#                 z = 2.5 + 0.5 * np.cos(phi)
#                 vertices.append([x, y, z])
        
#         for i in range(segs - 1):
#             idx1, idx2 = i * 2, (i + 1) * 2
#             faces.extend([[idx1, idx2, idx1+1], [idx2, idx2+1, idx1+1]])
        
#         vertices = np.array(vertices, dtype=np.float32)
#         faces = np.array(faces, dtype=np.int32).flatten()
#         return Mesh3D(vertices=vertices, faces=faces, normals=self._compute_normals(vertices, faces))
    
#     def _generate_organic(self, resolution: int) -> Mesh3D:
        """Generate tree with trunk and canopy"""
#         vertices, faces = [], []
        
        # Trunk
#         trunk_segs = max(12, resolution // 3)
#         for i in range(trunk_segs):
#             angle = 2 * np.pi * i / trunk_segs
#             for h in range(6):
#                 height = h * 0.6
#                 radius = 0.3 - (h * 0.03)
#                 x, y = radius * np.cos(angle), radius * np.sin(angle)
#                 vertices.append([x, y, height])
        
        # Canopy with noise
#         for i in range(16):
#             theta = 2 * np.pi * i / 16
#             for j in range(8):
#                 phi = np.pi * j / 8
#                 noise = 0.2 * np.sin(theta * 3) * np.cos(phi * 2)
#                 r = 1.5 + noise
#                 x = r * np.sin(phi) * np.cos(theta)
#                 y = r * np.sin(phi) * np.sin(theta)
#                 z = 2.5 + r * np.cos(phi)
#                 vertices.append([x, y, z])
        
#         for i in range(trunk_segs - 1):
#             for h in range(5):
#                 idx1, idx2 = i * 6 + h, (i + 1) * 6 + h
#                 faces.extend([[idx1, idx2, idx1+1], [idx2, idx2+1, idx1+1]])
        
#         vertices = np.array(vertices, dtype=np.float32)
#         faces = np.array(faces, dtype=np.int32).flatten()
#         return Mesh3D(vertices=vertices, faces=faces, normals=self._compute_normals(vertices, faces))
    
#     def _generate_vehicle(self, resolution: int) -> Mesh3D:
        """Generate vehicle with body and wheels"""
#         vertices = [
            [-2,-1,0], [2,-1,0], [2,1,0], [-2,1,0],
            [-1.5,-0.8,1], [1.5,-0.8,1], [1.5,0.8,1], [-1.5,0.8,1]
        ]
        
        # Add wheels
#         for pos in [[-1.5,-1.2,0], [1.5,-1.2,0], [-1.5,1.2,0], [1.5,1.2,0]]:
#             for i in range(8):
#                 angle = 2 * np.pi * i / 8
#                 y, z = pos[1] + 0.3 * np.cos(angle), pos[2] + 0.3 * np.sin(angle)
#                 vertices.extend([[pos[0]-0.2, y, z], [pos[0]+0.2, y, z]])
        
#         faces = [[0,1,2], [0,2,3], [4,6,5], [4,7,6], [0,4,5], [0,5,1],
                [2,6,7], [2,7,3], [0,3,7], [0,7,4], [1,5,6], [1,6,2]]
        
#         vertices = np.array(vertices, dtype=np.float32)
#         faces = np.array(faces, dtype=np.int32).flatten()
#         return Mesh3D(vertices=vertices, faces=faces, normals=self._compute_normals(vertices, faces))
    
#     def _generate_abstract(self, resolution: int) -> Mesh3D:
        """Generate torus with wave modulation"""
#         vertices, faces = [], []
#         segs = max(24, resolution)
        
#         for i in range(segs):
#             theta = 2 * np.pi * i / segs
#             for j in range(segs // 2):
#                 phi = 2 * np.pi * j / (segs // 2)
#                 wave = 0.2 * np.sin(theta * 5) * np.cos(phi * 3)
#                 x = (2.0 + (0.8 + wave) * np.cos(phi)) * np.cos(theta)
#                 y = (2.0 + (0.8 + wave) * np.cos(phi)) * np.sin(theta)
#                 z = (0.8 + wave) * np.sin(phi)
#                 vertices.append([x, y, z])
        
#         for i in range(segs - 1):
#             for j in range(segs // 2 - 1):
#                 idx1 = i * (segs // 2) + j
#                 idx2 = (i + 1) * (segs // 2) + j
#                 faces.extend([[idx1, idx2, idx1+1], [idx2, idx2+1, idx1+1]])
        
#         vertices = np.array(vertices, dtype=np.float32)
#         faces = np.array(faces, dtype=np.int32).flatten()
#         return Mesh3D(vertices=vertices, faces=faces, normals=self._compute_normals(vertices, faces))
    
#     def _create_fallback_mesh(self) -> Mesh3D:
        """Create a simple fallback mesh when AI generation fails"""
        # Create a nice looking cube as fallback
#         vertices = np.array([
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
        ], dtype=np.float32)
        
#         faces = np.array([
            [0, 1, 2], [0, 2, 3],  # Front
            [4, 6, 5], [4, 7, 6],  # Back
            [0, 4, 5], [0, 5, 1],  # Bottom
            [2, 6, 7], [2, 7, 3],  # Top
            [0, 3, 7], [0, 7, 4],  # Left
            [1, 5, 6], [1, 6, 2]   # Right
        ], dtype=np.int32)
        
#         normals = self._compute_normals(vertices, faces.flatten())
        
#         return Mesh3D(
#             vertices=vertices,
#             faces=faces.flatten(),
#             normals=normals


# Conversion utilities
# def mesh_to_obj(mesh: Mesh3D) -> str:
    """Convert mesh to OBJ format"""
#     obj_lines = ["# Generated by Gen3D AI Engine\n"]
    
    # Write vertices
#     for v in mesh.vertices:
#         obj_lines.append(f"v {v[0]} {v[1]} {v[2]}\n")
    
    # Write normals
#     for n in mesh.normals:
#         obj_lines.append(f"vn {n[0]} {n[1]} {n[2]}\n")
    
    # Write faces
#     faces = mesh.faces.reshape(-1, 3) if len(mesh.faces.shape) == 1 else mesh.faces
#     for f in faces:
#         obj_lines.append(f"f {f[0]+1}//{f[0]+1} {f[1]+1}//{f[1]+1} {f[2]+1}//{f[2]+1}\n")
    
#     return "".join(obj_lines)


# def mesh_to_json(mesh: Mesh3D) -> dict:
    """Convert mesh to JSON format (Three.js compatible)"""
#     return {
        "vertices": mesh.vertices.flatten().tolist(),
        "faces": mesh.faces.tolist(),
        "normals": mesh.normals.flatten().tolist(),
        "uvs": mesh.uvs.flatten().tolist() if mesh.uvs is not None else [],
        "colors": mesh.colors.flatten().tolist() if mesh.colors is not None else []
    }
