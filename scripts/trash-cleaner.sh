#!/bin/bash
# Trash Cleaner - Automated Health Check & Cleanup Routine
# Runs on Beast/Sloth to monitor, clean, and fix issues

HOSTNAME=$(hostname)
LOG_FILE="/var/log/queztl-trash-cleaner.log"
REPORT_FILE="/tmp/trash-cleaner-report.txt"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$HOSTNAME] $1" | tee -a "$LOG_FILE"
}

report() {
    echo "$1" >> "$REPORT_FILE"
}

check_disk_space() {
    log "🗑️  Checking disk space..."
    
    USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ "$USAGE" -gt 80 ]; then
        log "⚠️  Disk usage at ${USAGE}% - cleaning..."
        
        # Clean package caches
        sudo apt-get clean 2>/dev/null
        
        # Clean old logs
        sudo journalctl --vacuum-time=7d 2>/dev/null
        
        # Clean tmp files older than 7 days
        find /tmp -type f -mtime +7 -delete 2>/dev/null
        
        NEW_USAGE=$(df -h / | awk 'NR==2 {print $5}')
        log "✓ Cleaned. New usage: ${NEW_USAGE}"
        report "Disk: ${USAGE}% → ${NEW_USAGE}"
    else
        log "✓ Disk usage OK: ${USAGE}%"
        report "Disk: ${USAGE}% (OK)"
    fi
}

check_memory() {
    log "💾 Checking memory..."
    
    MEM_FREE=$(free -m | awk 'NR==2 {print $4}')
    MEM_TOTAL=$(free -m | awk 'NR==2 {print $2}')
    MEM_PERCENT=$(( (MEM_TOTAL - MEM_FREE) * 100 / MEM_TOTAL ))
    
    if [ "$MEM_PERCENT" -gt 90 ]; then
        log "⚠️  Memory usage at ${MEM_PERCENT}% - clearing caches..."
        sudo sync
        sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 2>/dev/null
        log "✓ Caches cleared"
        report "Memory: ${MEM_PERCENT}% (cleared caches)"
    else
        log "✓ Memory usage OK: ${MEM_PERCENT}%"
        report "Memory: ${MEM_PERCENT}% (OK)"
    fi
}

check_hung_processes() {
    log "🔍 Checking for hung processes..."
    
    # Find python processes using high CPU for >30 min
    HUNG_PROCS=$(ps aux | awk '$3 > 80.0 && $10 ~ /[3-9][0-9]:[0-9][0-9]/ {print $2,$11}' | grep python)
    
    if [ -n "$HUNG_PROCS" ]; then
        log "⚠️  Found hung processes:"
        echo "$HUNG_PROCS" | while read pid cmd; do
            log "  PID $pid: $cmd (killing...)"
            kill -9 "$pid" 2>/dev/null
        done
        report "Hung Processes: Killed"
    else
        log "✓ No hung processes"
        report "Hung Processes: None"
    fi
    
    # Check for zombie processes
    ZOMBIES=$(ps aux | awk '$8 ~ /Z/ {print $2}')
    if [ -n "$ZOMBIES" ]; then
        ZOMBIE_COUNT=$(echo "$ZOMBIES" | wc -l)
        log "⚠️  $ZOMBIE_COUNT zombie processes found"
        report "Zombies: $ZOMBIE_COUNT"
    fi
}

check_infinite_loops() {
    log "♾️  Checking for infinite loops..."
    
    # Find processes stuck in same state for >1 hour
    for pid in $(pgrep -f "python.*queztl"); do
        # Check if process has been in 'R' state (running) continuously
        STATE=$(ps -p "$pid" -o state= 2>/dev/null)
        RUNTIME=$(ps -p "$pid" -o etime= 2>/dev/null | awk '{print $1}')
        
        if [ "$STATE" = "R" ] && [[ "$RUNTIME" =~ ^[0-9]+-[0-9]+:[0-9]+ ]]; then
            # Process running for days - likely stuck
            CMD=$(ps -p "$pid" -o comm=)
            log "⚠️  Potential infinite loop: PID $pid ($CMD) - runtime $RUNTIME"
            
            # Try graceful kill first
            kill -15 "$pid" 2>/dev/null
            sleep 5
            
            # Force kill if still running
            if ps -p "$pid" > /dev/null 2>&1; then
                kill -9 "$pid" 2>/dev/null
                log "✓ Force killed PID $pid"
                report "Infinite Loop: Killed PID $pid"
            fi
        fi
    done
}

check_beast_services() {
    log "⚡ Checking Beast services..."
    
    # Check image generator
    if pgrep -f beast_image_generator > /dev/null; then
        log "✓ Beast image generator running"
        report "Beast Image Gen: Running"
        
        # Check if API responding
        if curl -sS --max-time 5 http://localhost:8001/ > /dev/null 2>&1; then
            log "✓ Beast API responding"
            report "Beast API: Healthy"
        else
            log "❌ Beast API not responding - restarting..."
            pkill -9 -f beast_image_generator
            sleep 2
            cd ~/queztl-core && source venv/bin/activate && \
                nohup python3 backend/beast_image_generator.py > ~/beast_image_server.log 2>&1 &
            log "✓ Beast API restarted"
            report "Beast API: Restarted"
        fi
    else
        log "❌ Beast image generator not running - starting..."
        cd ~/queztl-core && source venv/bin/activate && \
            nohup python3 backend/beast_image_generator.py > ~/beast_image_server.log 2>&1 &
        log "✓ Beast image generator started"
        report "Beast Image Gen: Started"
    fi
    
    # Check for stuck/failed jobs
    if [ -f ~/queztl-core/data/generation_results.json ]; then
        FAILED=$(grep -o '"status":"failed"' ~/queztl-core/data/generation_results.json | wc -l)
        PROCESSING=$(grep -o '"status":"processing"' ~/queztl-core/data/generation_results.json | wc -l)
        
        if [ "$FAILED" -gt 0 ]; then
            log "⚠️  $FAILED failed jobs found"
            report "Failed Jobs: $FAILED"
        fi
        
        # Check for stuck jobs (processing > 10 min)
        if [ "$PROCESSING" -gt 0 ]; then
            log "⏳ $PROCESSING jobs processing"
            
            # Find jobs stuck for >15 minutes
            python3 -c "
import json
from datetime import datetime, timedelta

try:
    with open('$HOME/queztl-core/data/generation_results.json') as f:
        results = json.load(f)
    
    stuck = 0
    for job_id, job in results.items():
        if job['status'] == 'processing':
            created = datetime.fromisoformat(job['created_at'])
            age = datetime.now() - created
            if age > timedelta(minutes=15):
                stuck += 1
                print(f'Stuck job: {job_id[:8]} ({age})')
    
    if stuck > 0:
        print(f'Found {stuck} stuck jobs - clearing...')
        # Mark them as failed
        for job_id, job in results.items():
            if job['status'] == 'processing':
                created = datetime.fromisoformat(job['created_at'])
                if datetime.now() - created > timedelta(minutes=15):
                    job['status'] = 'failed'
                    job['error'] = 'Stuck/timeout'
        
        with open('$HOME/queztl-core/data/generation_results.json', 'w') as f:
            json.dump(results, f, indent=2)
except Exception as e:
    print(f'Error: {e}')
" 2>&1 | while read line; do
                log "  $line"
            done
            
            report "Processing Jobs: $PROCESSING (cleaned stuck jobs)"
        fi
    fi
}

check_auto_queue_monitor() {
    log "🤖 Checking auto-queue monitor..."
    
    if pgrep -f beast_auto_queue > /dev/null; then
        # Check if it's been running too long (>2 hours)
        RUNTIME=$(ps -o etime= -p $(pgrep -f beast_auto_queue) | awk '{print $1}')
        if [[ "$RUNTIME" =~ ^[0-9][0-9]:[0-9][0-9]:[0-9][0-9] ]] || [[ "$RUNTIME" =~ ^[0-9]+-[0-9]+ ]]; then
            log "⚠️  Auto-queue monitor running too long ($RUNTIME) - restarting..."
            pkill -f beast_auto_queue
            sleep 2
            cd ~/queztl-core && nohup backend/beast_auto_queue.sh >> ~/queztl-core/logs/auto_queue.log 2>&1 &
            log "✓ Auto-queue monitor restarted"
            report "Auto-Queue: Restarted (was stuck)"
        else
            log "✓ Auto-queue monitor healthy"
            report "Auto-Queue: Running"
        fi
    else
        log "✓ Auto-queue monitor not running (normal)"
        report "Auto-Queue: Idle"
    fi
}

check_network() {
    log "🌐 Checking network..."
    
    if ping -c 1 8.8.8.8 > /dev/null 2>&1; then
        log "✓ Internet connection OK"
        report "Network: OK"
    else
        log "❌ No internet connection"
        report "Network: DOWN"
    fi
}

cleanup_old_images() {
    log "🖼️  Cleaning old generated images..."
    
    IMAGE_DIR=~/queztl-core/output/beast_generated_images
    
    if [ -d "$IMAGE_DIR" ]; then
        # Keep only images from last 7 days
        CLEANED=$(find "$IMAGE_DIR" -type f -name "*.png" -mtime +7 -delete -print | wc -l)
        
        if [ "$CLEANED" -gt 0 ]; then
            log "✓ Cleaned $CLEANED old images"
            report "Images Cleaned: $CLEANED"
        else
            log "✓ No old images to clean"
            report "Images: Up to date"
        fi
    fi
}

check_python_env() {
    log "🐍 Checking Python environment..."
    
    if [ -d ~/queztl-core/venv ]; then
        source ~/queztl-core/venv/bin/activate
        
        # Check critical packages
        TORCH_OK=$(python3 -c "import torch; print('OK')" 2>/dev/null)
        DIFFUSERS_OK=$(python3 -c "import diffusers; print('OK')" 2>/dev/null)
        
        if [ "$TORCH_OK" = "OK" ] && [ "$DIFFUSERS_OK" = "OK" ]; then
            log "✓ Python environment healthy"
            report "Python Env: Healthy"
        else
            log "⚠️  Python packages missing"
            report "Python Env: Needs attention"
        fi
    else
        log "❌ Python venv not found"
        report "Python Env: Missing"
    fi
}

generate_report() {
    log "📊 Generating report..."
    
    cat > "$REPORT_FILE" << EOF
╔══════════════════════════════════════════════════════════════╗
║  🗑️  TRASH CLEANER REPORT - $HOSTNAME
║  $(date '+%Y-%m-%d %H:%M:%S')
╚══════════════════════════════════════════════════════════════╝

$(cat "$REPORT_FILE")

System Uptime: $(uptime -p)
Load Average: $(uptime | awk -F'load average:' '{print $2}')

Log: $LOG_FILE
EOF
    
    cat "$REPORT_FILE"
    
    # Save to shared location
    cp "$REPORT_FILE" ~/queztl-core/data/trash-cleaner-$(hostname)-$(date +%Y%m%d-%H%M%S).txt
}

main() {
    log "🚀 Trash Cleaner starting on $HOSTNAME..."
    
    > "$REPORT_FILE"  # Clear report
    
    # System health checks
    check_disk_space
    check_memory
    check_network
    check_python_env
    
    # Cnueralostasis maintenance
    check_hung_processes
    check_infinite_loops
    
    # Host-specific checks
    if [ "$HOSTNAME" = "beast" ] || [ "$(hostname)" = "beast" ] || [[ "$(hostname)" =~ beast ]]; then
        check_beast_services
        check_auto_queue_monitor
        cleanup_old_images
    fi
    
    generate_report
    
    log "✅ Trash Cleaner complete - Cnueralostasis maintained"
}

main "$@"
