"""
Training engine for adaptive learning and performance optimization
"""
import asyncio
import random
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import numpy as np

from models import (
    PerformanceMetric, ScenarioResult, TrainingStatus, 
    MetricsSummary, MetricType, DifficultyLevel
)
from problem_generator import ProblemGenerator

class TrainingEngine:
    def __init__(self):
        self.is_training = False
        self.current_scenario = None
        self.scenarios_completed = 0
        self.start_time = None
        self.metrics_history: List[PerformanceMetric] = []
        self.scenario_results: List[ScenarioResult] = []
        self.problem_generator = ProblemGenerator()
        self.current_difficulty = DifficultyLevel.EASY
        
    async def execute_scenario(self, scenario_id: str) -> ScenarioResult:
        """Execute a training scenario and collect metrics"""
        scenario = await self.problem_generator.generate_scenario(self.current_difficulty)
        
        start_time = time.time()
        metrics = []
        errors = []
        
        # Simulate scenario execution
        duration = scenario.parameters.get("duration", 30)
        
        for i in range(duration):
            # Simulate collecting metrics
            response_time = self._simulate_response_time(scenario.difficulty)
            throughput = self._simulate_throughput(scenario.difficulty)
            cpu_usage = self._simulate_cpu_usage(scenario.difficulty)
            memory_usage = self._simulate_memory_usage(scenario.difficulty)
            error_rate = self._simulate_error_rate(scenario.difficulty)
            
            metrics.extend([
                PerformanceMetric(
                    metric_type=MetricType.RESPONSE_TIME,
                    value=response_time,
                    scenario_id=scenario_id
                ),
                PerformanceMetric(
                    metric_type=MetricType.THROUGHPUT,
                    value=throughput,
                    scenario_id=scenario_id
                ),
                PerformanceMetric(
                    metric_type=MetricType.CPU_USAGE,
                    value=cpu_usage,
                    scenario_id=scenario_id
                ),
                PerformanceMetric(
                    metric_type=MetricType.MEMORY_USAGE,
                    value=memory_usage,
                    scenario_id=scenario_id
                ),
                PerformanceMetric(
                    metric_type=MetricType.ERROR_RATE,
                    value=error_rate,
                    scenario_id=scenario_id
                )
            ])
            
            # Check for errors
            if error_rate > 0.1:
                errors.append(f"High error rate detected: {error_rate*100:.1f}%")
            
            await asyncio.sleep(1)  # Simulate 1 second of execution
        
        execution_time = time.time() - start_time
        
        # Calculate success rate
        avg_error_rate = np.mean([m.value for m in metrics if m.metric_type == MetricType.ERROR_RATE])
        success_rate = 1.0 - avg_error_rate
        
        # Generate recommendations
        recommendations = self._generate_recommendations(metrics, scenario)
        
        result = ScenarioResult(
            scenario_id=scenario_id,
            completed=True,
            success_rate=success_rate,
            execution_time=execution_time,
            metrics=metrics,
            errors=errors,
            recommendations=recommendations
        )
        
        self.metrics_history.extend(metrics)
        self.scenario_results.append(result)
        self.scenarios_completed += 1
        
        # Adaptive difficulty adjustment
        self._adjust_difficulty(success_rate)
        
        return result
    
    async def start_continuous_training(self, connection_manager):
        """Start continuous training loop"""
        self.is_training = True
        self.start_time = time.time()
        
        while self.is_training:
            # Generate and execute scenario
            scenario = await self.problem_generator.generate_scenario(self.current_difficulty)
            self.current_scenario = scenario.id
            
            result = await self.execute_scenario(scenario.id)
            
            # Broadcast result
            await connection_manager.broadcast({
                "type": "training_update",
                "data": {
                    "scenario_id": scenario.id,
                    "success_rate": result.success_rate,
                    "execution_time": result.execution_time,
                    "difficulty": self.current_difficulty.value,
                    "scenarios_completed": self.scenarios_completed
                }
            })
            
            # Wait before next scenario
            await asyncio.sleep(5)
    
    async def stop_training(self):
        """Stop continuous training"""
        self.is_training = False
        self.current_scenario = None
    
    async def get_status(self) -> TrainingStatus:
        """Get current training status"""
        total_runtime = 0
        if self.start_time:
            total_runtime = time.time() - self.start_time
        
        avg_success_rate = 0.0
        if self.scenario_results:
            avg_success_rate = np.mean([r.success_rate for r in self.scenario_results])
        
        return TrainingStatus(
            is_running=self.is_training,
            current_scenario=self.current_scenario,
            scenarios_completed=self.scenarios_completed,
            total_runtime=total_runtime,
            average_success_rate=avg_success_rate,
            current_difficulty=self.current_difficulty
        )
    
    async def get_latest_metrics(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get latest metrics"""
        return [
            {
                "timestamp": m.timestamp.isoformat(),
                "type": m.metric_type.value,
                "value": m.value,
                "scenario_id": m.scenario_id
            }
            for m in self.metrics_history[-limit:]
        ]
    
    async def get_metrics_summary(self) -> MetricsSummary:
        """Get aggregated metrics summary"""
        if not self.metrics_history:
            return MetricsSummary(
                total_scenarios=0,
                average_response_time=0,
                average_throughput=0,
                average_success_rate=0,
                total_errors=0,
                uptime=0,
                last_updated=datetime.utcnow()
            )
        
        response_times = [m.value for m in self.metrics_history if m.metric_type == MetricType.RESPONSE_TIME]
        throughputs = [m.value for m in self.metrics_history if m.metric_type == MetricType.THROUGHPUT]
        error_rates = [m.value for m in self.metrics_history if m.metric_type == MetricType.ERROR_RATE]
        
        return MetricsSummary(
            total_scenarios=self.scenarios_completed,
            average_response_time=np.mean(response_times) if response_times else 0,
            average_throughput=np.mean(throughputs) if throughputs else 0,
            average_success_rate=1.0 - (np.mean(error_rates) if error_rates else 0),
            total_errors=sum(1 for m in self.metrics_history if m.metric_type == MetricType.ERROR_RATE and m.value > 0.1),
            uptime=time.time() - self.start_time if self.start_time else 0,
            last_updated=datetime.utcnow()
        )
    
    async def get_performance_analytics(self) -> Dict[str, Any]:
        """Get detailed performance analytics"""
        if not self.metrics_history:
            return {"error": "No metrics available"}
        
        # Group metrics by type
        metrics_by_type = {}
        for metric in self.metrics_history:
            if metric.metric_type.value not in metrics_by_type:
                metrics_by_type[metric.metric_type.value] = []
            metrics_by_type[metric.metric_type.value].append(metric.value)
        
        analytics = {}
        for metric_type, values in metrics_by_type.items():
            analytics[metric_type] = {
                "min": float(np.min(values)),
                "max": float(np.max(values)),
                "mean": float(np.mean(values)),
                "median": float(np.median(values)),
                "std_dev": float(np.std(values))
            }
        
        return {
            "metrics": analytics,
            "scenarios_completed": self.scenarios_completed,
            "current_difficulty": self.current_difficulty.value,
            "training_duration": time.time() - self.start_time if self.start_time else 0
        }
    
    def _simulate_response_time(self, difficulty: DifficultyLevel) -> float:
        """Simulate response time based on difficulty"""
        base_times = {
            DifficultyLevel.EASY: 50,
            DifficultyLevel.MEDIUM: 100,
            DifficultyLevel.HARD: 200,
            DifficultyLevel.EXTREME: 400
        }
        base = base_times[difficulty]
        return max(10, random.gauss(base, base * 0.3))
    
    def _simulate_throughput(self, difficulty: DifficultyLevel) -> float:
        """Simulate throughput"""
        base_throughput = {
            DifficultyLevel.EASY: 1000,
            DifficultyLevel.MEDIUM: 500,
            DifficultyLevel.HARD: 200,
            DifficultyLevel.EXTREME: 100
        }
        base = base_throughput[difficulty]
        return max(10, random.gauss(base, base * 0.2))
    
    def _simulate_cpu_usage(self, difficulty: DifficultyLevel) -> float:
        """Simulate CPU usage percentage"""
        base_cpu = {
            DifficultyLevel.EASY: 20,
            DifficultyLevel.MEDIUM: 40,
            DifficultyLevel.HARD: 60,
            DifficultyLevel.EXTREME: 80
        }
        base = base_cpu[difficulty]
        return min(100, max(5, random.gauss(base, 10)))
    
    def _simulate_memory_usage(self, difficulty: DifficultyLevel) -> float:
        """Simulate memory usage percentage"""
        base_memory = {
            DifficultyLevel.EASY: 30,
            DifficultyLevel.MEDIUM: 50,
            DifficultyLevel.HARD: 70,
            DifficultyLevel.EXTREME: 85
        }
        base = base_memory[difficulty]
        return min(95, max(10, random.gauss(base, 10)))
    
    def _simulate_error_rate(self, difficulty: DifficultyLevel) -> float:
        """Simulate error rate"""
        base_error = {
            DifficultyLevel.EASY: 0.01,
            DifficultyLevel.MEDIUM: 0.03,
            DifficultyLevel.HARD: 0.06,
            DifficultyLevel.EXTREME: 0.10
        }
        base = base_error[difficulty]
        return max(0, min(1, random.gauss(base, base * 0.5)))
    
    def _adjust_difficulty(self, success_rate: float):
        """Adaptively adjust difficulty based on performance"""
        if success_rate > 0.95 and self.current_difficulty != DifficultyLevel.EXTREME:
            # Increase difficulty
            levels = list(DifficultyLevel)
            current_index = levels.index(self.current_difficulty)
            self.current_difficulty = levels[min(current_index + 1, len(levels) - 1)]
        elif success_rate < 0.70 and self.current_difficulty != DifficultyLevel.EASY:
            # Decrease difficulty
            levels = list(DifficultyLevel)
            current_index = levels.index(self.current_difficulty)
            self.current_difficulty = levels[max(current_index - 1, 0)]
    
    def _generate_recommendations(self, metrics: List[PerformanceMetric], 
                                 scenario: Any) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        # Analyze response times
        response_times = [m.value for m in metrics if m.metric_type == MetricType.RESPONSE_TIME]
        if response_times and np.mean(response_times) > 500:
            recommendations.append("Consider optimizing response time - average is high")
        
        # Analyze error rates
        error_rates = [m.value for m in metrics if m.metric_type == MetricType.ERROR_RATE]
        if error_rates and np.mean(error_rates) > 0.05:
            recommendations.append("Error rate exceeds threshold - investigate root cause")
        
        # Analyze resource usage
        cpu_usage = [m.value for m in metrics if m.metric_type == MetricType.CPU_USAGE]
        if cpu_usage and np.mean(cpu_usage) > 80:
            recommendations.append("High CPU usage detected - consider scaling horizontally")
        
        memory_usage = [m.value for m in metrics if m.metric_type == MetricType.MEMORY_USAGE]
        if memory_usage and np.mean(memory_usage) > 85:
            recommendations.append("Memory usage is high - check for memory leaks")
        
        if not recommendations:
            recommendations.append("Performance is within acceptable parameters")
        
        return recommendations
