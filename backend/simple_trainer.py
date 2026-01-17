#!/usr/bin/env python3
"""
SIMPLE TRAINER - The Vision Implemented Correctly
================================================
ONE program. Low power. Limited dataset. Self-improving.
Scales from 1 CPU → cluster when ready.

Philosophy (from QUETZALCOATL_VISION.md):
- Minimal moving parts
- Just-in-time development  
- Test single processor FIRST
- Distribute AFTER it works

What this does RIGHT:
1. Uses actual ML (PyTorch with real gradients)
2. Trains on limited dataset (10 objects, 50 images each)
3. Self-improves through transfer learning
4. Low power (runs on 1 CPU efficiently)
5. Scalable architecture (add --distributed later)
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional

# Core dependencies
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
from PIL import Image
import numpy as np

# Configuration
DATA_ROOT = Path("/tmp/simple_training")
OBJECTS = ["pencil", "apple", "book", "chair", "cup", "laptop", "phone", "scissors", "shoe", "watch"]
IMAGES_PER_OBJECT = 50  # Start small
BATCH_SIZE = 8
LEARNING_RATE = 0.001
MAX_EPOCHS = 100
TARGET_ACCURACY = 0.90


class SimpleImageDataset(Dataset):
    """Minimal dataset - just paths and labels."""
    
    def __init__(self, image_paths: List[Path], labels: List[int], transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform or transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        try:
            img = Image.open(self.image_paths[idx]).convert('RGB')
            img = self.transform(img)
            return img, self.labels[idx]
        except Exception as e:
            print(f"⚠️ Failed to load {self.image_paths[idx]}: {e}")
            # Return black image as fallback
            return torch.zeros(3, 224, 224), self.labels[idx]


class SimpleTrainer:
    """The actual trainer - does ONE thing well."""
    
    def __init__(self, data_root: Path, num_classes: int):
        self.data_root = data_root
        self.num_classes = num_classes
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Use pre-trained ResNet18 (lightweight, proven)
        print(f"🧠 Initializing ResNet18 model on {self.device}...")
        self.model = models.resnet18(pretrained=True)
        
        # Replace final layer for our classes
        num_features = self.model.fc.in_features
        self.model.fc = nn.Linear(num_features, num_classes)
        self.model = self.model.to(self.device)
        
        # Loss and optimizer
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=LEARNING_RATE)
        
        # Metrics
        self.best_accuracy = 0.0
        self.training_history = []
    
    def load_dataset(self, split='train') -> Optional[DataLoader]:
        """Load images from disk - simple and fast."""
        split_dir = self.data_root / split
        if not split_dir.exists():
            print(f"⚠️ No {split} data found at {split_dir}")
            return None
        
        image_paths = []
        labels = []
        
        for class_idx, obj_name in enumerate(OBJECTS):
            obj_dir = split_dir / obj_name
            if not obj_dir.exists():
                continue
            
            images = list(obj_dir.glob("*.png")) + list(obj_dir.glob("*.jpg"))
            image_paths.extend(images)
            labels.extend([class_idx] * len(images))
        
        if not image_paths:
            print(f"⚠️ No images found in {split_dir}")
            return None
        
        print(f"📂 Loaded {len(image_paths)} images from {split} set")
        
        dataset = SimpleImageDataset(image_paths, labels)
        return DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=(split=='train'), num_workers=2)
    
    def train_epoch(self, train_loader: DataLoader) -> Tuple[float, float]:
        """Train for one epoch - the core learning loop."""
        self.model.train()
        total_loss = 0.0
        correct = 0
        total = 0
        
        for batch_idx, (images, labels) in enumerate(train_loader):
            images = images.to(self.device)
            labels = labels.to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)
            
            # Backward pass (ACTUAL LEARNING!)
            loss.backward()
            self.optimizer.step()
            
            # Metrics
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            if batch_idx % 10 == 0:
                print(f"  Batch {batch_idx}/{len(train_loader)}: Loss={loss.item():.4f}", end='\r')
        
        epoch_loss = total_loss / len(train_loader)
        epoch_acc = 100.0 * correct / total
        return epoch_loss, epoch_acc
    
    def validate(self, val_loader: DataLoader) -> Tuple[float, float]:
        """Validate model - no gradients."""
        self.model.eval()
        total_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(self.device)
                labels = labels.to(self.device)
                
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                
                total_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
        
        val_loss = total_loss / len(val_loader)
        val_acc = 100.0 * correct / total
        return val_loss, val_acc
    
    def train(self, max_epochs: int, target_accuracy: float):
        """Main training loop - simple and focused."""
        print(f"\n🚀 Starting training: {max_epochs} epochs, target {target_accuracy*100:.0f}%")
        
        # Load data
        train_loader = self.load_dataset('train')
        val_loader = self.load_dataset('val')
        
        if not train_loader:
            print("❌ No training data - run data preparation first!")
            return False
        
        # Training loop
        start_time = time.time()
        
        for epoch in range(max_epochs):
            epoch_start = time.time()
            
            # Train
            train_loss, train_acc = self.train_epoch(train_loader)
            
            # Validate
            if val_loader:
                val_loss, val_acc = self.validate(val_loader)
            else:
                val_loss, val_acc = train_loss, train_acc
            
            # Record
            self.training_history.append({
                'epoch': epoch + 1,
                'train_loss': train_loss,
                'train_acc': train_acc,
                'val_loss': val_loss,
                'val_acc': val_acc,
                'time': time.time() - epoch_start
            })
            
            # Print progress
            print(f"\n📊 Epoch {epoch+1}/{max_epochs}")
            print(f"   Train: Loss={train_loss:.4f}, Acc={train_acc:.2f}%")
            print(f"   Val:   Loss={val_loss:.4f}, Acc={val_acc:.2f}%")
            print(f"   Time:  {time.time()-epoch_start:.1f}s")
            
            # Save best model
            if val_acc > self.best_accuracy:
                self.best_accuracy = val_acc
                self.save_checkpoint('best_model.pth')
                print(f"   🏆 NEW BEST! Saved checkpoint")
            
            # Check if target reached
            if val_acc >= target_accuracy * 100:
                print(f"\n🎉 TARGET REACHED! {val_acc:.2f}% >= {target_accuracy*100:.0f}%")
                break
        
        total_time = time.time() - start_time
        print(f"\n✅ Training complete: {total_time/60:.1f} minutes")
        print(f"   Best accuracy: {self.best_accuracy:.2f}%")
        
        return True
    
    def save_checkpoint(self, filename: str):
        """Save model state."""
        checkpoint_path = self.data_root / 'checkpoints' / filename
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        
        torch.save({
            'model_state': self.model.state_dict(),
            'optimizer_state': self.optimizer.state_dict(),
            'best_accuracy': self.best_accuracy,
            'history': self.training_history
        }, checkpoint_path)
    
    def save_report(self):
        """Save training report."""
        report_path = self.data_root / 'training_report.json'
        report = {
            'timestamp': datetime.now().isoformat(),
            'num_classes': self.num_classes,
            'best_accuracy': self.best_accuracy,
            'total_epochs': len(self.training_history),
            'history': self.training_history
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Report saved: {report_path}")


def prepare_minimal_dataset(data_root: Path):
    """
    Prepare minimal dataset using simple synthetic images.
    Low power, works offline, no external APIs.
    """
    print("\n📦 Preparing minimal dataset...")
    print("   (Using simple synthetic images for initial testing)")
    
    from PIL import ImageDraw, ImageFont
    
    splits = ['train', 'val']
    counts = {'train': 40, 'val': 10}  # 80/20 split
    
    for split in splits:
        for obj_name in OBJECTS:
            obj_dir = data_root / split / obj_name
            obj_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate simple synthetic images
            for i in range(counts[split]):
                img = Image.new('RGB', (224, 224), color=(
                    hash(obj_name) % 200 + 55,
                    hash(obj_name + str(i)) % 200 + 55,
                    hash(obj_name + str(i*2)) % 200 + 55
                ))
                
                # Add text label
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
                except:
                    font = ImageFont.load_default()
                
                draw.text((50, 90), obj_name, fill='white', font=font)
                
                # Save
                img.save(obj_dir / f"{obj_name}_{i:03d}.png")
            
            print(f"   ✅ {obj_name}: {counts[split]} images in {split}/")
    
    print("✅ Dataset ready!\n")


def main():
    parser = argparse.ArgumentParser(description='Simple Trainer - The Vision Implemented')
    parser.add_argument('--prepare', action='store_true', help='Prepare dataset first')
    parser.add_argument('--epochs', type=int, default=MAX_EPOCHS, help='Max epochs')
    parser.add_argument('--target', type=float, default=TARGET_ACCURACY, help='Target accuracy (0-1)')
    parser.add_argument('--data-root', type=str, default=str(DATA_ROOT), help='Data directory')
    args = parser.parse_args()
    
    data_root = Path(args.data_root)
    
    print("=" * 60)
    print("SIMPLE TRAINER - The Quetzalcoatl Vision")
    print("=" * 60)
    print(f"Data root: {data_root}")
    print(f"Classes: {len(OBJECTS)} objects")
    print(f"Target: {args.target*100:.0f}% accuracy")
    print(f"Max epochs: {args.epochs}")
    print("=" * 60)
    
    # Prepare dataset if requested
    if args.prepare or not (data_root / 'train').exists():
        prepare_minimal_dataset(data_root)
    
    # Train
    trainer = SimpleTrainer(data_root, num_classes=len(OBJECTS))
    success = trainer.train(max_epochs=args.epochs, target_accuracy=args.target)
    
    if success:
        trainer.save_report()
        print("\n🎯 MISSION ACCOMPLISHED")
        print(f"   Best accuracy: {trainer.best_accuracy:.2f}%")
        print(f"   Checkpoint: {data_root}/checkpoints/best_model.pth")
    else:
        print("\n⚠️ Training incomplete - check dataset")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
