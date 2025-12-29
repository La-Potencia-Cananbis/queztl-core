#!/bin/bash

echo "🐝 Hive Testing & Monitoring System - Local Development Setup"
echo "============================================================="
echo ""

# Backend setup
echo "Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Backend setup complete"
echo ""

# Dashboard setup
echo "Setting up Dashboard..."
cd ../dashboard

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

echo "✅ Dashboard setup complete"
echo ""

cd ..

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
fi

echo ""
echo "============================================================="
echo "🎉 Setup Complete!"
echo ""
echo "To start services:"
echo "1. Start database and Redis: docker-compose up -d db redis"
echo "2. Start backend: cd backend && source venv/bin/activate && python -m uvicorn main:app --reload"
echo "3. Start dashboard: cd dashboard && npm run dev"
echo ""
echo "Or use Docker Compose: ./start.sh"
echo "============================================================="
