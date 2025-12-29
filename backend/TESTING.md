# Testing Guide

## How to Test the Hive System

This guide walks you through testing all features of the Hive Testing & Monitoring System.

## Prerequisites

Ensure the system is running:
```bash
./start.sh
```

Wait 30 seconds for all services to initialize.

## Test 1: System Health Check

### API Health
```bash
# Test API is running
curl http://localhost:8000/

# Expected response:
# {"service":"Hive Testing & Monitoring System","status":"running","version":"1.0.0"}

# Test health endpoint
curl http://localhost:8000/api/health

# Expected response:
# {"status":"healthy","timestamp":"2024-..."}
```

### Dashboard Access
1. Open http://localhost:3000 in your browser
2. Verify the dashboard loads
3. Check connection indicator (should be green "Connected")

## Test 2: Manual Scenario Generation

### Via Dashboard
1. Click **"Generate & Execute Scenario"** button
2. Wait 5-10 seconds for execution
3. Verify:
   - Scenario appears in "Recent Training Problems"
   - Metrics chart updates with new data
   - Status cards show updated values

### Via API
```bash
# Generate a scenario
curl -X POST http://localhost:8000/api/scenarios/generate

# Example response:
# {
#   "id": "load_balancing_a1b2c3d4",
#   "scenario_type": "load_balancing",
#   "difficulty": "medium",
#   "parameters": {...},
#   "description": "Balance 150 req/s across 7 nodes"
# }

# Execute the scenario (replace ID)
curl -X POST http://localhost:8000/api/scenarios/load_balancing_a1b2c3d4/execute
```

## Test 3: Continuous Training

### Start Training
1. Click **"Start Continuous Training"** button
2. Verify:
   - Button changes to "Stop Training"
   - Training status shows "Running"
   - Scenarios completed counter increments
   - New problems appear every 30-40 seconds
   - Metrics chart updates continuously

### Monitor Training
Watch these metrics update:
- Scenarios Completed (increases)
- Current Difficulty (adapts based on success)
- Average Success Rate (should stabilize around 90%)
- Runtime (increases)

### Stop Training
1. Click **"Stop Training"** button
2. Verify:
   - Status changes to "Stopped"
   - Scenario generation stops
   - Final metrics are preserved

## Test 4: Real-time Updates

### WebSocket Connection
Open browser console (F12) and check:
```javascript
// You should see WebSocket messages like:
// WebSocket connected
// Received: {type: "training_update", data: {...}}
```

### Live Metrics
1. Start continuous training
2. Open a second browser tab with the dashboard
3. Verify both tabs show the same real-time updates
4. Stop training in one tab
5. Verify both tabs reflect the change

## Test 5: Metrics API

### Get Latest Metrics
```bash
curl http://localhost:8000/api/metrics/latest

# Returns array of recent metrics:
# {
#   "metrics": [
#     {
#       "timestamp": "2024-...",
#       "type": "response_time",
#       "value": 123.45,
#       "scenario_id": "..."
#     },
#     ...
#   ]
# }
```

### Get Summary
```bash
curl http://localhost:8000/api/metrics/summary

# Returns aggregated statistics:
# {
#   "total_scenarios": 10,
#   "average_response_time": 150.5,
#   "average_throughput": 450.2,
#   "average_success_rate": 0.95,
#   "total_errors": 2,
#   "uptime": 300.5,
#   "last_updated": "2024-..."
# }
```

### Get Performance Analytics
```bash
curl http://localhost:8000/api/analytics/performance

# Returns detailed analytics by metric type:
# {
#   "metrics": {
#     "response_time": {
#       "min": 50.0,
#       "max": 300.0,
#       "mean": 150.5,
#       "median": 145.0,
#       "std_dev": 45.2
#     },
#     ...
#   },
#   "scenarios_completed": 10,
#   "current_difficulty": "medium",
#   "training_duration": 300.5
# }
```

## Test 6: Difficulty Adaptation

### Test Difficulty Increase
1. Start continuous training
2. Monitor "Current Difficulty" in training progress
3. If success rate > 95%, difficulty should increase
4. Watch for: easy → medium → hard → extreme

### Test Difficulty Decrease
1. If you see high error rates (>30%)
2. System should automatically reduce difficulty
3. Watch for: extreme → hard → medium → easy

## Test 7: Scenario Types

Each scenario type should be testable:

### Load Balancing
```bash
curl -X POST http://localhost:8000/api/scenarios/generate
# Look for "scenario_type": "load_balancing"
```

Verify parameters include:
- request_rate
- concurrent_users
- distribution_strategy

### Resource Allocation
Verify parameters include:
- total_resources
- resource_types
- allocation_strategy

### Fault Tolerance
Verify parameters include:
- failure_rate
- recovery_time
- redundancy_level

### And so on for all 8 types...

## Test 8: Error Handling

### Invalid Requests
```bash
# Non-existent scenario
curl -X POST http://localhost:8000/api/scenarios/invalid_id/execute

# Should return appropriate error message
```

### Database Connection
```bash
# Stop database
docker-compose stop db

# Try to make request
curl http://localhost:8000/api/metrics/summary

# Should handle gracefully

# Restart database
docker-compose start db
```

## Test 9: Data Persistence

### Test Database Storage
1. Run several scenarios
2. Stop all services: `docker-compose down`
3. Restart services: `docker-compose up -d`
4. Verify metrics history is preserved
5. Check dashboard shows previous data

### Test Redis Cache
```bash
# Connect to Redis
docker exec -it hive-redis-1 redis-cli

# Check keys
KEYS *

# Should show cached data
```

## Test 10: Performance Testing

### Load Testing Backend
```bash
# Install Apache Bench if needed
# brew install httpd (macOS)

# Test API performance
ab -n 1000 -c 10 http://localhost:8000/api/health

# Check results:
# - Requests per second
# - Time per request
# - Failed requests (should be 0)
```

### Dashboard Performance
1. Open browser DevTools (F12)
2. Go to Performance tab
3. Start recording
4. Start continuous training
5. Stop recording after 30 seconds
6. Check for:
   - Smooth frame rate (60 FPS)
   - No memory leaks
   - Efficient rendering

## Test 11: Cross-browser Testing

Test dashboard in multiple browsers:
- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari

Verify:
- Charts render correctly
- Buttons work
- WebSocket connects
- Real-time updates work

## Test 12: Mobile Responsiveness

1. Open dashboard on mobile device or DevTools device mode
2. Verify:
   - Layout adapts to screen size
   - All buttons are clickable
   - Charts are readable
   - No horizontal scrolling

## Automated Testing (Future)

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd dashboard
npm test
```

## Expected Behavior Summary

✅ **Working Correctly:**
- API responds to all endpoints
- Dashboard loads and connects
- Scenarios generate and execute
- Metrics update in real-time
- WebSocket maintains connection
- Difficulty adapts automatically
- Data persists across restarts
- All 8 scenario types work
- Charts update smoothly
- Error handling works

❌ **Issues to Check:**
- Connection indicator is red
- Metrics not updating
- WebSocket disconnecting repeatedly
- Database errors in logs
- Frontend blank page
- API timeout errors

## Debugging Tips

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f dashboard
docker-compose logs -f db

# Check service status
docker-compose ps

# Restart specific service
docker-compose restart backend

# Check database
docker exec -it hive-db-1 psql -U postgres -d hive_monitoring
```

## Success Criteria

Your system is working correctly if:
1. ✅ All services start without errors
2. ✅ Dashboard loads and shows "Connected"
3. ✅ Manual scenarios execute successfully
4. ✅ Continuous training runs smoothly
5. ✅ Metrics update in real-time
6. ✅ All API endpoints respond
7. ✅ Data persists across restarts
8. ✅ Performance is acceptable (<500ms response)

## Next Steps After Testing

Once all tests pass:
1. Customize scenario parameters
2. Add new scenario types
3. Adjust difficulty thresholds
4. Implement custom metrics
5. Add authentication
6. Deploy to production

---

**Happy Testing! 🐝**
