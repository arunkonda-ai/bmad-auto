# PM Decision: Git Repository Restructure & Worktree Implementation

**Date**: 2025-09-30
**PM Coordinator**: John (PM)
**Decision Type**: Repository Architecture & Development Workflow
**Priority**: 🚨 HIGH - Infrastructure Foundation
**Status**: ✅ APPROVED - READY FOR IMPLEMENTATION

---

## 🎯 User Request Analysis

### Core Requirements
1. **Initialize clean git repository** for BMAD Auto standalone product development
2. **Resolve legacy .github/ folder** with outdated YAML workflows
3. **Implement git worktrees** for smooth parallel development
4. **Align with best practices** from GitHub integration documentation

### Current Git Status Assessment

**Branch**: `001-foundation-pm-orchestration`

**Staged Deletions** (Legacy Cleanup):
- `.claude/` directory (old Claude Code patterns)
- `.cursor/` directory (legacy IDE rules)
- `src/` directory (old application code)
- `web-bundles/` directory (legacy agent bundles)
- Multiple legacy documentation and test files

**Untracked Files** (New BMAD Auto Work):
- `.bmad-auto/` complete implementation tree
- `.specify/` Spec Kit development artifacts
- `archive/` organized legacy preservation
- New documentation and configuration

**Legacy Remnants**:
- `.github/` folder with outdated workflow YAML files
- Old git history from previous project direction

---

## 🔍 Problem Analysis

### Issues with Current Git Structure

1. **Mixed Context**: Git history contains legacy project direction unrelated to BMAD Auto vision
2. **Legacy .github/ Workflows**: Outdated CI/CD configurations for previous architecture
3. **Confusing History**: Massive deletions create unclear repository timeline
4. **No Worktree Setup**: Sequential branch switching disrupts parallel development

### Impact of Continuing Without Restructure

- **Context Pollution**: New developers confused by legacy history
- **CI/CD Conflicts**: Old .github/ workflows may interfere with new setup
- **Development Friction**: Branch switching interrupts concurrent agent work
- **Documentation Drift**: Git history doesn't reflect BMAD Auto product vision

---

## 💡 PM Decision: Clean Repository Foundation

### APPROVED: Fresh Git Repository with Worktree Architecture

**Strategy**: Initialize new repository preserving only BMAD Auto work

**Rationale**:
1. **Clean History**: Start fresh with BMAD Auto product vision
2. **Clear Intent**: Repository reflects standalone product from commit 1
3. **Worktree Foundation**: Proper structure for parallel development
4. **Legacy Preservation**: Archive old repo for reference if needed

---

## 📋 Implementation Plan

### Phase 1: Repository Initialization (30 minutes)

#### Step 1: Archive Current Repository
```bash
# Create complete backup of current state
cd /Users/apple/ai-projects/
cp -r Omcaro Omcaro-legacy-backup-2025-09-30
cd Omcaro-legacy-backup-2025-09-30
git bundle create ../omcaro-legacy-complete.bundle --all

# Archive location: Safe external backup
echo "Legacy backup complete: Omcaro-legacy-backup-2025-09-30/"
```

#### Step 2: Initialize Fresh BMAD Auto Repository
```bash
# Remove old git history
cd /Users/apple/ai-projects/Omcaro
rm -rf .git

# Initialize clean repository
git init
git config user.name "BMAD Auto Development"
git config user.email "dev@bmad-auto.local"

# Set main branch
git branch -M main
```

#### Step 3: Clean Legacy .github/ Folder
```bash
# Decision: Remove legacy .github/ workflows
# Rationale: Old CI/CD configs not applicable to BMAD Auto architecture

# Archive legacy workflows first
mkdir -p archive/legacy-github-workflows
cp -r .github/* archive/legacy-github-workflows/

# Remove legacy .github/
rm -rf .github

# Create new .github/ structure for BMAD Auto
mkdir -p .github/workflows
```

#### Step 4: Create Initial Commit - BMAD Auto Foundation
```bash
# Stage BMAD Auto work
git add .bmad-auto/
git add .specify/
git add README.md
git add CLAUDE.md
git add archive/
git add .env.local
git add .gitignore
git add package.json
git add package-lock.json

# First commit - Clean BMAD Auto foundation
git commit -m "feat: Initialize BMAD Auto standalone product repository

BMAD Auto - Autonomous Product Development Orchestration System

Foundation includes:
- .bmad-auto/ complete implementation (T001-T024 complete, 57%)
- Spec Kit integration for development workflow
- Multi-provider AI strategy (Claude + Z.ai GLM)
- PostgreSQL + coordination.db hybrid architecture
- Safety features (T029 git integration, T037 state persistence)

Architecture:
- PM-centric orchestration with 10-agent ecosystem
- Extension overlay pattern preserving .bmad-core
- LangGraph workflows with LangFuse monitoring
- CLI-first external integration (GitHub + Linear)

Status: MVP Phase 1 Foundation complete, API implementation next

🤖 Generated with BMAD Auto PM Orchestration
Co-Authored-By: John (PM) <pm@bmad-auto.local>"
```

### Phase 2: Git Worktree Setup (45 minutes)

#### Worktree Architecture Pattern

Based on GitHub best practices documentation, implement **feature-based worktree structure INSIDE Omcaro project**:

```
/Users/apple/ai-projects/Omcaro/                    # Main worktree (main branch)
├── .git/                                           # Central git directory
├── .bmad-auto/                                     # BMAD Auto implementation (main)
├── .worktrees/                                     # Worktree directory (INSIDE project)
│   ├── develop/                                    # Integration branch worktree
│   │   └── .bmad-auto/                            # Development work
│   ├── feature-api-implementation/                 # API development (James)
│   │   └── .bmad-auto/api/                        # API endpoints
│   ├── feature-agent-extensions/                   # Agent integration (Alex)
│   │   └── .bmad-auto/agents/                     # Agent enhancements
│   ├── feature-quality-gates/                      # QA automation (Quinn)
│   │   └── .bmad-auto/orchestration/              # Quality workflows
│   └── feature-pm-orchestration/                   # PM coordination (John)
│       └── .bmad-auto/intercept/                  # PM-specific changes
├── README.md
└── [other project files]
```

**Key Correction**: Worktrees stay within `.worktrees/` subdirectory of Omcaro project, not outside!

#### Step 1: Create Development Branch and Worktree
```bash
# Create worktree directory INSIDE Omcaro project
mkdir -p .worktrees

# Create develop branch for integration
git branch develop

# Create worktree for develop branch (INSIDE project)
git worktree add .worktrees/develop develop

# Verify worktree
git worktree list
# Output shows: .worktrees/develop linked to develop branch
```

#### Step 2: Create Feature Worktrees for Parallel Development
```bash
# API Implementation worktree (T031-T036) - James
git worktree add -b feature/api-implementation \
  .worktrees/feature-api-implementation develop

# Agent Extensions worktree (T025) - Alex
git worktree add -b feature/agent-extensions \
  .worktrees/feature-agent-extensions develop

# Quality Gates worktree (T029 enhancements) - Quinn
git worktree add -b feature/quality-gates \
  .worktrees/feature-quality-gates develop

# PM Orchestration worktree (ongoing coordination) - John
git worktree add -b feature/pm-orchestration \
  .worktrees/feature-pm-orchestration develop

# Verify all worktrees
git worktree list
```

#### Step 3: Configure Worktree-Specific Settings
```bash
# Enable worktree config extensions
git config extensions.worktreeConfig true

# Set up per-worktree configurations
cd .worktrees/feature-api-implementation
git config --worktree user.name "James (Developer)"
git config --worktree user.email "james@bmad-auto.local"

cd ../feature-agent-extensions
git config --worktree user.name "Alex (Architect)"
git config --worktree user.email "alex@bmad-auto.local"

cd ../feature-quality-gates
git config --worktree user.name "Quinn (QA)"
git config --worktree user.email "quinn@bmad-auto.local"

cd ../feature-pm-orchestration
git config --worktree user.name "John (PM)"
git config --worktree user.email "john@bmad-auto.local"

# Return to main project directory
cd /Users/apple/ai-projects/Omcaro
```

### Phase 3: GitHub Integration (30 minutes)

#### Step 1: Create New GitHub Repository
```bash
# Using GitHub CLI (preferred - CLI-first approach)
gh repo create bmad-auto/autonomous-product-development \
  --public \
  --description "BMAD Auto: Autonomous Product Development Orchestration System" \
  --homepage "https://bmad-auto.com"

# Add remote
git remote add origin https://github.com/bmad-auto/autonomous-product-development.git
```

#### Step 2: Configure Branch Protection
```bash
# Main branch protection
gh api repos/bmad-auto/autonomous-product-development/branches/main/protection \
  -X PUT \
  -f required_status_checks='{"strict":true,"contexts":["test","lint"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":2}' \
  -f restrictions=null
```

#### Step 3: Push Initial Structure
```bash
# Push main branch
git push -u origin main

# Push develop branch
git push -u origin develop

# Push feature branches (from worktrees)
cd ../Omcaro-worktrees/feature-api-implementation
git push -u origin feature/api-implementation

cd ../feature-agent-extensions
git push -u origin feature/agent-extensions

cd ../feature-quality-gates
git push -u origin feature/quality-gates
```

### Phase 4: Workflow Documentation (15 minutes)

#### Create Worktree Usage Guide
```bash
# Create documentation for team
cat > .bmad-auto/docs/development/git-worktree-workflow.md << 'EOF'
# Git Worktree Development Workflow

## Quick Start

### List All Worktrees
```bash
git worktree list
```

### Create New Feature Worktree
```bash
git worktree add -b feature/your-feature \
  ../Omcaro-worktrees/feature-your-feature develop
```

### Switch Between Features
```bash
# No git checkout needed - just cd to worktree
cd /Users/apple/ai-projects/Omcaro-worktrees/feature-api-implementation
# Start working immediately - different branch, different directory
```

### Update Worktree from Develop
```bash
cd ../Omcaro-worktrees/feature-api-implementation
git pull origin develop
git merge develop
```

### Clean Up Completed Feature
```bash
# After PR merged
git worktree remove ../Omcaro-worktrees/feature-api-implementation
git branch -d feature/api-implementation
```

## Benefits

- **Parallel Development**: Work on multiple features simultaneously
- **No Branch Switching**: Each worktree maintains its branch
- **Context Preservation**: IDE state, builds, dependencies separate per worktree
- **Agent Coordination**: Different agents work in different worktrees without conflicts

## Best Practices

1. **One worktree per major feature** (T031-T036 API = one worktree)
2. **Regularly sync with develop** to avoid conflicts
3. **Clean up merged worktrees** to maintain workspace hygiene
4. **Use descriptive branch names** following convention: `feature/agent-task`
EOF

# Stage and commit documentation
git add .bmad-auto/docs/development/git-worktree-workflow.md
git commit -m "docs: Add git worktree development workflow guide

Comprehensive guide for BMAD Auto team worktree usage"
```

---

## ✅ Success Criteria

### Repository Structure Validation
- [ ] Clean git history starting with BMAD Auto foundation commit
- [ ] No legacy .github/ workflows present
- [ ] All BMAD Auto work preserved and organized
- [ ] Main and develop branches established

### Worktree Implementation Validation
- [ ] Worktree directory structure created
- [ ] Feature worktrees operational for 4 parallel tracks
- [ ] Worktree-specific configurations applied
- [ ] Team documentation complete and accessible

### GitHub Integration Validation
- [ ] Repository created with proper naming
- [ ] Branch protection rules configured
- [ ] Remote tracking established
- [ ] Initial push successful

### Development Workflow Validation
- [ ] Agents can work in parallel worktrees without conflicts
- [ ] Branch switching eliminated from daily workflow
- [ ] Clear documentation for team adoption
- [ ] Backup of legacy repository confirmed

---

## 🎯 PM Reasoning: Why This Approach

### Decision Logic

**Option A: Keep Current Repo + Add Worktrees** ❌ REJECTED
- **Problem**: Legacy history causes confusion
- **Problem**: Old .github/ workflows interfere
- **Problem**: Massive deletions clutter history

**Option B: Fresh Repo + Worktree Architecture** ✅ APPROVED
- **Benefit**: Clean history reflecting product vision
- **Benefit**: No legacy interference or confusion
- **Benefit**: Proper foundation for parallel development
- **Benefit**: Clear separation of concerns per agent

### Risk Mitigation

**Risk**: Data loss during migration
- **Mitigation**: Complete backup of current repository before any changes
- **Mitigation**: Git bundle created for full history preservation
- **Mitigation**: Archive directory maintains legacy for reference

**Risk**: Team confusion during transition
- **Mitigation**: Comprehensive worktree workflow documentation
- **Mitigation**: Clear naming conventions for worktree directories
- **Mitigation**: Step-by-step onboarding guide created

**Risk**: GitHub integration complexity
- **Mitigation**: CLI-first approach reduces API complexity
- **Mitigation**: Branch protection configured upfront
- **Mitigation**: Remote tracking established systematically

---

## 📊 Timeline & Resource Allocation

### Implementation Timeline
- **Phase 1** (Repository Init): 30 minutes - James
- **Phase 2** (Worktree Setup): 45 minutes - James + Alex
- **Phase 3** (GitHub Integration): 30 minutes - James
- **Phase 4** (Documentation): 15 minutes - James + Quinn

**Total Time**: ~2 hours for complete implementation

### Team Assignment
- **James (Developer)**: Lead implementation, execute all git commands
- **Alex (Architect)**: Validate worktree architecture, review structure
- **Quinn (QA)**: Verify success criteria, test workflows
- **John (PM)**: Oversight and approval, team coordination

---

## 🔄 Post-Implementation Actions

### Immediate Next Steps (After Restructure)

1. **Resume API Implementation** (T031-T036)
   - Work in `feature-api-implementation` worktree
   - No branch switching disruption
   - Parallel development enabled

2. **Update Team Documentation**
   - Add worktree workflow to onboarding
   - Update CLAUDE.md with repository structure
   - Communicate changes to all agents

3. **Configure CI/CD**
   - Create new .github/workflows/ for BMAD Auto
   - Implement quality gates automation
   - Set up LangFuse monitoring integration

---

## ✅ PM Approval Statement

**I, John (PM), approve this git repository restructure with worktree implementation as the foundation for BMAD Auto parallel development.**

**Approved Strategy**:
1. ✅ Initialize fresh repository with clean BMAD Auto history
2. ✅ Remove legacy .github/ workflows (archived for reference)
3. ✅ Implement git worktree architecture for 4 parallel tracks
4. ✅ GitHub integration with branch protection and CLI-first approach

**Rationale**: Clean repository foundation eliminates legacy confusion, enables efficient parallel agent development, and establishes professional development workflow aligned with BMAD Auto product vision.

**Success Definition**: After implementation, team can work on 4+ features simultaneously in separate worktrees, with clean git history reflecting BMAD Auto product development from day one.

---

**Next Action**: James begins Phase 1 (Repository Initialization) with complete backup and fresh git init.

---

**PM Coordinator**: John (PM)
**Decision Date**: 2025-09-30
**Priority**: 🚨 HIGH - Infrastructure Foundation
**Status**: ✅ APPROVED - EXECUTE IMMEDIATELY