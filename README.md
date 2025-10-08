# LOTL APEX UNIFIED - Sovereign AI System

> Revolutionary sovereign AI architecture combining identity mirroring, multi-agent coordination, and complete local operation for privacy-first AI assistance.

## 🚀 Quick Start

```bash
# Setup and run
cd /Users/wmh/LOTL-APEX-UNIFIED
./scripts/setup.sh

# Start development
pnpm dev
```

## 🏗️ Project Structure

```
LOTL-APEX-UNIFIED/
├── apps/
│   ├── web/                 # Next.js 14 frontend
│   ├── api/                 # Fastify backend API
│   ├── agents/              # AI agent services
│   ├── lotlops-web/         # Legacy web interface
│   ├── lotlops-agent/       # Legacy agent system
│   └── dashboard/           # Management dashboard
├── packages/
│   ├── shared/              # Shared utilities
│   ├── database/            # Prisma schema & migrations
│   └── ui/                  # UI component library
├── core/
│   ├── agents/              # Agent implementations
│   ├── identity_engine.py   # Identity learning system
│   └── agent_swarm.py       # Multi-agent orchestration
├── tools/
│   ├── bin/                 # Executable binaries
│   ├── osint/               # OSINT investigation tools
│   ├── security/            # Security & red-team tools
│   ├── shell-enhancements/  # Shell optimization tools
│   ├── hanis-shell-suite/   # Custom shell configurations
│   ├── SuperEliteShellOps/  # Advanced shell operations
│   └── Sovereign-iTerm2-Suite/ # Terminal enhancements
├── config/
│   ├── weaviate/            # Vector database config
│   └── weaviate-local/      # Local vector DB setup
├── infra/
│   ├── docker/              # Docker configurations
│   ├── k8s/                 # Kubernetes manifests
│   └── monitoring/          # Prometheus & Grafana
├── docs/                    # Documentation
├── scripts/                 # Automation scripts
└── archive/                 # Legacy components
```

## 🤖 Core Features

### Agent Swarm System
- **6 Specialized Agents**: LOTL, OSINT, Security, Data, Task, Quick
- **Multi-Agent Coordination**: CrewAI framework integration
- **Task Queue Management**: BullMQ with Redis backend
- **Real-time Communication**: WebSocket-based coordination

### Identity Engine
- **Behavioral Learning**: Adapts to user communication patterns
- **Decision Analysis**: Learns from user preferences and choices
- **Pattern Recognition**: ML-based user behavior modeling
- **Privacy-First**: All learning data stays completely local

### OSINT Intelligence Suite
- **Domain Reconnaissance**: Automated domain scanning and analysis
- **Social Media Investigation**: Profile analysis and correlation
- **Threat Intelligence**: Security monitoring and alerting
- **Data Correlation**: Advanced analytics and pattern detection

### Modern UI Dashboard
- **Real-time Monitoring**: Live agent status and performance metrics
- **Investigation Workflows**: Complete OSINT case management
- **Terminal Integration**: Web-based command interface with Xterm.js
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS

## 🛠️ Technology Stack

### Backend
- **Runtime**: Node.js 20+ with TypeScript
- **Framework**: Fastify (high performance HTTP server)
- **Database**: PostgreSQL + Weaviate (vector database)
- **ORM**: Prisma with type-safe database access
- **Authentication**: JWT tokens with Passport.js
- **API**: GraphQL + REST hybrid architecture
- **Queue**: BullMQ with Redis for task management
- **LLM**: Ollama (local) + HuggingFace integration

### Frontend
- **Framework**: Next.js 14 with App Router
- **UI Library**: Shadcn/ui + Tailwind CSS
- **State Management**: Zustand + React Query
- **Real-time**: Socket.io for live updates
- **Charts**: Recharts for data visualization
- **Terminal**: Xterm.js for web-based terminal

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Traefik with automatic HTTPS
- **Monitoring**: Prometheus + Grafana dashboards
- **Logging**: Winston + ELK Stack
- **CI/CD**: GitHub Actions workflows

### AI/ML Stack
- **Local LLM**: Ollama serving Mistral, CodeLlama, Phi-3
- **Vector Database**: Weaviate for semantic search
- **Agent Framework**: CrewAI + LangChain integration
- **OSINT Tools**: Sherlock, theHarvester, Maltego
- **Security Tools**: Custom red-team and penetration testing tools

## 🚀 Development

### Prerequisites
- Node.js 20+
- pnpm 8+
- Docker & Docker Compose
- Git
- Python 3.9+ (for AI components)

### Environment Setup
```bash
# Install dependencies
pnpm install

# Start infrastructure services
pnpm docker:up

# Run database migrations
pnpm db:migrate

# Start all development servers
pnpm dev
```

### Available Scripts
```bash
pnpm dev              # Start all services in development mode
pnpm build            # Build all applications for production
pnpm test             # Run comprehensive test suites
pnpm lint             # Lint all code with ESLint
pnpm type-check       # TypeScript type checking
pnpm docker:up        # Start Docker infrastructure services
pnpm docker:down      # Stop all Docker services
pnpm docker:logs      # View Docker service logs
pnpm db:migrate       # Run Prisma database migrations
pnpm db:seed          # Seed database with initial data
pnpm ollama:pull      # Download AI models (Mistral, CodeLlama, Phi-3)
```

## 🌐 Services & Endpoints

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Next.js web application |
| API Server | http://localhost:3001 | Fastify backend API |
| API Documentation | http://localhost:3001/docs | Swagger/OpenAPI docs |
| Grafana Dashboard | http://localhost:3002 | Monitoring & metrics (admin/admin) |
| Prometheus | http://localhost:9090 | Metrics collection server |
| Traefik Dashboard | http://localhost:8080 | Reverse proxy management |
| Weaviate | http://localhost:8081 | Vector database interface |
| Ollama API | http://localhost:11434 | Local LLM API endpoint |

## 🔒 Security Features

- **Zero-Trust Architecture**: Every request authenticated and authorized
- **Local-First Operation**: No external dependencies or data leakage
- **End-to-End Encryption**: All data encrypted in transit and at rest
- **Comprehensive Audit Logging**: Complete activity tracking and forensics
- **Rate Limiting & DDoS Protection**: Built-in security middleware
- **Input Validation**: Zod schema validation for all API endpoints
- **Secure Key Management**: Proper secret handling and rotation

## 📊 Monitoring & Observability

- **Prometheus Metrics**: Comprehensive performance monitoring
- **Grafana Dashboards**: Visual analytics and alerting
- **Structured Logging**: Winston with ELK stack integration
- **Health Checks**: Automated service availability monitoring
- **Real-time Alerts**: System notification and escalation
- **Performance Profiling**: Application performance insights

## 🚢 Deployment Options

### Docker Production
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production environment
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f infra/k8s/

# Check deployment status
kubectl get pods -n lotl-apex
```

### Local Development
```bash
# Quick development setup
./scripts/setup.sh

# Start development environment
pnpm dev
```

## 🤝 Contributing

1. Fork the repository on GitHub
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request with detailed description

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for complete details.

## 🙏 Acknowledgments

- **CrewAI**: Multi-agent coordination framework
- **Ollama**: Local LLM serving infrastructure
- **Weaviate**: Vector database and semantic search
- **Fastify**: High-performance web framework
- **Next.js**: React-based frontend framework
- **Shadcn/ui**: Beautiful UI component library
- **Tailwind CSS**: Utility-first CSS framework

---

**Built with ❤️ for sovereign AI and privacy-first computing**

*"The future of AI is local, private, and under your complete control."*
