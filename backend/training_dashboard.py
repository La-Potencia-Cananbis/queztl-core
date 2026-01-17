#!/usr/bin/env python3
"""
Training Dashboard - Before/After Visualization
Shows what the model sees and what it learned
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import base64
from io import BytesIO

try:
    from flask import Flask, render_template, jsonify
    from PIL import Image, ImageDraw, ImageFont
    import torch
    from torchvision import transforms
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False
    print("⚠️ Install: pip install flask torch torchvision pillow")

app = Flask(__name__)

# Paths
DATA_ROOT = Path("/tmp/simple_training")
CHECKPOINT_PATH = DATA_ROOT / "checkpoints" / "best_model.pth"
REPORT_PATH = DATA_ROOT / "training_report.json"

OBJECTS = ["pencil", "apple", "book", "chair", "cup", "laptop", "phone", "scissors", "shoe", "watch"]


def load_training_report() -> Optional[Dict]:
    """Load training metrics."""
    if REPORT_PATH.exists():
        with open(REPORT_PATH) as f:
            return json.load(f)
    return None


def image_to_base64(img: Image.Image) -> str:
    """Convert PIL image to base64 for web display."""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def get_sample_images(split='train', max_per_class=3) -> Dict[str, List[str]]:
    """Get sample images from each class as base64."""
    samples = {}
    
    for obj_name in OBJECTS:
        obj_dir = DATA_ROOT / split / obj_name
        if not obj_dir.exists():
            continue
        
        images = list(obj_dir.glob("*.png"))[:max_per_class]
        samples[obj_name] = []
        
        for img_path in images:
            img = Image.open(img_path)
            samples[obj_name].append({
                'path': str(img_path.name),
                'base64': image_to_base64(img)
            })
    
    return samples


def create_prediction_visualization(model, device) -> Dict[str, List[Dict]]:
    """Run model on validation set and show predictions."""
    from torchvision import models
    import torch.nn as nn
    
    # Load model
    model = models.resnet18(pretrained=False)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(OBJECTS))
    
    if CHECKPOINT_PATH.exists():
        checkpoint = torch.load(CHECKPOINT_PATH, map_location=device)
        model.load_state_dict(checkpoint['model_state'])
        model = model.to(device)
        model.eval()
    else:
        return {}
    
    # Transform
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    results = {}
    
    # Test on validation images
    for obj_name in OBJECTS:
        obj_dir = DATA_ROOT / 'val' / obj_name
        if not obj_dir.exists():
            continue
        
        results[obj_name] = []
        
        for img_path in list(obj_dir.glob("*.png"))[:3]:
            img = Image.open(img_path).convert('RGB')
            img_tensor = transform(img).unsqueeze(0).to(device)
            
            with torch.no_grad():
                outputs = model(img_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted = probabilities.max(1)
                
                predicted_class = OBJECTS[predicted.item()]
                confidence_pct = confidence.item() * 100
                
                # Get top 3 predictions
                top3_conf, top3_idx = probabilities.topk(3, dim=1)
                top3 = [
                    {'class': OBJECTS[idx], 'confidence': conf.item() * 100}
                    for conf, idx in zip(top3_conf[0], top3_idx[0])
                ]
            
            results[obj_name].append({
                'image': image_to_base64(img),
                'true_label': obj_name,
                'predicted': predicted_class,
                'confidence': confidence_pct,
                'correct': predicted_class == obj_name,
                'top3': top3
            })
    
    return results


@app.route('/')
def dashboard():
    """Main dashboard."""
    return render_template('dashboard.html')


@app.route('/api/training_metrics')
def training_metrics():
    """Get training history."""
    report = load_training_report()
    if not report:
        return jsonify({'error': 'No training data found'}), 404
    
    return jsonify(report)


@app.route('/api/before_images')
def before_images():
    """Get training images (what model sees)."""
    samples = get_sample_images('train', max_per_class=5)
    return jsonify(samples)


@app.route('/api/after_predictions')
def after_predictions():
    """Get model predictions (what it learned)."""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    try:
        predictions = create_prediction_visualization(None, device)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status')
def status():
    """System status."""
    return jsonify({
        'checkpoint_exists': CHECKPOINT_PATH.exists(),
        'report_exists': REPORT_PATH.exists(),
        'num_classes': len(OBJECTS),
        'data_root': str(DATA_ROOT),
        'device': 'cuda' if torch.cuda.is_available() else 'cpu'
    })


def create_html_template():
    """Create the dashboard HTML."""
    template_dir = Path(__file__).parent / 'templates'
    template_dir.mkdir(exist_ok=True)
    
    html = '''<!DOCTYPE html>
<html>
<head>
    <title>Queztl Training Dashboard - Before/After</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #fff;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { 
            text-align: center; 
            margin-bottom: 10px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .subtitle {
            text-align: center;
            margin-bottom: 30px;
            opacity: 0.9;
            font-size: 1.2em;
        }
        
        .metrics-bar {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
        }
        .metric {
            text-align: center;
        }
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #4CAF50;
        }
        .metric-label {
            opacity: 0.8;
            margin-top: 5px;
        }
        
        .section {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
        }
        .section h2 {
            margin-bottom: 20px;
            border-bottom: 2px solid rgba(255,255,255,0.3);
            padding-bottom: 10px;
        }
        
        .comparison-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        
        .before-section, .after-section {
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            padding: 20px;
        }
        
        .image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .image-card {
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 10px;
            text-align: center;
            transition: transform 0.2s;
        }
        .image-card:hover {
            transform: scale(1.05);
            background: rgba(255,255,255,0.1);
        }
        .image-card img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 5px;
        }
        .image-label {
            margin-top: 8px;
            font-weight: bold;
        }
        
        .prediction-card {
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .prediction-card.correct {
            border-left: 4px solid #4CAF50;
        }
        .prediction-card.incorrect {
            border-left: 4px solid #f44336;
        }
        .prediction-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .confidence {
            font-size: 1.5em;
            font-weight: bold;
        }
        .confidence.high { color: #4CAF50; }
        .confidence.medium { color: #FFC107; }
        .confidence.low { color: #f44336; }
        
        .prediction-image {
            width: 100%;
            max-width: 200px;
            height: auto;
            border-radius: 5px;
            margin: 10px auto;
            display: block;
        }
        
        .top3 {
            margin-top: 10px;
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .learning-curve {
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .epoch-bar {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .epoch-label {
            width: 100px;
        }
        .progress-bar {
            flex: 1;
            height: 30px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            overflow: hidden;
            position: relative;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            transition: width 0.5s;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
        }
        
        .loading {
            text-align: center;
            padding: 50px;
            font-size: 1.5em;
        }
        
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-left: 10px;
        }
        .status-ready { background: #4CAF50; }
        .status-training { background: #FFC107; color: #000; }
        .status-error { background: #f44336; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Queztl Training Dashboard</h1>
        <p class="subtitle">Before/After Visualization - What The Agent Learned</p>
        
        <div class="metrics-bar" id="metrics">
            <div class="metric">
                <div class="metric-value" id="accuracy">--</div>
                <div class="metric-label">Best Accuracy</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="epochs">--</div>
                <div class="metric-label">Total Epochs</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="time">--</div>
                <div class="metric-label">Training Time</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="classes">10</div>
                <div class="metric-label">Object Classes</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Learning Progress</h2>
            <div class="learning-curve" id="learningCurve">
                <div class="loading">Loading training history...</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔍 Before & After Comparison</h2>
            <div class="comparison-grid">
                <div class="before-section">
                    <h3>📥 BEFORE: Training Data (What Agent Sees)</h3>
                    <div id="beforeImages">
                        <div class="loading">Loading training images...</div>
                    </div>
                </div>
                
                <div class="after-section">
                    <h3>🎯 AFTER: Predictions (What Agent Learned)</h3>
                    <div id="afterPredictions">
                        <div class="loading">Running predictions...</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Load training metrics
        async function loadMetrics() {
            try {
                const resp = await fetch('/api/training_metrics');
                const data = await resp.json();
                
                document.getElementById('accuracy').textContent = data.best_accuracy.toFixed(1) + '%';
                document.getElementById('epochs').textContent = data.total_epochs;
                
                // Calculate total time
                const totalTime = data.history.reduce((sum, h) => sum + h.time, 0);
                document.getElementById('time').textContent = (totalTime / 60).toFixed(1) + 'm';
                
                // Show learning curve
                showLearningCurve(data.history);
            } catch (e) {
                console.error('Failed to load metrics:', e);
            }
        }
        
        function showLearningCurve(history) {
            const container = document.getElementById('learningCurve');
            container.innerHTML = '';
            
            history.forEach(epoch => {
                const bar = document.createElement('div');
                bar.className = 'epoch-bar';
                bar.innerHTML = `
                    <div class="epoch-label">Epoch ${epoch.epoch}</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${epoch.val_acc}%">
                            ${epoch.val_acc.toFixed(1)}%
                        </div>
                    </div>
                `;
                container.appendChild(bar);
            });
        }
        
        // Load training images (BEFORE)
        async function loadBeforeImages() {
            try {
                const resp = await fetch('/api/before_images');
                const data = await resp.json();
                
                const container = document.getElementById('beforeImages');
                container.innerHTML = '';
                
                Object.entries(data).forEach(([objName, images]) => {
                    const section = document.createElement('div');
                    section.innerHTML = `<h4>${objName.toUpperCase()}</h4>`;
                    
                    const grid = document.createElement('div');
                    grid.className = 'image-grid';
                    
                    images.forEach(img => {
                        const card = document.createElement('div');
                        card.className = 'image-card';
                        card.innerHTML = `
                            <img src="data:image/png;base64,${img.base64}" alt="${objName}">
                            <div class="image-label">${objName}</div>
                        `;
                        grid.appendChild(card);
                    });
                    
                    section.appendChild(grid);
                    container.appendChild(section);
                });
            } catch (e) {
                console.error('Failed to load images:', e);
                document.getElementById('beforeImages').innerHTML = '<p>Error loading images</p>';
            }
        }
        
        // Load predictions (AFTER)
        async function loadAfterPredictions() {
            try {
                const resp = await fetch('/api/after_predictions');
                const data = await resp.json();
                
                const container = document.getElementById('afterPredictions');
                container.innerHTML = '';
                
                Object.entries(data).forEach(([objName, predictions]) => {
                    predictions.forEach(pred => {
                        const card = document.createElement('div');
                        card.className = `prediction-card ${pred.correct ? 'correct' : 'incorrect'}`;
                        
                        const confClass = pred.confidence > 90 ? 'high' : pred.confidence > 70 ? 'medium' : 'low';
                        
                        card.innerHTML = `
                            <div class="prediction-header">
                                <div>
                                    <strong>True:</strong> ${pred.true_label} → 
                                    <strong>Predicted:</strong> ${pred.predicted}
                                    ${pred.correct ? '✅' : '❌'}
                                </div>
                                <div class="confidence ${confClass}">${pred.confidence.toFixed(1)}%</div>
                            </div>
                            <img class="prediction-image" src="data:image/png;base64,${pred.image}" alt="prediction">
                            <div class="top3">
                                Top 3: ${pred.top3.map(t => `${t.class} (${t.confidence.toFixed(0)}%)`).join(', ')}
                            </div>
                        `;
                        container.appendChild(card);
                    });
                });
            } catch (e) {
                console.error('Failed to load predictions:', e);
                document.getElementById('afterPredictions').innerHTML = '<p>Error loading predictions</p>';
            }
        }
        
        // Load all data
        loadMetrics();
        loadBeforeImages();
        loadAfterPredictions();
        
        // Refresh every 30 seconds
        setInterval(() => {
            loadMetrics();
            loadAfterPredictions();
        }, 30000);
    </script>
</body>
</html>'''
    
    with open(template_dir / 'dashboard.html', 'w') as f:
        f.write(html)
    
    print(f"✅ Dashboard template created: {template_dir / 'dashboard.html'}")


if __name__ == '__main__':
    if not HAS_DEPS:
        print("Install dependencies: pip install flask torch torchvision pillow")
        exit(1)
    
    create_html_template()
    
    print("=" * 60)
    print("🚀 Starting Training Dashboard")
    print("=" * 60)
    print(f"📊 Dashboard: http://localhost:5000")
    print(f"📂 Data root: {DATA_ROOT}")
    print(f"🔍 Checkpoint: {CHECKPOINT_PATH.exists() and '✅ Found' or '⚠️ Not found'}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
