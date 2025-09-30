# BMAD Auto Deployment Guide

## Overview

This guide provides PM-centric deployment instructions for BMAD Auto with 10-agent orchestration, command simulation infrastructure, and AG UI human collaboration. All deployments preserve `.bmad-core` integrity while enabling autonomous product orchestration through John (PM) coordination hub.

## Infrastructure Requirements

### PM-Centric Service Architecture Requirements

#### Service-Specific Hardware Requirements
```yaml
production_infrastructure:
  pm_integration_hub:
    cpu_cores: 4
    memory: 16GB
    storage: 200GB SSD
    network: 1Gbps
    description: "Central PM coordination with command logging"

  agent_orchestration_cluster:
    cpu_cores: 12
    memory: 48GB
    storage: 500GB SSD
    network: 1Gbps
    description: "10-agent ecosystem with database context communication"

  command_simulation_layer:
    cpu_cores: 2
    memory: 8GB
    storage: 100GB SSD
    network: 1Gbps
    description: "Command interception and .bmad-core preservation"

  ag_ui_collaboration:
    cpu_cores: 2
    memory: 8GB
    storage: 50GB SSD
    network: 1Gbps
    description: "Human-AI collaboration interface"

  database_context_storage:
    cpu_cores: 4
    memory: 16GB
    storage: 1TB NVMe SSD
    network: 1Gbps
    description: "PM context distribution and agent learning vectors"
```

#### Cloud Provider Configurations

**AWS PM-Centric Deployment**:
```yaml
aws_infrastructure:
  pm_integration_hub:
    instance_type: "m5.xlarge"  # 4 vCPU, 16GB RAM
    auto_scaling_group:
      min_size: 2
      max_size: 4
      desired_capacity: 2
    placement_group: "pm-coordination-cluster"

  agent_orchestration:
    instance_type: "m5.2xlarge"  # 8 vCPU, 32GB RAM
    auto_scaling_group:
      min_size: 3
      max_size: 6
      desired_capacity: 3
    placement_group: "agent-cluster"

  database_storage:
    pm_context_db:
      engine: "RDS PostgreSQL 14 with pgvector"
      instance_class: "db.r5.xlarge"
      storage_type: "gp3"
      allocated_storage: 1000
    command_simulation_db:
      engine: "RDS PostgreSQL 14"
      instance_class: "db.r5.large"
      storage_type: "gp3"
      allocated_storage: 500

  networking:
    vpc_cidr: "10.0.0.0/16"
    pm_hub_subnets: ["10.0.1.0/24", "10.0.2.0/24"]
    agent_subnets: ["10.0.3.0/24", "10.0.4.0/24"]
    agui_subnets: ["10.0.5.0/24"]
    public_subnets: ["10.0.101.0/24", "10.0.102.0/24"]
```

**Azure Deployment**:
```yaml
azure_infrastructure:
  compute:
    vm_size: "Standard_D8s_v3"  # 8 vCPU, 32GB RAM
    availability_set: true
    vm_count: 3

  storage:
    database: "Azure Database for PostgreSQL"
    pricing_tier: "General Purpose"
    vcore: 8
    storage_gb: 500

  networking:
    vnet_address_space: "10.1.0.0/16"
    subnet_address_prefix: "10.1.1.0/24"
```

**Google Cloud Deployment**:
```yaml
gcp_infrastructure:
  compute:
    machine_type: "n2-standard-8"  # 8 vCPU, 32GB RAM
    instance_group:
      size: 3
      zones: ["us-central1-a", "us-central1-b", "us-central1-c"]

  storage:
    database: "Cloud SQL PostgreSQL"
    tier: "db-standard-8"
    storage_size_gb: 500
    storage_type: "SSD"
```

## Container Deployment

## PM-Centric Service Deployment

### PM Integration Hub Container
```dockerfile
# dockerfile.pm-hub
FROM python:3.11-slim as builder

# Install system dependencies for PM coordination
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install PM-specific dependencies
COPY requirements.pm-hub.txt .
RUN pip install --no-cache-dir -r requirements.pm-hub.txt

# Copy PM coordination code
COPY bmad-auto/coordination/ ./bmad-auto/coordination/
COPY bmad-auto/integration/ ./bmad-auto/integration/
COPY bmad-auto/context_management/ ./bmad-auto/context_management/

# Production stage
FROM python:3.11-slim as production

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create PM user
RUN groupadd -r pmhub && useradd -r -g pmhub pmhub

WORKDIR /app

# Copy from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app

RUN chown -R pmhub:pmhub /app
USER pmhub

# PM Hub health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health/pm-coordination || exit 1

EXPOSE 8001

# Start PM Integration Hub
CMD ["python", "-m", "bmad-auto.coordination.pm_integration_hub"]
```

### Agent Orchestration Container
```dockerfile
# dockerfile.agents
FROM python:3.11-slim as builder

# Install dependencies for 10-agent ecosystem
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install agent dependencies
COPY requirements.agents.txt .
RUN pip install --no-cache-dir -r requirements.agents.txt

# Copy agent code and .bmad-core (preserved)
COPY bmad-auto/agents/ ./bmad-auto/agents/
COPY bmad-auto/orchestration/ ./bmad-auto/orchestration/
COPY .bmad-core/ ./.bmad-core/

# Production stage
FROM python:3.11-slim as production

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create agent user
RUN groupadd -r agents && useradd -r -g agents agents

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app

RUN chown -R agents:agents /app
USER agents

# Agent health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8002/health/agents || exit 1

EXPOSE 8002

# Start Agent Orchestration
CMD ["python", "-m", "bmad-auto.orchestration.agent_coordinator"]
```

### AG UI Collaboration Container
```dockerfile
# dockerfile.agui
FROM node:18-alpine as builder

# Install AG UI dependencies
WORKDIR /app
COPY bmad-auto/agui/package*.json ./
RUN npm ci --only=production

# Copy AG UI source
COPY bmad-auto/agui/ ./

# Build AG UI
RUN npm run build

# Production stage
FROM node:18-alpine as production

# Create agui user
RUN addgroup -g 1001 -S agui && adduser -S agui -u 1001

WORKDIR /app

# Copy built application
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

RUN chown -R agui:agui /app
USER agui

# AG UI health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

EXPOSE 3000

# Start AG UI
CMD ["npm", "start"]
```

### PM-Centric Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  # PM Integration Hub
  pm-hub:
    build:
      context: .
      dockerfile: dockerfile.pm-hub
    ports:
      - "8001:8001"
    environment:
      - PM_CONTEXT_DB_URL=postgresql://pm_user:password@pm-context-db:5432/pm_context
      - COMMAND_LOG_DB_URL=postgresql://cmd_user:password@command-db:5432/command_logs
      - REDIS_URL=redis://redis:6379/0
      - LOG_LEVEL=INFO
      - AG_UI_ENDPOINT=http://ag-ui:3000
    depends_on:
      - pm-context-db
      - command-db
      - redis
    volumes:
      - ./logs/pm-hub:/app/logs
      - ./config/pm-coordination:/app/config
    restart: unless-stopped
    networks:
      - pm-network

  # Agent Orchestration
  agents:
    build:
      context: .
      dockerfile: dockerfile.agents
    ports:
      - "8002:8002"
    environment:
      - PM_HUB_URL=http://pm-hub:8001
      - AGENT_CONTEXT_DB_URL=postgresql://agent_user:password@pm-context-db:5432/pm_context
      - LOG_LEVEL=INFO
    depends_on:
      - pm-hub
      - pm-context-db
    volumes:
      - ./logs/agents:/app/logs
      - ./.bmad-core:/.bmad-core:ro  # Read-only mount to preserve integrity
    restart: unless-stopped
    networks:
      - pm-network

  # AG UI Human Collaboration
  ag-ui:
    build:
      context: .
      dockerfile: dockerfile.agui
    ports:
      - "3000:3000"
    environment:
      - PM_HUB_WS_URL=ws://pm-hub:8001/ws
      - NODE_ENV=production
    depends_on:
      - pm-hub
    volumes:
      - ./logs/ag-ui:/app/logs
    restart: unless-stopped
    networks:
      - pm-network

  # PM Context Database with pgvector
  pm-context-db:
    image: pgvector/pgvector:pg14
    environment:
      - POSTGRES_DB=pm_context
      - POSTGRES_USER=pm_user
      - POSTGRES_PASSWORD=password
    volumes:
      - pm_context_data:/var/lib/postgresql/data
      - ./init/pm-context-schema.sql:/docker-entrypoint-initdb.d/01-pm-context.sql
      - ./init/agent-learning-schema.sql:/docker-entrypoint-initdb.d/02-agent-learning.sql
    ports:
      - "5433:5432"
    restart: unless-stopped
    networks:
      - pm-network

  # Command Simulation Database
  command-db:
    image: postgres:14
    environment:
      - POSTGRES_DB=command_logs
      - POSTGRES_USER=cmd_user
      - POSTGRES_PASSWORD=password
    volumes:
      - command_logs_data:/var/lib/postgresql/data
      - ./init/command-logging-schema.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5434:5432"
    restart: unless-stopped
    networks:
      - pm-network

  # Redis for PM coordination cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - pm-network

  # PM Integration Monitoring
  monitoring:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/pm-prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    restart: unless-stopped
    networks:
      - pm-network

volumes:
  pm_context_data:
  command_logs_data:
  redis_data:
  prometheus_data:

networks:
  pm-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### PM-Centric Kubernetes Deployment

#### Namespace and ConfigMaps
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: bmad-auto
  labels:
    name: bmad-auto
    environment: production
    architecture: pm-centric

---
# k8s/pm-hub-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: pm-hub-config
  namespace: bmad-auto
data:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
  PM_BATCH_INTERVAL: "300"
  COMMAND_LOG_RETENTION: "30"
  EXTERNAL_API_TIMEOUT: "60"
  AGENT_COORDINATION_TIMEOUT: "120"

---
# k8s/agents-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: agents-config
  namespace: bmad-auto
data:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
  AGENT_COUNT: "10"
  CONTEXT_SYNC_INTERVAL: "60"
  LEARNING_STORAGE_ENABLED: "true"

---
# k8s/agui-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: agui-config
  namespace: bmad-auto
data:
  NODE_ENV: "production"
  WEBSOCKET_TIMEOUT: "30000"
  COLLABORATION_MODE: "real_time"
  APPROVAL_TIMEOUT: "300"
```

#### PM-Centric Service Deployments
```yaml
# k8s/pm-hub-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pm-hub
  namespace: bmad-auto
  labels:
    app: pm-hub
    component: coordination
    version: v1.0.0
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: pm-hub
  template:
    metadata:
      labels:
        app: pm-hub
        component: coordination
        version: v1.0.0
    spec:
      serviceAccountName: pm-hub-sa
      containers:
      - name: pm-hub
        image: bmadauto/pm-hub:v1.0.0
        ports:
        - containerPort: 8001
          name: http
        - containerPort: 8091
          name: metrics
        env:
        - name: PM_CONTEXT_DB_URL
          valueFrom:
            secretKeyRef:
              name: bmad-auto-secrets
              key: pm-context-db-url
        - name: COMMAND_LOG_DB_URL
          valueFrom:
            secretKeyRef:
              name: bmad-auto-secrets
              key: command-log-db-url
        - name: LINEAR_API_KEY
          valueFrom:
            secretKeyRef:
              name: external-apis
              key: linear-api-key
        envFrom:
        - configMapRef:
            name: pm-hub-config
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health/pm-coordination
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        volumeMounts:
        - name: logs
          mountPath: /app/logs
        - name: command-logs
          mountPath: /app/command-logs
      volumes:
      - name: logs
        emptyDir: {}
      - name: command-logs
        persistentVolumeClaim:
          claimName: command-logs-pvc

---
# k8s/agents-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agents
  namespace: bmad-auto
  labels:
    app: agents
    component: orchestration
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: agents
  template:
    metadata:
      labels:
        app: agents
        component: orchestration
        version: v1.0.0
    spec:
      serviceAccountName: agents-sa
      containers:
      - name: agents
        image: bmadauto/agents:v1.0.0
        ports:
        - containerPort: 8002
          name: http
        - containerPort: 8092
          name: metrics
        env:
        - name: PM_HUB_URL
          value: "http://pm-hub-service:8001"
        - name: AGENT_CONTEXT_DB_URL
          valueFrom:
            secretKeyRef:
              name: bmad-auto-secrets
              key: pm-context-db-url
        envFrom:
        - configMapRef:
            name: agents-config
        resources:
          requests:
            memory: "3Gi"
            cpu: "1500m"
          limits:
            memory: "6Gi"
            cpu: "3000m"
        livenessProbe:
          httpGet:
            path: /health/agents
            port: http
          initialDelaySeconds: 45
          periodSeconds: 15
          timeoutSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 15
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        volumeMounts:
        - name: logs
          mountPath: /app/logs
        - name: bmad-core
          mountPath: /.bmad-core
          readOnly: true
        - name: agent-learning
          mountPath: /app/learning
      volumes:
      - name: logs
        emptyDir: {}
      - name: bmad-core
        configMap:
          name: bmad-core-config
      - name: agent-learning
        persistentVolumeClaim:
          claimName: agent-learning-pvc

---
# k8s/agui-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ag-ui
  namespace: bmad-auto
  labels:
    app: ag-ui
    component: collaboration
    version: v1.0.0
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  selector:
    matchLabels:
      app: ag-ui
  template:
    metadata:
      labels:
        app: ag-ui
        component: collaboration
        version: v1.0.0
    spec:
      serviceAccountName: agui-sa
      containers:
      - name: ag-ui
        image: bmadauto/ag-ui:v1.0.0
        ports:
        - containerPort: 3000
          name: http
        env:
        - name: PM_HUB_WS_URL
          value: "ws://pm-hub-service:8001/ws"
        envFrom:
        - configMapRef:
            name: agui-config
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
```

#### Service and Ingress
```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: bmad-auto-service
  namespace: bmad-auto
  labels:
    app: bmad-auto
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
    name: http
  selector:
    app: bmad-auto

---
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: bmad-auto-ingress
  namespace: bmad-auto
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - bmad-auto.yourdomain.com
    secretName: bmad-auto-tls
  rules:
  - host: bmad-auto.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: bmad-auto-service
            port:
              number: 80
```

## Database Setup and Migration

## PM-Centric Database Setup

### PM Context Database with Vector Storage
```sql
-- init/pm-context-schema.sql
-- Create PM context database with pgvector support
CREATE DATABASE pm_context;
CREATE USER pm_user WITH ENCRYPTED PASSWORD 'secure_pm_password';
GRANT ALL PRIVILEGES ON DATABASE pm_context TO pm_user;

-- Connect to pm_context database
\c pm_context;

-- Create extensions for PM coordination
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";
CREATE EXTENSION IF NOT EXISTS "vector";  -- pgvector for agent learning

-- PM Context Distribution Tables
CREATE TABLE pm_agent_contexts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(50) NOT NULL,
    context_type VARCHAR(50) NOT NULL,
    context_data JSONB NOT NULL,
    context_vector vector(1536),  -- OpenAI embedding dimension
    created_by VARCHAR(50) DEFAULT 'john_pm',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    INDEX btree_gin_index ON context_data USING gin
);

-- PM Task Coordination
CREATE TABLE pm_task_coordination (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id VARCHAR(100) NOT NULL,
    coordinating_agent VARCHAR(50) DEFAULT 'john_pm',
    assigned_agents TEXT[],
    task_status VARCHAR(50) NOT NULL,
    task_boundaries JSONB,
    coordination_history JSONB[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Agent Learning Storage with Vector Search
CREATE TABLE agent_learning_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(50) NOT NULL,
    context_vector vector(1536),
    decision_made TEXT NOT NULL,
    outcome_success BOOLEAN,
    confidence_score FLOAT,
    similar_contexts TEXT[],
    learning_metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- PM Quality Gate Results
CREATE TABLE pm_quality_gates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id VARCHAR(100) NOT NULL,
    validation_agents TEXT[],
    quality_results JSONB,
    pm_decision VARCHAR(50),
    human_approval_required BOOLEAN DEFAULT FALSE,
    approved_by VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Grant permissions
GRANT ALL ON SCHEMA public TO pm_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pm_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO pm_user;

-- Vector similarity search index
CREATE INDEX agent_context_vector_idx ON pm_agent_contexts USING ivfflat (context_vector vector_cosine_ops);
CREATE INDEX learning_vector_idx ON agent_learning_entries USING ivfflat (context_vector vector_cosine_ops);
```

### Command Simulation Database
```sql
-- init/command-logging-schema.sql
-- Create command simulation database
CREATE DATABASE command_logs;
CREATE USER cmd_user WITH ENCRYPTED PASSWORD 'secure_cmd_password';
GRANT ALL PRIVILEGES ON DATABASE command_logs TO cmd_user;

\c command_logs;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- PM External Command Logs
CREATE TABLE pm_external_commands (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coordinator VARCHAR(50) DEFAULT 'john_pm',
    service VARCHAR(50) NOT NULL,
    action VARCHAR(100) NOT NULL,
    rationale TEXT,
    executing_agent VARCHAR(50),
    command_data JSONB,
    execution_result JSONB,
    success BOOLEAN,
    execution_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Integration Method Tracking
CREATE TABLE integration_method_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service VARCHAR(50) NOT NULL,
    method VARCHAR(50) NOT NULL,  -- 'mcp', 'direct_api', 'command_simulation'
    success_rate FLOAT,
    average_response_time_ms INTEGER,
    last_used TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Human Collaboration Logs via AG UI
CREATE TABLE human_collaboration_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    interaction_type VARCHAR(50) NOT NULL,
    pm_analysis JSONB,
    human_response JSONB,
    integration_result JSONB,
    collaboration_method VARCHAR(50) DEFAULT 'ag_ui',
    response_time_seconds INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Grant permissions
GRANT ALL ON SCHEMA public TO cmd_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cmd_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO cmd_user;

-- Performance optimizations for PM coordination
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET max_connections = 300;
ALTER SYSTEM SET shared_buffers = '512MB';
ALTER SYSTEM SET effective_cache_size = '2GB';
ALTER SYSTEM SET work_mem = '8MB';
ALTER SYSTEM SET maintenance_work_mem = '128MB';
```

### Alembic Migration Setup
```python
# alembic/env.py
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.base import Base
from src.utils.config import get_settings

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    settings = get_settings()
    return settings.database_url

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## Deployment Scripts and Automation

### CI/CD Pipeline Configuration

#### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy BMAD Auto

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_bmadauto
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt

    - name: Run database migrations
      run: |
        alembic upgrade head
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_bmadauto

    - name: Run tests
      run: |
        pytest tests/ -v --cov=src --cov-report=xml
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_bmadauto
        REDIS_URL: redis://localhost:6379

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - uses: actions/checkout@v4

    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}

    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v')
    environment: production

    steps:
    - uses: actions/checkout@v4

    - name: Deploy to Kubernetes
      uses: azure/k8s-deploy@v1
      with:
        manifests: |
          k8s/namespace.yaml
          k8s/configmap.yaml
          k8s/secrets.yaml
          k8s/deployment.yaml
          k8s/service.yaml
          k8s/ingress.yaml
        images: |
          ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
```

### Deployment Script
```bash
#!/bin/bash
# scripts/deploy.sh

set -euo pipefail

# Configuration
ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}
NAMESPACE="bmad-auto-${ENVIRONMENT}"

echo "🚀 Deploying BMAD Auto to ${ENVIRONMENT} environment"
echo "Version: ${VERSION}"
echo "Namespace: ${NAMESPACE}"

# Verify prerequisites
command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl is required but not installed"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ docker is required but not installed"; exit 1; }

# Check cluster connection
if ! kubectl cluster-info >/dev/null 2>&1; then
    echo "❌ Cannot connect to Kubernetes cluster"
    exit 1
fi

# Create namespace if it doesn't exist
kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

# Apply configuration
echo "📝 Applying configuration..."
kubectl apply -f k8s/configmap.yaml -n "${NAMESPACE}"

# Handle secrets
if kubectl get secret bmad-auto-secrets -n "${NAMESPACE}" >/dev/null 2>&1; then
    echo "🔐 Secrets already exist"
else
    echo "🔐 Creating secrets..."
    kubectl create secret generic bmad-auto-secrets \
        --from-literal=database-url="${DATABASE_URL}" \
        --from-literal=redis-url="${REDIS_URL}" \
        --from-literal=openai-api-key="${OPENAI_API_KEY}" \
        --from-literal=linear-api-key="${LINEAR_API_KEY}" \
        --from-literal=github-token="${GITHUB_TOKEN}" \
        -n "${NAMESPACE}"
fi

# Update deployment with new image
echo "🔄 Updating deployment..."
kubectl set image deployment/bmad-auto bmad-auto="ghcr.io/your-org/bmad-auto:${VERSION}" -n "${NAMESPACE}"

# Wait for rollout
echo "⏳ Waiting for rollout to complete..."
kubectl rollout status deployment/bmad-auto -n "${NAMESPACE}" --timeout=300s

# Verify deployment
echo "✅ Verifying deployment..."
kubectl get pods -n "${NAMESPACE}" -l app=bmad-auto

# Run health check
echo "🏥 Running health check..."
if kubectl wait --for=condition=ready pod -l app=bmad-auto -n "${NAMESPACE}" --timeout=120s; then
    echo "✅ Deployment successful!"

    # Get service URL
    SERVICE_URL=$(kubectl get ingress bmad-auto-ingress -n "${NAMESPACE}" -o jsonpath='{.spec.rules[0].host}')
    echo "🌐 Service available at: https://${SERVICE_URL}"
else
    echo "❌ Deployment failed - pods not ready"
    kubectl logs -l app=bmad-auto -n "${NAMESPACE}" --tail=50
    exit 1
fi

echo "🎉 Deployment completed successfully!"
```

## Environment Configuration

## PM-Centric Environment Configuration

### PM Hub Environment Variables
```bash
# .env.pm-hub
# PM Coordination Service
SERVICE_TYPE=pm_integration_hub
ENVIRONMENT=production
LOG_LEVEL=INFO
PM_BATCH_INTERVAL=300
COMMAND_LOG_RETENTION_DAYS=30

# PM Database Connections
PM_CONTEXT_DB_URL=postgresql://pm_user:secure_pm_password@pm-context-db:5432/pm_context
COMMAND_LOG_DB_URL=postgresql://cmd_user:secure_cmd_password@command-db:5432/command_logs
DATABASE_POOL_SIZE=30
DATABASE_MAX_OVERFLOW=50

# PM Coordination Cache
REDIS_URL=redis://redis:6379/0
REDIS_MAX_CONNECTIONS=25
CONTEXT_CACHE_TTL=3600

# External Service Coordination (PM-Managed)
LINEAR_API_KEY=your-linear-api-key
LINEAR_MCP_ENDPOINT=http://linear-mcp:8080
GITHUB_TOKEN=ghp_your-github-token
AG_UI_ENDPOINT=http://ag-ui:3000
AG_UI_WS_ENDPOINT=ws://ag-ui:3000/ws

# PM AI Service Coordination
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
AI_COST_TRACKING_ENABLED=true
AI_REQUEST_TIMEOUT=60

# PM Security
PM_HUB_SECRET_KEY=your-pm-hub-secret-minimum-32-chars
COMMAND_ENCRYPTION_KEY=your-command-encryption-key
EXTERNAL_API_RATE_LIMIT=100

# PM Monitoring
PM_METRICS_ENABLED=true
PM_METRICS_PORT=8091
COMMAND_LOG_METRICS=true
INTEGRATION_HEALTH_CHECK_INTERVAL=60
```

### Agent Orchestration Environment Variables
```bash
# .env.agents
# Agent Orchestration Service
SERVICE_TYPE=agent_orchestration
ENVIRONMENT=production
LOG_LEVEL=INFO
AGENT_COUNT=10
CONTEXT_SYNC_INTERVAL=60

# Agent Database Context
PM_HUB_URL=http://pm-hub:8001
AGENT_CONTEXT_DB_URL=postgresql://pm_user:secure_pm_password@pm-context-db:5432/pm_context
LEARNING_STORAGE_ENABLED=true
CONTEXT_VECTOR_DIMENSION=1536

# Agent Independence Boundaries
AGENT_AUTONOMY_LEVEL=high_within_pm_boundaries
QUALITY_GATE_THRESHOLD=0.8
PM_ESCALATION_THRESHOLD=0.9
AGENT_DECISION_TIMEOUT=120

# 10-Agent Ecosystem Configuration
MARY_ENABLED=true
JOHN_ENABLED=true  # PM Agent
JAMES_ENABLED=true
QUINN_ENABLED=true
SALLY_ENABLED=true
ALEX_ENABLED=true
PO_ENABLED=true
SM_ENABLED=true
BMAD_ORCHESTRATOR_ENABLED=true
BMAD_MASTER_ENABLED=true

# Agent Learning Configuration
LEARNING_VECTOR_STORAGE=postgresql
SEMANTIC_SEARCH_ENABLED=true
LEARNING_BATCH_SIZE=100
CONTEXT_SIMILARITY_THRESHOLD=0.85

# .bmad-core Preservation
BMAD_CORE_PATH=/.bmad-core
BMAD_CORE_READ_ONLY=true
COMMAND_SIMULATION_ENABLED=true
CORE_INTEGRITY_CHECK=true
```

### AG UI Environment Variables
```bash
# .env.ag-ui
# AG UI Human Collaboration Service
SERVICE_TYPE=ag_ui_collaboration
NODE_ENV=production
PORT=3000

# PM Hub Integration
PM_HUB_HTTP_URL=http://pm-hub:8001
PM_HUB_WS_URL=ws://pm-hub:8001/ws
WEBSOCKET_TIMEOUT=30000
RECONNECTION_ATTEMPTS=5

# Human Collaboration Configuration
COLLABORATION_MODE=real_time
APPROVAL_TIMEOUT_SECONDS=300
DISCUSSION_TIMEOUT_SECONDS=600
AUTO_ESCALATION_ENABLED=true

# AG UI Features
REAL_TIME_MONITORING=true
AGENT_OBSERVABILITY=true
PM_DASHBOARD=true
HUMAN_OVERRIDE_ENABLED=true

# Security
AG_UI_SECRET_KEY=your-agui-secret-key
CSRF_PROTECTION=true
CORS_ORIGINS=https://yourdomain.com

# Monitoring
AG_UI_METRICS_ENABLED=true
COLLABORATION_ANALYTICS=true
USER_INTERACTION_TRACKING=true
```

## PM-Centric Health Check Implementation

### PM Hub Health Checks
```python
# bmad-auto/coordination/health_checks.py
from fastapi import APIRouter, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
import asyncio
import time
from typing import Dict, Any
from .pm_integration_hub import PMIntegrationHub
from .command_logging_service import CommandLoggingService

router = APIRouter(prefix="/health", tags=["pm-health"])

@router.get("/pm-coordination")
async def pm_coordination_health():
    """PM Integration Hub coordination health check"""
    return {
        "service": "pm_integration_hub",
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "coordinator": "john_pm",
        "environment": "production"
    }

@router.get("/ready")
async def pm_readiness_check(response: Response):
    """Comprehensive PM hub readiness check"""
    checks = {}
    overall_healthy = True

    # PM Context Database check
    try:
        async with get_pm_context_session() as session:
            await session.execute("SELECT 1 FROM pm_agent_contexts LIMIT 1")
        checks["pm_context_db"] = {"status": "healthy", "response_time": 0.1}
    except Exception as e:
        checks["pm_context_db"] = {"status": "unhealthy", "error": str(e)}
        overall_healthy = False

    # Command Logging Database check
    try:
        async with get_command_log_session() as session:
            await session.execute("SELECT 1 FROM pm_external_commands LIMIT 1")
        checks["command_log_db"] = {"status": "healthy", "response_time": 0.1}
    except Exception as e:
        checks["command_log_db"] = {"status": "unhealthy", "error": str(e)}
        overall_healthy = False

    # Redis PM coordination cache check
    try:
        redis = Redis.from_url("redis://redis:6379/0")
        await redis.ping()
        await redis.close()
        checks["pm_cache"] = {"status": "healthy", "response_time": 0.05}
    except Exception as e:
        checks["pm_cache"] = {"status": "unhealthy", "error": str(e)}
        overall_healthy = False

    # PM External Integration Health
    checks["pm_integrations"] = await check_pm_external_integrations()
    if checks["pm_integrations"]["status"] != "healthy":
        overall_healthy = False

    # AG UI Collaboration Health
    checks["ag_ui_collaboration"] = await check_agui_health()
    if checks["ag_ui_collaboration"]["status"] != "healthy":
        overall_healthy = False

    # Command Simulation Health
    checks["command_simulation"] = await check_command_simulation_health()
    if checks["command_simulation"]["status"] != "healthy":
        overall_healthy = False

    if not overall_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "service": "pm_integration_hub",
        "status": "healthy" if overall_healthy else "unhealthy",
        "checks": checks,
        "timestamp": time.time()
    }

async def check_pm_external_integrations() -> Dict[str, Any]:
    """Check PM-coordinated external service connectivity"""
    services = {}

    # Check Linear integration (MCP preferred, API fallback)
    try:
        pm_hub = PMIntegrationHub()
        linear_health = await pm_hub.check_linear_integration_health()
        services["linear"] = {
            "status": "healthy" if linear_health.success else "unhealthy",
            "method": linear_health.integration_method,
            "response_time": linear_health.response_time
        }
    except Exception as e:
        services["linear"] = {"status": "unhealthy", "error": str(e)}

    # Check GitHub coordination
    try:
        github_health = await pm_hub.check_github_coordination_health()
        services["github"] = {
            "status": "healthy" if github_health.success else "unhealthy",
            "response_time": github_health.response_time
        }
    except Exception as e:
        services["github"] = {"status": "unhealthy", "error": str(e)}

    # Check AI Service coordination
    try:
        ai_health = await pm_hub.check_ai_service_coordination_health()
        services["ai_services"] = {
            "status": "healthy" if ai_health.success else "unhealthy",
            "active_providers": ai_health.active_providers,
            "cost_tracking": ai_health.cost_tracking_enabled
        }
    except Exception as e:
        services["ai_services"] = {"status": "unhealthy", "error": str(e)}

    overall_status = "healthy" if all(
        service["status"] == "healthy" for service in services.values()
    ) else "unhealthy"

    return {"status": overall_status, "services": services}

async def check_agui_health() -> Dict[str, Any]:
    """Check AG UI collaboration interface health"""
    try:
        # Test WebSocket connection to AG UI
        agui_response = await test_agui_websocket_connection()
        return {
            "status": "healthy" if agui_response.connected else "unhealthy",
            "websocket_latency": agui_response.latency,
            "collaboration_ready": agui_response.collaboration_ready
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

async def check_command_simulation_health() -> Dict[str, Any]:
    """Check command simulation and .bmad-core preservation"""
    try:
        # Check .bmad-core integrity
        bmad_core_integrity = await check_bmad_core_integrity()

        # Check command logging service
        cmd_logger = CommandLoggingService()
        log_health = await cmd_logger.health_check()

        return {
            "status": "healthy" if bmad_core_integrity and log_health else "unhealthy",
            "bmad_core_integrity": bmad_core_integrity,
            "command_logging": log_health,
            "simulation_active": True
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

### Agent Orchestration Health Checks
```python
# bmad-auto/orchestration/agent_health.py
@router.get("/agents")
async def agents_health_check():
    """10-agent ecosystem health check"""
    agent_status = {}

    # Check all 10 agents
    agents = ["mary", "john", "james", "quinn", "sally", "alex", "po", "sm", "bmad_orchestrator", "bmad_master"]

    for agent_id in agents:
        try:
            agent_health = await check_agent_health(agent_id)
            agent_status[agent_id] = {
                "status": "healthy" if agent_health.responsive else "unhealthy",
                "pm_connection": agent_health.pm_connection_active,
                "context_sync_time": agent_health.last_context_sync,
                "learning_storage": agent_health.learning_storage_active
            }
        except Exception as e:
            agent_status[agent_id] = {"status": "unhealthy", "error": str(e)}

    overall_healthy = all(agent["status"] == "healthy" for agent in agent_status.values())

    return {
        "service": "agent_orchestration",
        "status": "healthy" if overall_healthy else "unhealthy",
        "agent_count": len(agents),
        "healthy_agents": sum(1 for agent in agent_status.values() if agent["status"] == "healthy"),
        "agents": agent_status,
        "timestamp": time.time()
    }
```

## PM-Centric Deployment Commands

### Quick PM-Centric Deployment
```bash
#!/bin/bash
# scripts/deploy-pm-centric.sh

set -euo pipefail

ENVIRONMENT=${1:-production}
echo "🚀 Deploying PM-Centric BMAD Auto to ${ENVIRONMENT}"

# Deploy PM Hub first (central coordinator)
echo "📊 Deploying PM Integration Hub..."
kubectl apply -f k8s/pm-hub-deployment.yaml
kubectl rollout status deployment/pm-hub -n bmad-auto --timeout=300s

# Deploy Databases
echo "🗄️ Deploying PM Context and Command Databases..."
kubectl apply -f k8s/pm-context-db.yaml
kubectl apply -f k8s/command-db.yaml

# Deploy Agent Orchestration
echo "🤖 Deploying 10-Agent Orchestration..."
kubectl apply -f k8s/agents-deployment.yaml
kubectl rollout status deployment/agents -n bmad-auto --timeout=300s

# Deploy AG UI
echo "👥 Deploying AG UI Human Collaboration..."
kubectl apply -f k8s/agui-deployment.yaml
kubectl rollout status deployment/ag-ui -n bmad-auto --timeout=300s

# Verify PM coordination
echo "✅ Verifying PM coordination health..."
PM_HUB_URL=$(kubectl get service pm-hub-service -n bmad-auto -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl -f "http://${PM_HUB_URL}/health/pm-coordination" || {
    echo "❌ PM Hub health check failed"
    exit 1
}

echo "🎉 PM-Centric BMAD Auto deployment completed successfully!"
echo "📊 PM Hub: http://${PM_HUB_URL}"
echo "👥 AG UI: http://$(kubectl get service ag-ui-service -n bmad-auto -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')"
```

---

*This PM-centric deployment guide provides comprehensive instructions for deploying BMAD Auto with John (PM) coordination hub, 10-agent orchestration, command simulation infrastructure, and AG UI human collaboration while preserving `.bmad-core` integrity.*