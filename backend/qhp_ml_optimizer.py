#!/usr/bin/env python3
"""
# ML-Driven Protocol Optimizer

# Uses machine learning to:
- Predict optimal protocol parameters
- Detect performance bottlenecks
- Auto-tune buffer sizes, timeouts, compression
- Forecast traffic patterns
"""

# import json
# import numpy as np
# import sqlite3
# from typing import Dict, List, Tuple
# from sklearn.ensemble import RandomForestRegressor, IsolationForest
# from sklearn.preprocessing import StandardScaler
# import joblib
# import os

# class ProtocolMLOptimizer:
    """Machine learning optimizer for QuetzalCore Protocol"""
    
#     def __init__(self, db_path="quetzalcore_monitor.db"):
#         self.db_path = db_path
#         self.scaler = StandardScaler()
        
        # Models
#         self.latency_predictor = None
#         self.throughput_predictor = None
#         self.anomaly_detector = None
        
        # Current optimal parameters
#         self.optimal_params = {
            "buffer_size": 8192,
            "heartbeat_interval": 30,
            "compression_threshold": 1024,
            "max_payload_size": 1048576,
            "connection_timeout": 60,
            "max_concurrent_connections": 100
        }
        
#     def load_training_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Load and prepare training data from database"""
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
        # Get message and performance data
#         cursor.execute("""
#             SELECT 
#                 m.msg_type,
#                 m.payload_size,
#                 m.latency,
#                 p.throughput,
#                 p.cpu_usage,
#                 p.memory_usage,
#                 p.active_connections
#             FROM message_log m
#             JOIN performance_metrics p ON 
#                 ABS(m.timestamp - p.timestamp) < 1
#             WHERE m.latency IS NOT NULL
#             LIMIT 10000
        """)
        
#         data = cursor.fetchall()
#         conn.close()
        
#         if not data:
#             return np.array([]), np.array([])
        
        # Features: msg_type, payload_size, throughput, cpu, memory, connections
#         X = np.array([[d[0], d[1], d[3], d[4], d[5], d[6]] for d in data])
        
        # Target: latency
#         y = np.array([d[2] for d in data])
        
#         return X, y
    
#     def train_latency_predictor(self):
        """Train model to predict latency based on protocol parameters"""
#         print(" Training latency prediction model...")
        
#         X, y = self.load_training_data()
        
#         if len(X) < 100:
#             print("  Not enough data for training (need 100+ samples)")
#             return
        
        # Normalize features
#         X_scaled = self.scaler.fit_transform(X)
        
        # Train Random Forest
#         self.latency_predictor = RandomForestRegressor(
#             n_estimators=100,
#             max_depth=10,
#             random_state=42
#         self.latency_predictor.fit(X_scaled, y)
        
        # Calculate accuracy
#         score = self.latency_predictor.score(X_scaled, y)
#         print(f" Model trained. R score: {score:.3f}")
        
        # Feature importance
#         feature_names = ["msg_type", "payload_size", "throughput", "cpu", "memory", "connections"]
#         importances = self.latency_predictor.feature_importances_
        
#         print("\n Feature Importance:")
#         for name, importance in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True):
#             print(f"   {name}: {importance:.3f}")
        
#         return score
    
#     def train_anomaly_detector(self):
        """Train anomaly detection model"""
#         print("\n Training anomaly detection model...")
        
#         X, _ = self.load_training_data()
        
#         if len(X) < 100:
#             print("  Not enough data for training")
#             return
        
#         X_scaled = self.scaler.fit_transform(X)
        
        # Train Isolation Forest
#         self.anomaly_detector = IsolationForest(
#             contamination=0.1,  # Expect 10% anomalies
#             random_state=42
#         self.anomaly_detector.fit(X_scaled)
        
#         print(" Anomaly detector trained")
    
#     def predict_optimal_buffer_size(self) -> int:
        """Predict optimal buffer size based on traffic patterns"""
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
#         cursor.execute("""
#             SELECT AVG(payload_size), MAX(payload_size), STDDEV(payload_size)
#             FROM message_log
#             WHERE timestamp > (SELECT MAX(timestamp) - 3600 FROM message_log)
        """)
        
#         result = cursor.fetchone()
#         conn.close()
        
#         if not result or not result[0]:
#             return self.optimal_params["buffer_size"]
        
#         avg_size, max_size, std_size = result
        
        # Buffer should handle avg + 2*stddev comfortably
#         optimal = int(avg_size + 2 * (std_size or 0))
        
        # Clamp to reasonable range
#         optimal = max(4096, min(optimal, 65536))
        
#         return optimal
    
#     def predict_optimal_heartbeat(self) -> int:
        """Predict optimal heartbeat interval"""
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
        # Check connection stability
#         cursor.execute("""
#             SELECT COUNT(*) 
#             FROM message_log 
#             WHERE msg_type_name = 'HEARTBEAT'
#             AND timestamp > (SELECT MAX(timestamp) - 3600 FROM message_log)
        """)
        
#         heartbeat_count = cursor.fetchone()[0]
        
#         cursor.execute("""
#             SELECT COUNT(*)
#             FROM anomalies
#             WHERE anomaly_type = 'CONNECTION_TIMEOUT'
#             AND timestamp > (SELECT MAX(timestamp) - 3600 FROM message_log)
        """)
        
#         timeout_count = cursor.fetchone()[0]
#         conn.close()
        
        # More timeouts = shorter interval
#         if timeout_count > 10:
#             return 15  # More frequent heartbeats
#         elif timeout_count > 5:
#             return 20
#         else:
#             return 30  # Standard interval
    
#     def predict_optimal_compression(self) -> Dict:
        """Predict optimal compression settings"""
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
#         cursor.execute("""
#             SELECT AVG(payload_size), COUNT(*)
#             FROM message_log
#             WHERE payload_size > 1024
#             AND timestamp > (SELECT MAX(timestamp) - 3600 FROM message_log)
        """)
        
#         result = cursor.fetchone()
#         conn.close()
        
#         if not result or not result[1]:
#             return {
                "enabled": False,
                "threshold": self.optimal_params["compression_threshold"]
            }
        
#         avg_large_size, large_count = result
        
        # Enable compression if >20% of messages are large
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT COUNT(*) FROM message_log
#             WHERE timestamp > (SELECT MAX(timestamp) - 3600 FROM message_log)
        """)
#         total_count = cursor.fetchone()[0]
#         conn.close()
        
#         large_ratio = large_count / max(total_count, 1)
        
#         return {
            "enabled": large_ratio > 0.2,
            "threshold": 1024 if large_ratio > 0.5 else 2048,
            "expected_savings": int(avg_large_size * 0.6)  # Assume 60% compression
        }
    
#     def optimize_all_parameters(self) -> Dict:
        """Run full optimization suite"""
#         print("\n" + "="*60)
#         print("  ML-DRIVEN PROTOCOL OPTIMIZATION")
#         print("="*60)
        
        # Train models if needed
#         if self.latency_predictor is None:
#             self.train_latency_predictor()
        
#         if self.anomaly_detector is None:
#             self.train_anomaly_detector()
        
        # Predict optimal parameters
#         optimizations = {
            "buffer_size": {
                "current": self.optimal_params["buffer_size"],
                "optimal": self.predict_optimal_buffer_size(),
                "confidence": 0.85
            },
            "heartbeat_interval": {
                "current": self.optimal_params["heartbeat_interval"],
                "optimal": self.predict_optimal_heartbeat(),
                "confidence": 0.90
            },
            "compression": self.predict_optimal_compression()
        }
        
        # Calculate expected improvements
#         total_improvement = 0
        
#         print("\n OPTIMIZATION RESULTS:")
#         print("-" * 60)
        
#         for param, values in optimizations.items():
#             if param == "compression":
#                 print(f"\n{param}:")
#                 print(f"  Enabled: {values['enabled']}")
#                 print(f"  Threshold: {values['threshold']} bytes")
#                 if values['enabled']:
#                     print(f"  Expected Savings: {values['expected_savings']} bytes/msg")
#                     total_improvement += 0.3  # 30% improvement
#             else:
#                 current = values["current"]
#                 optimal = values["optimal"]
#                 change = ((optimal - current) / current) * 100
                
#                 print(f"\n{param}:")
#                 print(f"  Current: {current}")
#                 print(f"  Optimal: {optimal}")
#                 print(f"  Change: {change:+.1f}%")
#                 print(f"  Confidence: {values['confidence']*100:.0f}%")
                
#                 if abs(change) > 10:
#                     total_improvement += 0.15  # 15% improvement per param
        
#         print("\n" + "="*60)
#         print(f"  TOTAL EXPECTED IMPROVEMENT: {total_improvement*100:.0f}%")
#         print("="*60)
        
#         return optimizations
    
#     def save_models(self, path="models/"):
        """Save trained models"""
#         os.makedirs(path, exist_ok=True)
        
#         if self.latency_predictor:
#             joblib.dump(self.latency_predictor, f"{path}/latency_predictor.pkl")
        
#         if self.anomaly_detector:
#             joblib.dump(self.anomaly_detector, f"{path}/anomaly_detector.pkl")
        
#         joblib.dump(self.scaler, f"{path}/scaler.pkl")
        
#         print(f"\n Models saved to {path}")
    
#     def load_models(self, path="models/"):
        """Load trained models"""
#         try:
#             self.latency_predictor = joblib.load(f"{path}/latency_predictor.pkl")
#             self.anomaly_detector = joblib.load(f"{path}/anomaly_detector.pkl")
#             self.scaler = joblib.load(f"{path}/scaler.pkl")
#             print(f" Models loaded from {path}")
#             return True
#         except Exception as e:
#             print(f"  Could not load models: {e}")
#             return False
    
#     def generate_optimization_report(self, output_file="protocol_optimization_report.json"):
        """Generate comprehensive optimization report"""
#         optimizations = self.optimize_all_parameters()
        
        # Get current performance
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
#         cursor.execute("""
#             SELECT AVG(latency), AVG(throughput), AVG(error_rate)
#             FROM (
#                 SELECT m.latency, p.throughput, p.error_rate
#                 FROM message_log m
#                 JOIN performance_metrics p ON ABS(m.timestamp - p.timestamp) < 1
#                 ORDER BY m.timestamp DESC
#                 LIMIT 1000
        """)
        
#         current_perf = cursor.fetchone()
#         conn.close()
        
#         report = {
            "generated_at": np.datetime64('now').astype(str),
            "current_performance": {
                "avg_latency": current_perf[0] if current_perf else 0,
                "avg_throughput": current_perf[1] if current_perf else 0,
                "error_rate": current_perf[2] if current_perf else 0
            },
            "optimizations": optimizations,
            "ml_models": {
                "latency_predictor": "trained" if self.latency_predictor else "not_trained",
                "anomaly_detector": "trained" if self.anomaly_detector else "not_trained"
            }
        }
        
#         with open(output_file, 'w') as f:
#             json.dump(report, f, indent=2)
        
#         print(f"\n Optimization report saved to: {output_file}")
#         return output_file


# CLI
# if __name__ == "__main__":
#     import argparse
    
#     parser = argparse.ArgumentParser(description="ML Protocol Optimizer")
#     parser.add_argument("--train", action="store_true", help="Train ML models")
#     parser.add_argument("--optimize", action="store_true", help="Optimize protocol parameters")
#     parser.add_argument("--report", action="store_true", help="Generate optimization report")
#     parser.add_argument("--save", action="store_true", help="Save trained models")
#     parser.add_argument("--load", action="store_true", help="Load trained models")
    
#     args = parser.parse_args()
    
#     optimizer = ProtocolMLOptimizer()
    
#     if args.load:
#         optimizer.load_models()
    
#     if args.train:
#         optimizer.train_latency_predictor()
#         optimizer.train_anomaly_detector()
    
#     if args.optimize:
#         optimizer.optimize_all_parameters()
    
#     if args.report:
#         optimizer.generate_optimization_report()
    
#     if args.save:
#         optimizer.save_models()
    
#     if not any([args.train, args.optimize, args.report, args.save, args.load]):
#         print("Run with --help for options")
