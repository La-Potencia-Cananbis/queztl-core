#!/bin/bash
# Setup Queztl-Core Git Server

set -e

echo "🚀 Setting up Queztl-Core Git Server..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
mkdir -p data/gitea
mkdir -p data/postgres
mkdir -p data/redis
mkdir -p logs

# Generate Gitea token (will be set after first run)
echo "📝 Configuration:"
echo "  Git URL: http://localhost:3000"
echo "  SSH Port: 2222"
echo "  Admin user: Will be created on first run"

# Ask for configuration
read -p "Enter domain (or use localhost): " DOMAIN
DOMAIN=${DOMAIN:-localhost}

# Update docker-compose.yml with domain
sed -i.bak "s/git.queztl.local/$DOMAIN/g" docker-compose.yml

echo ""
echo "🐋 Starting containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check if Gitea is running
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Gitea is running!"
else
    echo "⚠️  Gitea may still be starting. Check logs with: docker-compose logs -f"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SETUP COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Access your Git server:"
echo "   Web UI:  http://$DOMAIN:3000"
echo "   SSH:     ssh://git@$DOMAIN:2222"
echo ""
echo "📝 Next steps:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Complete initial setup (create admin user)"
echo "3. Generate access token: Settings > Applications > Generate Token"
echo "4. Set token: export GITEA_TOKEN=your_token_here"
echo "5. Restart automation: docker-compose restart git-automation"
echo ""
echo "📖 Useful commands:"
echo "   Logs:       docker-compose logs -f"
echo "   Stop:       docker-compose stop"
echo "   Restart:    docker-compose restart"
echo "   Backup:     ./scripts/backup-repos.sh"
echo ""
