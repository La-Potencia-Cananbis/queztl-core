#!/bin/bash

echo "🐝 Hive Testing & Monitoring System - Startup Script"
echo "=================================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check if .env exists, if not create from example
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
else
    echo "✅ .env file exists"
fi

echo ""
echo "Starting services with Docker Compose..."
echo ""

# Start all services
docker-compose up -d

echo ""
echo "Waiting for services to be healthy..."
sleep 10

# Check service status
docker-compose ps

echo ""
echo "=================================================="
echo "🎉 Services are starting up!"
echo ""
echo "📊 Dashboard: http://localhost:3000"
echo "🔧 API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop services: docker-compose down"
echo "=================================================="
