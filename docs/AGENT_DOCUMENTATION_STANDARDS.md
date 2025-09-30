# 🤖 BMAD Auto Agent Documentation Standards

## 🎯 **Two-Layer Documentation System**

### **Layer 1: Common Instructions (All Agents)**
Universal guidelines that apply to every agent regardless of task type.

### **Layer 2: Agent-Specific Standards (Recurring Tasks)**
Predefined structures for routine documentation that each agent produces regularly.

---

## 🌍 **LAYER 1: COMMON INSTRUCTIONS FOR ALL AGENTS**

### **📁 File Organization Principles**
1. **Always check existing structure first** before creating new directories
2. **Use agent-owned directories** for routine work:
   - Mary → `research/`
   - John → `planning/`
   - James/Alex → `deployment/`
   - Quinn → `testing/`
   - Sally → UX docs across relevant directories
3. **For unique/new tasks**: Create logical subdirectories within your domain
4. **Cross-agent collaboration**: Use `docs/` for shared technical documentation

### **📝 Document Creation Rules**
1. **Start with README.md** in any new directory you create
2. **Use descriptive filenames** with dates for time-sensitive content
3. **Include metadata** at top of each document:
   ```markdown
   # Document Title
   **Agent**: [Your Name]
   **Created**: YYYY-MM-DD
   **Type**: [Research/Planning/Technical/Testing/UX]
   **Status**: [Draft/Review/Final/Archived]
   **Stakeholders**: [Who needs to review this]
   ```

### **🔄 Lifecycle Management**
1. **Active work** stays in main directories
2. **Completed work** moves to `archive/YYYY/QX/[your-domain]/`
3. **Update indexes** when archiving (maintain README.md files)
4. **Cross-reference** related documents across domains

### **🤝 Collaboration Protocol**
1. **Tag stakeholders** in document metadata
2. **Use consistent naming** for cross-agent projects
3. **Create links** between related documents
4. **Notify other agents** when their input is needed

---

## 🎭 **LAYER 2: AGENT-SPECIFIC STANDARDS**

### **🔬 MARY (Business Analyst) - Research Domain**

#### **📊 Recurring Documentation Types**

**Market Analysis Reports** (`research/findings/market-analysis-YYYY-MM-DD.md`)
```markdown
# Market Analysis: [Topic]
**Agent**: Mary
**Created**: YYYY-MM-DD
**Type**: Research
**Status**: [Draft/Final]
**Stakeholders**: John (Product Strategy)

## Executive Summary
[Key findings in 2-3 sentences]

## Market Size & Opportunity
- Total Addressable Market (TAM)
- Serviceable Available Market (SAM)
- Key growth drivers

## Competitive Landscape
- Direct competitors
- Indirect competitors
- Competitive advantages/gaps

## Key Insights
- Market trends
- Customer pain points
- Opportunities

## Recommendations
- Strategic recommendations
- Next research areas
- Timeline for implementation
```

**Competitive Analysis** (`research/findings/competitive-analysis-COMPANY-YYYY-MM-DD.md`)
```markdown
# Competitive Analysis: [Company Name]
**Agent**: Mary
**Created**: YYYY-MM-DD
**Type**: Research
**Status**: [Draft/Final]
**Stakeholders**: John (Strategy), James (Technical Comparison)

## Company Overview
- Business model
- Target market
- Key metrics (if available)

## Product Analysis
- Core features
- Pricing model
- Integration capabilities

## Strengths & Weaknesses
- Competitive advantages
- Identified gaps
- Market positioning

## Technical Architecture (if available)
- Technology stack
- Scalability approach
- Integration patterns

## Strategic Implications
- Threats to our roadmap
- Opportunities to differentiate
- Feature gap analysis
```

#### **🆓 Flexible Task Handling**
For unique research requests not covered above:
1. **Create logical subdirectory** in `research/active/[task-category]/`
2. **Use your expertise** to structure the investigation
3. **Follow common metadata standards**
4. **Inform John** of new research categories for potential standardization

---

### **📝 JOHN (Product Manager) - Planning Domain**

#### **📋 Recurring Documentation Types**

**Product Requirements Document** (`planning/requirements/prd-FEATURE-v1.0.md`)
```markdown
# PRD: [Feature Name] v1.0
**Agent**: John
**Created**: YYYY-MM-DD
**Type**: Planning
**Status**: [Draft/Review/Approved]
**Stakeholders**: James (Technical), Quinn (Testing), Sally (UX), Alex (Architecture)

## Executive Summary
[Problem, solution, success metrics in 3-4 sentences]

## Problem Statement
- User pain points (from Mary's research)
- Business impact
- Opportunity size

## Solution Overview
- Core functionality
- User experience flow
- Technical approach (high-level)

## Requirements
### Functional Requirements
- [Detailed feature specifications]

### Non-Functional Requirements
- Performance requirements
- Scalability needs
- Security considerations

## Success Metrics
- Key performance indicators
- Acceptance criteria
- Success benchmarks

## Dependencies & Constraints
- Technical dependencies
- Resource constraints
- Timeline considerations

## Implementation Plan
- Development phases
- Testing strategy
- Rollout approach
```

**Quarterly Roadmap** (`planning/strategy/roadmap-YYYY-Q1.md`)
```markdown
# Product Roadmap: YYYY Q1
**Agent**: John
**Created**: YYYY-MM-DD
**Type**: Planning
**Status**: [Draft/Approved]
**Stakeholders**: All Agents + Leadership

## Quarter Objectives
- Primary goals
- Success metrics
- Strategic alignment

## Planned Features
### High Priority
- [Feature 1] - [Timeline] - [Owner: Agent]
- [Feature 2] - [Timeline] - [Owner: Agent]

### Medium Priority
- [Feature 3] - [Timeline] - [Owner: Agent]

### Research & Planning
- [Investigation 1] - [Owner: Mary]
- [Technical Spike] - [Owner: James/Alex]

## Resource Allocation
- Agent workload distribution
- External dependencies
- Risk mitigation

## Success Metrics
- Quarterly OKRs
- Feature completion targets
- Quality benchmarks
```

#### **🆓 Flexible Task Handling**
For unique planning requests:
1. **Assess task category** (strategy, requirements, process)
2. **Create appropriate subdirectory** in `planning/`
3. **Adapt PRD template** for requirement-type tasks
4. **Use strategic planning format** for high-level decisions

---

### **🔧 JAMES (Developer) - Technical Implementation**

#### **⚙️ Recurring Documentation Types**

**Technical Architecture Document** (`docs/architecture/COMPONENT-architecture.md`)
```markdown
# Technical Architecture: [Component Name]
**Agent**: James
**Created**: YYYY-MM-DD
**Type**: Technical
**Status**: [Draft/Review/Approved]
**Stakeholders**: Alex (Architecture Review), Quinn (Testing), John (Product)

## Overview
- Component purpose
- Integration with overall system
- Key design decisions

## Architecture Diagram
[Visual representation or ASCII diagram]

## Technical Specifications
- Technology stack
- Database schema (if applicable)
- API contracts
- Security considerations

## Implementation Details
- Key algorithms
- Performance considerations
- Error handling strategy

## Testing Strategy
- Unit testing approach
- Integration testing requirements
- Performance testing needs

## Deployment Considerations
- Infrastructure requirements
- Configuration management
- Monitoring and logging

## Future Considerations
- Scalability roadmap
- Technical debt items
- Enhancement opportunities
```

**Implementation Guide** (`deployment/runbooks/FEATURE-implementation.md`)
```markdown
# Implementation Guide: [Feature Name]
**Agent**: James
**Created**: YYYY-MM-DD
**Type**: Technical
**Status**: [Draft/Ready]
**Stakeholders**: Quinn (Testing), Alex (Review)

## Prerequisites
- Required dependencies
- Environment setup
- Configuration requirements

## Implementation Steps
1. [Step 1] - [Detailed instructions]
2. [Step 2] - [Expected outcomes]
3. [Step 3] - [Validation steps]

## Configuration
- Environment variables
- Database changes
- Third-party integrations

## Validation
- Functional testing steps
- Performance validation
- Security checks

## Rollback Procedure
- Rollback triggers
- Rollback steps
- Data recovery process

## Monitoring
- Key metrics to watch
- Alert thresholds
- Troubleshooting guide
```

---

### **✅ QUINN (QA Engineer) - Testing Domain**

#### **🧪 Recurring Documentation Types**

**Test Plan** (`testing/manual/test-plans/FEATURE-test-plan.md`)
```markdown
# Test Plan: [Feature Name]
**Agent**: Quinn
**Created**: YYYY-MM-DD
**Type**: Testing
**Status**: [Draft/Approved/Executed]
**Stakeholders**: James (Developer), John (Product Owner)

## Test Scope
- Features to be tested
- Features not in scope
- Testing approach

## Test Objectives
- Functional validation
- Performance benchmarks
- Security verification

## Test Cases
### Functional Tests
1. [Test Case 1]
   - **Objective**: [What we're testing]
   - **Steps**: [Detailed steps]
   - **Expected Result**: [Expected outcome]

### Edge Cases
1. [Edge Case 1]
   - **Scenario**: [Edge condition]
   - **Expected Behavior**: [How system should respond]

## Performance Tests
- Load testing requirements
- Performance benchmarks
- Stress testing scenarios

## Test Environment
- Environment requirements
- Test data needs
- Dependencies

## Success Criteria
- Pass/fail criteria
- Performance thresholds
- Quality gates
```

**Test Results Report** (`testing/results/FEATURE-test-results-YYYY-MM-DD.json`)
```json
{
  "agent": "Quinn",
  "created": "YYYY-MM-DD",
  "type": "Testing",
  "status": "Complete",
  "feature": "[Feature Name]",
  "test_summary": {
    "total_tests": 0,
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "success_rate": 0.0
  },
  "test_results": [
    {
      "test_case": "[Test Case Name]",
      "status": "PASS/FAIL",
      "execution_time": "0.5s",
      "details": "[Additional details]"
    }
  ],
  "performance_metrics": {
    "response_time_avg": "0.2s",
    "throughput": "1000 req/s",
    "error_rate": "0.1%"
  },
  "recommendations": [
    "[Recommendation 1]",
    "[Recommendation 2]"
  ]
}
```

---

### **🎨 SALLY (UX Designer) - User Experience**

#### **🎭 Recurring Documentation Types**

**UX Research Report** (`research/findings/ux-research-FEATURE-YYYY-MM-DD.md`)
```markdown
# UX Research: [Feature Name]
**Agent**: Sally
**Created**: YYYY-MM-DD
**Type**: UX Research
**Status**: [Draft/Final]
**Stakeholders**: John (Product), James (Implementation)

## Research Objectives
- User experience goals
- Usability questions
- Design validation needs

## Methodology
- Research methods used
- Participant criteria
- Data collection approach

## Key Findings
- User behavior insights
- Pain points identified
- Opportunities discovered

## Design Recommendations
- UX improvements
- Accessibility considerations
- Implementation priorities

## Next Steps
- Design iterations needed
- Additional research required
- Implementation timeline
```

**Design System Component** (`docs/design-system/COMPONENT-specification.md`)
```markdown
# Design System: [Component Name]
**Agent**: Sally
**Created**: YYYY-MM-DD
**Type**: Design System
**Status**: [Draft/Approved]
**Stakeholders**: James (Implementation), Quinn (Testing)

## Component Overview
- Purpose and usage
- Design principles
- Accessibility requirements

## Visual Specifications
- Layout requirements
- Color specifications
- Typography guidelines

## Interaction Specifications
- User interaction patterns
- State changes
- Animation requirements

## Implementation Guidelines
- HTML structure
- CSS requirements
- JavaScript interactions

## Accessibility
- WCAG compliance requirements
- Screen reader considerations
- Keyboard navigation

## Testing Requirements
- Visual regression tests
- Accessibility tests
- Cross-browser compatibility
```

---

### **🏗️ ALEX (Architect) - System Architecture**

#### **🏛️ Recurring Documentation Types**

**System Design Document** (`docs/architecture/system-design-COMPONENT.md`)
```markdown
# System Design: [Component/System Name]
**Agent**: Alex
**Created**: YYYY-MM-DD
**Type**: Architecture
**Status**: [Draft/Review/Approved]
**Stakeholders**: James (Implementation), Quinn (Testing), John (Product)

## System Overview
- High-level architecture
- Integration points
- Scalability considerations

## Design Principles
- Architectural patterns used
- Design trade-offs
- Non-functional requirements

## Component Architecture
- System components
- Component interactions
- Data flow diagrams

## Technology Decisions
- Technology stack rationale
- Alternative considerations
- Migration strategy (if applicable)

## Scalability & Performance
- Performance requirements
- Scaling strategy
- Bottleneck analysis

## Security Architecture
- Security requirements
- Authentication/authorization
- Data protection measures

## Implementation Roadmap
- Development phases
- Dependencies
- Risk mitigation
```

---

## 🚀 **Implementation Guidelines**

### **🔄 For Unique Tasks (Any Agent)**
1. **Assess task type**: Is this similar to existing documentation patterns?
2. **Choose appropriate domain**: Use your agent-owned directory
3. **Create logical structure**: Make subdirectories that make sense
4. **Follow common metadata**: Use standard document headers
5. **Inform coordination**: Let John know about new documentation patterns

### **📋 For Recurring Tasks (All Agents)**
1. **Use predefined templates** above for standard documentation
2. **Maintain consistency** in naming and structure
3. **Cross-reference** related documents from other agents
4. **Archive systematically** when work is complete

### **🤝 Cross-Agent Collaboration**
1. **Tag relevant stakeholders** in document metadata
2. **Create shared documents** in `docs/` for multi-agent work
3. **Link related documents** across domains
4. **Maintain indexes** in README.md files for easy discovery

This system gives agents **flexibility for innovation** while ensuring **consistency for routine work**! 🎯