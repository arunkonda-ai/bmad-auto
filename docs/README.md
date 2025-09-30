---
title: Docs Processing Workflow & Index
type: reference
version: 1.0
created: 2025-01-18
updated: 2025-01-18
authors: [alex]
status: active
related: [../CLAUDE.md, TECHNICAL_TEMPLATE.md]
---

# 📐 Docs Domain - Processed Knowledge

## **📋 Workflow Overview**
This folder contains processed knowledge derived from research:
```
Research Findings → Technical Processing → Implementation Guides → Planning Integration
```

## **📁 Folder Structure (Updated)**
```
docs/
├── foundation/          # Core frameworks & cognitive systems
├── implementation/      # Development guides & technical how-to
├── operations/          # Deployment, monitoring, troubleshooting
├── api-reference/       # API documentation & technical reference
├── TECHNICAL_TEMPLATE.md # 📝 Mandatory template
└── README.md           # 📖 This guide
```

## **🤖 Agent Processing Rules**

### **Alex (Architect) - System Design**
- **Input**: Research findings from Mary
- **Output**: `foundation/` and `api-reference/` documents
- **Template**: Use `TECHNICAL_TEMPLATE.md`
- **Citations**: Always reference source research

### **James (Developer) - Implementation**
- **Input**: Architecture specs from Alex
- **Output**: `implementation/` guides and tutorials
- **Template**: Use `TECHNICAL_TEMPLATE.md`
- **Focus**: Practical development guidance

### **Quinn (QA) - Operations**
- **Input**: Implementation guides from James
- **Output**: `operations/` deployment and monitoring guides
- **Template**: Use `TECHNICAL_TEMPLATE.md`
- **Focus**: Quality assurance and operational excellence

## Quick Start Guide

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose
- Kubernetes cluster (for production)

### Development Setup
```bash
# Clone repository
git clone https://github.com/your-org/bmad-auto.git
cd bmad-auto

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start development server
python -m src.main
```

### Production Deployment
```bash
# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Or deploy to Kubernetes
kubectl apply -f k8s/
```

## System Capabilities

### Autonomous Product Development
- **Research Phase**: Automated market research and competitive analysis
- **Ideation Phase**: AI-facilitated innovation and concept development
- **Specification Phase**: Automated PRD generation and technical architecture
- **Development Phase**: Coordinated implementation with quality monitoring
- **Validation Phase**: Comprehensive testing and market validation

### AI Agent Ecosystem
- **Mary (Business Analyst)**: Market intelligence and user research
- **John (Product Manager)**: Product strategy and stakeholder coordination
- **James (Developer)**: Technical architecture and implementation
- **Quinn (QA Engineer)**: Quality assurance and testing orchestration
- **Sally (UX Designer)**: User experience and design systems
- **Alex (System Architect)**: Infrastructure and deployment optimization

### Quality Assurance
- **Mandatory Validation Pipeline**: PM → Dev → QA → UX → CEO approval
- **Automated Quality Gates**: Technical, design, and strategic validation
- **Human Oversight**: Strategic decision points with escalation protocols
- **Continuous Improvement**: Quality metrics drive system optimization

## Architecture Highlights

### Core Design Principles
- **Non-Invasive Integration**: Complete preservation of `.bmad-core` infrastructure
- **Size Compliance**: All components maintained under 300 lines for clarity
- **Real Integration**: Production-grade external service connections
- **Human-AI Collaboration**: Strategic human control with AI execution
- **Quality-First Orchestration**: No shortcuts in quality validation

### Technology Stack
- **Orchestration**: LangGraph with LangSmith monitoring
- **Backend**: FastAPI with async SQLAlchemy and Pydantic v2
- **Database**: PostgreSQL with Redis caching
- **AI Services**: OpenAI, Anthropic with intelligent model routing
- **Integration**: Linear project management, GitHub code management
- **Monitoring**: Prometheus, Grafana, ELK Stack, Jaeger tracing

## Key Features

### Workflow Orchestration
- **LangGraph Integration**: State-based workflow coordination
- **Agent Coordination**: Intelligent task assignment and handoff protocols
- **State Management**: Persistent workflow state with recovery capabilities
- **Progress Tracking**: Real-time workflow monitoring and reporting

### External Integration
- **Linear Sync**: Bidirectional project management synchronization
- **GitHub Integration**: Automated branch management and PR coordination
- **AI Service Management**: Multi-provider routing with cost optimization
- **MCP Integration**: Dynamic context management and documentation

### Quality & Monitoring
- **Comprehensive Metrics**: Workflow, agent, and business performance tracking
- **Distributed Tracing**: End-to-end workflow analysis with Jaeger
- **Centralized Logging**: Structured logging with ELK Stack
- **Intelligent Alerting**: Proactive issue detection and escalation

## Documentation Conventions

### Code Examples
All code examples are production-ready and follow established patterns:
- Python code uses async/await patterns with proper error handling
- Configuration examples include security best practices
- Infrastructure examples support high availability

### Navigation
- **Internal Links**: Use relative paths for cross-references
- **External Links**: Include context and purpose
- **Code References**: Include file path and line numbers where applicable

### Updates
This documentation is actively maintained and updated with each release:
- **Version**: 1.0.0
- **Last Updated**: January 2024
- **Next Review**: March 2024

## Getting Help

### Community Resources
- **Documentation Issues**: Report inaccuracies or suggest improvements
- **Technical Support**: Get help with implementation and deployment
- **Feature Requests**: Propose new capabilities and enhancements

### Contributing
We welcome contributions to improve BMAD Auto documentation:
1. Fork the documentation repository
2. Create a feature branch for your changes
3. Follow the documentation style guide
4. Submit a pull request with clear description

### Support Channels
- **GitHub Issues**: Technical issues and bug reports
- **Discord Community**: Real-time discussion and support
- **Email Support**: enterprise-support@bmad-auto.com

## License

BMAD Auto is released under the MIT License. See [LICENSE](../LICENSE) for details.

---

**Ready to transform your product development with autonomous AI orchestration?** Start with the [System Architecture](./01-foundation/system-architecture.md) to understand the foundational concepts, then follow the [Implementation Guide](./02-implementation/) to begin building your autonomous product team.

*Transform your product development from manual coordination to autonomous orchestration - where AI agents handle execution while humans focus on strategy and creativity.*