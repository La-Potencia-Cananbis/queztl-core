import asyncio
import sys
sys.path.insert(0, '/workspace/backend')
from backend.train_3d_models import Lightweight3DDiffusionModel, SimpleDiffusionTrainer, SyntheticTrainingDataGenerator
import torch
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def train_for_2_hours():
    logger.info("🎓 Starting 2-hour distributed 3D model training...")
    logger.info("Training 3 different models:")
    logger.info("  1. Diffusion model (512 vertices)")
    logger.info("  2. High-res diffusion (1024 vertices)")
    logger.info("  3. Neural SDF network")
    
    # Generate training dataset (reduced for faster startup)
    logger.info("📦 Generating 10,000 training samples...")
    dataset = SyntheticTrainingDataGenerator.generate_dataset(num_samples=10000)
    logger.info(f"✅ Dataset ready: {len(dataset)} samples")
    
    # Model 1: Standard diffusion (512 vertices)
    logger.info("\n🚀 Training Model 1: Standard Diffusion (512 vertices)")
    model1 = Lightweight3DDiffusionModel(
        text_embed_dim=512,
        latent_dim=256,
        num_layers=6,
        output_vertices=512
    )
    trainer1 = SimpleDiffusionTrainer(model1)
    
    # Calculate epochs for ~40 min training
    epochs_model1 = 500  # ~40 minutes
    batch_size = 32
    
    for epoch in range(epochs_model1):
        epoch_loss = 0
        num_batches = 0
        
        for i in range(0, len(dataset), batch_size):
            batch = dataset[i:i+batch_size]
            if len(batch) < batch_size:
                continue
            
            # Extract vertices and pad/truncate to 512
            batch_verts = []
            for item in batch:
                v = item['vertices']
                if len(v) > 512:
                    v = v[:512]  # Truncate
                elif len(v) < 512:
                    # Pad with zeros
                    pad_size = 512 - len(v)
                    v = np.vstack([v, np.zeros((pad_size, 3))])
                batch_verts.append(v)
            
            vertices = torch.tensor(
                np.stack(batch_verts),
                dtype=torch.float32
            )
            text_embeds = torch.tensor(
                np.stack([item['text_embed'] for item in batch]),
                dtype=torch.float32
            )
            
            loss = trainer1.train_step(vertices, text_embeds)
            epoch_loss += loss
            num_batches += 1
        
        avg_loss = epoch_loss / max(1, num_batches)
        if (epoch + 1) % 50 == 0:
            logger.info(f"  Epoch {epoch+1}/{epochs_model1} - Loss: {avg_loss:.6f}")
    
    # Save model 1
    torch.save(model1.state_dict(), "/workspace/trained_3d_diffusion_512.pt")
    logger.info("✅ Model 1 saved: trained_3d_diffusion_512.pt")
    
    # Model 2: High-res diffusion (1024 vertices)
    logger.info("\n🚀 Training Model 2: High-Res Diffusion (1024 vertices)")
    model2 = Lightweight3DDiffusionModel(
        text_embed_dim=512,
        latent_dim=512,
        num_layers=8,
        output_vertices=1024
    )
    trainer2 = SimpleDiffusionTrainer(model2)
    
    epochs_model2 = 400  # ~40 minutes
    
    for epoch in range(epochs_model2):
        epoch_loss = 0
        num_batches = 0
        
        for i in range(0, len(dataset), batch_size):
            batch = dataset[i:i+batch_size]
            if len(batch) < batch_size:
                continue
            
            # Extract vertices and pad/truncate to 1024
            batch_verts = []
            for item in batch:
                v = item['vertices']
                if len(v) > 1024:
                    v = v[:1024]  # Truncate
                elif len(v) < 1024:
                    # Pad with zeros
                    pad_size = 1024 - len(v)
                    v = np.vstack([v, np.zeros((pad_size, 3))])
                batch_verts.append(v)
            
            vertices = torch.tensor(
                np.stack(batch_verts),
                dtype=torch.float32
            )
            text_embeds = torch.tensor(
                np.stack([item['text_embed'] for item in batch]),
                dtype=torch.float32
            )
            
            loss = trainer2.train_step(vertices, text_embeds)
            epoch_loss += loss
            num_batches += 1
        
        avg_loss = epoch_loss / max(1, num_batches)
        if (epoch + 1) % 40 == 0:
            logger.info(f"  Epoch {epoch+1}/{epochs_model2} - Loss: {avg_loss:.6f}")
    
    # Save model 2
    torch.save(model2.state_dict(), "/workspace/trained_3d_diffusion_1024.pt")
    logger.info("✅ Model 2 saved: trained_3d_diffusion_1024.pt")
    
    # Model 3: Neural SDF (40 minutes)
    logger.info("\n🚀 Training Model 3: Neural SDF Network")
    from backend.train_3d_models import NeuralSDFNetwork
    
    model3 = NeuralSDFNetwork(
        text_embed_dim=512,
        hidden_dim=256,
        num_layers=8
    )
    optimizer3 = torch.optim.Adam(model3.parameters(), lr=1e-4)
    
    epochs_model3 = 300
    
    for epoch in range(epochs_model3):
        epoch_loss = 0
        num_batches = 0
        
        for i in range(0, len(dataset), batch_size):
            batch = dataset[i:i+batch_size]
            if len(batch) < batch_size:
                continue
            
            # Create query points
            query_points = torch.randn(len(batch), 1000, 3) * 1.5
            
            text_embeds = torch.tensor(
                np.stack([item['text_embed'] for item in batch]),
                dtype=torch.float32
            )
            
            # Forward pass
            sdf_pred = model3(query_points, text_embeds)
            
            # Compute target SDF (distance to nearest vertex)
            # Pad/truncate vertices to consistent size (512)
            batch_verts = []
            for item in batch:
                v = item['vertices']
                if len(v) > 512:
                    v = v[:512]
                elif len(v) < 512:
                    pad_size = 512 - len(v)
                    v = np.vstack([v, np.zeros((pad_size, 3))])
                batch_verts.append(v)
            
            vertices_batch = torch.tensor(
                np.stack(batch_verts),
                dtype=torch.float32
            )
            
            # Simple loss: predict distance
            dist = torch.cdist(query_points, vertices_batch)
            sdf_target = dist.min(dim=-1)[0].unsqueeze(-1)
            
            loss = torch.nn.functional.mse_loss(sdf_pred, sdf_target)
            
            optimizer3.zero_grad()
            loss.backward()
            optimizer3.step()
            
            epoch_loss += loss.item()
            num_batches += 1
        
        avg_loss = epoch_loss / max(1, num_batches)
        if (epoch + 1) % 30 == 0:
            logger.info(f"  Epoch {epoch+1}/{epochs_model3} - Loss: {avg_loss:.6f}")
    
    # Save model 3
    torch.save(model3.state_dict(), "/workspace/trained_3d_sdf.pt")
    logger.info("✅ Model 3 saved: trained_3d_sdf.pt")
    
    logger.info("\n🎉 All 3 models trained successfully!")
    logger.info("Models saved:")
    logger.info("  - trained_3d_diffusion_512.pt  (512 vertices)")
    logger.info("  - trained_3d_diffusion_1024.pt (1024 vertices)")
    logger.info("  - trained_3d_sdf.pt (Neural SDF)")
    logger.info("\n✨ Ready for production use!")

if __name__ == "__main__":
    asyncio.run(train_for_2_hours())
