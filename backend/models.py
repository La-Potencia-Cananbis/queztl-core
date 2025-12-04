"""
Pydantic models for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class MetricType(str, Enum):
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    SUCCESS_RATE = "success_rate"

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXTREME = "extreme"

class PerformanceMetric(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metric_type: MetricType
    value: float
    scenario_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TestScenario(BaseModel):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    scenario_type: str
    difficulty: DifficultyLevel
    parameters: Dict[str, Any]
    description: str
    expected_outcomes: Dict[str, Any]

class ScenarioResult(BaseModel):
    scenario_id: str
    completed: bool
    success_rate: float
    execution_time: float
    metrics: List[PerformanceMetric]
    errors: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)

class TrainingStatus(BaseModel):
    is_running: bool
    current_scenario: Optional[str] = None
    scenarios_completed: int
    total_runtime: float
    average_success_rate: float
    current_difficulty: DifficultyLevel

class MetricsSummary(BaseModel):
    total_scenarios: int
    average_response_time: float
    average_throughput: float
    average_success_rate: float
    total_errors: int
    uptime: float
    last_updated: datetime
