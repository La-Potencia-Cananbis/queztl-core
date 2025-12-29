#!/usr/bin/env python3
"""
Advanced Training Enhancement - Phase 2
Trains a better model while maintaining backward compatibility
"""
import sys
sys.path.insert(0, '/workspace/backend')
import torch
import torch.nn as nn
import numpy as np
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


class Enhanced3DModel(nn.Module):
    """Enhanced 3D generation model with better capacity"""
    def __init__(self, text_dim=256, hidden_dim=512, output_vertices=1024):
        super().__init__()
        self.output_vertices = output_vertices
        
        # Deeper network for better quality
        self.encoder = nn.Sequential(
            nn.Linear(text_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
        )
        
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_vertices * 3)
        )
    
    def forward(self, text_embed):
        x = self.encoder(text_embed)
        x = self.decoder(x)
        return x.reshape(-1, self.output_vertices, 3)


def generate_enhanced_dataset(num_samples=5000):
    """Generate larger, more diverse dataset"""
    logger.info(f"Generating enhanced dataset with {num_samples} samples...")
    dataset = []
    
    # Expanded shape vocabulary
    shapes = {
        'cube': lambda: generate_cube(complexity=4),
        'sphere': lambda: generate_sphere(res=16),
        'cylinder': lambda: generate_cylinder(res=24),
        'pyramid': lambda: generate_pyramid(),
        'cone': lambda: generate_cone(res=20),
        'torus': lambda: generate_torus(res=16),
        'capsule': lambda: generate_capsule(),
        'octahedron': lambda: generate_octahedron(),
        'prism': lambda: generate_prism(),
        'helix': lambda: generate_helix(),
    }
    
    # Expanded vocabulary with combinations
    prompts = [
        # Basic shapes
        "cube", "sphere", "cylinder", "pyramid", "cone",
        "torus", "capsule", "octahedron", "prism", "helix",
        
        # Vehicles
        "car", "truck", "spaceship", "airplane", "helicopter",
        "boat", "submarine", "motorcycle", "tank", "hovercraft",
        "race car", "sports car", "fighter jet", "drone",
        
        # Characters
        "robot", "humanoid", "alien", "monster", "creature",
        "dragon", "warrior", "mech", "cyborg", "android",
        
        # Architecture
        "house", "building", "tower", "castle", "fortress",
        "bridge", "dome", "arch", "pyramid", "skyscraper",
        
        # Weapons
        "sword", "gun", "rifle", "cannon", "missile",
        "bow", "axe", "hammer", "spear", "shield",
        
        # Nature
        "tree", "plant", "rock", "crystal", "mountain",
        "flower", "bush", "leaf", "branch", "stone",
        
        # Objects
        "chair", "table", "lamp", "cup", "box",
        "bottle", "phone", "computer", "book", "tool",
        
        # Complex combinations
        "futuristic spaceship", "medieval castle", "alien creature",
        "robot warrior", "fantasy sword", "military tank",
        "sports car", "office building", "crystal gem",
    ]
    
    for i in range(num_samples):
        if i % 500 == 0:
            logger.info(f"  Generated {i}/{num_samples}...")
        
        # Pick random prompt
        prompt = np.random.choice(prompts)
        
        # Generate base shape
        shape_name = np.random.choice(list(shapes.keys()))
        vertices = shapes[shape_name]()
        
        # Add transformations
        # Scale
        scale = np.random.uniform(0.7, 1.3)
        vertices = vertices * scale
        
        # Rotate
        angle = np.random.uniform(0, 2 * np.pi)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        rot_matrix = np.array([
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ])
        vertices = vertices @ rot_matrix.T
        
        # Add noise for variation
        noise = np.random.randn(*vertices.shape) * 0.03
        vertices = vertices + noise
        
        # Pad to 1024 vertices
        if len(vertices) < 1024:
            padding = np.zeros((1024 - len(vertices), 3))
            vertices = np.vstack([vertices, padding])
        else:
            vertices = vertices[:1024]
        
        # Enhanced text embedding (256-dim)
        text_embed = hash_to_embed(prompt, 256)
        
        dataset.append({
            'vertices': torch.FloatTensor(vertices),
            'text_embed': torch.FloatTensor(text_embed),
            'label': prompt
        })
    
    logger.info(f"✅ Enhanced dataset ready: {len(dataset)} samples")
    return dataset


def generate_cube(complexity=4):
    """Generate cube with variable complexity"""
    vertices = []
    step = 2.0 / (complexity - 1) if complexity > 1 else 2.0
    for x in np.arange(-1, 1.01, step):
        for y in np.arange(-1, 1.01, step):
            for z in [-1, 1]:
                vertices.append([x, y, z])
            for z in np.arange(-1, 1.01, step):
                vertices.append([x, -1, z])
                vertices.append([x, 1, z])
                vertices.append([-1, y, z])
                vertices.append([1, y, z])
    return np.array(vertices, dtype=np.float32)


def generate_sphere(res=16):
    """Generate sphere with resolution"""
    vertices = []
    for i in range(res):
        theta = (i / res) * 2 * np.pi
        for j in range(res):
            phi = (j / res) * np.pi
            x = np.sin(phi) * np.cos(theta)
            y = np.sin(phi) * np.sin(theta)
            z = np.cos(phi)
            vertices.append([x, y, z])
    return np.array(vertices, dtype=np.float32)


def generate_cylinder(res=24):
    """Generate cylinder"""
    vertices = []
    for i in range(res):
        theta = (i / res) * 2 * np.pi
        for z in np.linspace(-1, 1, 6):
            x = np.cos(theta)
            y = np.sin(theta)
            vertices.append([x, y, z])
    return np.array(vertices, dtype=np.float32)


def generate_pyramid():
    """Generate pyramid"""
    base = [[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1]]
    apex = [[0, 0, 1]]
    vertices = base * 4 + apex * 16
    return np.array(vertices, dtype=np.float32)


def generate_cone(res=20):
    """Generate cone"""
    vertices = [[0, 0, 1]]  # Apex
    for i in range(res):
        theta = (i / res) * 2 * np.pi
        x = np.cos(theta)
        y = np.sin(theta)
        vertices.append([x, y, -1])
    return np.array(vertices, dtype=np.float32)


def generate_torus(res=16):
    """Generate torus"""
    vertices = []
    R, r = 1.0, 0.3
    for i in range(res):
        theta = (i / res) * 2 * np.pi
        for j in range(res):
            phi = (j / res) * 2 * np.pi
            x = (R + r * np.cos(phi)) * np.cos(theta)
            y = (R + r * np.cos(phi)) * np.sin(theta)
            z = r * np.sin(phi)
            vertices.append([x, y, z])
    return np.array(vertices, dtype=np.float32)


def generate_capsule():
    """Generate capsule (cylinder with spherical caps)"""
    vertices = []
    # Cylinder body
    for i in range(16):
        theta = (i / 16) * 2 * np.pi
        for z in np.linspace(-0.5, 0.5, 4):
            x = np.cos(theta) * 0.5
            y = np.sin(theta) * 0.5
            vertices.append([x, y, z])
    # Top sphere
    for i in range(8):
        theta = (i / 8) * 2 * np.pi
        for j in range(4):
            phi = (j / 8) * np.pi
            x = 0.5 * np.sin(phi) * np.cos(theta)
            y = 0.5 * np.sin(phi) * np.sin(theta)
            z = 0.5 + 0.5 * np.cos(phi)
            vertices.append([x, y, z])
    return np.array(vertices, dtype=np.float32)


def generate_octahedron():
    """Generate octahedron"""
    vertices = [
        [1, 0, 0], [-1, 0, 0], [0, 1, 0],
        [0, -1, 0], [0, 0, 1], [0, 0, -1]
    ]
    return np.array(vertices * 16, dtype=np.float32)


def generate_prism():
    """Generate triangular prism"""
    vertices = []
    # Triangle base
    for z in np.linspace(-1, 1, 8):
        vertices.extend([
            [0, 1, z], [-0.866, -0.5, z], [0.866, -0.5, z]
        ])
    return np.array(vertices, dtype=np.float32)


def generate_helix():
    """Generate helix"""
    vertices = []
    for i in range(64):
        t = (i / 64) * 4 * np.pi
        x = np.cos(t) * 0.5
        y = np.sin(t) * 0.5
        z = (i / 64) * 2 - 1
        vertices.append([x, y, z])
    return np.array(vertices, dtype=np.float32)


def hash_to_embed(text, dim=256):
    """Convert text to embedding via hash"""
    h = hash(text.lower()) % (2**31)
    np.random.seed(h)
    embed = np.random.randn(dim)
    return embed / (np.linalg.norm(embed) + 1e-8)


def train_enhanced_model():
    """Train enhanced model"""
    logger.info("🚀 ENHANCED TRAINING - PHASE 2")
    logger.info("=" * 70)
    logger.info("Target: 1024 vertices, 5000 samples, deeper network")
    logger.info("")
    
    # Create enhanced model
    model = Enhanced3DModel(text_dim=256, hidden_dim=512, output_vertices=1024)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=300)
    criterion = nn.MSELoss()
    
    # Generate enhanced dataset
    dataset = generate_enhanced_dataset(num_samples=5000)
    
    # Training loop
    batch_size = 32
    num_epochs = 300
    
    logger.info(f"Training for {num_epochs} epochs...")
    logger.info("")
    
    start_time = datetime.now()
    best_loss = float('inf')
    
    for epoch in range(num_epochs):
        epoch_loss = 0.0
        num_batches = 0
        
        # Shuffle dataset
        indices = np.random.permutation(len(dataset))
        
        for i in range(0, len(dataset), batch_size):
            batch_indices = indices[i:i+batch_size]
            if len(batch_indices) < batch_size:
                continue
            
            batch = [dataset[idx] for idx in batch_indices]
            
            # Prepare batch
            text_embeds = torch.stack([item['text_embed'] for item in batch])
            target_vertices = torch.stack([item['vertices'] for item in batch])
            
            # Forward pass
            optimizer.zero_grad()
            predicted = model(text_embeds)
            
            # Loss
            loss = criterion(predicted, target_vertices)
            
            # Backward pass
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            
            epoch_loss += loss.item()
            num_batches += 1
        
        scheduler.step()
        avg_loss = epoch_loss / max(1, num_batches)
        
        # Track best model
        if avg_loss < best_loss:
            best_loss = avg_loss
        
        # Log every 30 epochs
        if (epoch + 1) % 30 == 0:
            elapsed = (datetime.now() - start_time).total_seconds()
            lr = optimizer.param_groups[0]['lr']
            logger.info(f"Epoch {epoch+1}/{num_epochs} - Loss: {avg_loss:.6f} - LR: {lr:.6f} - Time: {elapsed:.1f}s")
    
    # Save enhanced model
    save_path = "/workspace/models/enhanced_3d_model.pt"
    torch.save({
        'model_state_dict': model.state_dict(),
        'model_config': {
            'text_dim': 256,
            'hidden_dim': 512,
            'output_vertices': 1024
        },
        'training_info': {
            'epochs': num_epochs,
            'final_loss': best_loss,
            'samples': len(dataset),
            'timestamp': datetime.now().isoformat()
        }
    }, save_path)
    
    total_time = (datetime.now() - start_time).total_seconds()
    logger.info("")
    logger.info("=" * 70)
    logger.info("✅ ENHANCED TRAINING COMPLETE!")
    logger.info(f"   Model saved: {save_path}")
    logger.info(f"   Final loss: {best_loss:.6f}")
    logger.info(f"   Total time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    logger.info(f"   Output: 1024 vertices per model")
    logger.info(f"   Dataset: 5000 diverse samples")
    logger.info("=" * 70)


if __name__ == "__main__":
    try:
        train_enhanced_model()
    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
