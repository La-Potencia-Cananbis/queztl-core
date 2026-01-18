#!/bin/bash
# Train Advanced Marxist Meme Generator on Beast with 4-pass training

set -e

echo "🚩 ADVANCED MARXIST MEME GENERATOR - BEAST TRAINING"
echo "=================================================="
echo ""

BEAST_IP="192.168.1.105"
BEAST_USER="xava"
REMOTE_DIR="~/queztl-core"

echo "📡 Connecting to Beast (${BEAST_IP})..."
echo ""

# Check if Beast is online
if ! ping -c 1 ${BEAST_IP} &> /dev/null; then
    echo "❌ Beast is not reachable at ${BEAST_IP}"
    exit 1
fi

echo "✓ Beast is online"
echo ""

# Transfer files to Beast
echo "📤 Transferring advanced meme generator to Beast..."
scp backend/advanced_marxist_memes.py ${BEAST_USER}@${BEAST_IP}:${REMOTE_DIR}/backend/
echo "✓ Files transferred"
echo ""

# Run 4-pass training on Beast
echo "🔥 Starting 4-pass training on Beast..."
echo ""

ssh ${BEAST_USER}@${BEAST_IP} << 'ENDSSH'
cd ~/queztl-core
source venv/bin/activate

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASS 1: CONSTRUCTIVIST STYLE (10 memes)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 << 'PASS1'
from backend.advanced_marxist_memes import AdvancedMarxistMemeGenerator
generator = AdvancedMarxistMemeGenerator(high_res=True)
for i in range(10):
    img = generator.generate_constructivist_meme()
    generator.save_meme(img, f"pass1_constructivist_{i+1:02d}.png")
print("✓ Pass 1 complete: 10 constructivist memes")
PASS1

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASS 2: AGITPROP POSTERS (10 memes)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 << 'PASS2'
from backend.advanced_marxist_memes import AdvancedMarxistMemeGenerator
generator = AdvancedMarxistMemeGenerator(high_res=True)
for i in range(10):
    img = generator.generate_agitprop_poster()
    generator.save_meme(img, f"pass2_agitprop_{i+1:02d}.png")
print("✓ Pass 2 complete: 10 agitprop posters")
PASS2

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASS 3: RADICAL STATISTICS (10 memes)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 << 'PASS3'
from backend.advanced_marxist_memes import AdvancedMarxistMemeGenerator
generator = AdvancedMarxistMemeGenerator(high_res=True)
for i in range(10):
    img = generator.generate_radical_statistic()
    generator.save_meme(img, f"pass3_statistic_{i+1:02d}.png")
print("✓ Pass 3 complete: 10 radical statistics")
PASS3

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASS 4: VINTAGE PROPAGANDA (10 memes)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 << 'PASS4'
from backend.advanced_marxist_memes import AdvancedMarxistMemeGenerator
generator = AdvancedMarxistMemeGenerator(high_res=True)
for i in range(10):
    img = generator.generate_vintage_propaganda()
    generator.save_meme(img, f"pass4_vintage_{i+1:02d}.png")
print("✓ Pass 4 complete: 10 vintage propaganda")
PASS4

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✓ ALL 4 PASSES COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
ls -lh output/marxist_memes/ | grep -E "pass[1-4]" | wc -l | xargs echo "Total memes generated:"
du -sh output/marxist_memes/
echo ""

ENDSSH

echo ""
echo "📥 Downloading results from Beast..."
echo ""

# Create local directory
mkdir -p output/marxist_memes_beast

# Download all memes
scp ${BEAST_USER}@${BEAST_IP}:${REMOTE_DIR}/output/marxist_memes/pass*.png output/marxist_memes_beast/ 2>/dev/null || true

echo ""
echo "✓ Download complete"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚩 BEAST TRAINING COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Results:"
echo "  - 40 high-resolution memes (2160x2160)"
echo "  - 4 distinct styles (10 each)"
echo "  - 30 advanced Marxist slogans"
echo "  - 10 radical statistics"
echo ""
echo "📂 Local output: output/marxist_memes_beast/"
echo "📂 Beast output: ${BEAST_USER}@${BEAST_IP}:${REMOTE_DIR}/output/marxist_memes/"
echo ""
echo "🎨 Open folder:"
echo "  open output/marxist_memes_beast/"
echo ""
