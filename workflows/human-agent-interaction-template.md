# Human-Agent Interaction Session Template

**Template Type**: Workflow Template
**Version**: 1.0
**Purpose**: Standardized documentation for all human-agent coordination sessions
**Location Pattern**: `.bmad-auto/planning/planning-sessions/session-{YYYY-MM-DD}-{agent-name}-{human-role}-{purpose}.md`

## Template Structure

```markdown
# {Project Name} {Purpose} Coordination Session

**Session Date**: {YYYY-MM-DD}
**Session Type**: {Select: Technical|Strategic|Review|Approval|Brainstorming|Quality Gate|Escalation}
**Primary Agent**: {Agent Name} ({Agent Role: PM|Architect|Developer|QA|UX|Analyst})
**Human Participant**: {Human Role/Name}
**Duration**: {Timeline or "Active session (ongoing)"}
**Status**: {In Progress|Completed|Deferred|Escalated}
**Next Session**: {Date/TBD/Not Required}

## Session Overview

{Brief description of session purpose, context, and goals}

## Key Decisions Made

### ✅ **{Decision Category 1}**

**{Decision Title}**:
- **Decision**: {What was decided}
- **Rationale**: {Why this decision was made}
- **Impact**: {Business/technical impact}
- **Validation**: {How decision was validated}

**{Additional decisions as needed}**

### ✅ **{Decision Category 2}**
{Follow same pattern}

## Technical Discussions

### **{Technical Topic 1}**

**Discussion Summary**:
{Key technical points discussed}

**Technical Decisions**:
- **Architecture Pattern**: {Selected approach and rationale}
- **Technology Selection**: {Chosen technologies and justification}
- **Integration Approach**: {How components will integrate}

**Trade-offs Considered**:
- **Option A**: {Pros/cons considered}
- **Option B**: {Pros/cons considered}
- **Selected**: {Final choice and rationale}

### **Current Implementation Status**

**Progress Indicators**:
- ✅ {Completed items}
- 🔄 {In progress items}
- 📋 {Pending items}

**Blockers/Risks Identified**:
- {Blocker 1}: {Description and mitigation approach}
- {Risk 1}: {Description and risk mitigation}

## Strategic Considerations

### **Business Impact Assessment**

**Immediate Impact**:
- {Short-term business implications}

**Long-term Strategic Value**:
- {Long-term strategic benefits}

**Resource Allocation**:
- {Resource requirements and allocation decisions}

### **Timeline and Prioritization**

**Current Phase Integration**:
- {How session decisions integrate with current development phase}

**Future Phase Implications**:
- {Impact on future development phases}

**Priority Adjustments**:
- {Any priority changes resulting from session}

## Quality Gate Considerations

### **Approval Requirements**

**Human Approval Needed For**:
- {List items requiring human oversight}

**Automated Validation Sufficient For**:
- {List items that can proceed with automated checks}

**Escalation Triggers**:
- {Conditions that require escalation to human oversight}

### **Risk Assessment**

**Technical Risks**:
- {Risk description}: {Mitigation strategy}

**Business Risks**:
- {Risk description}: {Mitigation strategy}

**Integration Risks**:
- {Risk description}: {Mitigation strategy}

## Action Items

### **For {Agent Name} ({Agent Role}) - Immediate**
- [ ] **{Action Item 1}**: {Description and timeline}
- [ ] **{Action Item 2}**: {Description and timeline}

### **For Human Oversight - This Session**
- [ ] **{Review Item 1}**: {What needs human review}
- [ ] **{Approval Item 1}**: {What needs human approval}

### **For PM Coordination - Context Integration**
- [ ] **{PM Action 1}**: {PM coordination requirements}
- [ ] **{Cross-Agent Item}**: {Multi-agent coordination needs}

## Context for Future Sessions

### **For PM and Other Agents**

**Key Context to Preserve**:
1. **{Context Item 1}**: {Why this context is important}
2. **{Context Item 2}**: {How this affects future work}
3. **{Context Item 3}**: {Integration requirements}

**Decision Patterns Established**:
- **{Pattern 1}**: {Decision-making approach established}
- **{Pattern 2}**: {Quality gate pattern established}
- **{Pattern 3}**: {Human oversight pattern established}

### **For Future {Session Type} Sessions**

**Established Baselines**:
- {Technical baselines established}
- {Process baselines established}
- {Quality baselines established}

**Remaining Decisions Needed**:
- {Future decision points identified}
- {Future validation requirements}
- {Future integration points}

## Learning and Optimization

### **Process Improvements Identified**

**What Worked Well**:
- {Effective approaches from this session}

**What Could Be Improved**:
- {Areas for optimization in future sessions}

**Recommendations for Future Sessions**:
- {Process recommendations based on this session}

### **Human-AI Collaboration Insights**

**Effective Collaboration Patterns**:
- {Successful interaction patterns observed}

**Areas for Enhancement**:
- {Ways to improve human-AI collaboration}

**Context Preservation Effectiveness**:
- {How well context was maintained and used}

## Session Artifacts

### **Documents Created This Session**
- **{Document 1}**: {Purpose and location}
- **{Document 2}**: {Purpose and location}

### **Templates/Patterns Established**
- **{Template/Pattern 1}**: {Description and location}
- **{Template/Pattern 2}**: {Description and location}

### **Decisions Recorded**
- **{Decision Set 1}**: {Summary and implications}
- **{Decision Set 2}**: {Summary and implications}

### **Next Session Preparation**
- **Prerequisites**: {What needs to be completed before next session}
- **Agenda Items**: {Topics for next session}
- **Context Handoff**: {Key information for next session}

---

**Session Status**: {Final status}
**Next Update**: {When this document will be updated}
**Context Handoff**: {Summary of what future agents/PM need to know}
```

## Usage Guidelines

### **When to Use This Template**

**Required For**:
- All technical architecture decisions involving human oversight
- Strategic planning sessions with human input
- Quality gate approvals requiring human validation
- Cross-agent coordination with human mediation
- Escalation sessions for complex decisions

**Session Types**:
- **Technical**: Architecture, design, implementation decisions
- **Strategic**: Business direction, priority, resource allocation
- **Review**: Progress assessment, quality validation
- **Approval**: Go/no-go decisions, quality gate sign-offs
- **Brainstorming**: Creative ideation, problem-solving
- **Quality Gate**: Formal validation checkpoints
- **Escalation**: Complex issues requiring human intervention

### **Integration with BMAD Auto Workflows**

**PM Integration**:
- PM agents should reference session documents for context
- Session decisions inform autonomous command selection
- Quality gate patterns from sessions guide automated validation

**Agent Coordination**:
- Agents should check relevant session documents before major decisions
- Cross-agent handoffs should reference session context
- Session templates provide context for agent extension frameworks

**Lifecycle Integration**:
- Each product lifecycle phase should maintain session documentation
- Session patterns inform quality gate design
- Human oversight patterns scale across development phases

### **Maintenance and Updates**

**Document Maintenance**:
- Update session documents in real-time during active sessions
- Mark sessions as completed with final status
- Link related sessions for context continuity

**Template Evolution**:
- Improve template based on usage feedback
- Add new session types as needed
- Maintain backward compatibility with existing sessions

**Context Preservation**:
- Ensure session documents are accessible to all relevant agents
- Maintain cross-references between related sessions
- Archive completed sessions but keep them accessible

## Integration Points

### **With PM Extension Framework**

**Autonomous Decision Support**:
- Session patterns inform command selection algorithms
- Human approval patterns guide escalation triggers
- Context from sessions enhances PM orchestration capabilities

**Quality Gate Integration**:
- Session-defined approval workflows integrated into quality gates
- Human oversight patterns automated where appropriate
- Escalation protocols based on session decision patterns

### **With Agent Extension System**

**Context Enhancement**:
- Agent extensions access session context for enhanced decision-making
- Session patterns inform agent capability enhancements
- Human feedback loops integrated into agent learning systems

**Coordination Optimization**:
- Session documentation improves cross-agent coordination
- Human decision patterns inform agent interaction protocols
- Context preservation enables more sophisticated agent collaboration