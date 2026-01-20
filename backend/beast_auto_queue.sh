#!/bin/bash
# Monitor Beast model download and auto-queue images when ready

LOG_FILE="$HOME/queztl-core/beast_auto_queue.log"

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🎨 Monitoring Beast model download..."

# Wait for model to finish downloading
while true; do
    # Check if processing
    STATUS=$(curl -sS http://192.168.1.105:8001/status/fa71e421-5a58-43f1-bc50-f30d8b061af2 2>/dev/null | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    
    if [ "$STATUS" = "complete" ]; then
        log "✅ Model downloaded! First image generated successfully!"
        break
    elif [ "$STATUS" = "failed" ]; then
        log "❌ Test image failed, checking logs..."
        ssh xava@192.168.1.105 "tail -5 ~/beast_image_server.log"
        exit 1
    elif [ "$STATUS" = "processing" ]; then
        log "⏳ Model downloading/processing..."
    fi
    
    sleep 30
done

log "🚀 Queueing fresh propaganda images..."

# Queue of fresh images
IMAGES=(
    "Karl Marx leading revolutionary workers, raised fist, red banners, dramatic lighting, powerful composition"
    "Fred Hampton speaking at rally, Black Panther Party, rainbow coalition, all power to the people"
    "Brown Berets community patrol, Chicano liberation, East LA, solidarity"
    "Huey Newton with law books, revolutionary self-defense, dignity and power"
    "La Raza Unida organizing, Aztlán cultural resistance, united fists raised"
    "PSL campaign poster, housing is a human right, homes guarantee"
    "Palestine liberation, end occupation, free Palestine solidarity"
    "Workers breaking chains, united fists, socialism rising, red dawn"
    "Anti-imperialist solidarity, global resistance, internationalism"
    "Black and Brown unity, rainbow coalition, revolutionary alliance"
)

for prompt in "${IMAGES[@]}"; do
    log "📤 Queuing: ${prompt:0:50}..."
    
    JOB_ID=$(curl -sS -X POST http://192.168.1.105:8001/generate \
        -H "Content-Type: application/json" \
        -d "{\"prompt\":\"$prompt\",\"style\":\"propaganda\",\"width\":1024,\"height\":1024,\"steps\":30,\"guidance_scale\":7.5}" \
        2>/dev/null | grep -o '"job_id":"[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$JOB_ID" ]; then
        log "✅ Queued: ${JOB_ID:0:8}"
    else
        log "❌ Failed to queue"
    fi
    
    sleep 2
done

log "🎉 All images queued! Check progress: tail -f ~/beast_image_server.log"
log "📊 View results: curl http://192.168.1.105:8001/recent"
