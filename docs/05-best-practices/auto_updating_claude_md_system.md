# Self-Maintaining Claude.md System - Auto-Update Architecture

*Autonomous maintenance for BMAD agent documentation without human intervention*

---

## 🎯 Core Philosophy: Self-Maintaining Documentation

### **The Problem**
- Manual Claude.md updates are unsustainable
- Context pollution from outdated information
- Broken links and legacy references
- Inconsistent information across agent files
- Human bottlenecks in autonomous systems

### **The Solution: Event-Driven Auto-Maintenance**
```
Code Changes → Events → Auto-Update → Validation → Commit
     ↓
Git Hooks → Triggers → Claude.md Updates → Link Checks → Deploy
```

---

## 🔄 Auto-Update Architecture

### **1. Event-Driven Update System**

```markdown
# Auto-Update Triggers (.bmad-auto/system/auto-update/triggers.md)

## 📡 EVENT SOURCES

### Git Events (Primary Triggers)
- **Pre-commit**: Validate Claude.md before commit
- **Post-commit**: Update related documentation
- **Pre-push**: Final validation and link checking
- **Post-merge**: Sync changes across agent files

### File System Events
- **File Creation**: Add to relevant Claude.md file lists
- **File Deletion**: Remove references and update links
- **Directory Changes**: Update project structure documentation
- **Configuration Changes**: Propagate to dependent Claude.md files

### Agent Action Events
- **Task Completion**: Update progress and learning
- **Decision Made**: Record in decision logs
- **Error Encountered**: Update troubleshooting guides
- **Pattern Discovered**: Add to best practices

### Project Milestone Events
- **Sprint Start/End**: Update project context
- **Release**: Archive completed features, update status
- **Architecture Changes**: Propagate to all relevant agents
- **Team Changes**: Update responsibility matrices
```

### **2. Smart Template System**

```markdown
# Template-Based Auto-Generation (.bmad-auto/system/templates/)

## 🎯 DYNAMIC CLAUDE.MD TEMPLATES

### Base Template Structure
```yaml
# claude.template.yaml
metadata:
  agent_type: "{{AGENT_TYPE}}"
  project: "{{PROJECT_NAME}}"
  last_updated: "{{AUTO_TIMESTAMP}}"
  
sections:
  critical_rules:
    source: "shared/rules/{{AGENT_TYPE}}-rules.md"
    auto_update: true
    
  project_context:
    source: "projects/{{PROJECT_NAME}}/context.md"
    auto_update: true
    
  file_boundaries:
    source: "auto-generated/file-structure.md"
    auto_update: true
    
  commands:
    source: "projects/{{PROJECT_NAME}}/commands.md"
    auto_update: true
    
  agent_memory:
    source: "agents/{{AGENT_TYPE}}/memory/current.md"
    auto_update: true
```

### Template Compilation Process
1. **Trigger Event**: Git commit, file change, agent action
2. **Context Gathering**: Collect current project state
3. **Template Processing**: Replace variables with current values
4. **Content Validation**: Check for broken links and outdated info
5. **Atomic Update**: Replace Claude.md atomically
6. **Verification**: Validate updated file works correctly
```

### **3. Intelligent Content Management**

```markdown
# Smart Content Updates (.bmad-auto/system/content-manager/)

## 🧠 CONTENT INTELLIGENCE SYSTEM

### Auto-Discovery Mechanisms
```bash
# File structure auto-detection
find . -name "*.md" -o -name "*.js" -o -name "*.py" | \
  grep -v node_modules | \
  sort > .bmad-auto/cache/current-files.txt

# Compare with previous state
diff .bmad-auto/cache/previous-files.txt .bmad-auto/cache/current-files.txt > \
  .bmad-auto/cache/file-changes.txt

# Update Claude.md file boundary sections
python .bmad-auto/system/update-file-boundaries.py
```

### Link Validation and Auto-Repair
```python
# link-validator.py
def validate_and_repair_links():
    for claude_file in find_claude_md_files():
        links = extract_markdown_links(claude_file)
        for link in links:
            if not link_exists(link):
                new_link = find_moved_file(link)
                if new_link:
                    replace_link(claude_file, link, new_link)
                    log_repair(f"Fixed link: {link} → {new_link}")
                else:
                    remove_broken_link(claude_file, link)
                    log_removal(f"Removed broken link: {link}")
```

### Context Compression
```python
# context-compressor.py
def compress_outdated_context():
    """Compress old context to prevent pollution"""
    for memory_file in find_memory_files():
        if is_stale(memory_file, days=30):
            summary = ai_summarize(memory_file)
            archive_original(memory_file)
            create_summary_file(memory_file, summary)
            log_compression(f"Compressed: {memory_file}")
```
```

---

## 🔧 Implementation Components

### **1. Git Hooks for Auto-Maintenance**

```bash
# .git/hooks/pre-commit (Auto-Update Before Commit)
#!/bin/bash

echo "🔄 Auto-updating