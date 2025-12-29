#!/usr/bin/env python3
"""
QHP Project Manager Agent
AI-powered autonomous project manager that tracks progress, manages tasks,
and drives execution using QHP protocol for communication.
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
from pathlib import Path

class TaskStatus(Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    REVIEW = "review"
    DONE = "done"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    CRITICAL = "critical"  # Do NOW
    HIGH = "high"         # Do today
    MEDIUM = "medium"     # Do this week
    LOW = "low"          # Nice to have

class TaskType(Enum):
    FEATURE = "feature"
    BUG = "bug"
    DOCS = "docs"
    LEGAL = "legal"
    MARKETING = "marketing"
    FUNDRAISING = "fundraising"
    RESEARCH = "research"
    DEPLOYMENT = "deployment"

@dataclass
class Task:
    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    task_type: TaskType
    assignee: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    due_date: Optional[str] = None
    depends_on: Optional[List[str]] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    tags: Optional[List[str]] = None
    progress: int = 0  # 0-100%
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.now().isoformat()
        if self.depends_on is None:
            self.depends_on = []
        if self.tags is None:
            self.tags = []

@dataclass
class Milestone:
    id: str
    title: str
    description: str
    due_date: str
    tasks: List[str]
    completed: bool = False
    
class PMAgent:
    """AI Project Manager Agent"""
    
    def __init__(self, db_path: str = "pm_agent.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                task_type TEXT NOT NULL,
                assignee TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                due_date TEXT,
                estimated_hours REAL,
                actual_hours REAL,
                progress INTEGER DEFAULT 0,
                tags TEXT,
                depends_on TEXT
            )
        """)
        
        # Milestones table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS milestones (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT NOT NULL,
                tasks TEXT,
                completed INTEGER DEFAULT 0
            )
        """)
        
        # Activity log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                task_id TEXT,
                action TEXT NOT NULL,
                details TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_task(self, task: Task) -> Task:
        """Create a new task"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tasks 
            (id, title, description, status, priority, task_type, assignee,
             created_at, updated_at, due_date, estimated_hours, actual_hours,
             progress, tags, depends_on)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task.id, task.title, task.description,
            task.status.value, task.priority.value, task.task_type.value,
            task.assignee, task.created_at, task.updated_at, task.due_date,
            task.estimated_hours, task.actual_hours, task.progress,
            json.dumps(task.tags), json.dumps(task.depends_on)
        ))
        
        self.log_activity(task.id, "created", f"Task created: {task.title}")
        
        conn.commit()
        conn.close()
        return task
    
    def update_task(self, task_id: str, **updates) -> Optional[Task]:
        """Update a task"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates['updated_at'] = datetime.now().isoformat()
        
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [task_id]
        
        cursor.execute(f"""
            UPDATE tasks SET {set_clause} WHERE id = ?
        """, values)
        
        self.log_activity(task_id, "updated", f"Task updated: {updates}")
        
        conn.commit()
        conn.close()
        
        return self.get_task(task_id)
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return self._row_to_task(row)
    
    def get_tasks(self, status: Optional[TaskStatus] = None,
                  priority: Optional[TaskPriority] = None) -> List[Task]:
        """Get tasks with optional filters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status.value)
        
        if priority:
            query += " AND priority = ?"
            params.append(priority.value)
        
        query += " ORDER BY priority DESC, created_at ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_task(row) for row in rows]
    
    def _row_to_task(self, row) -> Task:
        """Convert database row to Task object"""
        return Task(
            id=row[0],
            title=row[1],
            description=row[2],
            status=TaskStatus(row[3]),
            priority=TaskPriority(row[4]),
            task_type=TaskType(row[5]),
            assignee=row[6],
            created_at=row[7],
            updated_at=row[8],
            due_date=row[9],
            estimated_hours=row[10],
            actual_hours=row[11],
            progress=row[12],
            tags=json.loads(row[13]) if row[13] else [],
            depends_on=json.loads(row[14]) if row[14] else []
        )
    
    def log_activity(self, task_id: str, action: str, details: str):
        """Log activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO activity_log (timestamp, task_id, action, details)
            VALUES (?, ?, ?, ?)
        """, (datetime.now().isoformat(), task_id, action, details))
        
        conn.commit()
        conn.close()
    
    def get_daily_standup(self) -> Dict:
        """Generate daily standup report"""
        tasks = self.get_tasks()
        
        in_progress = [t for t in tasks if t.status == TaskStatus.IN_PROGRESS]
        blocked = [t for t in tasks if t.status == TaskStatus.BLOCKED]
        completed_today = [t for t in tasks 
                          if t.status == TaskStatus.DONE 
                          and t.updated_at and t.updated_at.startswith(datetime.now().strftime("%Y-%m-%d"))]
        high_priority = [t for t in tasks 
                        if t.priority == TaskPriority.CRITICAL 
                        and t.status != TaskStatus.DONE]
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "in_progress": [{"id": t.id, "title": t.title} for t in in_progress],
            "blocked": [{"id": t.id, "title": t.title, "reason": t.description} for t in blocked],
            "completed_today": [{"id": t.id, "title": t.title} for t in completed_today],
            "high_priority": [{"id": t.id, "title": t.title} for t in high_priority],
            "summary": {
                "total_tasks": len(tasks),
                "in_progress": len(in_progress),
                "blocked": len(blocked),
                "completed_today": len(completed_today),
                "high_priority_pending": len(high_priority)
            }
        }
    
    def suggest_next_task(self) -> Optional[Task]:
        """AI suggests what to work on next"""
        tasks = self.get_tasks()
        
        # Filter available tasks (not done, not blocked, dependencies met)
        available = []
        for task in tasks:
            if task.status in [TaskStatus.DONE, TaskStatus.CANCELLED]:
                continue
            if task.status == TaskStatus.BLOCKED:
                continue
            
            # Check dependencies
            if task.depends_on:
                deps_met = all(
                    (dep_task := self.get_task(dep_id)) and dep_task.status == TaskStatus.DONE 
                    for dep_id in task.depends_on
                )
                if not deps_met:
                    continue
            
            available.append(task)
        
        if not available:
            return None
        
        # Sort by priority, then by due date
        available.sort(key=lambda t: (
            -list(TaskPriority).index(t.priority),
            t.due_date or "9999-99-99"
        ))
        
        return available[0] if available else None
    
    def export_to_github_issues(self) -> str:
        """Export tasks as GitHub Issues format"""
        tasks = self.get_tasks()
        
        output = "# QHP Protocol - GitHub Issues\n\n"
        
        for task in tasks:
            output += f"## {task.title}\n\n"
            output += f"**Status:** {task.status.value}\n"
            output += f"**Priority:** {task.priority.value}\n"
            output += f"**Type:** {task.task_type.value}\n"
            output += f"**Progress:** {task.progress}%\n\n"
            output += f"{task.description}\n\n"
            
            if task.tags:
                output += f"**Tags:** {', '.join(task.tags)}\n\n"
            
            if task.depends_on:
                output += f"**Depends on:** {', '.join(task.depends_on)}\n\n"
            
            output += "---\n\n"
        
        return output
    
    def generate_sprint_report(self, days: int = 7) -> Dict:
        """Generate sprint report"""
        tasks = self.get_tasks()
        
        start_date = datetime.now() - timedelta(days=days)
        
        completed = [t for t in tasks 
                    if t.status == TaskStatus.DONE 
                    and t.updated_at and datetime.fromisoformat(t.updated_at) >= start_date]
        
        in_progress = [t for t in tasks if t.status == TaskStatus.IN_PROGRESS]
        
        total_estimated = sum(t.estimated_hours or 0 for t in completed + in_progress)
        total_actual = sum(t.actual_hours or 0 for t in completed)
        
        return {
            "sprint_duration_days": days,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": datetime.now().strftime("%Y-%m-%d"),
            "completed_tasks": len(completed),
            "in_progress_tasks": len(in_progress),
            "total_estimated_hours": total_estimated,
            "total_actual_hours": total_actual,
            "velocity": len(completed) / days if days > 0 else 0,
            "completed_by_priority": {
                priority.value: len([t for t in completed if t.priority == priority])
                for priority in TaskPriority
            }
        }

def load_qhp_project_tasks(agent: PMAgent):
    """Load all QHP project tasks into PM agent"""
    
    print("🤖 Loading QHP Protocol project into PM Agent...")
    
    # CRITICAL PATH - USPTO Filing
    agent.create_task(Task(
        id="legal-001",
        title="File QHP™ Trademark with USPTO",
        description="""
        File trademark application for QHP (Queztl Hybrid Protocol) with USPTO.
        
        Steps:
        1. Go to https://www.uspto.gov/trademarks/apply
        2. Use TEAS Plus form ($250)
        3. Class 009: Computer software protocols
        4. Mark type: Standard character mark
        5. Use file USPTO_TRADEMARK_FILING.md as guide
        
        Documents ready: USPTO_TRADEMARK_FILING.md
        """,
        status=TaskStatus.TODO,
        priority=TaskPriority.CRITICAL,
        task_type=TaskType.LEGAL,
        due_date=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        estimated_hours=2.0,
        tags=["uspto", "trademark", "critical", "revenue-blocker"]
    ))
    
    agent.create_task(Task(
        id="legal-002",
        title="File QAP™ Trademark with USPTO",
        description="""
        File trademark application for QAP (Quantized Action Packets) with USPTO.
        
        Same process as QHP trademark but for QAP mark.
        Class 009: Computer software, communication protocols.
        
        Documents ready: USPTO_TRADEMARK_FILING.md
        """,
        status=TaskStatus.TODO,
        priority=TaskPriority.CRITICAL,
        task_type=TaskType.LEGAL,
        due_date=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        estimated_hours=2.0,
        depends_on=["legal-001"],
        tags=["uspto", "trademark", "critical"]
    ))
    
    agent.create_task(Task(
        id="legal-003",
        title="File Provisional Patent with USPTO",
        description="""
        File provisional patent for QHP protocol technology.
        
        Documents ready: USPTO_PATENT_FILING.md
        Cost: $150 (micro entity)
        Claims: 7 claims covering port-free routing, QAPs, ML optimization
        
        MUST file before open sourcing code!
        """,
        status=TaskStatus.TODO,
        priority=TaskPriority.CRITICAL,
        task_type=TaskType.LEGAL,
        due_date=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        estimated_hours=3.0,
        tags=["uspto", "patent", "critical", "pre-open-source"]
    ))
    
    # FUNDRAISING
    agent.create_task(Task(
        id="fund-001",
        title="Create Google Slides Pitch Deck",
        description="""
        Convert QHP_PITCH_DECK.md into professional Google Slides presentation.
        
        16 slides covering:
        - Problem/Solution
        - Market size ($50B)
        - Business model
        - Financial projections
        - Team & ask ($25K-$100K)
        
        Template: QHP_PITCH_DECK.md
        """,
        status=TaskStatus.TODO,
        priority=TaskPriority.HIGH,
        task_type=TaskType.FUNDRAISING,
        due_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        estimated_hours=2.0,
        tags=["fundraising", "investor", "presentation"]
    ))
    
    agent.create_task(Task(
        id="fund-002",
        title="Set Up AngelList Profile",
        description="""
        Create founder profile on AngelList to get matched with investors.
        
        Steps:
        1. Go to https://angel.co/
        2. Create founder profile
        3. Add QHP project
        4. Upload pitch deck
        5. Set funding round: $25K-$100K seed
        
        Template: INVESTOR_STRATEGY.md (section on AngelList)
        """,
        status=TaskStatus.TODO,
        priority=TaskPriority.HIGH,
        task_type=TaskType.FUNDRAISING,
        due_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        estimated_hours=1.0,
        depends_on=["fund-001"],
        tags=["fundraising", "investor", "angellist"]
    ))
    
    agent.create_task(Task(
        id="fund-003",
        title="Send 20 Investor Emails",
        description="""
        Send personalized emails to 20 potential investors.
        
        Use templates from INVESTOR_EMAILS.md:
        - 10 to angel investors (Email Template 1)
        - 5 to friends/family (Email Template 2)
        - 5 to professional contacts (Email Template 3)
        
        Track responses in spreadsheet.
        """,
        status=TaskStatus.TODO,
        priority=TaskPriority.HIGH,
        task_type=TaskType.FUNDRAISING,
        due_date=(datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        estimated_hours=2.0,
        depends_on=["fund-001"],
        tags=["fundraising", "investor", "outreach"]
    ))
    
    agent.create_task(Task(
        id="fund-004",
        title="Post LinkedIn Investor Update",
        description="""
        Post on LinkedIn about QHP protocol and fundraising.
        
        Use template from INVESTOR_STRATEGY.md (LinkedIn Strategy section).
        
        Key points:
        - Filed patents for 10-20x faster protocol
        - Looking for $25K-$50K from technical angels
        - Patent pending, working implementation
        """,
        status=TaskStatus.TODO,
        priority=TaskPriority.MEDIUM,
        task_type=TaskType.MARKETING,
        due_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        estimated_hours=0.5,
        tags=["fundraising", "marketing", "linkedin"]
    ))
    
    agent.create_task(Task(
        id="fund-005",
        title="Apply to Y Combinator",
        description="""
        Submit application to Y Combinator W26 batch.
        
        URL: https://www.ycombinator.com/apply
        Template: INVESTOR_EMAILS.md (Email Template 7)
        
        Funding: $500K for 7%
        Timeline: 4-8 weeks
        """,
        status=TaskStatus.BACKLOG,
        priority=TaskPriority.MEDIUM,
        task_type=TaskType.FUNDRAISING,
        due_date=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        estimated_hours=3.0,
        depends_on=["fund-001"],
        tags=["fundraising", "yc", "accelerator"]
    ))
    
    # TECHNICAL
    agent.create_task(Task(
        id="tech-001",
        title="Open Source QHP on GitHub",
        description="""
        Publish QHP protocol to GitHub as open source.
        
        IMPORTANT: Must file patent BEFORE open sourcing!
        Depends on: legal-003
        
        Steps:
        1. Create public repo: github.com/SalChicanoLoco/qhp-protocol
        2. Add MIT license
        3. Add README with ™ symbols and "Patent Pending"
        4. Push all QHP code (qhp_server.py, qhp_client.js, etc.)
        5. Create releases
        """,
        status=TaskStatus.BLOCKED,
        priority=TaskPriority.HIGH,
        task_type=TaskType.DEPLOYMENT,
        due_date=(datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
        estimated_hours=2.0,
        depends_on=["legal-003"],
        tags=["open-source", "github", "deployment", "blocked-on-patent"]
    ))
    
    agent.create_task(Task(
        id="tech-002",
        title="Register qhp-protocol.org Domain",
        description="""
        Register official domain for QHP protocol.
        
        Domain: qhp-protocol.org
        Registrar: Namecheap or Google Domains
        Cost: ~$12/year
        
        Setup simple landing page with:
        - Protocol overview
        - Documentation
        - GitHub link
        - Certification signup
        """,
        status=TaskStatus.TODO,
        priority=TaskPriority.MEDIUM,
        task_type=TaskType.DEPLOYMENT,
        due_date=(datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
        estimated_hours=1.0,
        tags=["domain", "website", "branding"]
    ))
    
    agent.create_task(Task(
        id="tech-003",
        title="Deploy Remote Worker Nodes",
        description="""
        Deploy first QHP worker nodes on remote infrastructure.
        
        Options:
        - Studio machine
        - AWS/Azure/GCP
        - DigitalOcean droplets
        
        Use: docker-compose.worker.yml
        Script: setup-distributed-hive.sh
        """,
        status=TaskStatus.BACKLOG,
        priority=TaskPriority.MEDIUM,
        task_type=TaskType.DEPLOYMENT,
        estimated_hours=3.0,
        tags=["distributed", "deployment", "hive"]
    ))
    
    agent.create_task(Task(
        id="tech-004",
        title="Create QHP npm Package",
        description="""
        Package QHP JavaScript client for npm.
        
        Package name: qhp-protocol
        Files: qhp_client.js
        
        Steps:
        1. Create package.json
        2. Add TypeScript definitions
        3. Publish to npm
        4. Add usage examples
        """,
        status=TaskStatus.BACKLOG,
        priority=TaskPriority.LOW,
        task_type=TaskType.FEATURE,
        estimated_hours=2.0,
        depends_on=["tech-001"],
        tags=["npm", "javascript", "packaging"]
    ))
    
    agent.create_task(Task(
        id="tech-005",
        title="Create QHP Python Package (PyPI)",
        description="""
        Package QHP Python server for PyPI.
        
        Package name: qhp-protocol
        Files: qhp_server.py, qhp_monitor.py
        
        Steps:
        1. Create setup.py
        2. Add type hints
        3. Publish to PyPI
        4. Add CLI tool
        """,
        status=TaskStatus.BACKLOG,
        priority=TaskPriority.LOW,
        task_type=TaskType.FEATURE,
        estimated_hours=2.0,
        depends_on=["tech-001"],
        tags=["pypi", "python", "packaging"]
    ))
    
    # MARKETING
    agent.create_task(Task(
        id="mkt-001",
        title="Post QHP on Hacker News",
        description="""
        Launch QHP protocol on Hacker News.
        
        MUST DO AFTER patent filing!
        
        Title: "QHP - A protocol 10-20x faster than REST (open source)"
        URL: Link to GitHub repo
        
        Best time: Tuesday-Thursday, 8-10am PT
        """,
        status=TaskStatus.BLOCKED,
        priority=TaskPriority.HIGH,
        task_type=TaskType.MARKETING,
        estimated_hours=1.0,
        depends_on=["tech-001"],
        tags=["marketing", "launch", "hacker-news", "blocked-on-patent"]
    ))
    
    agent.create_task(Task(
        id="mkt-002",
        title="Write Dev.to Article on QHP",
        description="""
        Write technical article explaining QHP protocol.
        
        Title: "Building a Protocol 10x Faster Than REST"
        
        Sections:
        - Why REST is slow
        - How QAPs work
        - Port-free routing explained
        - Benchmarks
        - How to use QHP
        """,
        status=TaskStatus.BACKLOG,
        priority=TaskPriority.MEDIUM,
        task_type=TaskType.MARKETING,
        estimated_hours=3.0,
        depends_on=["tech-001"],
        tags=["marketing", "content", "dev.to"]
    ))
    
    agent.create_task(Task(
        id="mkt-003",
        title="Create QHP Demo Video",
        description="""
        Record 5-minute demo video showing QHP performance.
        
        Content:
        - Side-by-side comparison (REST vs QHP)
        - Latency measurements
        - Easy integration demo
        - Use cases
        
        Upload to YouTube, embed on website.
        """,
        status=TaskStatus.BACKLOG,
        priority=TaskPriority.LOW,
        task_type=TaskType.MARKETING,
        estimated_hours=4.0,
        tags=["marketing", "video", "demo"]
    ))
    
    # DOCUMENTATION
    agent.create_task(Task(
        id="docs-001",
        title="Create QHP Quick Start Guide",
        description="""
        Write 5-minute quick start guide for developers.
        
        Sections:
        - Installation (npm/pip)
        - Hello World example
        - Common patterns
        - Troubleshooting
        
        Keep it simple, focus on getting started fast.
        """,
        status=TaskStatus.BACKLOG,
        priority=TaskPriority.MEDIUM,
        task_type=TaskType.DOCS,
        estimated_hours=2.0,
        depends_on=["tech-001"],
        tags=["documentation", "quickstart"]
    ))
    
    agent.create_task(Task(
        id="docs-002",
        title="Create API Reference Documentation",
        description="""
        Complete API reference for QHP protocol.
        
        Use Sphinx or similar tool.
        Cover all QHP methods, QAP structure, error codes.
        
        Host on qhp-protocol.org/docs
        """,
        status=TaskStatus.BACKLOG,
        priority=TaskPriority.LOW,
        task_type=TaskType.DOCS,
        estimated_hours=4.0,
        depends_on=["tech-002"],
        tags=["documentation", "api", "reference"]
    ))
    
    # ENTERPRISE
    agent.create_task(Task(
        id="ent-001",
        title="Reach Out to 10 Enterprise CTOs",
        description="""
        Email 10 CTOs at mid-size companies about QHP pilots.
        
        Use template: INVESTOR_EMAILS.md (Email Template 8)
        
        Offer:
        - Free proof-of-concept
        - Lifetime 50% discount ($2.5K/year)
        - Early access
        
        Target companies using microservices, real-time data.
        """,
        status=TaskStatus.BACKLOG,
        priority=TaskPriority.MEDIUM,
        task_type=TaskType.MARKETING,
        estimated_hours=2.0,
        depends_on=["fund-001"],
        tags=["enterprise", "sales", "b2b"]
    ))
    
    print(f"✅ Loaded {len(agent.get_tasks())} tasks into PM Agent")
    
    return agent

if __name__ == "__main__":
    # Initialize PM Agent
    agent = PMAgent()
    
    # Load QHP project
    load_qhp_project_tasks(agent)
    
    # Generate daily standup
    print("\n" + "="*60)
    print("📊 DAILY STANDUP REPORT")
    print("="*60)
    
    standup = agent.get_daily_standup()
    print(f"\n📅 Date: {standup['date']}")
    print(f"\n📈 Summary:")
    print(f"   Total tasks: {standup['summary']['total_tasks']}")
    print(f"   In progress: {standup['summary']['in_progress']}")
    print(f"   Blocked: {standup['summary']['blocked']}")
    print(f"   High priority pending: {standup['summary']['high_priority_pending']}")
    
    print(f"\n🚨 HIGH PRIORITY TASKS:")
    for task in standup['high_priority']:
        print(f"   • {task['id']}: {task['title']}")
    
    if standup['blocked']:
        print(f"\n⛔ BLOCKED TASKS:")
        for task in standup['blocked']:
            print(f"   • {task['id']}: {task['title']}")
    
    # Suggest next task
    print("\n" + "="*60)
    print("🤖 AI RECOMMENDATION")
    print("="*60)
    
    next_task = agent.suggest_next_task()
    if next_task:
        print(f"\n👉 You should work on: {next_task.title}")
        print(f"   ID: {next_task.id}")
        print(f"   Priority: {next_task.priority.value}")
        print(f"   Estimated: {next_task.estimated_hours} hours")
        print(f"   Due: {next_task.due_date}")
        print(f"\n   Description:")
        print(f"   {next_task.description[:200]}...")
    else:
        print("\n✅ No tasks available! Everything is done or blocked.")
    
    # Export to GitHub
    print("\n" + "="*60)
    print("💾 Exporting to GitHub Issues format...")
    print("="*60)
    
    Path("PM_GITHUB_ISSUES.md").write_text(agent.export_to_github_issues())
    print("✅ Exported to PM_GITHUB_ISSUES.md")
    
    print("\n🎯 PM Agent initialized! Database: pm_agent.db")
