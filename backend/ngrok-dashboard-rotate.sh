#!/bin/bash
# ngrok-dashboard-rotate.sh: Stop any running ngrok, start a new tunnel, and print the new public URL

# Stop all running ngrok processes
echo "Stopping any running ngrok tunnels..."
pkill -f "ngrok http" 2>/dev/null
sleep 2

# Start new ngrok tunnel in background and save output
echo "Starting new ngrok tunnel on port 8080..."
nohup ngrok http 8080 > ngrok.log 2>&1 &
sleep 5

# Extract the public URL from ngrok API
NGROK_API_URL="http://127.0.0.1:4040/api/tunnels"
PUBLIC_URL=$(curl -s $NGROK_API_URL | grep -o '"public_url":"https:[^"]*' | head -n1 | cut -d '"' -f4)

if [ -n "$PUBLIC_URL" ]; then
  echo "Your new public dashboard URL: $PUBLIC_URL"
else
  echo "Could not retrieve ngrok public URL. Check ngrok.log for errors."
fi
