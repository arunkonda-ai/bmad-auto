---
type: reference
version: 1.0
created: 2025-01-18
updated: 2025-01-18
status: active
owners: [architect]
related: [CLAUDE.md, CONSOLIDATION_REPORT.md]
consolidation_date: 2025-01-18
---

# BMAD Auto Documentation Standards

## **Mandatory Documentation Protocols**

### **1. Document Header Requirements (ALL FILES)**

Every documentation file MUST include this header:

```yaml
---
type: [prd|architecture|research|reference|guide|legacy]
version: 1.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: [active|deprecated|draft|review]
owners: [architect|pm|analyst|dev|qa|ux]
related: [list of related document paths]
source: [if derived from other docs]
consolidation_date: 2025-01-18
original_location: [if moved during consolidation]
---
```

**Field Definitions**:
- **type**: Document category for navigation and organization
- **version**: Semantic versioning for document evolution
- **created**: Original creation date
- **updated**: Last modification date (MUST update on every change)
- **status**: Current document lifecycle state
- **owners**: Responsible team roles for maintenance
- **related**: Cross-reference list for navigation
- **source**: Source documents if derived/compiled
- **consolidation_date**: Date of 2025-01-18 reorganization
- **original_location**: Previous path if moved during consolidation

### **2. File Naming Convention**

**Kebab-case naming**:
- ✅ `bmad-auto-comprehensive-prd.md`
- ✅ `system-architecture-v2.md`
- ✅ `2024-12-01-market-analysis.md`
- ❌ `BMAD_Auto_PRD.md`
- ❌ `SystemArchitecture.md`

**Date prefixes for research**:
- `YYYY-MM-DD-research-topic.md`
- Example: `2024-12-01-competitive-analysis.md`

**Version suffixes for iterations**:
- `document-name-v2.md`
- Example: `technical-architecture-v3.md`

### **3. Cross-Reference System**

**Relative path references**:
```markdown
[Architecture Guide](../01-foundation/system-architecture.md)
[PRD Section 2](../../planning/requirements/bmad-auto-comprehensive-prd.md#section-2)
```

**Mandatory related documents section**:
```markdown
## Related Documents
- [System Architecture](docs/01-foundation/system-architecture.md)
- [Implementation Guide](docs/02-implementation/workflow-orchestration.md)
- [Testing Framework](testing/README.md)
```

### **4. Agent Documentation Protocols**

**When ANY agent creates/updates documentation**:

1. **Update document header** with current timestamp in `updated` field
2. **Update master index** in `.bmad-auto/CLAUDE.md` if new document
3. **Check related documents** and update their reference lists
4. **Archive old versions** to `.bmad-auto/archive/` if major changes
5. **Validate internal links** still work after changes

**Agent-specific responsibilities**:
- **architect**: System architecture, technical specifications
- **pm**: PRD, requirements, project management
- **analyst**: Research, competitive analysis, market intelligence
- **dev**: Implementation guides, technical documentation
- **qa**: Testing frameworks, quality assurance procedures
- **ux**: Design specifications, user experience guides

### **5. Directory Organization Standards**

**Primary structure**:
```
.bmad-auto/
├── docs/                    # Implementation & operational docs
│   ├── 01-foundation/       # Core architecture & frameworks
│   ├── 02-implementation/   # Development guides
│   ├── 03-operations/       # Deployment & monitoring
│   ├── 04-reference/        # API & configuration reference
│   ├── 05-best-practices/   # Integration best practices
│   └── architecture/        # System architecture (merged)
├── planning/                # PRD, strategy, design
│   ├── requirements/        # PRD and specifications
│   ├── architecture/        # Technical architecture
│   ├── design/              # UX and system design
│   └── strategy/            # Strategic planning
├── research/                # Research materials & analysis
│   ├── source-materials/    # Original research (from consolidation)
│   ├── findings/            # Analysis results
│   └── analysis/            # Technical evaluations
├── archive/                 # Legacy & deprecated content
│   ├── legacy-v1/           # Pre-consolidation legacy
│   ├── claude-integration/  # Archived duplicates
│   └── versions/            # Archived document versions
└── CLAUDE.md               # Master navigation index
```

### **6. Quality Assurance Checklist**

**Before committing documentation changes**:

- [ ] Document header complete with all required fields
- [ ] `updated` timestamp current
- [ ] All internal links functional
- [ ] Related documents updated with cross-references
- [ ] Master index (CLAUDE.md) updated if new document
- [ ] Proper file naming convention followed
- [ ] Content follows established style guidelines
- [ ] Archive created if major version change

### **7. Master Index Maintenance**

**CLAUDE.md requirements**:
- **Complete navigation hierarchy** for all documents
- **Quick reference sections** by document type
- **Agent-specific guidance** for finding relevant docs
- **Update log** with recent changes
- **Relationship mapping** between documents

**Update triggers**:
- New document creation
- Document relocation
- Major content updates
- Directory structure changes
- Link updates after moves

### **8. Automated Validation (Future Implementation)**

**Planned automation**:
- Link validation across all documents
- Header completeness checking
- Cross-reference validation
- Duplicate content detection
- Style guide compliance

**Manual validation until automation**:
- Weekly link checking
- Monthly cross-reference audit
- Quarterly comprehensive review
- Agent feedback integration

### **9. Archive Management**

**Archive criteria**:
- Document becomes obsolete
- Major version change (>1.0 increment)
- Superseded by new approach
- Consolidation source materials

**Archive structure**:
```
archive/
├── legacy-v1/           # Pre-2025-01-18 content
├── claude-integration/  # Duplicate agent files
├── versions/            # Document version history
│   ├── 2025-01/         # Monthly archive folders
│   └── 2025-02/
└── youtube-legacy/      # Moved YouTube-specific content
```

**Archive document headers**:
```yaml
---
type: legacy
status: deprecated
archived_date: 2025-01-18
reason: [superseded|obsolete|consolidated|duplicate]
replacement: [path to current version]
original_location: [pre-consolidation path]
---
```

### **10. Success Metrics**

**Documentation health indicators**:
- Zero broken internal links
- 100% header compliance
- Complete cross-reference network
- Active maintenance by assigned owners
- Regular agent accessibility validation

**Quality gates**:
- All new documents have complete headers
- Cross-references updated within 24 hours
- Master index updated within 1 hour
- Archive management monthly
- Link validation weekly

---

## **Implementation Status**

- ✅ **Standards Defined**: Complete framework established
- ✅ **Directory Structure**: Consolidated and organized
- 🔄 **Header Implementation**: In progress for all documents
- 📋 **Master Index Update**: Pending comprehensive rewrite
- 📋 **Automation**: Planned for future implementation

**Next Actions**: Apply headers to all consolidated documents and create comprehensive CLAUDE.md master index.