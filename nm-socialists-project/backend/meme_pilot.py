#!/usr/bin/env python3
"""
NM SOCIALISTS AGENT PILOT
Autonomous meme generation using Queztl agents system

This pilot:
- Spawns meme generator agents
- Distributes work across cluster
- Learns from engagement metrics
- Auto-scales based on demand
"""

import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import logging

# Add backend to path for agent imports
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

try:
    from queztl_agents import (
        AgentType, AgentDNA, BaseAgent,
        TrainerAgent, RunnerAgent, create_agent
    )
    AGENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Queztl agents not available: {e}")
    AGENTS_AVAILABLE = False

from ai_meme_generator import ClusterMemeGenerator, MEME_THEMES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemeGeneratorAgent(BaseAgent):
    """
    Agent that generates revolutionary memes
    Inherits from Queztl BaseAgent system
    """
    
    def __init__(self, dna: AgentDNA, workspace: Path):
        super().__init__(dna, workspace)
        self.generator = None
        
        # Register meme generation skills
        self.rna.register_skill('generate_meme', self.generate_meme)
        self.rna.register_skill('generate_batch', self.generate_batch)
        self.rna.register_skill('analyze_engagement', self.analyze_engagement)
    
    async def generate_meme(self, theme: str) -> Path:
        """Generate a single meme"""
        if not self.generator:
            self.generator = ClusterMemeGenerator()
            await self.generator.__aenter__()
        
        self.log(f"Generating meme: {theme}")
        result = await self.generator.generate_meme(theme)
        self.log(f"✅ Generated: {result}")
        
        # Record in DNA (agent learning)
        self.dna.performance_metrics[f"meme_{theme}"] = datetime.now().isoformat()
        self.save_dna()
        
        return result
    
    async def generate_batch(self, count: int = 8) -> List[Path]:
        """Generate multiple memes"""
        if not self.generator:
            self.generator = ClusterMemeGenerator()
            await self.generator.__aenter__()
        
        self.log(f"Generating batch of {count} memes")
        results = await self.generator.generate_batch(count=count)
        self.log(f"✅ Generated {len(results)} memes")
        
        # Update DNA
        self.dna.performance_metrics['total_generated'] = \
            self.dna.performance_metrics.get('total_generated', 0) + len(results)
        self.save_dna()
        
        return results
    
    def analyze_engagement(self, meme_stats: Dict) -> Dict:
        """
        Analyze which memes get most engagement
        This feeds back into the agent's learning
        """
        self.log("Analyzing meme engagement...")
        
        # Record engagement patterns in DNA
        for meme_id, stats in meme_stats.items():
            if stats['shares'] > 10:
                self.dna.learned_skills.append(f"high_engagement_{meme_id}")
        
        self.save_dna()
        
        return {
            "top_themes": self._get_top_themes(meme_stats),
            "total_engagement": sum(s['shares'] + s['likes'] for s in meme_stats.values())
        }
    
    def _get_top_themes(self, meme_stats: Dict) -> List[str]:
        """Identify most successful meme themes"""
        ranked = sorted(
            meme_stats.items(),
            key=lambda x: x[1]['shares'] + x[1]['likes'],
            reverse=True
        )
        return [theme for theme, _ in ranked[:3]]
    
    def _run_logic(self):
        """Main agent loop"""
        self.log("Meme Generator Agent activated")
        
        # Example: Generate memes on schedule
        asyncio.run(self.generate_batch(count=5))


class MemePilot:
    """
    Pilot that coordinates multiple meme generator agents
    Distributes work across cluster nodes
    """
    
    def __init__(self, workspace: Path = None):
        self.workspace = workspace or Path.home() / "queztl-core" / "agents"
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.agents: List[MemeGeneratorAgent] = []
    
    def spawn_agent(self, agent_id: str) -> MemeGeneratorAgent:
        """Spawn a new meme generator agent"""
        dna = AgentDNA(
            agent_id=agent_id,
            agent_type=AgentType.RUNNER,
            created_at=datetime.now().isoformat(),
            learned_skills=["generate_meme", "analyze_engagement"]
        )
        
        agent = MemeGeneratorAgent(dna, self.workspace)
        self.agents.append(agent)
        
        logger.info(f"✅ Spawned agent: {agent_id}")
        return agent
    
    async def distribute_work(self, total_memes: int):
        """Distribute meme generation across agents"""
        if not self.agents:
            logger.warning("No agents available, spawning one...")
            self.spawn_agent(f"meme_agent_{int(datetime.now().timestamp())}")
        
        # Distribute work evenly
        memes_per_agent = total_memes // len(self.agents)
        remainder = total_memes % len(self.agents)
        
        tasks = []
        for i, agent in enumerate(self.agents):
            count = memes_per_agent + (1 if i < remainder else 0)
            task = agent.generate_batch(count)
            tasks.append(task)
        
        # Run in parallel
        results = await asyncio.gather(*tasks)
        
        all_memes = []
        for result in results:
            all_memes.extend(result)
        
        logger.info(f"✅ Generated {len(all_memes)} total memes across {len(self.agents)} agents")
        return all_memes
    
    async def continuous_generation(self, interval_minutes: int = 60):
        """Continuously generate memes at intervals"""
        logger.info(f"🔄 Starting continuous generation (every {interval_minutes} min)")
        
        while True:
            try:
                await self.distribute_work(total_memes=8)
                logger.info(f"😴 Sleeping for {interval_minutes} minutes...")
                await asyncio.sleep(interval_minutes * 60)
            except KeyboardInterrupt:
                logger.info("⏹️  Stopping continuous generation")
                break
            except Exception as e:
                logger.error(f"❌ Error in continuous generation: {e}")
                await asyncio.sleep(60)  # Wait 1 min before retry


async def main():
    """CLI interface for meme pilot"""
    import argparse
    
    parser = argparse.ArgumentParser(description="NM Socialists Meme Pilot")
    parser.add_argument("--agents", type=int, default=2, help="Number of agents to spawn")
    parser.add_argument("--memes", type=int, default=16, help="Total memes to generate")
    parser.add_argument("--continuous", action="store_true", help="Run continuously")
    parser.add_argument("--interval", type=int, default=60, help="Minutes between generations")
    
    args = parser.parse_args()
    
    if not AGENTS_AVAILABLE:
        print("❌ Queztl agents system not available")
        print("Falling back to direct generation...")
        
        async with ClusterMemeGenerator() as gen:
            results = await gen.generate_batch(count=args.memes)
            print(f"\n✅ Generated {len(results)} memes")
            for path in results:
                print(f"   - {path.name}")
        return
    
    # Use full agent system
    pilot = MemePilot()
    
    # Spawn agents
    print(f"\n🚁 Spawning {args.agents} meme generator agents...")
    for i in range(args.agents):
        pilot.spawn_agent(f"meme_agent_{i + 1}")
    
    if args.continuous:
        # Run continuously
        await pilot.continuous_generation(interval_minutes=args.interval)
    else:
        # One-time generation
        print(f"\n🎨 Generating {args.memes} memes across {args.agents} agents...")
        results = await pilot.distribute_work(total_memes=args.memes)
        
        print(f"\n✅ Generation complete!")
        print(f"📊 Total memes: {len(results)}")
        print(f"📁 Location: {results[0].parent if results else 'N/A'}")


if __name__ == "__main__":
    asyncio.run(main())
