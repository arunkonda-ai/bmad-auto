#!/bin/bash
# Week 1 Safety Features Test Runner

echo "🧪 Running Week 1 Safety Features Tests"
echo "========================================"

# Check if PostgreSQL is running
if ! pg_isready -q; then
    echo "⚠️  PostgreSQL is not running. Please start it first."
    echo "   Run: brew services start postgresql"
    exit 1
fi

# Check if database exists
if ! psql -lqt | cut -d \| -f 1 | grep -qw bmad_auto; then
    echo "⚠️  Database 'bmad_auto' not found. Creating it..."
    createdb bmad_auto
fi

# Apply schema
echo ""
echo "📊 Applying database schema..."
psql bmad_auto < .bmad-auto/database/schema/state_persistence.sql

# Run tests
echo ""
echo "🧪 Running Git Coordinator tests..."
python3 -m pytest .bmad-auto/tests/integration/test_git_coordinator.py -v

echo ""
echo "🧪 Running Workflow State tests..."
python3 -m pytest .bmad-auto/tests/integration/test_workflow_state.py -v

echo ""
echo "✅ Week 1 tests complete!"