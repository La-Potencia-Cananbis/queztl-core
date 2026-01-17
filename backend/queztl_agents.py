#!/usr/bin/env python3
"""
QUEZTL AGENT SYSTEM - The Living Architecture
==============================================
Agents can be: coders, runners, fixers, formers, seeders, trainers... anything

Philosophy (from DISTRIBUTED_VISION.md):
- Tlamacazqui (stem cells) - can spawn anywhere
- Self-organizing, self-replicating
- One agent teaches another
- Each node hosts multiple agent types

Architecture:
- Agent DNA: What the agent knows (code, models, data)
- Agent RNA: What the agent does (skills, behaviors)
- Agent spawning: One creates another
- Agent evolution: Learning transfers between agents
"""

import os
import sys
import json
import time
import pickle
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import subprocess


class AgentType(Enum):
    """Types of agents in the Queztl system."""
    TRAINER = "trainer"        # Trains ML models
    CODER = "coder"            # Writes/fixes code
    RUNNER = "runner"          # Executes tasks
    FIXER = "fixer"            # Debugs and repairs
    FORMER = "former"          # Creates new agents
    SEEDER = "seeder"          # Initializes datasets
    TESTER = "tester"          # Validates outputs
    MONITOR = "monitor"        # Watches system health
    COORDINATOR = "coordinator" # Orchestrates others


@dataclass
class AgentDNA:
    """
    Agent DNA - What the agent KNOWS
    - Knowledge, models, datasets
    - Can be copied/transferred to spawn new agents
    """
    agent_id: str
    agent_type: AgentType
    created_at: str
    parent_id: Optional[str] = None
    generation: int = 0
    
    # Knowledge base
    code_snippets: Dict[str, str] = None  # name -> code
    models: Dict[str, str] = None         # name -> model_path
    datasets: Dict[str, str] = None       # name -> data_path
    learned_skills: List[str] = None      # skill names
    
    # Metadata
    training_history: List[Dict] = None
    performance_metrics: Dict[str, float] = None
    
    def __post_init__(self):
        self.code_snippets = self.code_snippets or {}
        self.models = self.models or {}
        self.datasets = self.datasets or {}
        self.learned_skills = self.learned_skills or []
        self.training_history = self.training_history or []
        self.performance_metrics = self.performance_metrics or {}
    
    def save(self, path: Path):
        """Save DNA to disk."""
        with open(path, 'w') as f:
            json.dump(asdict(self), f, indent=2, default=str)
    
    @classmethod
    def load(cls, path: Path):
        """Load DNA from disk."""
        with open(path) as f:
            data = json.load(f)
            data['agent_type'] = AgentType(data['agent_type'])
            return cls(**data)
    
    def clone(self, new_id: str) -> 'AgentDNA':
        """Clone this DNA to create offspring."""
        return AgentDNA(
            agent_id=new_id,
            agent_type=self.agent_type,
            created_at=datetime.now().isoformat(),
            parent_id=self.agent_id,
            generation=self.generation + 1,
            code_snippets=self.code_snippets.copy(),
            models=self.models.copy(),
            datasets=self.datasets.copy(),
            learned_skills=self.learned_skills.copy(),
            training_history=[],
            performance_metrics={}
        )


@dataclass
class AgentRNA:
    """
    Agent RNA - What the agent DOES
    - Behaviors, actions, skills
    - Runtime state, not persisted
    """
    skills: Dict[str, Callable] = None  # skill_name -> function
    state: Dict[str, Any] = None         # runtime state
    
    def __post_init__(self):
        self.skills = self.skills or {}
        self.state = self.state or {}
    
    def register_skill(self, name: str, func: Callable):
        """Register a new skill."""
        self.skills[name] = func
    
    def execute_skill(self, name: str, *args, **kwargs) -> Any:
        """Execute a skill by name."""
        if name not in self.skills:
            raise ValueError(f"Unknown skill: {name}")
        return self.skills[name](*args, **kwargs)


class BaseAgent:
    """
    Base Agent - All agents inherit from this
    Implements: DNA (knowledge), RNA (behavior), lifecycle
    """
    
    def __init__(self, dna: AgentDNA, workspace: Path):
        self.dna = dna
        self.rna = AgentRNA()
        self.workspace = workspace / dna.agent_id
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        self.log_file = self.workspace / "agent.log"
        self.is_running = False
        
        self._register_base_skills()
    
    def _register_base_skills(self):
        """Register skills all agents have."""
        self.rna.register_skill('log', self.log)
        self.rna.register_skill('save_dna', self.save_dna)
        self.rna.register_skill('spawn_child', self.spawn_child)
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message."""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry + "\n")
        
        print(f"[{self.dna.agent_id}] {log_entry}")
    
    def save_dna(self):
        """Save current DNA state."""
        dna_path = self.workspace / "dna.json"
        self.dna.save(dna_path)
        self.log(f"DNA saved to {dna_path}")
    
    def spawn_child(self, child_type: Optional[AgentType] = None) -> 'BaseAgent':
        """
        Spawn a child agent - TEACHING ANOTHER AGENT
        Child inherits parent's knowledge
        """
        child_id = f"{self.dna.agent_id}_child_{int(time.time())}"
        child_dna = self.dna.clone(child_id)
        
        if child_type:
            child_dna.agent_type = child_type
        
        self.log(f"Spawning child: {child_id} (type: {child_dna.agent_type.value})")
        
        # Create appropriate agent type
        child_agent = create_agent(child_dna, self.workspace.parent)
        child_agent.log(f"Born from parent {self.dna.agent_id} (generation {child_dna.generation})")
        
        return child_agent
    
    def run(self):
        """Main agent loop - override in subclasses."""
        self.is_running = True
        self.log(f"Agent {self.dna.agent_id} starting...")
        
        try:
            self._run_logic()
        except Exception as e:
            self.log(f"Error: {e}", level="ERROR")
        finally:
            self.is_running = False
            self.save_dna()
    
    def _run_logic(self):
        """Override this in subclasses."""
        raise NotImplementedError


class TrainerAgent(BaseAgent):
    """
    Trainer Agent - Trains ML models
    Can learn, then teach another agent what it learned
    """
    
    def _register_base_skills(self):
        super()._register_base_skills()
        self.rna.register_skill('train_model', self.train_model)
        self.rna.register_skill('teach_agent', self.teach_agent)
        self.rna.register_skill('load_model', self.load_model)
    
    def train_model(self, dataset_path: str, epochs: int = 10, target_accuracy: float = 0.90):
        """Train a model using simple_trainer.py."""
        self.log(f"Starting training: {epochs} epochs, target {target_accuracy*100}%")
        
        # Use the simple trainer we built
        cmd = [
            'python', '/code/backend/simple_trainer.py',
            '--epochs', str(epochs),
            '--target', str(target_accuracy),
            '--data-root', str(dataset_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            self.log("Training completed successfully")
            
            # Load training report
            report_path = Path(dataset_path) / 'training_report.json'
            if report_path.exists():
                with open(report_path) as f:
                    report = json.load(f)
                
                # Store in DNA
                self.dna.performance_metrics['accuracy'] = report['best_accuracy']
                self.dna.performance_metrics['epochs'] = report['total_epochs']
                self.dna.training_history.append(report)
                
                # Mark skill as learned
                if 'image_classification' not in self.dna.learned_skills:
                    self.dna.learned_skills.append('image_classification')
                
                # Store model path
                model_path = Path(dataset_path) / 'checkpoints' / 'best_model.pth'
                if model_path.exists():
                    self.dna.models['image_classifier'] = str(model_path)
                
                self.log(f"Achieved {report['best_accuracy']}% accuracy")
                return True
        else:
            self.log(f"Training failed: {result.stderr}", level="ERROR")
            return False
    
    def teach_agent(self, student_agent: 'TrainerAgent'):
        """
        Teach another agent what this agent learned
        Transfer: models, knowledge, skills
        """
        self.log(f"Teaching agent {student_agent.dna.agent_id}")
        
        # Transfer learned skills
        for skill in self.dna.learned_skills:
            if skill not in student_agent.dna.learned_skills:
                student_agent.dna.learned_skills.append(skill)
                self.log(f"  Transferred skill: {skill}")
        
        # Transfer models
        for model_name, model_path in self.dna.models.items():
            if model_name not in student_agent.dna.models:
                # Copy model file
                src_path = Path(model_path)
                if src_path.exists():
                    dst_path = student_agent.workspace / 'models' / src_path.name
                    dst_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    import shutil
                    shutil.copy(src_path, dst_path)
                    
                    student_agent.dna.models[model_name] = str(dst_path)
                    self.log(f"  Transferred model: {model_name}")
        
        # Transfer training insights
        if self.dna.training_history:
            latest = self.dna.training_history[-1]
            student_agent.dna.training_history.append({
                'inherited_from': self.dna.agent_id,
                'parent_accuracy': latest.get('best_accuracy'),
                'inherited_at': datetime.now().isoformat()
            })
        
        student_agent.save_dna()
        self.log(f"Teaching complete. Student now has {len(student_agent.dna.learned_skills)} skills")
    
    def load_model(self, model_name: str):
        """Load a trained model from DNA."""
        if model_name not in self.dna.models:
            self.log(f"Model {model_name} not found in DNA", level="WARNING")
            return None
        
        model_path = Path(self.dna.models[model_name])
        if not model_path.exists():
            self.log(f"Model file not found: {model_path}", level="ERROR")
            return None
        
        self.log(f"Loaded model: {model_name}")
        return model_path
    
    def _run_logic(self):
        """Trainer agent main loop."""
        self.log("Trainer agent ready")
        
        # Example: Train if we don't have a model yet
        if not self.dna.models:
            self.log("No models found - starting training")
            self.train_model('/tmp/simple_training', epochs=5, target_accuracy=0.90)
        else:
            self.log(f"Already trained. Best accuracy: {self.dna.performance_metrics.get('accuracy', 'N/A')}%")


class CoderAgent(BaseAgent):
    """
    Coder Agent - Writes and fixes code
    """
    
    def _register_base_skills(self):
        super()._register_base_skills()
        self.rna.register_skill('write_code', self.write_code)
        self.rna.register_skill('fix_code', self.fix_code)
    
    def write_code(self, code: str, filename: str):
        """Write code to a file."""
        filepath = self.workspace / 'code' / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        # Store in DNA
        self.dna.code_snippets[filename] = code
        self.log(f"Wrote code: {filename}")
    
    def fix_code(self, filename: str, error: str):
        """Attempt to fix broken code."""
        self.log(f"Fixing code in {filename}: {error}")
        # TODO: Implement actual fix logic
        # Could use LLM, pattern matching, etc.
    
    def _run_logic(self):
        self.log("Coder agent ready")


class RunnerAgent(BaseAgent):
    """
    Runner Agent - Executes tasks
    """
    
    def _register_base_skills(self):
        super()._register_base_skills()
        self.rna.register_skill('execute_task', self.execute_task)
    
    def execute_task(self, command: List[str]):
        """Execute a command."""
        self.log(f"Executing: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            self.log("Task completed successfully")
            return result.stdout
        else:
            self.log(f"Task failed: {result.stderr}", level="ERROR")
            return None
    
    def _run_logic(self):
        self.log("Runner agent ready")


class SeederAgent(BaseAgent):
    """
    Seeder Agent - Initializes datasets
    """
    
    def _register_base_skills(self):
        super()._register_base_skills()
        self.rna.register_skill('create_dataset', self.create_dataset)
    
    def create_dataset(self, dataset_name: str, size: int):
        """Create a new dataset."""
        self.log(f"Creating dataset: {dataset_name} (size: {size})")
        
        dataset_path = self.workspace / 'datasets' / dataset_name
        dataset_path.mkdir(parents=True, exist_ok=True)
        
        # TODO: Implement actual dataset creation
        # For now, just prepare the structure
        
        self.dna.datasets[dataset_name] = str(dataset_path)
        self.log(f"Dataset created: {dataset_path}")
        
        return dataset_path
    
    def _run_logic(self):
        self.log("Seeder agent ready")


def create_agent(dna: AgentDNA, workspace: Path) -> BaseAgent:
    """Factory function to create appropriate agent type."""
    agent_classes = {
        AgentType.TRAINER: TrainerAgent,
        AgentType.CODER: CoderAgent,
        AgentType.RUNNER: RunnerAgent,
        AgentType.SEEDER: SeederAgent,
        # Add more as needed
    }
    
    agent_class = agent_classes.get(dna.agent_type, BaseAgent)
    return agent_class(dna, workspace)


class AgentNode:
    """
    Agent Node - Hosts multiple agents on one machine
    Each node can run different types of agents
    """
    
    def __init__(self, node_id: str, workspace: Path):
        self.node_id = node_id
        self.workspace = workspace / node_id
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        self.agents: Dict[str, BaseAgent] = {}
        self.log_file = self.workspace / "node.log"
    
    def log(self, message: str):
        """Log node-level message."""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [NODE:{self.node_id}] {message}"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry + "\n")
        
        print(log_entry)
    
    def spawn_agent(self, agent_type: AgentType, agent_id: Optional[str] = None) -> BaseAgent:
        """Spawn a new agent on this node."""
        if agent_id is None:
            agent_id = f"{self.node_id}_{agent_type.value}_{int(time.time())}"
        
        dna = AgentDNA(
            agent_id=agent_id,
            agent_type=agent_type,
            created_at=datetime.now().isoformat()
        )
        
        agent = create_agent(dna, self.workspace)
        self.agents[agent_id] = agent
        
        self.log(f"Spawned agent: {agent_id} (type: {agent_type.value})")
        return agent
    
    def list_agents(self) -> List[Dict]:
        """List all agents on this node."""
        return [
            {
                'id': agent.dna.agent_id,
                'type': agent.dna.agent_type.value,
                'generation': agent.dna.generation,
                'skills': agent.dna.learned_skills,
                'running': agent.is_running
            }
            for agent in self.agents.values()
        ]
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get agent by ID."""
        return self.agents.get(agent_id)


def demo_agent_teaching():
    """
    Demo: One agent learns, then teaches another
    This is the core vision - self-propagating knowledge
    """
    print("=" * 60)
    print("QUEZTL AGENT SYSTEM - Teaching Demo")
    print("=" * 60)
    
    workspace = Path("/tmp/queztl_agents")
    workspace.mkdir(parents=True, exist_ok=True)
    
    # Create a node
    node = AgentNode("beast", workspace)
    
    print("\n📦 Step 1: Spawn trainer agent (Teacher)")
    teacher = node.spawn_agent(AgentType.TRAINER, "teacher_001")
    
    print("\n🧠 Step 2: Teacher learns (trains model)")
    teacher.train_model('/tmp/simple_training', epochs=3, target_accuracy=0.85)
    
    print("\n👶 Step 3: Teacher spawns student")
    student = teacher.spawn_child(AgentType.TRAINER)
    
    print("\n📚 Step 4: Teacher teaches student")
    teacher.teach_agent(student)
    
    print("\n🎓 Step 5: Student verifies learned skills")
    print(f"   Student ID: {student.dna.agent_id}")
    print(f"   Generation: {student.dna.generation}")
    print(f"   Learned skills: {student.dna.learned_skills}")
    print(f"   Has models: {list(student.dna.models.keys())}")
    
    print("\n✅ Demo complete!")
    print(f"   Workspace: {workspace}")
    print(f"   Teacher DNA: {teacher.workspace / 'dna.json'}")
    print(f"   Student DNA: {student.workspace / 'dna.json'}")
    
    return node, teacher, student


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Queztl Agent System')
    parser.add_argument('--demo', action='store_true', help='Run teaching demo')
    parser.add_argument('--node-id', default='beast', help='Node ID')
    parser.add_argument('--spawn', choices=['trainer', 'coder', 'runner', 'seeder'], help='Spawn agent type')
    
    args = parser.parse_args()
    
    if args.demo:
        demo_agent_teaching()
    elif args.spawn:
        workspace = Path("/tmp/queztl_agents")
        node = AgentNode(args.node_id, workspace)
        agent_type = AgentType(args.spawn)
        agent = node.spawn_agent(agent_type)
        agent.run()
    else:
        parser.print_help()
