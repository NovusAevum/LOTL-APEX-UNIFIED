#!/bin/bash
# LOTL-APEX Advanced Terminal Interface Runner

cd "$(dirname "$0")/.."

echo "🧠 Starting LOTL-APEX Advanced Sovereign Terminal..."
echo "════════════════════════════════════════════════════════"

# Activate Python environment
source .venv/bin/activate

# Check if required services are running
echo "🔍 Checking system services..."

# Check Ollama
if ! pgrep ollama > /dev/null; then
    echo "⚠️ Starting Ollama..."
    ollama serve &
    sleep 3
fi

# Check Weaviate
if ! docker ps | grep -q weaviate; then
    echo "⚠️ Starting Weaviate..."
    cd config/weaviate && docker-compose up -d && cd ../..
    sleep 5
fi

# Check Redis
if ! pgrep redis-server > /dev/null; then
    echo "⚠️ Starting Redis..."
    redis-server --daemonize yes
fi

echo "✅ All services ready"
echo ""
echo "🚀 Launching LOTL-APEX Sovereign Terminal..."
echo "   • Identity Engine: Learning your patterns"
echo "   • Agent Swarm: 6 specialized agents ready"
echo "   • Memory System: Persistent context enabled"
echo "   • OSINT Tools: Reconnaissance capabilities active"
echo ""

# Start the advanced terminal app
python3 scripts/advanced_terminal.py
