# System Architecture

## Overview

The Hive Testing & Monitoring System is a full-stack application designed for real-time performance testing and monitoring with adaptive learning capabilities.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │         Next.js Dashboard (Port 3000)                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐    │   │
│  │  │ Metrics  │  │  Status  │  │    Training      │    │   │
│  │  │  Chart   │  │  Cards   │  │    Controls      │    │   │
│  │  └──────────┘  └──────────┘  └──────────────────┘    │   │
│  │  ┌─────────────────────────────────────────────┐      │   │
│  │  │        Recent Problems List                 │      │   │
│  │  └─────────────────────────────────────────────┘      │   │
│  └────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/HTTPS + WebSocket
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND SERVICES                           │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │         FastAPI Backend (Port 8000)                    │   │
│  │  ┌──────────────────────────────────────────────────┐ │   │
│  │  │  REST API Endpoints                               │ │   │
│  │  │  • /api/health                                    │ │   │
│  │  │  • /api/metrics/*                                 │ │   │
│  │  │  • /api/training/*                                │ │   │
│  │  │  • /api/scenarios/*                               │ │   │
│  │  └──────────────────────────────────────────────────┘ │   │
│  │  ┌──────────────────────────────────────────────────┐ │   │
│  │  │  WebSocket Endpoint                               │ │   │
│  │  │  • /ws/metrics (Real-time updates)                │ │   │
│  │  └──────────────────────────────────────────────────┘ │   │
│  │  ┌──────────────────────────────────────────────────┐ │   │
│  │  │  Core Components                                  │ │   │
│  │  │  • Problem Generator                              │ │   │
│  │  │  • Training Engine                                │ │   │
│  │  │  • Metrics Collector                              │ │   │
│  │  └──────────────────────────────────────────────────┘ │   │
│  └────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ SQL Queries + Redis Commands
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
│                                                                 │
│  ┌──────────────────────────┐  ┌──────────────────────────┐   │
│  │  PostgreSQL (Port 5432)  │  │   Redis (Port 6379)      │   │
│  │  ┌────────────────────┐  │  │  ┌────────────────────┐  │   │
│  │  │ performance_metrics│  │  │  │   Cache Storage    │  │   │
│  │  │ test_scenarios     │  │  │  │   Session Data     │  │   │
│  │  │ training_sessions  │  │  │  │   Temp Metrics     │  │   │
│  │  └────────────────────┘  │  │  └────────────────────┘  │   │
│  └──────────────────────────┘  └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Training Scenario Execution
```
User clicks "Start Training"
       ↓
Dashboard → POST /api/training/start
       ↓
Training Engine generates scenario
       ↓
Problem Generator creates parameters
       ↓
Training Engine executes scenario
       ↓
Metrics collected in real-time
       ↓
Data saved to PostgreSQL
       ↓
WebSocket broadcasts updates
       ↓
Dashboard updates charts
```

### 2. Real-time Metrics Flow
```
Training Engine collects metric
       ↓
Metric stored in memory
       ↓
WebSocket manager notified
       ↓
Broadcast to all connected clients
       ↓
Dashboard receives update
       ↓
Chart re-renders with new data
```

### 3. Scenario Generation Flow
```
User clicks "Generate Scenario"
       ↓
POST /api/scenarios/generate
       ↓
Problem Generator selects type
       ↓
Parameters generated based on difficulty
       ↓
Scenario created and returned
       ↓
POST /api/scenarios/{id}/execute
       ↓
Training Engine runs scenario
       ↓
Results broadcast via WebSocket
```

## Component Details

### Frontend (Next.js)

**Pages**
- `app/page.tsx` - Main dashboard with all components
- `app/layout.tsx` - Root layout and metadata

**Components**
- `MetricsChart.tsx` - Real-time line chart for response times
- `StatusCard.tsx` - Reusable card for displaying metrics
- `TrainingControls.tsx` - Start/stop training buttons
- `RecentProblems.tsx` - List of generated scenarios

**Features**
- Server-side rendering with Next.js 14
- Real-time WebSocket updates
- Responsive design with TailwindCSS
- Dark mode support
- Interactive charts with Recharts

### Backend (FastAPI)

**Core Files**
- `main.py` - FastAPI app, routes, WebSocket handling
- `database.py` - SQLAlchemy models and connection
- `models.py` - Pydantic schemas for validation
- `problem_generator.py` - Dynamic scenario creation
- `training_engine.py` - Execution and metrics logic

**API Endpoints**
- Health: `/`, `/api/health`
- Metrics: `/api/metrics/latest`, `/api/metrics/summary`, `/api/analytics/performance`
- Training: `/api/training/start`, `/api/training/stop`, `/api/training/status`
- Scenarios: `/api/scenarios/generate`, `/api/scenarios/{id}/execute`
- Problems: `/api/problems/recent`
- WebSocket: `/ws/metrics`

**Features**
- Async/await for performance
- WebSocket real-time communication
- Comprehensive error handling
- Type hints with Pydantic
- Database migrations ready

### Database Schema

**performance_metrics**
- id: Primary key
- timestamp: When metric was recorded
- metric_type: Type of metric (response_time, throughput, etc.)
- value: Numeric value
- scenario_id: Foreign key to scenario
- metadata: JSON field for additional data

**test_scenarios**
- id: Unique scenario identifier
- created_at: Creation timestamp
- scenario_type: Type of test
- difficulty: Easy, medium, hard, extreme
- parameters: JSON configuration
- completed: Boolean status
- success_rate: Float 0-1
- execution_time: Duration in seconds
- results: JSON with detailed results

**training_sessions**
- id: Primary key
- started_at: Session start time
- ended_at: Session end time
- total_scenarios: Count of scenarios run
- successful_scenarios: Count of successes
- average_performance: Overall performance metric
- metrics: JSON aggregated data

## Deployment

### Development
```bash
# Backend
cd backend
source .venv/bin/activate
uvicorn main:app --reload

# Frontend
cd dashboard
npm run dev
```

### Production (Docker)
```bash
docker-compose up -d
```

**Services in Docker Compose:**
- `db` - PostgreSQL database
- `redis` - Redis cache
- `backend` - FastAPI application
- `dashboard` - Next.js frontend

## Scalability Considerations

**Horizontal Scaling**
- Backend can run multiple instances behind load balancer
- WebSocket sticky sessions required
- PostgreSQL connection pooling configured
- Redis for shared state across instances

**Vertical Scaling**
- Increase container resources in docker-compose.yml
- Adjust database connection pool size
- Optimize query performance with indexes

**Performance Optimizations**
- Redis caching for frequently accessed data
- Database query optimization with proper indexes
- Async I/O throughout backend
- Static asset optimization in Next.js
- Connection pooling for database

## Security Features

- Environment variable configuration
- CORS middleware configured
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- Type safety with TypeScript

## Monitoring & Logging

- Docker Compose logs: `docker-compose logs -f`
- API request logging via FastAPI
- WebSocket connection tracking
- Database query logging (development)
- Frontend error boundaries

## Future Enhancements

Potential additions:
- User authentication and authorization
- Historical data analysis and trends
- Machine learning for performance prediction
- Email/Slack notifications for failures
- Advanced filtering and search
- Export reports to PDF/CSV
- Custom scenario builder UI
- Multi-region deployment
- Kubernetes orchestration
- Prometheus metrics export

---

This architecture provides a robust, scalable foundation for hive testing and monitoring with real-time capabilities and room for growth.
