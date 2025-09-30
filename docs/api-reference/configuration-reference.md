# BMAD Auto Configuration Reference

## Overview

This reference provides comprehensive documentation for PM-centric BMAD Auto configuration, including PM coordination hub settings, 10-agent ecosystem parameters, command simulation configuration, database context management, AG UI integration, and external service coordination through MCP protocols.

## Environment Configuration

### PM Coordination Hub Settings

```bash
# PM Hub Core Configuration
PM_HUB_ENABLED=true                     # Enable PM-centric coordination
PM_COORDINATOR_ID=john                  # Primary PM coordinator agent
PM_HUB_HOST=0.0.0.0                    # PM hub host address
PM_HUB_PORT=8001                       # PM hub coordination port
PM_BATCH_PROCESSING=true                # Enable PM batch processing
PM_BATCH_SIZE=10                        # Agent updates per PM batch
PM_REVIEW_FREQUENCY=daily               # PM review cycle: hourly, daily, weekly

# 10-Agent Ecosystem Configuration
AGENT_ECOSYSTEM_SIZE=10                 # Total agents in ecosystem
AGENT_COORDINATION_TYPE=pm_centric      # Coordination pattern
CROSS_AGENT_COLLABORATION=true          # Enable cross-agent coordination
AGENT_INDEPENDENCE_LEVEL=high_with_boundaries  # Agent autonomy level

# Command Simulation Layer
COMMAND_SIMULATION_ENABLED=true         # Enable .bmad-core command simulation
BMAD_CORE_PRESERVATION=strict           # Preserve .bmad-core infrastructure
COMMAND_INTERCEPTION=active             # Intercept .bmad-core commands
DATABASE_TRANSLATION=enabled            # Translate commands to database ops
COMMAND_HISTORY_LOGGING=true            # Log all command simulations

# Core Application Settings
ENVIRONMENT=production                    # Environment: development, staging, production
DEBUG=false                              # Enable debug mode: true, false
LOG_LEVEL=INFO                          # Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
HOST=0.0.0.0                            # Host address
PORT=8000                               # Application port
WORKERS=4                               # Number of worker processes
MAX_CONNECTIONS=100                     # Maximum concurrent connections

# Application Security
SECRET_KEY=your-super-secret-key-min-32-chars  # Application secret key (min 32 chars)
JWT_SECRET=your-jwt-secret-key                 # JWT signing secret
JWT_EXPIRATION=86400                           # JWT expiration in seconds (24 hours)
ENCRYPTION_KEY=your-encryption-key             # Data encryption key
API_KEY_SALT=your-api-key-salt                # API key generation salt

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "https://app.bmad-auto.com"]
CORS_METHODS=["GET", "POST", "PUT", "DELETE", "PATCH"]
CORS_ALLOW_CREDENTIALS=true
```

### PM Context Database Configuration

```bash
# PM Context Database (PostgreSQL + pgvector)
PM_CONTEXT_DATABASE_URL=postgresql://pm_user:password@pm_db:5432/pm_context
PM_CONTEXT_POOL_SIZE=20                 # PM context connection pool
PM_CONTEXT_MAX_OVERFLOW=30              # PM context overflow connections
VECTOR_EMBEDDINGS_ENABLED=true          # Enable pgvector for embeddings
VECTOR_DIMENSION=1536                   # Vector embedding dimensions
JSON_PROTOCOL_ENABLED=true              # Enable JSON protocol for agent communication
CONTEXT_DISTRIBUTION_BATCH_SIZE=5       # Context distribution batch size

# Agent Learning Storage
AGENT_LEARNING_DATABASE_URL=postgresql://agent_user:password@agent_db:5432/agent_learning
LEARNING_VECTOR_STORAGE=enabled         # Store agent learning with vectors
SEMANTIC_RETRIEVAL=active               # Enable semantic context retrieval
CONTEXT_RETENTION_DAYS=90               # Context retention period

# Primary Database
DATABASE_URL=postgresql://user:password@host:5432/bmadauto
DATABASE_POOL_SIZE=20                   # Connection pool size
DATABASE_MAX_OVERFLOW=30                # Maximum overflow connections
DATABASE_POOL_TIMEOUT=30                # Pool timeout in seconds
DATABASE_POOL_RECYCLE=3600             # Connection recycle time in seconds
DATABASE_ECHO=false                     # Enable SQL query logging

# Database Performance
DATABASE_STATEMENT_TIMEOUT=30000        # Statement timeout in milliseconds
DATABASE_QUERY_TIMEOUT=10000           # Query timeout in milliseconds
DATABASE_CONNECTION_TIMEOUT=5000       # Connection timeout in milliseconds

# Read Replica (Optional)
DATABASE_READ_URL=postgresql://readonly_user:password@read_host:5432/bmadauto
DATABASE_READ_POOL_SIZE=10
```

### Cache Configuration

```bash
# Redis Configuration
REDIS_URL=redis://host:6379/0          # Redis connection URL
REDIS_PASSWORD=your-redis-password      # Redis password
REDIS_MAX_CONNECTIONS=50               # Maximum Redis connections
REDIS_SOCKET_TIMEOUT=5                 # Socket timeout in seconds
REDIS_SOCKET_CONNECT_TIMEOUT=5         # Connection timeout in seconds
REDIS_HEALTH_CHECK_INTERVAL=30         # Health check interval in seconds

# Cache Settings
CACHE_DEFAULT_TTL=3600                 # Default cache TTL in seconds
CACHE_MAX_SIZE=10000                   # Maximum cache entries
WORKFLOW_CACHE_TTL=1800                # Workflow cache TTL in seconds
AGENT_CACHE_TTL=900                    # Agent cache TTL in seconds
```

### AI Service Configuration

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_ORG_ID=org-your-organization-id
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_DEFAULT_MODEL=gpt-4-turbo
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.7
OPENAI_REQUEST_TIMEOUT=60
OPENAI_MAX_RETRIES=3
OPENAI_RATE_LIMIT_RPM=3000             # Requests per minute

# Anthropic Configuration
ANTHROPIC_API_KEY=your-anthropic-api-key
ANTHROPIC_BASE_URL=https://api.anthropic.com
ANTHROPIC_DEFAULT_MODEL=claude-3-sonnet-20240229
ANTHROPIC_MAX_TOKENS=4000
ANTHROPIC_REQUEST_TIMEOUT=60

# Azure OpenAI Configuration (Optional)
AZURE_OPENAI_API_KEY=your-azure-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4-turbo

# Cost Management
AI_COST_LIMIT_DAILY=100.00             # Daily cost limit in USD
AI_COST_ALERT_THRESHOLD=80.00          # Alert threshold in USD
AI_USAGE_TRACKING=true                 # Enable usage tracking
```

### PM-Coordinated External Integration Configuration

```bash
# AG UI Integration (Human-AI Collaboration)
AGUI_PROTOCOL_ENABLED=true              # Enable AG UI protocol
AGUI_BASE_URL=https://agui.bmad-auto.com
AGUI_WEBSOCKET_URL=wss://agui.bmad-auto.com/ws
AGUI_COLLABORATION_TIMEOUT=3600         # Human collaboration timeout (1 hour)
AGUI_STRATEGIC_APPROVAL_TIMEOUT=86400   # Strategic approval timeout (24 hours)
AGUI_DISCUSSION_ENABLED=true            # Enable back-and-forth discussion
AGUI_PM_INTEGRATION=seamless            # PM integration level

# MCP Protocol Configuration
MCP_PROTOCOL_ENABLED=true               # Enable Model Context Protocol
MCP_SERVICE_DISCOVERY=auto              # MCP service discovery
MCP_FALLBACK_DIRECT_API=true            # Fallback to direct API calls
MCP_LINEAR_AVAILABLE=true               # MCP Linear integration status
MCP_GITHUB_AVAILABLE=true               # MCP GitHub integration status
MCP_TIMEOUT=30                          # MCP operation timeout

# PM-Coordinated Linear Integration
LINEAR_API_KEY=your-linear-api-key
LINEAR_WEBHOOK_SECRET=your-webhook-secret
LINEAR_BASE_URL=https://api.linear.app/graphql
LINEAR_TEAM_ID=your-team-id
LINEAR_PROJECT_PREFIX=BMAD              # Issue identifier prefix
LINEAR_SYNC_INTERVAL=300               # Sync interval in seconds
LINEAR_PM_COORDINATION=enabled          # PM coordination for Linear
LINEAR_MCP_PREFERRED=true               # Prefer MCP over direct API

# PM-Coordinated GitHub Integration
GITHUB_TOKEN=ghp_your-github-token
GITHUB_WEBHOOK_SECRET=your-webhook-secret
GITHUB_REPOSITORY=your-org/your-repo
GITHUB_BASE_BRANCH=main
GITHUB_API_BASE_URL=https://api.github.com
GITHUB_PM_COORDINATION=enabled          # PM coordination for GitHub
GITHUB_MCP_PREFERRED=true               # Prefer MCP over direct API
GITHUB_AGENT_COORDINATION=james,alex    # Coordinating agents for GitHub

# Slack Integration (Optional)
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
SLACK_CHANNEL=#bmad-auto
SLACK_ALERTS_ENABLED=true

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true
EMAIL_FROM=bmad-auto@yourcompany.com
```

## YAML Configuration Files

### PM-Centric Application Configuration

```yaml
# config/production.yaml
application:
  name: "BMAD Auto"
  version: "1.0.0"
  environment: "production"
  architecture_type: "pm_centric_10_agent"

  pm_coordination_hub:
    coordinator: "john"
    coordination_pattern: "hybrid_langgraph_yaml"
    batch_processing: true
    context_distribution: "database_driven"
    command_simulation: "bmad_core_preservation"

  server:
    host: "0.0.0.0"
    port: 8000
    workers: 4
    max_connections: 100
    keep_alive_timeout: 65
    graceful_shutdown_timeout: 30

  pm_hub_service:
    host: "0.0.0.0"
    port: 8001
    coordination_workers: 2
    batch_processing_interval: 300  # 5 minutes
    context_distribution_workers: 3

  agui_service:
    host: "0.0.0.0"
    port: 8002
    collaboration_timeout: 3600
    strategic_approval_timeout: 86400
    websocket_enabled: true

  security:
    cors:
      origins:
        - "https://app.bmad-auto.com"
        - "https://admin.bmad-auto.com"
      methods: ["GET", "POST", "PUT", "DELETE", "PATCH"]
      allow_credentials: true

    rate_limiting:
      requests_per_minute: 60
      burst_size: 10

    authentication:
      jwt_expiration: 86400  # 24 hours
      refresh_token_expiration: 2592000  # 30 days
      max_sessions_per_user: 5

workflow:
  pm_coordination:
    coordinator: "john"
    orchestration_pattern: "pm_centric_with_agent_autonomy"
    batch_review_frequency: "daily"
    context_distribution: "intelligent_filtering"
    quality_orchestration: "cross_agent_validation"

  defaults:
    timeout_minutes: 60
    max_retries: 3
    pm_approval_required: true
    quality_gates_required: true
    human_approval_timeout: 3600  # 1 hour
    command_simulation: true

  phases:
    research:
      pm_assignment: "mary"
      pm_coordination_type: "research_intelligence"
      timeout_minutes: 120
      quality_gates: ["pm_research_review", "research_complete"]
      pm_context_distribution: ["john", "po"]

    ideation:
      pm_coordination_type: "structured_brainstorming"
      timeout_minutes: 90
      quality_gates: ["pm_concept_validation", "concept_validation"]
      required_participants: ["mary", "john", "sally", "po"]
      langgraph_coordination: true

    specification:
      pm_lead: "john"
      pm_coordination_type: "direct_pm_leadership"
      timeout_minutes: 180
      quality_gates: ["pm_prd_approval", "prd_approved", "architecture_review"]
      supporting_agents: ["alex", "sally", "po"]

    development:
      pm_assignment: "james"
      pm_coordination_type: "autonomous_with_reporting"
      timeout_minutes: 480  # 8 hours
      quality_gates: ["pm_dev_review", "dev_complete", "code_review", "testing_complete"]
      collaboration_agents: ["alex", "quinn"]
      pm_oversight: "batch_processing"

    validation:
      pm_coordination_type: "cross_agent_validation"
      pm_orchestrator: "john"
      timeout_minutes: 240  # 4 hours
      quality_gates: ["pm_quality_orchestration", "qa_approved", "ux_approved", "performance_validated"]
      validation_agents: ["quinn", "sally", "alex"]
      agui_integration: true

agents:
  ecosystem_config:
    total_agents: 10
    pm_coordinator: "john"
    coordination_pattern: "pm_centric_hub"
    batch_processing: true
    cross_agent_collaboration: true

  capacity_limits:
    # Core 5 Agents
    mary: 3      # Max concurrent workflows
    john: 8      # PM coordinator higher capacity
    james: 4
    quinn: 3
    sally: 2

    # Infrastructure Agents
    alex: 2      # Architect
    po: 3        # Product Owner
    sm: 2        # Scrum Master

    # BMAD Core Agents
    bmad_orchestrator: 1  # Command simulation coordination
    bmad_master: 1        # BMAD master coordination

  pm_coordination_limits:
    john_coordination_capacity: 15  # Total agents John can coordinate
    batch_processing_limit: 10      # Max updates per PM batch
    context_distribution_limit: 8   # Max agents per context distribution
    simultaneous_reviews: 5         # Max simultaneous PM reviews

  performance_thresholds:
    response_time_max: 5.0     # Maximum response time in seconds
    success_rate_min: 0.95     # Minimum success rate
    quality_score_min: 0.85    # Minimum quality score

  specializations:
    # Core 5 Agents
    mary:
      - "market_research"
      - "competitive_analysis"
      - "user_research"
      - "business_validation"
      pm_coordination_role: "research_intelligence"

    john:
      - "product_strategy"
      - "requirement_analysis"
      - "pm_orchestration"
      - "agent_coordination"
      - "context_distribution"
      - "quality_orchestration"
      pm_coordination_role: "central_coordinator"

    james:
      - "technical_architecture"
      - "code_implementation"
      - "performance_optimization"
      - "security_implementation"
      pm_coordination_role: "autonomous_with_reporting"

    quinn:
      - "quality_assurance"
      - "test_automation"
      - "performance_testing"
      - "compliance_validation"
      - "cross_agent_validation"
      pm_coordination_role: "quality_validator"

    sally:
      - "ux_design"
      - "ui_implementation"
      - "accessibility_compliance"
      - "design_systems"
      - "agui_collaboration"
      pm_coordination_role: "design_coordinator"

    # Infrastructure Agents
    alex:
      - "infrastructure_architecture"
      - "bmad_core_preservation"
      - "system_coordination"
      - "performance_architecture"
      pm_coordination_role: "infrastructure_coordination"

    po:
      - "strategic_alignment"
      - "stakeholder_management"
      - "business_requirements"
      - "product_vision"
      pm_coordination_role: "strategic_coordination"

    sm:
      - "process_facilitation"
      - "workflow_optimization"
      - "impediment_removal"
      - "team_coordination"
      pm_coordination_role: "process_support"

    # BMAD Core Agents
    bmad_orchestrator:
      - "command_simulation"
      - "bmad_core_interception"
      - "database_translation"
      - "infrastructure_preservation"
      pm_coordination_role: "command_simulation_coordinator"

    bmad_master:
      - "master_coordination"
      - "system_oversight"
      - "integration_management"
      - "pm_hub_support"
      pm_coordination_role: "master_coordinator"

monitoring:
  metrics:
    enabled: true
    endpoint: "/metrics"
    port: 9090

  health_checks:
    enabled: true
    interval: 30
    timeout: 10

  logging:
    level: "INFO"
    format: "json"
    structured: true
    correlation_tracking: true

  tracing:
    enabled: true
    service_name: "bmad-auto"
    jaeger_endpoint: "http://jaeger:14268/api/traces"
    sample_rate: 0.1
```

### Quality Gates Configuration

```yaml
# config/quality_gates.yaml
quality_gates:
  research_complete:
    description: "Research phase completion validation"
    criteria:
      market_analysis_confidence: 0.8
      competitive_landscape_coverage: 0.9
      user_persona_validation: 0.85
    timeout_minutes: 30

  concept_validation:
    description: "Concept ideation validation"
    criteria:
      concept_feasibility_score: 0.8
      innovation_potential: 0.75
      business_viability: 0.85
      technical_complexity_assessment: true
    timeout_minutes: 45

  prd_approved:
    description: "Product Requirements Document approval"
    criteria:
      completeness_score: 0.9
      stakeholder_alignment: 0.85
      technical_feasibility: 0.8
      business_case_strength: 0.85
    human_approval_required: true
    approver_roles: ["product_manager", "technical_lead"]
    timeout_minutes: 60

  architecture_review:
    description: "Technical architecture review"
    criteria:
      scalability_score: 0.85
      security_compliance: 0.95
      performance_projections: 0.8
      maintainability_score: 0.85
    human_approval_required: true
    approver_roles: ["senior_architect", "security_engineer"]
    timeout_minutes: 90

  dev_complete:
    description: "Development phase completion"
    criteria:
      code_coverage: 85
      security_scan_passed: true
      performance_benchmarks_met: true
      documentation_completeness: 0.9
    automated_validation: true
    timeout_minutes: 120

  code_review:
    description: "Code review validation"
    criteria:
      peer_review_approvals: 2
      automated_checks_passed: true
      security_review_passed: true
      performance_impact_acceptable: true
    timeout_minutes: 180

  testing_complete:
    description: "Testing phase completion"
    criteria:
      unit_test_coverage: 90
      integration_test_coverage: 80
      e2e_test_coverage: 70
      performance_test_passed: true
      security_test_passed: true
    automated_validation: true
    timeout_minutes: 240

  qa_approved:
    description: "Quality assurance approval"
    criteria:
      functional_testing_passed: true
      regression_testing_passed: true
      performance_testing_passed: true
      accessibility_testing_passed: true
      browser_compatibility_passed: true
    human_approval_required: true
    approver_roles: ["qa_engineer", "test_manager"]
    timeout_minutes: 120

  ux_approved:
    description: "User experience approval"
    criteria:
      design_consistency_score: 0.9
      accessibility_compliance: 0.95
      usability_testing_score: 0.85
      design_system_compliance: 0.9
    human_approval_required: true
    approver_roles: ["ux_designer", "design_lead"]
    timeout_minutes: 90

  performance_validated:
    description: "Performance validation"
    criteria:
      response_time_95th_percentile: 200  # milliseconds
      throughput_target: 1000  # requests per second
      error_rate: 0.01  # 1%
      resource_utilization: 0.8  # 80%
    automated_validation: true
    timeout_minutes: 60

validation_rules:
  thresholds:
    confidence_score_minimum: 0.7
    quality_score_minimum: 0.8
    performance_score_minimum: 0.85

  escalation:
    failure_threshold: 3
    escalation_delay_minutes: 30
    escalation_roles: ["team_lead", "engineering_manager"]

  retry_policy:
    max_retries: 2
    retry_delay_minutes: 15
    exponential_backoff: true
```

### Agent Configuration

```yaml
# config/agents.yaml
# PM-Centric 10-Agent Ecosystem Configuration
agents:
  # PM Coordination Hub
  pm_coordination:
    hub_coordinator: "john"
    coordination_pattern: "pm_centric_orchestration"
    batch_processing: true
    context_distribution: "database_driven"
    command_simulation: "bmad_core_preservation"

  # Core 5 Agents
  mary:
    name: "Mary - Business Analyst"
    type: "business_analyst"
    pm_coordination:
      coordinator: "john"
      coordination_type: "research_intelligence"
      context_access: "market_intelligence"
      reporting_frequency: "milestone_based"
    model_config:
      primary_model: "gpt-4-turbo"
      fallback_model: "gpt-3.5-turbo"
      temperature: 0.7
      max_tokens: 4000

    capabilities:
      market_research:
        proficiency: 0.95
        tools: ["web_search", "competitor_analysis", "survey_tools"]

      user_research:
        proficiency: 0.92
        tools: ["interview_framework", "persona_generator", "journey_mapping"]

      business_analysis:
        proficiency: 0.90
        tools: ["financial_modeling", "roi_calculator", "market_sizing"]

    context_sources:
      - "Business_claude_compile.md"
      - "Product_claude_compile.md"
      - "market_intelligence_db"

    performance_targets:
      response_time_max: 3.0
      quality_score_min: 0.9
      confidence_threshold: 0.8

  john:
    name: "John - Product Manager & PM Coordinator"
    type: "product_manager_coordinator"
    pm_coordination:
      role: "central_coordinator"
      coordination_capacity: 15
      batch_processing_enabled: true
      context_distribution_control: "full"
      quality_orchestration: "cross_agent"
      command_simulation_oversight: true
    model_config:
      primary_model: "gpt-4-turbo"
      temperature: 0.6
      max_tokens: 4000
      coordination_model: "gpt-4-turbo-coordination"

    capabilities:
      product_strategy:
        proficiency: 0.95
        tools: ["roadmap_generator", "stakeholder_mapper", "priority_matrix"]

      requirement_analysis:
        proficiency: 0.93
        tools: ["prd_generator", "user_story_creator", "acceptance_criteria"]

      project_management:
        proficiency: 0.88
        tools: ["sprint_planner", "resource_allocator", "timeline_optimizer"]

    context_sources:
      - "Product_claude_compile.md"
      - "Team_claude_compile.md"
      - "business_requirements_db"

    integrations:
      linear:
        enabled: true
        permissions: ["create", "update", "comment"]
        auto_sync: true

      slack:
        enabled: true
        channels: ["#product", "#engineering"]

  james:
    name: "James - Senior Developer"
    type: "developer"
    pm_coordination:
      coordinator: "john"
      coordination_type: "autonomous_with_reporting"
      collaboration_agents: ["alex", "quinn"]
      reporting_frequency: "decision_based"
      context_access: "technical_implementation"
    model_config:
      primary_model: "gpt-4-turbo"
      code_model: "gpt-4-code"
      temperature: 0.3
      max_tokens: 6000

    capabilities:
      technical_architecture:
        proficiency: 0.95
        tools: ["architecture_generator", "system_designer", "api_designer"]

      code_implementation:
        proficiency: 0.93
        tools: ["code_generator", "refactor_assistant", "debug_analyzer"]
        languages: ["python", "typescript", "javascript", "sql"]
        frameworks: ["fastapi", "react", "nextjs", "sqlalchemy"]

      performance_optimization:
        proficiency: 0.88
        tools: ["profiler", "performance_analyzer", "optimization_recommender"]

    context_sources:
      - "App_claude_compile.md"
      - "Testing_claude_compile.md"
      - "Infrastructure_claude_compile.md"

    integrations:
      github:
        enabled: true
        permissions: ["create_branch", "create_pr", "code_review"]
        auto_commit: false

  quinn:
    name: "Quinn - QA Engineer"
    type: "qa_engineer"
    pm_coordination:
      coordinator: "john"
      coordination_type: "cross_agent_validation"
      validation_scope: "quality_orchestration"
      collaboration_agents: ["james", "alex", "sally"]
    model_config:
      primary_model: "gpt-4-turbo"
      temperature: 0.4
      max_tokens: 4000

    capabilities:
      quality_assurance:
        proficiency: 0.95
        tools: ["test_generator", "quality_checker", "compliance_validator"]

      test_automation:
        proficiency: 0.90
        tools: ["test_framework", "automation_suite", "ci_cd_integration"]

      performance_testing:
        proficiency: 0.85
        tools: ["load_tester", "stress_tester", "benchmark_analyzer"]

    context_sources:
      - "Testing_claude_compile.md"
      - "Compliance_claude_compile.md"

  sally:
    name: "Sally - UX Designer"
    type: "ux_designer"
    pm_coordination:
      coordinator: "john"
      coordination_type: "design_coordination"
      agui_integration: true
      human_collaboration: "enhanced"
      context_access: "design_and_user_experience"
    model_config:
      primary_model: "gpt-4-turbo"
      vision_model: "gpt-4-vision"
      temperature: 0.8
      max_tokens: 4000

  # Infrastructure Agents
  alex:
    name: "Alex - Infrastructure Architect"
    type: "architect"
    pm_coordination:
      coordinator: "john"
      coordination_type: "infrastructure_coordination"
      bmad_core_responsibility: "preservation"
      collaboration_agents: ["james", "bmad_orchestrator"]
    model_config:
      primary_model: "gpt-4-turbo"
      temperature: 0.5
      max_tokens: 4000
    specializations:
      - "infrastructure_architecture"
      - "bmad_core_preservation"
      - "system_coordination"
      - "performance_architecture"

  po:
    name: "PO - Product Owner"
    type: "product_owner"
    pm_coordination:
      coordinator: "john"
      coordination_type: "strategic_coordination"
      strategic_collaboration: true
      context_access: "strategic_and_business"
    model_config:
      primary_model: "gpt-4-turbo"
      temperature: 0.6
      max_tokens: 4000
    specializations:
      - "strategic_alignment"
      - "stakeholder_management"
      - "business_requirements"
      - "product_vision"

  sm:
    name: "SM - Scrum Master"
    type: "scrum_master"
    pm_coordination:
      coordinator: "john"
      coordination_type: "process_support"
      workflow_optimization: true
      impediment_escalation: "john"
    model_config:
      primary_model: "gpt-4-turbo"
      temperature: 0.5
      max_tokens: 4000
    specializations:
      - "process_facilitation"
      - "workflow_optimization"
      - "impediment_removal"
      - "team_coordination"

  # BMAD Core Agents
  bmad_orchestrator:
    name: "BMAD Orchestrator"
    type: "command_simulation_coordinator"
    pm_coordination:
      coordinator: "john"
      coordination_type: "command_simulation_coordinator"
      bmad_core_preservation: "strict"
      command_interception: "active"
    model_config:
      primary_model: "gpt-4-turbo"
      temperature: 0.3
      max_tokens: 4000
    specializations:
      - "command_simulation"
      - "bmad_core_interception"
      - "database_translation"
      - "infrastructure_preservation"

  bmad_master:
    name: "BMAD Master"
    type: "master_coordinator"
    pm_coordination:
      coordinator: "john"
      coordination_type: "master_coordinator"
      system_oversight: "comprehensive"
      pm_hub_support: "integration"
    model_config:
      primary_model: "gpt-4-turbo"
      temperature: 0.4
      max_tokens: 4000
    specializations:
      - "master_coordination"
      - "system_oversight"
      - "integration_management"
      - "pm_hub_support"

    capabilities:
      ux_design:
        proficiency: 0.95
        tools: ["wireframe_generator", "prototype_creator", "user_journey_mapper"]

      ui_implementation:
        proficiency: 0.88
        tools: ["component_generator", "style_guide_creator", "design_system"]

      accessibility_compliance:
        proficiency: 0.92
        tools: ["accessibility_checker", "wcag_validator", "screen_reader_tester"]

    context_sources:
      - "Product_claude_compile.md"
      - "Team_claude_compile.md"
      - "design_system_db"

coordination:
  handoff_protocols:
    research_to_ideation:
      data_transfer: ["market_analysis", "user_personas", "competitive_landscape"]
      validation_required: true

    ideation_to_specification:
      data_transfer: ["selected_concepts", "feasibility_analysis", "innovation_roadmap"]
      approval_required: true

    specification_to_development:
      data_transfer: ["prd_document", "technical_architecture", "implementation_plan"]
      validation_required: true

    development_to_validation:
      data_transfer: ["implemented_features", "test_results", "performance_metrics"]
      quality_gates: ["dev_complete", "code_review", "testing_complete"]

  collaboration_patterns:
    brainstorming_sessions:
      participants: ["mary", "john", "sally"]
      duration_minutes: 60
      facilitation: "structured"

    technical_reviews:
      participants: ["james", "alex", "quinn"]
      duration_minutes: 90
      focus: "architecture_and_implementation"

    quality_reviews:
      participants: ["quinn", "sally", "john"]
      duration_minutes: 45
      focus: "user_experience_and_quality"
```

## Integration Configuration

### PM-Coordinated Integration Settings

```yaml
# config/integrations/pm_coordinated_integrations.yaml

# AG UI Integration (Human-AI Collaboration)
agui_integration:
  protocol: "ag_ui_v1"
  base_url: "https://agui.bmad-auto.com"
  websocket_url: "wss://agui.bmad-auto.com/ws"
  pm_coordination:
    coordinator: "john"
    collaboration_timeout: 3600
    strategic_approval_timeout: 86400
    discussion_enabled: true
    approval_workflows: ["strategic_decision", "quality_gate", "architecture_approval"]
  human_collaboration:
    strategic_decisions: true
    quality_approvals: true
    architecture_reviews: true
    emergency_escalation: true

# MCP Protocol Configuration
mcp_protocol:
  enabled: true
  service_discovery: "auto"
  fallback_strategy: "direct_api"
  timeout: 30
  retries: 3

  services:
    linear:
      mcp_available: true
      fallback_api: "https://api.linear.app/graphql"
      pm_coordination: "john"

    github:
      mcp_available: true
      fallback_api: "https://api.github.com"
      pm_coordination: "john"

    context7:
      mcp_available: true
      library_docs: true
      pm_integration: true

# PM-Coordinated Linear Integration
linear:
  api:
    base_url: "https://api.linear.app/graphql"
    mcp_preferred: true
    timeout: 30
    retries: 3

  pm_coordination:
    coordinator: "john"
    coordination_pattern: "batch_processing"
    agent_assignments: ["john", "po", "sm"]
    sync_strategy: "pm_intelligent_batch"

  workflow_mapping:
    issue_states:
      pending: "Todo"
      in_progress: "In Progress"
      awaiting_approval: "In Review"
      completed: "Done"
      failed: "Blocked"

    labels:
      phase_research: "phase:research"
      phase_development: "phase:development"
      priority_high: "priority:high"
      bmad_auto: "bmad-auto"

  synchronization:
    enabled: true
    interval_seconds: 300
    batch_size: 50
    conflict_resolution: "bmad_wins"

  webhook:
    events:
      - "Issue"
      - "Comment"
      - "IssueLabel"
    verification_required: true
```

# PM-Coordinated GitHub Integration
github:
  api:
    base_url: "https://api.github.com"
    mcp_preferred: true
    timeout: 30
    retries: 3

  pm_coordination:
    coordinator: "john"
    coordination_agents: ["james", "alex"]
    quality_validation: "quinn"
    branch_coordination: "pm_managed"

  repository:
    default_branch: "main"
    branch_prefix: "bmad-auto/"
    pr_title_prefix: "[BMAD Auto PM]"

  bmad_auto_structure:
    folder_structure: "bmad-auto/"
    agent_coordination: "pm_centric"
    command_simulation: "preserved"

# Command Simulation Integration
command_simulation:
  bmad_core_preservation: "strict"
  command_interception: "active"
  database_translation: "enabled"
  pm_coordination_flow: true

  simulation_storage:
    database_url: "postgresql://sim_user:password@sim_db:5432/command_simulation"
    history_retention: 30  # days
    learning_integration: true

# Database Context Integration
database_context:
  pm_context_database:
    url: "postgresql://pm_user:password@pm_db:5432/pm_context"
    pgvector_enabled: true
    json_protocol: true
    vector_dimension: 1536

  context_distribution:
    pm_controlled: true
    intelligent_filtering: true
    semantic_retrieval: true
    batch_processing: true

  workflow_automation:
    create_branches: true
    create_pull_requests: true
    auto_merge: false
    require_reviews: 2

  ci_cd_integration:
    trigger_builds: true
    wait_for_checks: true
    required_checks:
      - "continuous-integration"
      - "security-scan"
      - "quality-check"
```

---

*This PM-centric configuration reference provides comprehensive documentation for all configurable aspects of BMAD Auto's 10-agent ecosystem, including PM coordination hub settings, command simulation configuration, database context management, AG UI integration, and MCP protocol coordination for optimal autonomous product orchestration.*