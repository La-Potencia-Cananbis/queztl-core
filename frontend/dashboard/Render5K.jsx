/**
 * 5K Renderer Dashboard Component
 * Add to your Next.js dashboard
 */

import { useState } from 'react';

export default function Render5K() {
    const [rendering, setRendering] = useState(false);
    const [result, setResult] = useState(null);
    const [preview, setPreview] = useState(null);
    const [sceneType, setSceneType] = useState('photorealistic');

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://queztl-core-backend.onrender.com';

    const startRender = async () => {
        setRendering(true);
        setResult(null);
        setPreview(null);

        try {
            const response = await fetch(`${API_URL}/api/render/5k`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    scene_type: sceneType,
                    width: 5120,
                    height: 2880,
                    return_image: true
                })
            });

            const data = await response.json();
            setResult(data);
            if (data.image_preview) {
                setPreview(data.image_preview);
            }
        } catch (error) {
            console.error('Render failed:', error);
            setResult({ error: error.message });
        } finally {
            setRendering(false);
        }
    };

    return (
        <div className="render-5k-container">
            <style jsx>{`
        .render-5k-container {
          padding: 2rem;
          max-width: 1200px;
          margin: 0 auto;
        }
        .header {
          text-align: center;
          margin-bottom: 2rem;
        }
        .header h1 {
          font-size: 2.5rem;
          margin-bottom: 0.5rem;
        }
        .controls {
          background: #1a1a1a;
          padding: 1.5rem;
          border-radius: 12px;
          margin-bottom: 2rem;
        }
        .control-group {
          margin-bottom: 1rem;
        }
        .control-group label {
          display: block;
          margin-bottom: 0.5rem;
          color: #aaa;
        }
        .control-group select {
          width: 100%;
          padding: 0.75rem;
          background: #2a2a2a;
          border: 1px solid #444;
          border-radius: 6px;
          color: white;
          font-size: 1rem;
        }
        .render-button {
          width: 100%;
          padding: 1rem 2rem;
          font-size: 1.2rem;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          transition: transform 0.2s;
          margin-top: 1rem;
        }
        .render-button:hover {
          transform: scale(1.02);
        }
        .render-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
          transform: none;
        }
        .status {
          text-align: center;
          padding: 2rem;
          font-size: 1.5rem;
        }
        .results {
          background: #1a1a1a;
          padding: 2rem;
          border-radius: 12px;
          margin-top: 2rem;
        }
        .result-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
          margin-top: 1rem;
        }
        .result-item {
          background: #2a2a2a;
          padding: 1rem;
          border-radius: 8px;
        }
        .result-label {
          color: #888;
          font-size: 0.9rem;
          margin-bottom: 0.5rem;
        }
        .result-value {
          font-size: 1.5rem;
          font-weight: bold;
          color: #667eea;
        }
        .grade {
          font-size: 3rem;
        }
        .preview {
          margin-top: 2rem;
        }
        .preview img {
          width: 100%;
          border-radius: 8px;
          box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }
        .qi-card-info {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          padding: 1rem;
          border-radius: 8px;
          margin-bottom: 1rem;
        }
      `}</style>

            <div className="header">
                <h1>🎨 5K Renderer</h1>
                <p>QI Card GPU Accelerated - 5120×2880 Resolution</p>
            </div>

            <div className="controls">
                <div className="control-group">
                    <label htmlFor="scene-type">Scene Type</label>
                    <select
                        id="scene-type"
                        value={sceneType}
                        onChange={(e) => setSceneType(e.target.value)}
                        disabled={rendering}
                    >
                        <option value="photorealistic">Photorealistic (Ray-traced Sphere)</option>
                        <option value="fractal">Fractal (Mandelbrot Set)</option>
                        <option value="benchmark">Benchmark (GPU Compute Test)</option>
                    </select>
                </div>

                <button
                    className="render-button"
                    onClick={startRender}
                    disabled={rendering}
                >
                    {rendering ? '⏳ Rendering 5K...' : '🚀 Start Render'}
                </button>
            </div>

            {rendering && (
                <div className="status">
                    <div>⚡ QI Card Processing...</div>
                    <div style={{ fontSize: '1rem', marginTop: '1rem', color: '#888' }}>
                        Rendering 14,745,600 pixels with GPU acceleration
                    </div>
                </div>
            )}

            {result && !result.error && (
                <div className="results">
                    {result.qi_card && (
                        <div className="qi-card-info">
                            <strong>🎮 {result.qi_card.name}</strong>
                            <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>
                                {result.qi_card.type} • {result.qi_card.memory_gb} GB
                            </div>
                        </div>
                    )}

                    <div className="result-grid">
                        <div className="result-item">
                            <div className="result-label">Resolution</div>
                            <div className="result-value">{result.resolution}</div>
                        </div>
                        <div className="result-item">
                            <div className="result-label">Time</div>
                            <div className="result-value">{result.duration}s</div>
                        </div>
                        <div className="result-item">
                            <div className="result-label">Speed</div>
                            <div className="result-value">{result.mpixels_per_sec} MP/s</div>
                        </div>
                        <div className="result-item">
                            <div className="result-label">Compute</div>
                            <div className="result-value">{result.gflops} GFLOPS</div>
                        </div>
                        <div className="result-item">
                            <div className="result-label">Grade</div>
                            <div className="result-value grade">{result.grade}</div>
                        </div>
                    </div>

                    {preview && (
                        <div className="preview">
                            <h3>Preview (downscaled to 1080p)</h3>
                            <img src={preview} alt="5K Render Preview" />
                            <p style={{ textAlign: 'center', marginTop: '1rem', color: '#888' }}>
                                Full 5K resolution rendered on backend
                            </p>
                        </div>
                    )}
                </div>
            )}

            {result && result.error && (
                <div className="results" style={{ color: '#ff6b6b' }}>
                    <h3>❌ Error</h3>
                    <p>{result.error}</p>
                </div>
            )}
        </div>
    );
}
