#!/bin/bash
# BMAD Auto Installation Script

set -e

echo "🚀 Installing BMAD Auto..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if running in project directory
if [ ! -d ".bmad-auto" ]; then
    echo "❌ Error: Please run this from a project directory containing .bmad-auto/"
    exit 1
fi

cd .bmad-auto

# Create virtual environment if not exists
if [ ! -d "bmad-auto-env" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv bmad-auto-env
fi

# Activate virtual environment
source bmad-auto-env/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment file
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "📝 Please edit .env with your configuration"
fi

# Initialize coordination database
if [ ! -f "intercept/coordination.db" ] || [ ! -s "intercept/coordination.db" ]; then
    echo "🗄️  Initializing coordination database..."
    PYTHONPATH=. python3 -c "
from intercept.pm_coordinator import PMCoordinator
print('✓ Database initialized')
"
fi

echo ""
echo "✅ BMAD Auto installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit .bmad-auto/.env with your configuration"
echo "2. Activate environment: source .bmad-auto/bmad-auto-env/bin/activate"
echo "3. Start using BMAD Auto for your project"
echo ""
