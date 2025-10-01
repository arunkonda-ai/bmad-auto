# BMAD Auto Installation Guide
**Date**: 2025-10-01
**For**: New workspace setup and development environment
**Status**: Complete installation instructions

---

## 🎯 Quick Installation (5 Minutes)

### Prerequisites Check
```bash
# 1. Verify Python 3.11+ installed
python3 --version
# Expected: Python 3.11.x or higher (you have 3.13.5 ✓)

# 2. Verify Git installed
git --version

# 3. Check PostgreSQL (optional for MVP)
psql --version
# If not installed: brew install postgresql@15
```

### Installation Steps

#### Option A: Standalone Development (Recommended)

```bash
# Navigate to bmad-auto repository
cd /Users/apple/ai-projects/bmad-auto/

# Run installation script
./scripts/install.sh

# This will:
# - Create Python virtual environment (bmad-auto-env/)
# - Install all dependencies from requirements.txt
# - Create .env from .env.example
# - Initialize coordination.db
```

#### Option B: Manual Installation (If script fails)

```bash
cd /Users/apple/ai-projects/bmad-auto/

# 1. Create virtual environment
python3 -m venv bmad-auto-env

# 2. Activate virtual environment
source bmad-auto-env/bin/activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create environment file
cp .env.example .env

# 6. Initialize database
PYTHONPATH=. python3 -c "from intercept.pm_coordinator import PMCoordinator; print('✓ Database initialized')"
```

---

## 📦 What Gets Installed

### Python Dependencies (from requirements.txt)

**Core Orchestration**:
- `langgraph>=0.2.0` - LangGraph workflow orchestration
- `langsmith>=0.1.0` - LangSmith monitoring
- `langchain>=0.2.0` - LangChain framework
- `langchain-core>=0.2.0` - LangChain core

**Database Stack**:
- `psycopg2-binary>=2.9.9` - PostgreSQL driver
- `sqlalchemy==2.0.23` - Database ORM
- `alembic==1.13.0` - Database migrations
- `aiosqlite==0.19.0` - SQLite async support

**API Framework**:
- `fastapi==0.104.1` - FastAPI web framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `pydantic>=2.7.4` - Data validation
- `pydantic-settings>=2.1.0` - Settings management

**HTTP & Integration**:
- `httpx==0.25.2` - Async HTTP client
- `requests==2.31.0` - HTTP client

**Utilities**:
- `python-multipart==0.0.6` - File upload support
- `python-json-logger==2.0.7` - Structured logging
- `PyYAML==6.0.1` - YAML configuration

**Development & Testing**:
- `pytest==7.4.3` - Testing framework
- `pytest-asyncio==0.21.1` - Async test support
- `pytest-cov==4.1.0` - Coverage reporting
- `black==23.11.0` - Code formatter
- `isort==5.12.0` - Import sorting
- `flake8==6.1.0` - Linting

### Directory Structure Created

```
bmad-auto/
├── bmad-auto-env/          # Python virtual environment (NEW)
│   ├── bin/
│   ├── lib/
│   └── pyvenv.cfg
├── .env                    # Environment configuration (NEW)
├── intercept/
│   └── coordination.db     # Initialized SQLite database (NEW)
└── [existing BMAD Auto files]
```

---

## ⚙️ Environment Configuration

### .env File Setup

After installation, edit `.bmad-auto/.env`:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/bmad_auto
COORDINATION_DB_PATH=intercept/coordination.db

# LangGraph/LangSmith Configuration
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_PROJECT=bmad-auto-dev

# Claude Code Integration (Local AI)
CLAUDE_MODEL=claude-sonnet-4-20250514
GLM_MODEL=glm-4.5

# GitHub Integration (for T037)
GITHUB_TOKEN=your_github_token_here

# Linear Integration (for T038 - optional)
LINEAR_API_KEY=your_linear_key_here

# Development Settings
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

### Required Configuration

**Minimal (MVP)**:
- `DATABASE_URL` - PostgreSQL connection (or skip for file-based development)
- `COORDINATION_DB_PATH` - SQLite database path (defaults to intercept/coordination.db)
- `ENVIRONMENT=development`

**Optional (Post-MVP)**:
- `LANGSMITH_API_KEY` - For workflow monitoring
- `GITHUB_TOKEN` - For external integration
- `LINEAR_API_KEY` - For project management

---

## 🔧 PostgreSQL Setup (Optional for MVP)

### Install PostgreSQL

```bash
# macOS
brew install postgresql@15
brew services start postgresql@15

# Verify installation
psql --version
```

### Create BMAD Auto Database

```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE bmad_auto;
CREATE USER bmad_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE bmad_auto TO bmad_user;

# Exit
\q
```

### Initialize Schema

```bash
cd /Users/apple/ai-projects/bmad-auto/

# Activate virtual environment
source bmad-auto-env/bin/activate

# Run database schema
PYTHONPATH=. python3 -c "
from database.connection_manager import get_connection
import asyncio

async def init_db():
    conn = await get_connection()
    print('✓ PostgreSQL connected')

asyncio.run(init_db())
"

# Apply schema from SQL file
psql -U bmad_user -d bmad_auto -f database/postgresql_schema.sql
```

---

## ✅ Verification Steps

### 1. Virtual Environment Active

```bash
# Check if virtual environment is active
which python3
# Expected: /Users/apple/ai-projects/bmad-auto/bmad-auto-env/bin/python3

# Check installed packages
pip list | grep langgraph
# Expected: langgraph 0.2.x
```

### 2. Import Core Modules

```bash
cd /Users/apple/ai-projects/bmad-auto/

# Activate environment
source bmad-auto-env/bin/activate

# Test imports
PYTHONPATH=. python3 -c "
from intercept.pm_coordinator import PMCoordinator
from orchestration.agent_manager import AgentStateManager
from database.connection_manager import DatabaseConnectionManager
print('✅ All core modules import successfully')
"
```

### 3. Database Connectivity

```bash
# Test SQLite coordination.db
PYTHONPATH=. python3 -c "
import sqlite3
conn = sqlite3.connect('intercept/coordination.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')
tables = cursor.fetchall()
print(f'✅ coordination.db tables: {tables}')
conn.close()
"

# Test PostgreSQL (if configured)
PYTHONPATH=. python3 -c "
import asyncio
from database.connection_manager import get_connection

async def test():
    conn = await get_connection()
    print('✅ PostgreSQL connected')

asyncio.run(test())
"
```

### 4. .bmad-core Accessibility

```bash
# Verify .bmad-core is accessible
ls -la .bmad-core/
# Expected: agents/, tasks/, templates/, checklists/, workflows/, etc.

# Test loading agent definitions
PYTHONPATH=. python3 -c "
from intercept.agent_loader import load_agent
agent = load_agent('pm')
print(f'✅ PM agent loaded: {agent[\"name\"]}')
"
```

---

## 🚀 Quick Start After Installation

### Activate Environment (Always First)

```bash
cd /Users/apple/ai-projects/bmad-auto/
source bmad-auto-env/bin/activate
```

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/integration/test_pm_coordinator.py -v

# Run with coverage
pytest tests/ -v --cov=intercept --cov=orchestration
```

### Start Development Server (When API is ready)

```bash
# Start FastAPI server
cd /Users/apple/ai-projects/bmad-auto/
source bmad-auto-env/bin/activate
PYTHONPATH=. uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Interactive Python Session

```bash
cd /Users/apple/ai-projects/bmad-auto/
source bmad-auto-env/bin/activate
PYTHONPATH=. python3

# Inside Python REPL
>>> from intercept.pm_coordinator import PMCoordinator
>>> pm = PMCoordinator()
>>> # Start experimenting!
```

---

## 🔍 Troubleshooting

### Issue: Virtual environment not activating

```bash
# Try absolute path
source /Users/apple/ai-projects/bmad-auto/bmad-auto-env/bin/activate

# Or recreate environment
rm -rf bmad-auto-env
python3 -m venv bmad-auto-env
source bmad-auto-env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Module not found errors

```bash
# Always set PYTHONPATH
export PYTHONPATH=/Users/apple/ai-projects/bmad-auto:$PYTHONPATH

# Or run from project root
cd /Users/apple/ai-projects/bmad-auto/
PYTHONPATH=. python3 your_script.py
```

### Issue: Database connection fails

```bash
# Check PostgreSQL running
brew services list | grep postgresql

# Start if not running
brew services start postgresql@15

# Check connection
psql -U bmad_user -d bmad_auto -c "SELECT 1"
```

### Issue: coordination.db not initialized

```bash
cd /Users/apple/ai-projects/bmad-auto/

# Delete and recreate
rm intercept/coordination.db
PYTHONPATH=. python3 -c "
from intercept.pm_coordinator import PMCoordinator
pm = PMCoordinator(db_path='intercept/coordination.db')
print('✓ Database reinitialized')
"
```

### Issue: Import errors from .bmad-core

```bash
# Verify .bmad-core exists
ls -la .bmad-core/agents/

# If missing, copy from reference
cp -r /path/to/reference/.bmad-core .bmad-core
```

---

## 📋 Installation Checklist

### Pre-Installation
- [ ] Python 3.11+ installed (you have 3.13.5 ✓)
- [ ] Git installed and configured
- [ ] PostgreSQL installed (optional for MVP)
- [ ] 8GB RAM, 4 CPU cores available

### Installation Process
- [ ] Navigated to /Users/apple/ai-projects/bmad-auto/
- [ ] Ran `./scripts/install.sh` successfully
- [ ] Virtual environment created (bmad-auto-env/)
- [ ] All dependencies installed from requirements.txt
- [ ] .env file created from .env.example
- [ ] coordination.db initialized

### Post-Installation Verification
- [ ] Virtual environment activates correctly
- [ ] Core modules import without errors
- [ ] coordination.db contains tables
- [ ] PostgreSQL connects (if configured)
- [ ] .bmad-core directory accessible
- [ ] Tests run successfully

### Configuration
- [ ] .env file edited with necessary values
- [ ] DATABASE_URL configured (if using PostgreSQL)
- [ ] PYTHONPATH set correctly for development
- [ ] Claude Code terminal accessible

---

## 🎯 Next Steps After Installation

1. **Update Session Handoff**: Note that installation is complete
2. **Run Verification**: Execute all verification steps above
3. **Configure Environment**: Edit .env with your settings
4. **Test Core Functionality**: Run basic tests to ensure everything works
5. **Begin API Development**: Start T031-T036 implementation

---

## 📞 Support

**Installation Issues**: Check troubleshooting section above
**Module Import Errors**: Verify PYTHONPATH and virtual environment
**Database Problems**: Check PostgreSQL service and connection string
**General Help**: Refer to main README.md and architecture docs

---

**Installation Guide Created**: 2025-10-01
**For**: BMAD Auto standalone repository
**Status**: Complete - Ready for use
