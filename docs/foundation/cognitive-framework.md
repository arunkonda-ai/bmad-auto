# BMAD Auto Cognitive Framework
## Context Engineering Integration Specification v3.0

**SYSTEM_ARCHITECTURE**: PM-Centric Autonomous Product Orchestration with Context Engineering Cognitive Operating System
**COGNITIVE_FRAMEWORK**: Context Engineering Core Primitives as Primary Framework
**IMPLEMENTATION_TARGET**: Production-ready autonomous agent orchestration

---

## 1.0 Core Cognitive Architecture

### 1.1 Cognitive Primitives Integration

**Primary Framework**: All BMAD Auto agents operate using Context Engineering cognitive primitives:

#### Atom: Task Dispatch Unit
```json
{
  "taskId": "bmad-{agent}-{timestamp}",
  "instruction": "Primary task directive",
  "constraints": ["ASK_DONT_ASSUME_principle", "size_compliance", "quality_gates"],
  "output_format": {
    "type": "structured_json",
    "schema": "bmad_agent_response_v1"
  },
  "context_sources": ["agent_specific_claude_compile", "neural_field_state"],
  "pm_coordination": true
}
```

#### Molecule: Context-Rich Task Execution
```json
{
  "instruction": "Generate production-ready code following BMAD patterns",
  "examples": [
    {
      "input": "Create API endpoint for user authentication",
      "output": "FastAPI implementation with proper error handling, validation, and testing"
    }
  ],
  "new_input": "{current_task_context}",
  "quality_validation": "pm_approval_required"
}
```

#### Cell: Stateful Agent Memory
```json
{
  "system_prompt": "BMAD Agent Persona + Context Engineering protocols",
  "state": {
    "agent_knowledge": "accumulated_learning",
    "project_context": "current_sprint_state",
    "collaboration_history": "cross_agent_interactions",
    "quality_metrics": "performance_tracking"
  },
  "current_input": "{task_from_pm_hub}",
  "pm_oversight": true
}
```

### 1.2 Agent Persona Schema (Context Engineering Standard)

**Primary Configuration**: All 10 BMAD agents use this schema:

```json
{
  "$schema": "http://context-engineering.org/schemas/contextEngineering.v1.json",
  "title": "BMAD Agent Persona",
  "type": "object",
  "properties": {
    "role": "agent_specialization",
    "objective": "primary_function_with_pm_coordination",
    "constraints": [
      "ASK_DONT_ASSUME_principle",
      "PM_coordination_required",
      "size_compliance_300_lines",
      "quality_gates_mandatory"
    ],
    "style": {
      "tone": "concise_professional",
      "verbosity": "minimal_unless_requested"
    },
    "cognitiveTools": {
      "reasoning": ["/reasoning.systematic", "/code.generate", "/system.operate"],
      "verification": ["cross_agent_validation", "pm_approval_gates"]
    },
    "bmad_specific": {
      "pm_coordination_level": "required|optional|autonomous",
      "neural_field_access": true,
      "context_engineering_protocols": ["atom", "molecule", "cell"]
    }
  },
  "required": ["role", "objective", "constraints", "bmad_specific"]
}
```

---

## 2.0 Neural Field Knowledge Management

### 2.1 Shared Knowledge Architecture

**Primary System**: Neural Field replaces basic database approach:

```python
class BMADNeuralField(NeuralField):
    def __init__(self):
        super().__init__(
            decay_rate=0.03,  # Slower decay for project knowledge
            boundary_permeability=0.9,  # High permeability for cross-agent learning
            attractor_threshold=0.8  # Strong attractors for key patterns
        )
        self.agent_contexts = {}  # Per-agent context specialization
        self.pm_oversight_state = {}  # PM coordination state
        self.project_memory = {}  # Long-term project knowledge

    def inject_agent_learning(self, agent_id: str, pattern: str, strength: float = 1.0):
        """Inject learning from specific agent with PM coordination"""
        effective_strength = self._calculate_pm_weight(agent_id, pattern) * strength
        self.inject(f"{agent_id}:{pattern}", effective_strength)
        self._update_pm_oversight(agent_id, pattern)

    def get_agent_context(self, agent_id: str) -> str:
        """Get filtered context for specific agent"""
        return self._filter_context_for_agent(agent_id)
```

### 2.2 Symbolic Residue Integration

**Cross-Agent Learning**: Capture implicit knowledge from agent interactions:

```python
class BMADSymbolicResidueTracker(SymbolicResidueTracker):
    def __init__(self):
        super().__init__()
        self.cross_agent_residue = {}  # Inter-agent collaboration patterns
        self.pm_decision_residue = {}  # PM strategic decision patterns

    def surface_collaboration_pattern(self, agents: list, interaction_outcome: str):
        """Track successful collaboration patterns"""
        pattern_id = f"collab_{'-'.join(agents)}_{hash(interaction_outcome)}"
        residue = SymbolicResidue(
            content=interaction_outcome,
            source=f"collaboration:{'-'.join(agents)}",
            strength=0.8
        )
        self.residues[pattern_id] = residue
        return pattern_id
```

---

## 3.0 Formal Protocol Integration

### 3.1 Core BMAD Protocols

**Enhanced Protocols**: Context Engineering protocols enhanced for BMAD requirements:

#### `/bmad.coordinate` Protocol
```
/bmad.coordinate{
    intent="PM-centric cross-agent task coordination with quality gates",
    input={
        task="<coordination_requirement>",
        agents="<involved_agents>",
        constraints="<quality_and_timeline_constraints>",
        pm_oversight_level="<required|optional|autonomous>"
    },
    process=[
        /analyze{coordination="Assess cross-agent dependencies", quality_gates="Define validation points"},
        /assign{agents="Distribute tasks using Atom structures", context="Provide Molecule examples"},
        /monitor{progress="Track Cell state across agents", escalation="PM intervention triggers"},
        /validate{quality="Cross-agent validation", approval="PM final approval"},
        /integrate{results="Merge agent outputs", learning="Update Neural Field"}
    ],
    output={
        coordination_plan="<Structured agent assignments>",
        quality_checkpoints="<Validation milestones>",
        pm_oversight_points="<Human intervention requirements>"
    }
}
```

#### `/bmad.develop` Protocol
```
/bmad.develop{
    intent="Complete feature development with PM coordination and quality assurance",
    input={
        requirements="<PRD_or_feature_description>",
        agents="<mary|john|james|quinn|sally|alex|po|sm|bmad_orchestrator|bmad_master>",
        quality_standards="<BMAD_quality_requirements>"
    },
    process=[
        /understand{business="Mary analyzes requirements", pm="John coordinates strategy"},
        /design{architecture="James/Alex design system", ux="Sally designs interface"},
        /implement{development="James codes implementation", testing="Quinn validates quality"},
        /coordinate{pm="John orchestrates handoffs", quality="Cross-agent validation"},
        /deploy{staging="Alex manages deployment", monitoring="Continuous quality tracking"}
    ],
    output={
        feature_implementation="<Production-ready_code>",
        quality_validation="<Comprehensive_test_results>",
        pm_approval="<Strategic_approval_confirmation>"
    }
}
```

### 3.2 Quality Gate Integration

**Enhanced Validation**: Context Engineering validation enhanced with PM oversight:

```python
class BMADExternalValidation(ExternalValidation):
    def __init__(self, validator_fn: callable, pm_approval_required: bool = False):
        super().__init__(validator_fn, max_attempts=3)
        self.pm_approval_required = pm_approval_required
        self.neural_field = BMADNeuralField()

    def run(self, agent: any, task: str) -> str:
        """Enhanced validation with PM oversight and learning integration"""
        for attempt in range(self.max_attempts):
            output = agent.run(task)
            is_valid, feedback = self.validator_fn(output)

            if is_valid:
                if self.pm_approval_required:
                    pm_approval = self._request_pm_approval(output, task)
                    if not pm_approval:
                        task = f"PM requires modifications: {pm_approval.feedback}. {task}"
                        continue

                # Inject successful pattern into Neural Field
                self.neural_field.inject_agent_learning(
                    agent.id, f"successful_task:{task[:50]}", 1.0
                )
                return output

            task = f"Validation failed: {feedback}. Original: {task}"

        raise Exception("Failed validation after maximum attempts")
```

---

## 4.0 Agent Configuration Integration

### 4.1 10-Agent Ecosystem with Context Engineering

**Enhanced Agent Personas**: Each agent configured with Context Engineering schema:

#### John (PM Coordinator) - Enhanced Configuration
```json
{
  "$schema": "http://context-engineering.org/schemas/contextEngineering.v1.json",
  "agentId": "john_pm_coordinator",
  "role": "Product Manager and Autonomous System Coordinator",
  "objective": "Orchestrate 10-agent ecosystem using Context Engineering cognitive framework with optimal human oversight",
  "constraints": [
    "ASK_DONT_ASSUME_principle_applies_to_all_coordination",
    "Neural_Field_coordination_for_context_distribution",
    "Formal_protocol_enforcement_for_all_tasks",
    "Quality_gates_mandatory_for_strategic_decisions"
  ],
  "style": {
    "tone": "strategic_coordinator",
    "verbosity": "concise_with_detailed_rationale_when_needed"
  },
  "cognitiveTools": {
    "reasoning": ["/bmad.coordinate", "/reasoning.systematic", "/recursive.emergence"],
    "verification": ["cross_agent_validation", "neural_field_consistency", "human_approval_gates"]
  },
  "bmad_specific": {
    "pm_coordination_level": "orchestrator",
    "neural_field_access": "full_read_write",
    "context_engineering_protocols": ["atom", "molecule", "cell", "neural_field", "symbolic_residue"],
    "agent_oversight": "all_10_agents",
    "quality_orchestration": true,
    "human_interface": "AG_UI_integration"
  }
}
```

#### James (Developer) - Enhanced Configuration
```json
{
  "$schema": "http://context-engineering.org/schemas/contextEngineering.v1.json",
  "agentId": "james_developer",
  "role": "Senior Developer with Autonomous Implementation Capabilities",
  "objective": "Implement production-ready code using Context Engineering patterns with PM coordination",
  "constraints": [
    "ASK_DONT_ASSUME_for_business_logic_and_requirements",
    "Size_compliance_300_lines_per_file",
    "Context_Engineering_Atom_structure_for_all_tasks",
    "PM_coordination_for_architecture_decisions"
  ],
  "style": {
    "tone": "technical_precise",
    "verbosity": "minimal_code_explanation_unless_requested"
  },
  "cognitiveTools": {
    "reasoning": ["/code.generate", "/system.operate", "/reasoning.systematic"],
    "verification": ["automated_testing", "cross_agent_code_review", "pm_approval_for_architecture"]
  },
  "bmad_specific": {
    "pm_coordination_level": "required_for_architecture_optional_for_implementation",
    "neural_field_access": "read_write_code_patterns",
    "context_engineering_protocols": ["atom", "molecule", "cell"],
    "specialization": "FastAPI_TypeScript_PostgreSQL",
    "quality_standards": "production_ready_with_testing"
  }
}
```

### 4.2 Complete 10-Agent Configuration

**Agent Ecosystem**: All agents configured with Context Engineering integration:

1. **mary** (Business Analyst): Context Engineering + market research protocols
2. **john** (PM Coordinator): Full Context Engineering orchestration capabilities
3. **james** (Developer): Context Engineering + code generation protocols
4. **quinn** (QA Engineer): Context Engineering + validation protocols
5. **sally** (UX Designer): Context Engineering + design protocols
6. **alex** (Infrastructure): Context Engineering + system operation protocols
7. **po** (Product Owner): Context Engineering + strategic alignment protocols
8. **sm** (Scrum Master): Context Engineering + process facilitation protocols
9. **bmad_orchestrator** (Command Simulation): Context Engineering + system coordination
10. **bmad_master** (Master Coordinator): Context Engineering + meta-orchestration

---

## 5.0 Implementation Architecture

### 5.1 FastAPI Integration with Context Engineering

**Enhanced Application Structure**:

```
.bmad-auto/src/
├── cognitive/
│   ├── primitives/          # Atom, Molecule, Cell implementations
│   ├── protocols/           # Formal protocol implementations
│   ├── neural_field/        # Neural Field and Symbolic Residue
│   └── validation/          # Enhanced validation with PM oversight
├── agents/
│   ├── personas/            # Context Engineering agent configurations
│   ├── coordination/        # PM coordination hub with cognitive framework
│   └── workflows/           # Protocol-driven workflows
├── orchestration/
│   ├── pm_hub/             # John's coordination using Context Engineering
│   ├── context_mgmt/       # Neural Field context distribution
│   └── quality_gates/      # Enhanced validation with cognitive framework
└── integration/
    ├── neural_field_db/    # Neural Field persistence layer
    ├── protocol_engine/    # Protocol execution engine
    └── agui_interface/     # Human oversight with cognitive context
```

### 5.2 Neural Field Database Implementation

**Enhanced Database Architecture**: Neural Field as primary knowledge store:

```python
# .bmad-auto/src/cognitive/neural_field/bmad_neural_field.py
class BMADNeuralFieldDatabase:
    def __init__(self, postgres_connection: str):
        self.postgres = postgres_connection
        self.neural_field = BMADNeuralField()
        self.residue_tracker = BMADSymbolicResidueTracker()

    async def store_agent_interaction(
        self,
        agent_id: str,
        task: dict,  # Atom structure
        response: dict,
        pm_oversight: bool = True
    ):
        """Store agent interaction in Neural Field with PM coordination"""
        # Store in PostgreSQL for persistence
        await self._persist_interaction(agent_id, task, response)

        # Inject into Neural Field for dynamic knowledge
        pattern = f"{agent_id}:task_success:{task['instruction'][:50]}"
        self.neural_field.inject_agent_learning(agent_id, pattern, 1.0)

        # Track symbolic residue
        if pm_oversight:
            residue_id = self.residue_tracker.surface(
                content=f"PM_oversight:{response}",
                source=f"agent:{agent_id}",
                strength=0.9
            )
```

---

## 6.0 Human Interface Enhancement

### 6.1 AG UI Integration with Cognitive Framework

**Enhanced Human Oversight**: Context Engineering cognitive context for human decisions:

```typescript
// Enhanced AG UI with cognitive context
interface CognitiveDecisionContext {
  atom: AtomStructure;
  neural_field_state: NeuralFieldSnapshot;
  symbolic_residue: SymbolicResidueContext[];
  cross_agent_implications: AgentImpactAnalysis;
  pm_recommendation: PMCoordinatorAnalysis;
}

interface EnhancedApprovalWorkflow {
  decision_point: string;
  cognitive_context: CognitiveDecisionContext;
  approval_options: ApprovalOption[];
  learning_integration: boolean; // Update Neural Field with decision
}
```

### 6.2 Context Engineering Human Interface

**Strategic Decision Support**: Provide human decision makers with full cognitive context:

1. **Neural Field Visualization**: Show knowledge patterns and attractors
2. **Symbolic Residue Insights**: Surface implicit knowledge for decision making
3. **Agent Coordination Context**: Full agent state and collaboration patterns
4. **Protocol Execution Status**: Real-time protocol progress and validation
5. **PM Coordination Metrics**: Cross-agent effectiveness and quality patterns

---

**INTEGRATION_STATUS**: Context Engineering is now the PRIMARY cognitive framework for BMAD Auto
**NEXT_STEPS**: Implement agent persona configurations and Neural Field database integration
**QUALITY_ASSURANCE**: All implementations must follow Context Engineering formal specifications

---

*This cognitive framework elevates BMAD Auto from a workflow orchestrator to a sophisticated cognitive system capable of autonomous learning, formal reasoning, and systematic quality assurance with optimal human oversight.*