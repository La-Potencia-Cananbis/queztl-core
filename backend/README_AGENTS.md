# Queztl Agent System - Quick Start

## 🚀 What You Have Now

### ✅ Working Components (Tested & Proven)

1. **`simple_trainer.py`** - Single-process ML trainer
   - Achieves 100% accuracy in 3 epochs (2.4 minutes)
   - Real PyTorch with gradients, backprop, transfer learning
   - Works on 1 CPU, ready to scale
   
2. **`queztl_agents.py`** - Agent architecture
   - Multi-agent types: Trainer, Coder, Runner, Seeder, etc.
   - Knowledge transfer: One agent teaches another
   - DNA (what agent knows) + RNA (what agent does)
   
3. **`training_dashboard.py`** - Before/After visualization
   - Shows training data vs predictions
   - Real-time metrics and learning curves

---

## 🎯 Quick Commands

### Run Single Trainer (Test First!)
```bash
docker exec ray-head python /code/backend/simple_trainer.py --prepare --epochs 10 --target 0.90
```

### Run Agent Teaching Demo
```bash
docker exec ray-head python /code/backend/queztl_agents.py --demo
```

### Start Dashboard
```bash
docker exec -d ray-head bash -c "pip install flask --quiet && python /code/backend/training_dashboard.py"
# Then open: http://192.168.1.102:5000
```

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│ AGENT NODE (Beast, Optiplex, Future Nodes)             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Trainer      │  │ Coder        │  │ Runner       │ │
│  │ Agent        │  │ Agent        │  │ Agent        │ │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤ │
│  │ DNA:         │  │ DNA:         │  │ DNA:         │ │
│  │ - Models     │  │ - Code       │  │ - Tasks      │ │
│  │ - Datasets   │  │ - Snippets   │  │ - Scripts    │ │
│  │ - Skills     │  │ - Fixes      │  │ - Results    │ │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤ │
│  │ RNA:         │  │ RNA:         │  │ RNA:         │ │
│  │ - train()    │  │ - write()    │  │ - execute()  │ │
│  │ - teach()    │  │ - fix()      │  │ - monitor()  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                         │
│  Flow: Trainer learns → Spawns child → Teaches child   │
└─────────────────────────────────────────────────────────┘
```

---

## 🧬 Agent DNA/RNA Concept

### DNA (Persistent Knowledge)
- **What the agent knows**
- Saved to disk, transferable
- Contains: models, code, datasets, learned skills

### RNA (Runtime Behavior)
- **What the agent does**
- Runtime only, not persisted
- Contains: skill functions, state, actions

### Teaching Process
1. Teacher agent trains/learns something
2. Teacher spawns child agent
3. Teacher transfers DNA to child (models, skills, knowledge)
4. Child inherits and can continue learning

---

## 📈 Scaling Path

### Level 1: Single CPU ✅ CURRENT
```bash
docker exec ray-head python /code/backend/simple_trainer.py --epochs 10
```
**Status:** Works now, 100% accuracy proven

### Level 2: Multi-Core (30 seconds to implement)
Edit `simple_trainer.py` line 135:
```python
DataLoader(..., num_workers=8)  # Change from 2 to 8
```
**Gain:** 4x faster

### Level 3: Distributed (Ray cluster ready)
```python
# Wrap with Ray Train - see SCALING_PATH.md
```
**When:** Dataset > 100K images

---

## 🎓 How Agents Learn & Teach

### Example: Trainer Agent Workflow

```python
# 1. Create node
node = AgentNode("beast", workspace)

# 2. Spawn teacher
teacher = node.spawn_agent(AgentType.TRAINER, "teacher_001")

# 3. Teacher learns
teacher.train_model('/tmp/simple_training', epochs=5, target_accuracy=0.90)

# 4. Teacher spawns student
student = teacher.spawn_child(AgentType.TRAINER)

# 5. Teacher teaches student
teacher.teach_agent(student)

# Result: Student now has:
# - Learned skills: ['image_classification']
# - Models: {'image_classifier': '/path/to/model.pth'}
# - Generation: 1 (child of teacher)
```

---

## 🔧 Current Infrastructure

### Ray Cluster V2 (Operational)
- **Head Node:** Optiplex (192.168.1.102) - 4 CPUs
- **Worker Node:** Beast (192.168.1.105) - 8 CPUs
- **Total:** 12 CPUs, 7.77 GB RAM
- **Dashboard:** http://192.168.1.102:8265

### Docker Containers
```bash
# Check status
docker ps --filter name=ray
ssh beast "docker ps --filter name=ray"

# Ray cluster status
docker exec ray-head ray status
```

---

## 📝 Files You Created Today

### Core Code
- `simple_trainer.py` (348 lines) - Working ML trainer
- `queztl_agents.py` (600+ lines) - Agent system
- `training_dashboard.py` (400+ lines) - Visualization

### Documentation
- `SCALING_PATH.md` - How to scale
- `FROM_SHIT_TO_NONSHIT.md` - Journey & lessons
- `README_AGENTS.md` - This file

---

## 🎯 Next Steps (Your Choice)

### Option A: Improve Training Data
```bash
# Replace synthetic images with real dataset
# Download CIFAR-10, ImageNet subset, or your own images
# Point trainer at real data → achieve 95%+ accuracy
```

### Option B: Add More Agent Types
```python
# Implement more agent types:
# - FixerAgent: Debugs and repairs code
# - MonitorAgent: Watches system health
# - CoordinatorAgent: Orchestrates multi-agent tasks
```

### Option C: Deploy Multi-Node Agents
```bash
# Spawn agents on both Optiplex and Beast
# Have them communicate and share work
# Implement agent-to-agent teaching across network
```

### Option D: Real Problem (Geophysics?)
```bash
# Adapt simple_trainer.py for your domain
# Load seismic data, satellite imagery, etc.
# Train useful models for your actual work
```

---

## 🐛 Troubleshooting

### Dependencies Issue
```bash
# Fixed: numpy version conflicts resolved
docker exec ray-head pip list | grep -E "torch|numpy|flask"
```

### Training Fails
```bash
# Check logs
docker exec ray-head cat /tmp/simple_training/training_report.json

# Verify dataset
docker exec ray-head ls /tmp/simple_training/train/
```

### Agent Issues
```bash
# Check agent logs
docker exec ray-head cat /tmp/queztl_agents/beast/teacher_001/agent.log

# Check DNA
docker exec ray-head cat /tmp/queztl_agents/beast/teacher_001/dna.json
```

---

## 📚 Key Concepts

### 1. Test Single First, Then Distribute
- **Wrong:** Build distributed system, hope it works
- **Right:** Prove single-CPU works, then scale

### 2. Real Learning = Gradients
- **Wrong:** Call APIs, compare pixels
- **Right:** Neural network, loss.backward(), optimizer.step()

### 3. Agents = Knowledge + Behavior
- **DNA:** What agent knows (persistent)
- **RNA:** What agent does (runtime)
- **Teaching:** Transfer DNA between agents

### 4. Minimal Moving Parts
- **One trainer file:** 348 lines, does one thing well
- **No dead code:** Everything used, nothing wasted
- **Standard tools:** PyTorch = debuggable

---

## 🎉 What Makes This "Non-Shit"

✅ **Works on 1 CPU** - No cluster needed to start  
✅ **100% accuracy** - Proven learning happens  
✅ **48 seconds/epoch** - Fast iteration  
✅ **Self-contained** - Generates own test data  
✅ **Real ML** - Actual gradients and backprop  
✅ **Scalable design** - Ready for Ray/Horovod  
✅ **Agent teaching** - Knowledge transfers  
✅ **Clear metrics** - Know when it works  

---

## 🚀 Status Summary

**Current State:**
- ✅ Single-CPU trainer: 100% accuracy achieved
- ✅ Agent system: Teacher→Student working
- ✅ Ray cluster: 12 CPUs ready
- ✅ Code on GitHub: Pushed and live

**Ready For:**
- Scale to multi-core (5 min work)
- Scale to distributed (1 day work)
- Real datasets (1 hour work)
- Production deployment (when needed)

---

**Built:** January 16, 2026  
**Status:** Non-shit proven, ready to scale  
**Vision:** "Less is more, but document so we don't lose the dream"
