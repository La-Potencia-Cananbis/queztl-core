"""
Database configuration and connection management
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean
import os
from datetime import datetime

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@db:5432/queztl_core"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class PerformanceMetricDB(Base):
    __tablename__ = "performance_metrics"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    metric_type = Column(String(50), index=True)
    value = Column(Float)
    scenario_id = Column(String(100), index=True)
    meta_data = Column(JSON)

class TestScenarioDB(Base):
    __tablename__ = "test_scenarios"

    id = Column(String(100), primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    scenario_type = Column(String(50), index=True)
    difficulty = Column(String(20))
    parameters = Column(JSON)
    completed = Column(Boolean, default=False)
    success_rate = Column(Float)
    execution_time = Column(Float)
    results = Column(JSON)

class TrainingSessionDB(Base):
    __tablename__ = "training_sessions"

    id = Column(Integer, primary_key=True, index=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    total_scenarios = Column(Integer, default=0)
    successful_scenarios = Column(Integer, default=0)
    average_performance = Column(Float)
    metrics = Column(JSON)

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """Get database session"""
    async with async_session() as session:
        yield session
