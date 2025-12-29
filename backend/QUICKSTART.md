# 🚀 Quick Start Guide

## Option 1: Using Docker (Recommended)

This is the fastest way to get everything running:

```bash
# Make sure Docker Desktop is running, then:
./start.sh
```

That's it! The script will:
- ✅ Check Docker is running
- ✅ Create environment configuration
- ✅ Start all services (Database, Redis, Backend, Dashboard)
- ✅ Display service URLs

**Access your applications:**
- 📊 **Dashboard**: http://localhost:3000
- 🔧 **API**: http://localhost:8000
- 📖 **API Docs**: http://localhost:8000/docs

## Option 2: Local Development

For development with hot-reload:

### Step 1: Initial Setup
```bash
./setup-local.sh
```

### Step 2: Start Infrastructure
```bash
docker-compose up -d db redis
```

### Step 3: Start Backend
```bash
cd backend
source .venv/bin/activate  # or: source venv/bin/activate
python -m uvicorn main:app --reload
```

### Step 4: Start Dashboard (new terminal)
```bash
cd dashboard
npm run dev
```

## 🎯 Using the System

### 1. Start Training
- Open http://localhost:3000
- Click **"Start Continuous Training"**
- Watch metrics update in real-time

### 2. Manual Testing
- Click **"Generate & Execute Scenario"**
- View results in the charts
- Check performance statistics

### 3. Monitor Performance
The dashboard shows:
- Total scenarios completed
- Average response time
- Success rate
- Error counts
- Real-time charts

## 🛠️ Useful Commands

```bash
# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Restart services
docker-compose restart

# Rebuild containers
docker-compose up -d --build

# Check service status
docker-compose ps
```

## 🐛 Troubleshooting

**Dashboard shows "Disconnected"?**
- Check backend is running: http://localhost:8000/health
- Check Docker containers: `docker-compose ps`

**"Cannot connect to database"?**
- Ensure database is running: `docker-compose up -d db`
- Wait 10 seconds for database to initialize

**Port already in use?**
- Stop conflicting services or change ports in `docker-compose.yml`

## 📚 Learn More

- See [README.md](README.md) for complete documentation
- Visit http://localhost:8000/docs for API documentation
- Check `.github/copilot-instructions.md` for development guidelines

---

**Need help?** Open an issue or check the logs with `docker-compose logs -f`
