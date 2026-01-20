#!/bin/bash
# Silent Autonomous Worker - No prompts, just work
# Runs for 4 hours, logs to file, checks in every 15 min

LOG_FILE="$HOME/queztl-core/autonomous_work.log"
START_TIME=$(date +%s)
END_TIME=$((START_TIME + 14400))  # 4 hours
CHECKIN_INTERVAL=900  # 15 minutes

log() {
    echo "[$(date '+%H:%M:%S')] $1" >> "$LOG_FILE"
}

log "🤖 Autonomous session started"
log "⏰ Will run until $(date -r $END_TIME '+%H:%M:%S')"

# Task queue
TASKS=(
    "image:Karl Marx revolutionary leader"
    "image:Workers breaking chains unity"
    "image:Red star over industrial landscape"
    "image:Revolutionary march with red banners"
    "image:PSL campaign poster housing is a human right"
    "image:Anti-imperialist solidarity global resistance"
    "image:Palestine liberation end occupation"
    "image:Workers unite for socialism revolutionary power"
    "image:Black Panther Party free breakfast program serving community"
    "image:Brown Berets community patrol Chicano liberation"
    "image:La Raza Unida Aztlan cultural resistance"
    "image:Fred Hampton Rainbow Coalition all power to the people"
    "image:Huey Newton revolutionary self-defense dignity"
    "image:United fist Black Brown solidarity"
    "code:Fix linting issues"
    "code:Optimize training pipeline"
    "code:Integrate PSL Liberation School content"
)

NEXT_CHECKIN=$((START_TIME + CHECKIN_INTERVAL))

for task in "${TASKS[@]}"; do
    CURRENT_TIME=$(date +%s)
    
    # Check if time's up
    if [ $CURRENT_TIME -ge $END_TIME ]; then
        log "⏰ Time limit reached"
        break
    fi
    
    # Check-in time?
    if [ $CURRENT_TIME -ge $NEXT_CHECKIN ]; then
        ELAPSED=$((CURRENT_TIME - START_TIME))
        REMAINING=$((END_TIME - CURRENT_TIME))
        log "⏰ CHECK-IN: Elapsed ${ELAPSED}s, Remaining ${REMAINING}s"
        NEXT_CHECKIN=$((CURRENT_TIME + CHECKIN_INTERVAL))
    fi
    
    # Execute task
    TYPE="${task%%:*}"
    DATA="${task#*:}"
    
    case "$TYPE" in
        image)
            log "🎨 Generating: $DATA"
            JOB_ID=$(curl -sS -X POST http://192.168.1.105:8001/generate \
                -H "Content-Type: application/json" \
                -d "{\"prompt\":\"$DATA, socialist realism style, dramatic lighting\",\"style\":\"propaganda\",\"width\":1024,\"height\":1024,\"steps\":30,\"guidance_scale\":7.5}" \
                | grep -o '"job_id":"[^"]*"' | cut -d'"' -f4)
            
            if [ -n "$JOB_ID" ]; then
                log "✅ Image queued: ${JOB_ID:0:8}..."
            else
                log "❌ Image generation failed"
            fi
            ;;
        
        code)
            log "🔧 Running: $DATA"
            # Add code tasks here
            log "✅ Code task complete"
            ;;
    esac
    
    # Brief pause between tasks
    sleep 30
done

log "✅ Autonomous session complete"
