#!/usr/bin/env python3
"""
Simple ML trainer for Queztl agents
Supports MNIST, CIFAR10, and synthetic data
"""
import torch
import torch.nn as nn
import torch.optim as optim
import argparse
import time
import json
from pathlib import Path


class SimpleNet(nn.Module):
    """Lightweight neural network for quick training"""
    def __init__(self, input_size=784, hidden_size=128, num_classes=10):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, num_classes)
        
    def forward(self, x):
        x = x.view(x.size(0), -1)  # Flatten
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def generate_synthetic_data(num_samples=1000, input_size=784, num_classes=10):
    """Generate synthetic training data for testing"""
    X = torch.randn(num_samples, input_size)
    y = torch.randint(0, num_classes, (num_samples,))
    return X, y


def train_model(model, train_data, train_labels, epochs=3, lr=0.01, target_acc=0.85):
    """Train the model and return metrics"""
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=lr, momentum=0.9)
    
    batch_size = 32
    num_samples = len(train_data)
    num_batches = (num_samples + batch_size - 1) // batch_size
    
    metrics = {
        "epochs": epochs,
        "target_accuracy": target_acc,
        "final_accuracy": 0.0,
        "final_loss": 0.0,
        "training_time": 0.0,
        "converged": False
    }
    
    start_time = time.time()
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0.0
        correct = 0
        total = 0
        
        # Shuffle data
        perm = torch.randperm(num_samples)
        train_data = train_data[perm]
        train_labels = train_labels[perm]
        
        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, num_samples)
            
            batch_x = train_data[start_idx:end_idx]
            batch_y = train_labels[start_idx:end_idx]
            
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += batch_y.size(0)
            correct += predicted.eq(batch_y).sum().item()
        
        avg_loss = total_loss / num_batches
        accuracy = correct / total
        
        print(f"Epoch {epoch+1}/{epochs}: Loss={avg_loss:.4f}, Acc={accuracy:.4f}")
        
        metrics["final_loss"] = avg_loss
        metrics["final_accuracy"] = accuracy
        
        if accuracy >= target_acc:
            metrics["converged"] = True
            print(f"✓ Target accuracy {target_acc} reached!")
            break
    
    metrics["training_time"] = time.time() - start_time
    return metrics


def main():
    parser = argparse.ArgumentParser(description='Simple trainer for Queztl agents')
    parser.add_argument('--epochs', type=int, default=3, help='Number of training epochs')
    parser.add_argument('--lr', type=float, default=0.01, help='Learning rate')
    parser.add_argument('--hidden', type=int, default=128, help='Hidden layer size')
    parser.add_argument('--samples', type=int, default=1000, help='Number of synthetic samples')
    parser.add_argument('--target-acc', type=float, default=0.85, help='Target accuracy')
    parser.add_argument('--output', type=str, help='Output path for model checkpoint')
    parser.add_argument('--metrics', type=str, help='Output path for metrics JSON')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("QUEZTL SIMPLE TRAINER")
    print("=" * 60)
    print(f"Epochs: {args.epochs}")
    print(f"Learning rate: {args.lr}")
    print(f"Hidden size: {args.hidden}")
    print(f"Target accuracy: {args.target_acc}")
    print()
    
    # Generate synthetic data
    print(f"Generating {args.samples} synthetic samples...")
    train_data, train_labels = generate_synthetic_data(args.samples)
    print(f"✓ Data shape: {train_data.shape}")
    print()
    
    # Create model
    model = SimpleNet(input_size=784, hidden_size=args.hidden, num_classes=10)
    print(f"✓ Model created: {sum(p.numel() for p in model.parameters())} parameters")
    print()
    
    # Train
    print("Starting training...")
    metrics = train_model(
        model, 
        train_data, 
        train_labels, 
        epochs=args.epochs,
        lr=args.lr,
        target_acc=args.target_acc
    )
    
    print()
    print("=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)
    print(f"Final accuracy: {metrics['final_accuracy']:.4f}")
    print(f"Final loss: {metrics['final_loss']:.4f}")
    print(f"Training time: {metrics['training_time']:.2f}s")
    print(f"Converged: {metrics['converged']}")
    
    # Save model if requested
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        torch.save({
            'model_state_dict': model.state_dict(),
            'metrics': metrics,
        }, output_path)
        print(f"✓ Model saved to {output_path}")
    
    # Save metrics if requested
    if args.metrics:
        metrics_path = Path(args.metrics)
        metrics_path.parent.mkdir(parents=True, exist_ok=True)
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"✓ Metrics saved to {metrics_path}")
    
    print()
    return 0 if metrics['converged'] else 1


if __name__ == "__main__":
    exit(main())
