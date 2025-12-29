#!/usr/bin/env python3
"""
Fast 3D model training - completes in 10-15 minutes
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

class Fast3DModel(nn.Module):
    """Lightweight 3D generation model"""
    def __init__(self, text_dim=128, hidden_dim=256, output_vertices=512):
        super().__init__()
        self.output_vertices = output_vertices
        
        self.net = nn.Sequential(
            nn.Linear(text_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_vertices * 3)
        )
    
    def forward(self, text_embed):
        x = self.net(text_embed)
        return x.reshape(-1, self.output_vertices, 3)

def generate_simple_dataset(num_samples=1000):
    """Generate lightweight training data"""
    logger.info(f"Generating {num_samples} training samples...")
    dataset = []
    
    shapes = ['cube', 'sphere', 'cylinder', 'pyramid', 'cone']
    
    for i in range(num_samples):
        if i % 200 == 0:
            logger.info(f"  Generated {i}/{num_samples}...")
        
        # Random shape
        shape = shapes[i % len(shapes)]
        
        # Simple procedural vertices
        if shape == 'cube':
            vertices = generate_cube()
        elif shape == 'sphere':
            vertices = generate_sphere()
        elif shape == 'cylinder':
            vertices = generate_cylinder()
        elif shape == 'pyramid':
            vertices = generate_pyramid()
        else:
            vertices = generate_cone()
        
        # Pad to 512 vertices
        if len(vertices) < 512:
            padding = np.zeros((512 - len(vertices), 3))
            vertices = np.vstack([vertices, padding])
        else:
            vertices = vertices[:512]
        
        # Simple text embedding (hash-based)
        text_embed = hash_to_embed(shape, 128)
        
        dataset.append({
            'vertices': torch.FloatTensor(vertices),
            'text_embed': torch.FloatTensor(text_embed),
            'label': shape
        })
    
    logger.info(f"✅ Dataset ready: {len(dataset)} samples")
    return dataset

def generate_cube():
    """Generate cube vertices"""
    vertices = []
    for x in np.linspace(-1, 1, 4):
        for y in np.linspace(-1, 1, 4):
            for z in np.linspace(-1, 1, 4):
                vertices.append([x, y, z])
    return np.array(vertices, dtype=np.float32)

def generate_sphere():
    """Generate sphere vertices"""
    vertices = []
    for i in range(8):
        theta = (i / 8) * 2 * np.pi
        for j in range(8):
            phi = (j / 8) * np.pi
            x = np.sin(phi) * np.cos(theta)
            y = np.sin(phi) * np.sin(theta)
            z = np.cos(phi)
            vertices.append([x, y, z])
    return np.array(vertices, dtype=np.float32)

def generate_cylinder():
    """Generate cylinder vertices"""
    vertices = []
    for i in range(16):
        theta = (i / 16) * 2 * np.pi
        for z in np.linspace(-1, 1, 4):
            x = np.cos(theta)
            y = np.sin(theta)
            vertices.append([x, y, z])
    return np.array(vertices, dtype=np.float32)

def generate_pyramid():
    """Generate pyramid vertices"""
    base = [[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1]]
    apex = [[0, 0, 1]]
    vertices = base + apex * 12  # Repeat apex
    return np.array(vertices, dtype=np.float32)

def generate_cone():
    """Generate cone vertices"""
    vertices = [[0, 0, 1]]  # Apex
    for i in range(16):
        theta = (i / 16) * 2 * np.pi
        x = np.cos(theta)
        y = np.sin(theta)
        vertices.append([x, y, -1])
    return np.array(vertices, dtype=np.float32)

def hash_to_embed(text, dim=128):
    """Convert text to embedding via hash"""
    h = hash(text) % (2**31)
    np.random.seed(h)
    embed = np.random.randn(dim)
    return embed / (np.linalg.norm(embed) + 1e-8)

def train_fast():
    """Train fast 3D model"""
    logger.info("🚀 FAST TRAINING MODE - 10 minute completion")
    logger.info("=" * 60)
    
    # Create model
    model = Fast3DModel(text_dim=128, hidden_dim=256, output_vertices=512)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.MSELoss()
    
    # Generate dataset
    dataset = generate_simple_dataset(num_samples=1000)
    
    # Training loop
    batch_size = 32
    num_epochs = 200
    
    logger.info(f"Training for {num_epochs} epochs...")
    logger.info(f"Batch size: {batch_size}")
    logger.info("")
    
    start_time = datetime.now()
    
    for epoch in range(num_epochs):
        epoch_loss = 0.0
        num_batches = 0
        
        # Shuffle dataset
        np.random.shuffle(dataset)
        
        for i in range(0, len(dataset), batch_size):
            batch = dataset[i:i+batch_size]
            if len(batch) < batch_size:
                continue
            
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
            optimizer.step()
            
            epoch_loss += loss.item()
            num_batches += 1
        
        avg_loss = epoch_loss / max(1, num_batches)
        
        # Log every 20 epochs
        if (epoch + 1) % 20 == 0:
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"Epoch {epoch+1}/{num_epochs} - Loss: {avg_loss:.6f} - Time: {elapsed:.1f}s")
    
    # Save model
    save_path = "/workspace/models/fast_3d_model.pt"
    torch.save({
        'model_state_dict': model.state_dict(),
        'model_config': {
            'text_dim': 128,
            'hidden_dim': 256,
            'output_vertices': 512
        }
    }, save_path)
    
    total_time = (datetime.now() - start_time).total_seconds()
    logger.info("")
    logger.info("=" * 60)
    logger.info(f"✅ TRAINING COMPLETE!")
    logger.info(f"   Model saved: {save_path}")
    logger.info(f"   Final loss: {avg_loss:.6f}")
    logger.info(f"   Total time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    logger.info(f"   Output: 512 vertices per model")
    logger.info("=" * 60)

if __name__ == "__main__":
    try:
        train_fast()
    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
