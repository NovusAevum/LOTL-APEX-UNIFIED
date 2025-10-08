#!/bin/bash
# LOTL-APEX-UNIFIED Advanced Setup Script

set -e

echo "🚀 Setting up LOTL-APEX-UNIFIED: Sovereign AI Terminal..."
echo "════════════════════════════════════════════════════════"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Check system requirements
echo -e "${BLUE}📋 Checking system requirements...${NC}"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✅ Python ${PYTHON_VERSION} found${NC}"

# Check Node.js version  
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️ Node.js not found. Installing via Homebrew...${NC}"
    if command -v brew &> /dev/null; then
        brew install node
    else
        echo -e "${RED}❌ Please install Node.js manually${NC}"
        exit 1
    fi
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✅ Node.js ${NODE_VERSION} found${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠️ Docker not found. Please install Docker Desktop${NC}"
else
    echo -e "${GREEN}✅ Docker found${NC}"
fi

# Setup Python environment
echo -e "${BLUE}📦 Setting up Python environment...${NC}"
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install core requirements
echo -e "${BLUE}📚 Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Install additional OSINT tools
echo -e "${PURPLE}🔍 Installing OSINT tools...${NC}"
pip install sherlock-project theharvester recon-ng

# Setup Ollama for local LLM
echo -e "${BLUE}🤖 Setting up Ollama for local AI...${NC}"
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}Installing Ollama...${NC}"
    curl -fsSL https://ollama.ai/install.sh | sh
fi

# Pull essential models
echo -e "${BLUE}📥 Downloading AI models...${NC}"
ollama pull mistral:7b-instruct
ollama pull codellama:7b-code
ollama pull phi3:mini

# Setup agent backend
echo -e "${BLUE}🤖 Setting up agent backend...${NC}"
cd apps/lotlops-agent
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt
cd ../..

# Setup web interface
echo -e "${BLUE}🌐 Setting up web interface...${NC}"
cd apps/lotlops-web/lotlops
npm install
cd ../../..

# Setup Weaviate vector database
echo -e "${BLUE}🧠 Setting up Weaviate vector database...${NC}"
cd config/weaviate
if [ -f "docker-compose.yml" ]; then
    docker-compose up -d
    echo -e "${GREEN}✅ Weaviate started${NC}"
else
    echo -e "${YELLOW}⚠️ Weaviate config not found, skipping...${NC}"
fi
cd ../..

# Create necessary directories
echo -e "${BLUE}📁 Creating directory structure...${NC}"
mkdir -p {data,logs,cache,backups}
mkdir -p data/{memory,identity,vectors,sessions}
mkdir -p logs/{agents,system,security,osint}

# Setup shell configurations
echo -e "${BLUE}🐚 Configuring shell environment...${NC}"

# Backup existing zshrc
if [ -f ~/.zshrc ]; then
    cp ~/.zshrc ~/.zshrc.lotl-backup
    echo -e "${GREEN}✅ Backed up existing .zshrc${NC}"
fi

# Add LOTL-APEX to shell
LOTL_PATH=$(pwd)
echo "# LOTL-APEX-UNIFIED Configuration" >> ~/.zshrc
echo "export LOTL_APEX_HOME=\"${LOTL_PATH}\"" >> ~/.zshrc
echo "export PATH=\"\$LOTL_APEX_HOME/tools/bin:\$PATH\"" >> ~/.zshrc
echo "source \$LOTL_APEX_HOME/tools/hanis-shell-suite/init.zsh" >> ~/.zshrc

# Make scripts executable
echo -e "${BLUE}🔧 Setting permissions...${NC}"
chmod +x scripts/*.sh
chmod +x scripts/*.py
chmod +x tools/bin/*

# Setup systemd service (Linux) or launchd (macOS)
echo -e "${BLUE}⚙️ Setting up system services...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS launchd
    cat > ~/Library/LaunchAgents/com.lotl-apex.agent.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lotl-apex.agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>${LOTL_PATH}/scripts/start-agent.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF
    echo -e "${GREEN}✅ macOS service configured${NC}"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux systemd
    sudo tee /etc/systemd/system/lotl-apex.service > /dev/null << EOF
[Unit]
Description=LOTL-APEX Sovereign AI Agent
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=${LOTL_PATH}
ExecStart=${LOTL_PATH}/scripts/start-agent.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    sudo systemctl daemon-reload
    sudo systemctl enable lotl-apex
    echo -e "${GREEN}✅ Linux service configured${NC}"
fi

# Create configuration files
echo -e "${BLUE}📝 Creating configuration files...${NC}"

# Main config
cat > config/lotl-apex.yaml << EOF
# LOTL-APEX Configuration
system:
  name: "LOTL-APEX-UNIFIED"
  version: "1.0.0"
  user: "hanis"
  
ai:
  local_llm: "ollama"
  models:
    primary: "mistral:7b-instruct"
    code: "codellama:7b-code"
    fast: "phi3:mini"
  
agents:
  max_concurrent: 6
  timeout: 300
  memory_limit: "2GB"
  
security:
  sandbox_enabled: true
  audit_logging: true
  encryption: true
  
osint:
  enabled: true
  safe_mode: true
  rate_limit: 10
  
memory:
  vector_db: "weaviate"
  retention_days: 365
  max_context: 10000
EOF

# Environment variables
cat > .env << EOF
# LOTL-APEX Environment Configuration
LOTL_APEX_ENV=development
LOTL_APEX_HOME=${LOTL_PATH}

# AI Configuration
OLLAMA_HOST=http://localhost:11434
HUGGINGFACE_API_KEY=your_hf_key_here
MISTRAL_API_KEY=your_mistral_key_here

# Database Configuration
WEAVIATE_URL=http://localhost:8080
REDIS_URL=redis://localhost:6379

# Security Configuration
ENCRYPTION_KEY=generate_secure_key_here
AUDIT_LOG_LEVEL=INFO

# OSINT Configuration
OSINT_SAFE_MODE=true
OSINT_RATE_LIMIT=10
EOF

# Create startup script
cat > scripts/start-agent.sh << 'EOF'
#!/bin/bash
# LOTL-APEX Agent Startup Script

cd "$(dirname "$0")/.."
source .venv/bin/activate

echo "🚀 Starting LOTL-APEX Agent..."

# Start Weaviate if not running
if ! docker ps | grep -q weaviate; then
    echo "Starting Weaviate..."
    cd config/weaviate && docker-compose up -d && cd ../..
fi

# Start Redis if not running
if ! pgrep redis-server > /dev/null; then
    echo "Starting Redis..."
    redis-server --daemonize yes
fi

# Start the agent
python apps/lotlops-agent/main.py &
AGENT_PID=$!

echo "Agent started with PID: $AGENT_PID"
echo $AGENT_PID > .agent.pid

# Keep script running
wait $AGENT_PID
EOF

chmod +x scripts/start-agent.sh

# Final setup
echo -e "${BLUE}🔧 Final configuration...${NC}"

# Initialize databases
python3 -c "
from core.identity_engine import IdentityEngine
from core.agent_swarm import AgentSwarmOrchestrator

print('Initializing identity engine...')
identity = IdentityEngine()

print('Initializing agent swarm...')
swarm = AgentSwarmOrchestrator()

print('Setup complete!')
"

echo ""
echo -e "${GREEN}✅ LOTL-APEX-UNIFIED Setup Complete!${NC}"
echo "════════════════════════════════════════════════════════"
echo ""
echo -e "${PURPLE}🚀 Quick Start Commands:${NC}"
echo -e "${BLUE}  Terminal Interface:${NC} ./scripts/run-terminal.sh"
echo -e "${BLUE}  Advanced Terminal:${NC} ./scripts/advanced-terminal.sh"
echo -e "${BLUE}  Web Interface:${NC} cd apps/lotlops-web/lotlops && npm run dev"
echo -e "${BLUE}  Agent Backend:${NC} ./scripts/start-agent.sh"
echo ""
echo -e "${YELLOW}📚 Documentation:${NC}"
echo -e "${BLUE}  Master Plan:${NC} docs/ADVANCED_MASTER_PLAN.md"
echo -e "${BLUE}  Optimization:${NC} docs/OPTIMIZATION_PLAN.md"
echo ""
echo -e "${GREEN}🧠 Your sovereign AI is ready to evolve with you!${NC}"
