#!/usr/bin/env python3
"""
Model Verification & Tuning System
Compares generated models with reference data and tunes the system
"""
import requests
import json
import time
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
import sys

# Reference models from free3d.com and similar sites
REFERENCE_MODELS = [
    {
        "name": "Military Tank",
        "prompt": "military tank with turret and tracks",
        "category": "vehicles",
        "expected_vertices_range": (500, 2000),
        "expected_complexity": "medium",
        "keywords": ["vehicle", "military", "tank", "armor"]
    },
    {
        "name": "Sci-Fi Spaceship",
        "prompt": "futuristic spaceship with engines and wings",
        "category": "vehicles",
        "expected_vertices_range": (300, 1500),
        "expected_complexity": "medium",
        "keywords": ["spaceship", "scifi", "vehicle", "futuristic"]
    },
    {
        "name": "Medieval Castle",
        "prompt": "medieval castle with towers and walls",
        "category": "architecture",
        "expected_vertices_range": (400, 1200),
        "expected_complexity": "high",
        "keywords": ["castle", "medieval", "building", "fortress"]
    },
    {
        "name": "Dragon Creature",
        "prompt": "fantasy dragon with wings and tail",
        "category": "creatures",
        "expected_vertices_range": (350, 1000),
        "expected_complexity": "high",
        "keywords": ["dragon", "creature", "fantasy", "monster"]
    },
    {
        "name": "Robot Character",
        "prompt": "humanoid robot with mechanical parts",
        "category": "characters",
        "expected_vertices_range": (300, 1000),
        "expected_complexity": "medium",
        "keywords": ["robot", "character", "humanoid", "mechanical"]
    },
    {
        "name": "Sports Car",
        "prompt": "sleek sports car with low profile",
        "category": "vehicles",
        "expected_vertices_range": (400, 1200),
        "expected_complexity": "medium",
        "keywords": ["car", "vehicle", "sports", "automotive"]
    },
    {
        "name": "Fantasy Sword",
        "prompt": "ornate fantasy sword with decorative blade",
        "category": "weapons",
        "expected_vertices_range": (150, 500),
        "expected_complexity": "low",
        "keywords": ["sword", "weapon", "blade", "fantasy"]
    },
    {
        "name": "Alien Creature",
        "prompt": "alien creature with tentacles and multiple eyes",
        "category": "creatures",
        "expected_vertices_range": (300, 900),
        "expected_complexity": "medium",
        "keywords": ["alien", "creature", "monster", "scifi"]
    },
    {
        "name": "Wooden Chair",
        "prompt": "simple wooden chair with four legs",
        "category": "furniture",
        "expected_vertices_range": (100, 400),
        "expected_complexity": "low",
        "keywords": ["chair", "furniture", "wooden", "simple"]
    },
    {
        "name": "Tree with Branches",
        "prompt": "deciduous tree with branches and leaves",
        "category": "nature",
        "expected_vertices_range": (200, 800),
        "expected_complexity": "medium",
        "keywords": ["tree", "nature", "plant", "organic"]
    },
    {
        "name": "Helicopter",
        "prompt": "military helicopter with rotors and tail",
        "category": "vehicles",
        "expected_vertices_range": (350, 1000),
        "expected_complexity": "medium",
        "keywords": ["helicopter", "aircraft", "vehicle", "military"]
    },
    {
        "name": "Human Head",
        "prompt": "realistic human head with facial features",
        "category": "characters",
        "expected_vertices_range": (400, 1500),
        "expected_complexity": "high",
        "keywords": ["head", "human", "face", "character"]
    },
    {
        "name": "Building Complex",
        "prompt": "modern office building with windows",
        "category": "architecture",
        "expected_vertices_range": (300, 1000),
        "expected_complexity": "medium",
        "keywords": ["building", "architecture", "office", "modern"]
    },
    {
        "name": "Weapon Rifle",
        "prompt": "tactical assault rifle with scope",
        "category": "weapons",
        "expected_vertices_range": (250, 700),
        "expected_complexity": "medium",
        "keywords": ["rifle", "weapon", "gun", "tactical"]
    },
    {
        "name": "Crystal Gem",
        "prompt": "geometric crystal with faceted surfaces",
        "category": "objects",
        "expected_vertices_range": (100, 300),
        "expected_complexity": "low",
        "keywords": ["crystal", "gem", "geometric", "faceted"]
    }
]


class ModelVerifier:
    """Verify and tune the trained model"""
    
    def __init__(self, api_base="http://localhost:8000"):
        self.api_base = api_base
        self.results = []
        
    def generate_model(self, prompt: str) -> Dict[str, Any]:
        """Generate model using trained system"""
        try:
            url = f"{self.api_base}/api/gen3d/trained-model"
            params = {"prompt": prompt, "format": "json"}
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def evaluate_model(self, generated: Dict, reference: Dict) -> Dict[str, Any]:
        """Evaluate generated model against reference"""
        if "error" in generated:
            return {
                "score": 0.0,
                "passed": False,
                "reason": f"Generation failed: {generated['error']}"
            }
        
        stats = generated.get('stats', {})
        vertices = stats.get('vertices', 0)
        faces = stats.get('faces', 0)
        gen_time = generated.get('generation_time_ms', 0)
        
        # Scoring criteria
        scores = {}
        
        # 1. Vertex count in expected range (30%)
        min_v, max_v = reference['expected_vertices_range']
        if min_v <= vertices <= max_v:
            scores['vertex_range'] = 1.0
        elif vertices < min_v:
            scores['vertex_range'] = max(0, vertices / min_v)
        else:
            scores['vertex_range'] = max(0, 1 - (vertices - max_v) / max_v)
        
        # 2. Face/vertex ratio (20%) - good meshes have ~1.5-2.0 faces per vertex
        if vertices > 0:
            ratio = faces / vertices
            ideal_ratio = 1.8
            scores['mesh_quality'] = max(0, 1 - abs(ratio - ideal_ratio) / ideal_ratio)
        else:
            scores['mesh_quality'] = 0
        
        # 3. Generation speed (20%) - should be under 50ms
        if gen_time < 10:
            scores['speed'] = 1.0
        elif gen_time < 50:
            scores['speed'] = 0.8
        elif gen_time < 100:
            scores['speed'] = 0.5
        else:
            scores['speed'] = 0.2
        
        # 4. Model exists and has geometry (30%)
        if vertices > 10 and faces > 3:
            scores['validity'] = 1.0
        elif vertices > 0:
            scores['validity'] = 0.5
        else:
            scores['validity'] = 0.0
        
        # Calculate weighted score
        weights = {
            'vertex_range': 0.30,
            'mesh_quality': 0.20,
            'speed': 0.20,
            'validity': 0.30
        }
        
        total_score = sum(scores[k] * weights[k] for k in scores)
        
        return {
            "score": total_score,
            "passed": total_score >= 0.6,
            "scores": scores,
            "metrics": {
                "vertices": vertices,
                "faces": faces,
                "generation_time_ms": gen_time,
                "vertex_ratio": vertices / reference['expected_vertices_range'][1]
            }
        }
    
    def run_verification(self) -> Dict[str, Any]:
        """Run full verification suite"""
        print("🔍 MODEL VERIFICATION & TUNING SYSTEM")
        print("=" * 70)
        print(f"Testing {len(REFERENCE_MODELS)} reference models...")
        print()
        
        all_results = []
        passed_count = 0
        total_score = 0
        
        for idx, ref_model in enumerate(REFERENCE_MODELS, 1):
            print(f"[{idx}/{len(REFERENCE_MODELS)}] Testing: {ref_model['name']}")
            print(f"  Prompt: {ref_model['prompt']}")
            
            # Generate model
            start_time = time.time()
            generated = self.generate_model(ref_model['prompt'])
            generation_time = time.time() - start_time
            
            # Evaluate
            evaluation = self.evaluate_model(generated, ref_model)
            
            # Store results
            result = {
                "reference": ref_model,
                "generated": generated,
                "evaluation": evaluation,
                "timestamp": datetime.now().isoformat()
            }
            all_results.append(result)
            
            # Display results
            score = evaluation['score']
            passed = evaluation['passed']
            
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  Score: {score:.2%} {status}")
            
            if "error" not in generated:
                metrics = evaluation['metrics']
                print(f"  Vertices: {metrics['vertices']} "
                      f"(expected: {ref_model['expected_vertices_range'][0]}-{ref_model['expected_vertices_range'][1]})")
                print(f"  Faces: {metrics['faces']}")
                print(f"  Time: {metrics['generation_time_ms']:.1f}ms")
            else:
                print(f"  Error: {generated['error']}")
            
            print()
            
            if passed:
                passed_count += 1
            total_score += score
        
        # Calculate overall statistics
        avg_score = total_score / len(REFERENCE_MODELS)
        pass_rate = passed_count / len(REFERENCE_MODELS)
        
        print("=" * 70)
        print("📊 VERIFICATION RESULTS")
        print("=" * 70)
        print(f"Total Tests: {len(REFERENCE_MODELS)}")
        print(f"Passed: {passed_count}/{len(REFERENCE_MODELS)} ({pass_rate:.1%})")
        print(f"Average Score: {avg_score:.2%}")
        print()
        
        # Category breakdown
        print("📈 CATEGORY BREAKDOWN:")
        categories = {}
        for result in all_results:
            cat = result['reference']['category']
            if cat not in categories:
                categories[cat] = {'scores': [], 'count': 0, 'passed': 0}
            
            categories[cat]['scores'].append(result['evaluation']['score'])
            categories[cat]['count'] += 1
            if result['evaluation']['passed']:
                categories[cat]['passed'] += 1
        
        for cat, data in sorted(categories.items()):
            avg = np.mean(data['scores'])
            rate = data['passed'] / data['count']
            print(f"  {cat:15s}: {avg:.2%} ({data['passed']}/{data['count']} passed)")
        
        print()
        
        # Generate recommendations
        recommendations = self.generate_recommendations(all_results)
        
        print("💡 TUNING RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        
        print()
        print("=" * 70)
        
        # Save results
        results_file = "/tmp/model_verification_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                'summary': {
                    'total_tests': len(REFERENCE_MODELS),
                    'passed': passed_count,
                    'pass_rate': pass_rate,
                    'average_score': avg_score,
                    'timestamp': datetime.now().isoformat()
                },
                'category_breakdown': {
                    cat: {
                        'average_score': float(np.mean(data['scores'])),
                        'pass_rate': data['passed'] / data['count'],
                        'count': data['count']
                    }
                    for cat, data in categories.items()
                },
                'results': all_results,
                'recommendations': recommendations
            }, f, indent=2)
        
        print(f"📁 Full results saved to: {results_file}")
        
        return {
            'pass_rate': pass_rate,
            'average_score': avg_score,
            'results': all_results,
            'recommendations': recommendations
        }
    
    def generate_recommendations(self, results: List[Dict]) -> List[str]:
        """Generate tuning recommendations based on results"""
        recommendations = []
        
        # Analyze vertex counts
        vertices = [r['evaluation']['metrics']['vertices'] 
                   for r in results if 'metrics' in r['evaluation']]
        
        if vertices:
            avg_vertices = np.mean(vertices)
            if avg_vertices < 200:
                recommendations.append(
                    "Increase model capacity: Average vertices too low. "
                    "Train with output_vertices=1024 or higher."
                )
            elif avg_vertices > 400:
                recommendations.append(
                    "Model generating too many vertices. Consider pruning or "
                    "training with more varied dataset sizes."
                )
        
        # Analyze speed
        times = [r['evaluation']['metrics']['generation_time_ms'] 
                for r in results if 'metrics' in r['evaluation']]
        
        if times:
            avg_time = np.mean(times)
            if avg_time > 50:
                recommendations.append(
                    f"Generation slow (avg {avg_time:.1f}ms). Consider model optimization "
                    "or GPU acceleration."
                )
        
        # Analyze category performance
        categories = {}
        for r in results:
            cat = r['reference']['category']
            score = r['evaluation']['score']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(score)
        
        for cat, scores in categories.items():
            avg_score = np.mean(scores)
            if avg_score < 0.5:
                recommendations.append(
                    f"Poor performance on '{cat}' category ({avg_score:.1%}). "
                    f"Add more {cat} examples to training data."
                )
        
        # Mesh quality
        ratios = [r['evaluation']['metrics']['faces'] / max(1, r['evaluation']['metrics']['vertices'])
                 for r in results if 'metrics' in r['evaluation']]
        
        if ratios:
            avg_ratio = np.mean(ratios)
            if avg_ratio < 1.0:
                recommendations.append(
                    f"Low face/vertex ratio ({avg_ratio:.2f}). Improve face generation algorithm."
                )
        
        if not recommendations:
            recommendations.append("Model performing well! Consider training on real 3D assets for quality improvement.")
        
        return recommendations


if __name__ == "__main__":
    print("Starting Model Verification...")
    print()
    
    verifier = ModelVerifier()
    results = verifier.run_verification()
    
    if results['pass_rate'] >= 0.7:
        print("✅ System verification PASSED")
        sys.exit(0)
    else:
        print("⚠️  System needs tuning")
        sys.exit(1)
