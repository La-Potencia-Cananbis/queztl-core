"""
Dynamic problem generator for Queztl-Core training
Generates realistic scenarios with varying complexity
"""
import random
import uuid
from typing import List, Dict, Any
from datetime import datetime, timedelta
import numpy as np

from models import TestScenario, DifficultyLevel

class ProblemGenerator:
    def __init__(self):
        self.scenario_types = [
            "load_balancing",
            "resource_allocation",
            "fault_tolerance",
            "data_processing",
            "concurrent_requests",
            "network_latency",
            "memory_optimization",
            "cache_efficiency"
        ]
        self.generated_problems: List[TestScenario] = []
        
    async def generate_scenario(self, difficulty: DifficultyLevel = None) -> TestScenario:
        """Generate a new training scenario"""
        if difficulty is None:
            difficulty = random.choice(list(DifficultyLevel))
        
        scenario_type = random.choice(self.scenario_types)
        scenario_id = f"{scenario_type}_{uuid.uuid4().hex[:8]}"
        
        parameters = self._generate_parameters(scenario_type, difficulty)
        description = self._generate_description(scenario_type, difficulty, parameters)
        expected_outcomes = self._generate_expected_outcomes(scenario_type, parameters)
        
        scenario = TestScenario(
            id=scenario_id,
            scenario_type=scenario_type,
            difficulty=difficulty,
            parameters=parameters,
            description=description,
            expected_outcomes=expected_outcomes
        )
        
        self.generated_problems.append(scenario)
        return scenario
    
    def _generate_parameters(self, scenario_type: str, difficulty: DifficultyLevel) -> Dict[str, Any]:
        """Generate scenario-specific parameters"""
        base_params = {
            "duration": self._get_duration(difficulty),
            "target_nodes": self._get_node_count(difficulty),
        }
        
        if scenario_type == "load_balancing":
            return {
                **base_params,
                "request_rate": self._get_request_rate(difficulty),
                "concurrent_users": self._get_concurrent_users(difficulty),
                "distribution_strategy": random.choice(["round_robin", "least_connections", "ip_hash"])
            }
        elif scenario_type == "resource_allocation":
            return {
                **base_params,
                "total_resources": 1000 * (1 + list(DifficultyLevel).index(difficulty)),
                "resource_types": random.randint(3, 8),
                "allocation_strategy": random.choice(["fair", "priority", "dynamic"])
            }
        elif scenario_type == "fault_tolerance":
            return {
                **base_params,
                "failure_rate": 0.05 * (1 + list(DifficultyLevel).index(difficulty)),
                "recovery_time": random.uniform(1.0, 5.0),
                "redundancy_level": random.randint(1, 3)
            }
        elif scenario_type == "data_processing":
            return {
                **base_params,
                "data_size_mb": 10 * (2 ** list(DifficultyLevel).index(difficulty)),
                "processing_complexity": difficulty.value,
                "parallel_workers": self._get_node_count(difficulty)
            }
        elif scenario_type == "concurrent_requests":
            return {
                **base_params,
                "concurrent_connections": self._get_concurrent_users(difficulty),
                "request_complexity": random.choice(["simple", "moderate", "complex"]),
                "timeout_ms": random.randint(100, 1000)
            }
        elif scenario_type == "network_latency":
            return {
                **base_params,
                "base_latency_ms": random.uniform(10, 100),
                "jitter_ms": random.uniform(5, 50),
                "packet_loss": random.uniform(0.0, 0.05)
            }
        elif scenario_type == "memory_optimization":
            return {
                **base_params,
                "memory_limit_mb": 512 * (1 + list(DifficultyLevel).index(difficulty)),
                "object_count": 10000 * (2 ** list(DifficultyLevel).index(difficulty)),
                "gc_strategy": random.choice(["aggressive", "balanced", "lazy"])
            }
        else:  # cache_efficiency
            return {
                **base_params,
                "cache_size_mb": 128 * (1 + list(DifficultyLevel).index(difficulty)),
                "hit_rate_target": 0.9 - (0.1 * list(DifficultyLevel).index(difficulty)),
                "eviction_policy": random.choice(["lru", "lfu", "fifo"])
            }
    
    def _generate_description(self, scenario_type: str, difficulty: DifficultyLevel, 
                            parameters: Dict[str, Any]) -> str:
        """Generate human-readable description"""
        descriptions = {
            "load_balancing": f"Balance {parameters['request_rate']} req/s across {parameters['target_nodes']} nodes",
            "resource_allocation": f"Allocate {parameters['total_resources']} resources across {parameters['resource_types']} types",
            "fault_tolerance": f"Maintain {parameters['redundancy_level']}x redundancy with {parameters['failure_rate']*100:.1f}% failure rate",
            "data_processing": f"Process {parameters['data_size_mb']}MB with {parameters['parallel_workers']} workers",
            "concurrent_requests": f"Handle {parameters['concurrent_connections']} concurrent connections",
            "network_latency": f"Operate with {parameters['base_latency_ms']:.1f}ms latency and {parameters['jitter_ms']:.1f}ms jitter",
            "memory_optimization": f"Manage {parameters['object_count']} objects in {parameters['memory_limit_mb']}MB",
            "cache_efficiency": f"Achieve {parameters['hit_rate_target']*100:.0f}% hit rate with {parameters['cache_size_mb']}MB cache"
        }
        return descriptions.get(scenario_type, f"{scenario_type} scenario ({difficulty.value})")
    
    def _generate_expected_outcomes(self, scenario_type: str, 
                                   parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate expected performance outcomes"""
        return {
            "min_success_rate": 0.95,
            "max_response_time_ms": 1000,
            "max_error_rate": 0.05,
            "min_throughput": parameters.get("request_rate", 100) * 0.9
        }
    
    def _get_duration(self, difficulty: DifficultyLevel) -> int:
        """Get scenario duration in seconds"""
        durations = {
            DifficultyLevel.EASY: random.randint(10, 30),
            DifficultyLevel.MEDIUM: random.randint(30, 60),
            DifficultyLevel.HARD: random.randint(60, 120),
            DifficultyLevel.EXTREME: random.randint(120, 300)
        }
        return durations[difficulty]
    
    def _get_node_count(self, difficulty: DifficultyLevel) -> int:
        """Get number of nodes for scenario"""
        counts = {
            DifficultyLevel.EASY: random.randint(2, 5),
            DifficultyLevel.MEDIUM: random.randint(5, 10),
            DifficultyLevel.HARD: random.randint(10, 20),
            DifficultyLevel.EXTREME: random.randint(20, 50)
        }
        return counts[difficulty]
    
    def _get_request_rate(self, difficulty: DifficultyLevel) -> int:
        """Get requests per second"""
        rates = {
            DifficultyLevel.EASY: random.randint(10, 50),
            DifficultyLevel.MEDIUM: random.randint(50, 200),
            DifficultyLevel.HARD: random.randint(200, 500),
            DifficultyLevel.EXTREME: random.randint(500, 2000)
        }
        return rates[difficulty]
    
    def _get_concurrent_users(self, difficulty: DifficultyLevel) -> int:
        """Get concurrent user count"""
        users = {
            DifficultyLevel.EASY: random.randint(10, 50),
            DifficultyLevel.MEDIUM: random.randint(50, 200),
            DifficultyLevel.HARD: random.randint(200, 1000),
            DifficultyLevel.EXTREME: random.randint(1000, 5000)
        }
        return users[difficulty]
    
    async def get_recent_problems(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recently generated problems"""
        return [
            {
                "id": p.id,
                "type": p.scenario_type,
                "difficulty": p.difficulty.value,
                "description": p.description,
                "created_at": p.created_at.isoformat()
            }
            for p in self.generated_problems[-limit:]
        ]
