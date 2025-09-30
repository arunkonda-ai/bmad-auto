# Git Worktrees for Parallel Development

## Quick Setup

**Create 4 parallel work environments:**

```bash
cd /Users/apple/ai-projects/Omcaro

git worktree add ../Omcaro-youtube youtube-platform
git worktree add ../Omcaro-orchestration bmad-orchestration
git worktree add ../Omcaro-agents agent-development
git worktree add ../Omcaro-quality quality-gates
```

## Development Sessions

**4 Parallel Claude Sessions:**

1. **YouTube Platform**: `cd ../Omcaro-youtube && claude`
2. **BMAD Orchestration**: `cd ../Omcaro-orchestration && claude`
3. **Agent Development**: `cd ../Omcaro-agents && claude`
4. **Quality & Testing**: `cd ../Omcaro-quality && claude`

## Sync & Merge

**When ready to integrate:**

```bash
# From main Omcaro directory
git checkout master
git merge youtube-platform
git merge bmad-orchestration
git merge agent-development
git merge quality-gates
```

**Benefits**: No conflicts, parallel development, focused work streams.