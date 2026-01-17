#!/bin/bash
# Start VNC server and code-server (VS Code server) in the background

# Start VNC server
vncserver :1 -geometry 1280x800 -depth 24 &

# Start code-server (no auth, runs as 'admin')
code-server --bind-addr 0.0.0.0:8080 --auth none --disable-telemetry --user-data-dir /workspace/.vscode-server &

# Wait on both processes
wait -n
