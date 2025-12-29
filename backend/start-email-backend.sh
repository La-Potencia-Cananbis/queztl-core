#!/bin/bash
# 🚀 Start Queztl Email Backend
set -e

echo "🚀 Starting Queztl Email Backend"
echo "================================"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Start the email service
echo "📧 Starting email service on port 8001..."
python3 backend/email_service.py

echo ""
echo "✅ Email backend running at http://localhost:8001"
echo "📊 API docs available at http://localhost:8001/docs"
