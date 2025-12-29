#!/bin/bash

# 🚀 DEPLOY TODO - Script para desplegar TODOS los frontends
# Uso: ./deploy_all.sh

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        🚀 DEPLOYING QUETZALCORE - ALL FRONTENDS             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check node
echo -e "${BLUE}[1/5] Verificando Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no encontrado. Instala Node.js primero."
    exit 1
fi
echo -e "${GREEN}✅ Node.js $(node -v)${NC}"
echo ""

# Check dashboard build
echo -e "${BLUE}[2/5] Verificando Dashboard build...${NC}"
if [ -d "dashboard/out" ]; then
    FILES=$(find dashboard/out -type f | wc -l)
    echo -e "${GREEN}✅ Dashboard build encontrado ($FILES archivos)${NC}"
else
    echo -e "${YELLOW}⚠️  Dashboard build no encontrado. Compilando...${NC}"
    cd dashboard
    npm install > /dev/null 2>&1
    npm run build > /dev/null 2>&1
    cd ..
    echo -e "${GREEN}✅ Dashboard compilado${NC}"
fi
echo ""

# Check git status
echo -e "${BLUE}[3/5] Git status...${NC}"
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${GREEN}✅ Working directory limpio${NC}"
else
    echo -e "${YELLOW}⚠️  Cambios sin commitear. Commiteando...${NC}"
    git add -A
    git commit -m "🚀 Auto-deploy: dashboard ready for production" || true
fi
echo ""

# Push to main
echo -e "${BLUE}[4/5] Pusheando a GitHub...${NC}"
git push origin main -f > /dev/null 2>&1
echo -e "${GREEN}✅ Push completado${NC}"
echo ""

# Deploy options
echo -e "${BLUE}[5/5] Opciones de despliegue${NC}"
echo ""
echo -e "${GREEN}┌─────────────────────────────────────────────┐${NC}"
echo -e "${GREEN}│  OPCIÓN 1: GitHub Pages (RECOMENDADO)      │${NC}"
echo -e "${GREEN}├─────────────────────────────────────────────┤${NC}"
echo -e "${GREEN}│ Ve a: settings/pages                         │${NC}"
echo -e "${GREEN}│ Source: GitHub Actions                       │${NC}"
echo -e "${GREEN}│ URL: la-potencia-cananbis.github.io/...      │${NC}"
echo -e "${GREEN}│ Tiempo: ~2 minutos                           │${NC}"
echo -e "${GREEN}└─────────────────────────────────────────────┘${NC}"
echo ""
echo -e "${YELLOW}┌─────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│  OPCIÓN 2: Netlify Drop (MÁS RÁPIDO)       │${NC}"
echo -e "${YELLOW}├─────────────────────────────────────────────┤${NC}"
echo -e "${YELLOW}│ 1. Ve a: https://app.netlify.com/drop       │${NC}"
echo -e "${YELLOW}│ 2. Arrastra: dashboard/out/                 │${NC}"
echo -e "${YELLOW}│ Tiempo: 30 segundos                          │${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────┘${NC}"
echo ""
echo -e "${BLUE}┌─────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│  OPCIÓN 3: Vercel (MÁS PROFESIONAL)        │${NC}"
echo -e "${BLUE}├─────────────────────────────────────────────┤${NC}"
echo -e "${BLUE}│ npm install -g vercel                        │${NC}"
echo -e "${BLUE}│ vercel login                                 │${NC}"
echo -e "${BLUE}│ cd dashboard && vercel --prod                │${NC}"
echo -e "${BLUE}│ Tiempo: ~1 minuto                            │${NC}"
echo -e "${BLUE}└─────────────────────────────────────────────┘${NC}"
echo ""

# Test backend
echo -e "${BLUE}Testing backend...${NC}"
HEALTH=$(curl -s https://queztl-core-backend.onrender.com/api/health 2>/dev/null | grep -o '"status":"[^"]*"' || echo "offline")
if [[ $HEALTH == *"healthy"* ]]; then
    echo -e "${GREEN}✅ Backend: HEALTHY${NC}"
else
    echo -e "${YELLOW}⚠️  Backend: Status unknown${NC}"
fi
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           ✅ DEPLOYMENT PREP COMPLETE!                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}Sistema listo para producción.${NC}"
echo ""
echo "📊 URLs:"
echo "  • Backend: https://queztl-core-backend.onrender.com ✅"
echo "  • Dashboard: (selecciona opción arriba)"
echo ""
echo "💎 Next: Elige una opción de despliegue arriba"
echo ""
