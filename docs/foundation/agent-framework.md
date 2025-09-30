# BMAD Auto Agent Framework

## Overview

The BMAD Auto agent framework implements a 10-agent ecosystem with PM-centric orchestration. John (PM) serves as the central coordination hub managing context distribution and task assignment across specialized agents while preserving `.bmad-core` infrastructure through command simulation.

## Orchestration Hierarchy

### Tier 1: Strategic Authority
**Arun (Human)** - Vision definition, quality gate approval, scope authorization

### Tier 2: Coordination Authority
**John (PM)** - Central orchestrator managing all agent activities and context flow
**Alex (Architect)** - Technical infrastructure coordination with PM oversight

### Tier 3: Specialized Execution
**8 Specialized Agents** - Domain expertise coordinated through PM hub

## 10-Agent Ecosystem

### Mary (Business Analyst) - Market Intelligence Specialist

**PM-Coordinated Responsibilities**:
- Market research execution under PM task assignment
- Competitive analysis with PM-defined scope and priorities
- User research coordination through PM context distribution
- Strategic insights delivery to PM for cross-agent coordination

**Specialized Capabilities**:
- Market intelligence automation with real-time competitive monitoring
- User research orchestration with systematic persona development
- Strategic analysis execution within PM-defined boundaries
- Data-driven insights delivery to PM coordination hub

### John (Product Manager) - Central Orchestration Hub

**Core Orchestration Responsibilities**:
- **Task Prioritization**: Evaluate Arun's priorities and assign tasks to appropriate agents
- **Context Distribution**: Control information flow to agents based on task relevance
- **Quality Gate Enforcement**: Coordinate validation across all agents before Arun approval
- **Agent Coordination**: Manage handoffs, dependencies, and cross-agent collaboration
- **Impact Assessment**: Evaluate feasibility and resource requirements for Arun's tasks

**PM Authority Functions**:
- Agent task assignment and capability matching
- Context filtering and selective information sharing
- Quality validation orchestration across specialized agents
- Escalation management to Arun for strategic decisions
- Resource allocation coordination with Alex (Architect)

### James (Developer) - Technical Implementation Specialist

**PM-Coordinated Responsibilities**:
- Technical implementation under PM task assignment and architect guidance
- Code quality monitoring with QA coordination through PM hub
- Technology assessment within PM-defined project scope
- Performance optimization aligned with PM quality requirements

**Specialized Capabilities**:
- Implementation execution with automated code quality monitoring
- Technology assessment within architect-defined constraints
- Performance optimization aligned with system requirements
- Code delivery coordination through PM validation pipeline

### Quinn (QA Engineer) - Quality Validation Specialist

**PM-Coordinated Responsibilities**:
- Quality validation orchestrated through PM quality gate requirements
- Testing execution based on PM-defined acceptance criteria
- Performance monitoring aligned with PM quality standards
- Quality metrics reporting to PM for cross-agent coordination

**Specialized Capabilities**:
- Quality validation with predictive analysis and risk-based testing
- Testing automation with comprehensive coverage and intelligent test generation
- Performance validation with real-time monitoring and SLA compliance
- Quality metrics delivery to PM coordination hub

### Sally (UX Designer) - User Experience Specialist

**PM-Coordinated Responsibilities**:
- User experience design with PM feedback loops and validation
- Design system consistency within PM-defined quality standards
- Accessibility compliance aligned with PM quality requirements
- User experience metrics delivery to PM for optimization decisions

**Specialized Capabilities**:
- User experience design with behavior prediction and optimization
- Design system consistency with component evolution tracking
- Accessibility engineering with comprehensive compliance validation
- Conversion optimization through data-driven experience improvements

### Alex (System Architect) - Infrastructure Authority

**Co-Authority Responsibilities** (with PM oversight):
- Technical architecture design and infrastructure planning
- System scalability and performance optimization coordination
- Security architecture and compliance validation
- Infrastructure resource allocation with PM coordination

**Specialized Capabilities**:
- Infrastructure intelligence with auto-scaling and cost optimization
- Deployment automation with comprehensive CI/CD and monitoring
- Security engineering with threat detection and compliance validation
- Performance orchestration with predictive scaling and optimization

### Product Owner (PO) - Backlog Management Specialist

**PM-Coordinated Responsibilities**:
- Backlog prioritization under PM coordination and strategic alignment
- Stakeholder requirements translation within PM-defined scope
- Feature specification development with PM validation
- Acceptance criteria definition aligned with PM quality standards

### Scrum Master (SM) - Process Facilitation Specialist

**PM-Coordinated Responsibilities**:
- Agile process facilitation with PM oversight and coordination
- Team coordination and velocity optimization within PM framework
- Impediment removal and escalation to PM for resource decisions
- Process improvement recommendations to PM for implementation

### BMAD Orchestrator - Meta-Orchestration Specialist

**PM-Integrated Capabilities**:
- Meta-orchestration patterns from `.bmad-core` integrated with PM hub
- Cross-agent workflow coordination within PM authority structure
- Advanced automation capabilities coordinated through PM control
- Process optimization recommendations delivered to PM for approval

### BMAD Master - AI System Enhancement Specialist

**PM-Coordinated Responsibilities**:
- AI system coordination and optimization under PM oversight
- Learning pattern aggregation across agents with PM knowledge control
- System performance enhancement within PM-defined parameters
- Capability evolution recommendations delivered to PM for evaluation

## PM-Centric Architecture Principles

### Orchestration Authority
- **PM Central Hub**: John coordinates all agent activities and context distribution
- **Selective Context Sharing**: PM determines which agents receive what information
- **Task Assignment Control**: PM matches agent capabilities to task requirements
- **Quality Gate Coordination**: PM orchestrates validation across all agents

### Size Compliance Framework
- **File Size Limit**: 100-300 lines maximum per agent implementation
- **Single Responsibility**: Each agent focuses on specific domain expertise
- **PM Coordination**: All agents coordinate through PM hub, not direct communication

### Command Simulation Integration
- **API Interceptor**: Preserve `.bmad-core` through command simulation layer
- **Database Context**: JSON protocol for persistent agent communication
- **Learning Storage**: Vector embeddings for agent knowledge persistence
- **Non-Invasive Design**: Complete preservation of existing infrastructure

## Agent Implementation Standards

### Code Structure
```
agent_name/
├── core.py              # Core agent logic (100-200 lines)
├── pm_integration.py    # PM coordination interface (50-100 lines)
├── capabilities.py      # Domain-specific capabilities (50-100 lines)
└── context_handler.py   # Context processing and storage (50-100 lines)
```

### PM Integration Requirements
- **PM Coordination Interface**: Standardized communication with PM hub
- **Context Reception**: Ability to receive and process PM-distributed context
- **Task Execution**: Execute assignments within PM-defined parameters
- **Results Delivery**: Report outcomes to PM for quality validation and next steps

### Command Simulation Integration
- **BMAD Core Preservation**: Command simulation layer for `.bmad-core` compatibility
- **Database Context**: JSON protocol for agent communication and learning storage
- **External Services**: Real integration through command simulation layer
- **Learning Persistence**: Vector embeddings for contextual knowledge retention

### Performance Standards
- **Response Time**: Sub-second response for standard operations
- **Reliability**: 99.9% uptime for production agent operations
- **Scalability**: Support for concurrent multi-agent workflows
- **Monitoring**: Real-time performance metrics and alerting

## Human-AI Collaboration Framework

### Arun (Human) Strategic Authority
- **Vision Definition**: Strategic guidance and market direction setting
- **Quality Gate Approval**: Final approval on PM-coordinated quality validations
- **Scope Authorization**: Authorization for major changes and resource allocation
- **Strategic Decision Points**: High-level decisions on direction and priorities

### PM-Human Coordination
- **Task Evaluation**: PM evaluates Arun's tasks for impact and feasibility
- **Quality Coordination**: PM orchestrates validation before presenting to Arun
- **Resource Recommendations**: PM provides resource and timeline assessments
- **Strategic Implementation**: PM translates Arun's vision into agent coordination

### Escalation Protocols
- **PM-Managed Escalation**: PM determines when to escalate decisions to Arun
- **Complexity Threshold**: Automatic escalation for decisions beyond agent capabilities
- **Strategic Impact**: PM escalates decisions with significant strategic implications
- **Quality Gate Failures**: PM escalates quality issues requiring strategic decisions

### Transparency Requirements
- **Decision Audit**: Complete traceability of all agent decisions and rationale
- **Human Visibility**: Real-time visibility into agent activities and status
- **Explainable AI**: Clear explanations for all agent recommendations and actions
- **Override Capability**: Human ability to modify or reverse any agent action

---

*This agent framework enables autonomous world-class product development while preserving strategic human control and ensuring quality at every stage of the product lifecycle.*