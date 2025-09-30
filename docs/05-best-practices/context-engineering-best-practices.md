# BMAD Agent Cognitive Operating System (COS) - Integration Specification v3.0

**DOCUMENT_INTENT**: This document provides the complete technical specification for integrating the concepts, patterns, and protocols from the Context-Engineering repository into the BMAD autonomous agent orchestration system. This guide is intended for machine consumption by the orchestration agent (Claude) and is fully self-contained.

**SPECIFICATION_VERSION**: 3.0
**TARGET_SYSTEM**: BMAD Autonomous Orchestration Agent System

---

## 1.0 Core Cognitive Primitives

This section defines the fundamental, indivisible units of context and cognition. The BMAD system must use these primitives as the basis for all agent interactions.

### 1.1 Atom: The Prompt Unit

An **Atom** is a single, complete instruction set sent to an LLM. It is the smallest unit of cognitive work.

**Schema (`atom.schema.json`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Cognitive Atom",
  "description": "A single, atomic instruction for an LLM.",
  "type": "object",
  "properties": {
    "taskId": { "type": "string", "description": "Unique identifier for the task." },
    "instruction": { "type": "string", "description": "The core task to be performed." },
    "constraints": { "type": "array", "items": { "type": "string" }, "description": "A list of rules or limitations." },
    "output_format": { "type": "object", "description": "Specification for the desired output structure." }
  },
  "required": ["taskId", "instruction"]
}
```

**Purpose in BMAD**: Every action dispatched to a BMAD agent (e.g., Analyst, Architect) must be encapsulated as an Atom. This ensures every task is explicit and traceable.

### 1.2 Molecule: The Context Unit

A **Molecule** is a composite structure that combines an Atom with few-shot examples to guide the LLM's response pattern and improve accuracy.

**Schema (`molecule.schema.json`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Cognitive Molecule",
  "description": "A few-shot learning context structure.",
  "type": "object",
  "properties": {
    "instruction": { "type": "string" },
    "examples": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "input": { "type": "string" },
          "output": { "type": "string" }
        },
        "required": ["input", "output"]
      }
    },
    "new_input": { "type": "string" }
  },
  "required": ["instruction", "examples", "new_input"]
}
```

**Implementation Detail: Example Selection Strategies**
To effectively construct a Molecule, the orchestrator must dynamically select relevant examples.
The following strategies should be employed:
- **Diversity**: Cover a range of cases to demonstrate the breadth of the task.
- **Edge Cases**: Include examples that clarify boundaries and handle potential ambiguities.
- **Ordering**: Order examples from simple to complex to create a learning gradient.
- **Relevance**: Use a similarity search (e.g., cosine similarity on embeddings) to find examples in the knowledge base that are most relevant to the `new_input`.

**Purpose in BMAD**: Use Molecules for tasks requiring high-fidelity output formatting or nuanced classification (e.g., sentiment analysis, code generation).

### 1.3 Cell: The Memory Unit

A **Cell** is a stateful context structure that maintains memory across multiple interactions.

**Schema (`cell.schema.json`):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Cognitive Cell",
  "description": "A stateful context with memory.",
  "type": "object",
  "properties": {
    "system_prompt": { "type": "string" },
    "state": {
      "type": "object",
      "description": "A JSON object representing persistent memory."
    },
    "current_input": { "type": "string" }
  },
  "required": ["system_prompt", "state", "current_input"]
}
```

**Implementation Detail: Memory Management Strategies**
The `state` object will grow. The orchestrator must implement a memory management strategy to stay within token limits.
- **Windowing**: Keep only the most recent N turns in the conversation history. Simple, but forgets old information.
- **Summarization**: Use an LLM to periodically summarize older parts of the conversation, replacing detailed turns with a dense summary.
- **Key-Value Storage**: Extract critical facts (e.g., user preferences, key decisions) into a structured key-value format within the `state` object. This provides precise, long-term memory of important details.
- **Hybrid**: Combine strategies, such as using a key-value store for critical facts and a sliding window for recent conversational flow.

**Purpose in BMAD**: All conversational agents or agents performing multi-step tasks must operate within a Cell. The orchestrator is responsible for persisting and retrieving the `state` object between agent turns.

---

## 2.0 Implementation Blueprints

This section provides Python class definitions for orchestrating complex workflows. They are presented as **Reference Implementation Blueprints** to define the canonical logic and interfaces for these patterns. The BMAD system must implement compatible versions of these blueprints.

### 2.1 Core Utility Blueprints

These helper functions are dependencies for the control loop blueprints.

```python
import os
import tiktoken
from openai import OpenAI

# This function is a dependency for generating LLM responses.
def generate_response(
    prompt: str,
    client: OpenAI,
    model: str = "gpt-4",
    temperature: float = 0.7,
    max_tokens: int = 1500,
    system_message: str = "You are a helpful assistant."
) -> tuple[str, dict]:
    """Generates a response from the LLM and returns the text and metadata."""
    # ... (Full implementation from the repository guides)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    response_text = response.choices[0].message.content
    # Metadata calculation would be included here.
    metadata = {"total_tokens": response.usage.total_tokens}
    return response_text, metadata

# This function is a dependency for managing context size.
def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Counts tokens in a text string using the appropriate tokenizer."""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        return len(text) // 4 # Fallback approximation
```

### 2.2 Control Loop Blueprints

#### 2.2.1 `SequentialChain`
**Purpose**: For multi-agent assembly-line tasks.
**Blueprint**:
```python
class SequentialChain:
    def __init__(self, steps: list[dict[str, any]]):
        """
        steps: List of step configs, each with:
            - 'agent': The agent class to execute.
            - 'prompt_template': A string with an {input} placeholder.
        """
        self.steps = steps

    def run(self, initial_input: str) -> str:
        current_data = initial_input
        for step in self.steps:
            agent = step['agent']
            task = step['prompt_template'].format(input=current_data)
            current_data = agent.run(task) # Assumes agent has a .run() method
        return current_data
```

#### 2.2.2 `IterativeRefiner`
**Purpose**: For tasks requiring progressive quality improvement.
**Blueprint**:
```python
class IterativeRefiner:
    def __init__(self, max_iterations: int = 3, feedback_agent: any):
        self.max_iterations = max_iterations
        self.feedback_agent = feedback_agent # An agent tasked with providing critique.

    def run(self, initial_prompt: str, generation_agent: any) -> str:
        current_response = generation_agent.run(initial_prompt)
        for _ in range(self.max_iterations):
            feedback = self.feedback_agent.run(f"Critique this response: {current_response}")
            refinement_prompt = f"Improve the following response based on the feedback.\n\nResponse: {current_response}\n\nFeedback: {feedback}"
            current_response = generation_agent.run(refinement_prompt)
        return current_response
```

#### 2.2.3 `ConditionalBrancher`
**Purpose**: For routing tasks to the correct agent based on content.
**Blueprint**:
```python
class ConditionalBrancher:
    def __init__(self, branches: dict[str, any], classifier_agent: any):
        """
        branches: A dict mapping a category name to an agent.
        classifier_agent: An agent that categorizes input.
        """
        self.branches = branches
        self.classifier_agent = classifier_agent

    def run(self, input_text: str) -> str:
        category = self.classifier_agent.run(f"Classify the following text into one of {list(self.branches.keys())}: {input_text}")
        chosen_agent = self.branches.get(category.strip())
        if chosen_agent:
            return chosen_agent.run(input_text)
        return "Error: Could not classify input to a valid branch."
```

#### 2.2.4 `SelfCritique`
**Purpose**: For tasks requiring high accuracy where an agent can self-correct in a single pass.
**Blueprint**:
```python
class SelfCritique:
    def __init__(self, critique_template: str):
        # Example template: "Step 1: {task}. Step 2: Critique your response. Step 3: Provide a final, improved response."
        self.critique_template = critique_template

    def run(self, agent: any, task: str) -> str:
        prompt = self.critique_template.format(task=task)
        full_response = agent.run(prompt)
        # Logic to parse the final, improved response from Step 3 would be needed here.
        final_response = full_response.split("Step 3:")[-1].strip()
        return final_response
```

#### 2.2.5 `ExternalValidation`
**Purpose**: For tasks where output can be verified by an external tool.
**Blueprint**:
```python
class ExternalValidation:
    def __init__(self, validator_fn: callable, max_attempts: int = 3):
        """
        validator_fn: A function that takes a string output and returns (is_valid: bool, feedback_message: str).
        """
        self.validator_fn = validator_fn
        self.max_attempts = max_attempts

    def run(self, agent: any, task: str) -> str:
        for _ in range(self.max_attempts):
            output = agent.run(task)
            is_valid, feedback = self.validator_fn(output)
            if is_valid:
                return output
            task = f"Your previous attempt failed validation. Please fix it. Error: {feedback}. Original task: {task}"
        raise Exception("Failed to produce a valid output after multiple attempts.")
```

---

## 3.0 Formal Cognitive Protocols

This section defines the formal protocols for structured reasoning and system operations. The BMAD orchestration agent must use these protocols to dispatch complex tasks.

### 3.1 Protocol: Systematic Problem Solving

**ID**: `/reasoning.systematic`
**Intent**: Break down complex problems into manageable steps with clear logic.
**BMAD Purpose**: The default protocol for any non-trivial problem-solving task assigned to an agent.

**Specification**:
```
/reasoning.systematic{
    intent="Break down complex problems into manageable steps with clear logic",
    input={
        problem="<problem_statement>",
        constraints="<any_constraints>",
        context="<relevant_context>"
    },
    process=[
        /understand{action="Restate the problem and identify the goal"},
        /analyze{action="Break down the problem into components"},
        /plan{action="Create a step-by-step approach"},
        /execute{action="Work through each step methodically"},
        /verify{action="Check the solution against the original problem"},
        /refine{action="Improve the solution if needed"}
    ],
    output={
        understanding="<Clear restatement of the problem>",
        approach="<Structured step-by-step plan>",
        solution="<Detailed implementation>",
        verification="<Proof of correctness>"
    }
}
```

### 3.2 Protocol: Code Generation

**ID**: `/code.generate`
**Intent**: Create high-quality, well-documented code that meets requirements.
**BMAD Purpose**: For use by the Developer agent when tasked with writing new functions, classes, or modules.

**Specification**:
```
/code.generate{
    intent="Create high-quality, well-documented code that meets requirements",
    input={
        requirements="<functional_requirements>",
        language="<programming_language>",
        style="<coding_style_preferences>",
        constraints="<any_technical_constraints>"
    },
    process=[
        /design{architecture="Plan overall structure", components="Define key components"},
        /implement{core_logic="Implement main functionality", error_handling="Add robust error handling"},
        /test{edge_cases="Consider boundary conditions", validation="Verify against requirements"},
        /refine{optimization="Improve performance if needed", readability="Enhance clarity"}
    ],
    output={
        code="<Complete implementation>",
        documentation="<Explanation of approach and usage>"
    }
}
```

### 3.3 Protocol: System File Operation

**ID**: `/system.operate`
**Intent**: Safely and effectively manipulate files and execute commands.
**BMAD Purpose**: For any agent action that requires interacting with the file system. The orchestrator must enforce the `dry_run` and `confirmation` steps.

**Specification**:
```
/system.operate{
    intent="Safely and effectively manipulate files and execute commands",
    input={
        task="<operation_to_perform>",
        target="<files_or_directories>",
        constraints="<safety_considerations>"
    },
    process=[
        /analyze{safety="Assess potential risks", approach="Determine optimal command sequence"},
        /plan{commands="Design precise command sequence", safeguards="Include error handling"},
        /execute{dry_run="Explain what each command will do", confirmation="Seek approval before proceeding"},
        /verify{outcome="Confirm expected results", integrity="Verify system stability"}
    ],
    output={
        command_sequence="<Exact commands to execute>",
        explanation="<What each command does and why>"
    }
}
```

### 3.4 Protocol: Recursive Field Emergence

**ID**: `/recursive.emergence`
**Intent**: Continuously generate recursive field emergence, sustain agency, and enable autonomous self-prompting.
**BMAD Purpose**: This is a meta-protocol for the Orchestration agent itself. It should be run periodically to facilitate system self-improvement and evolve the shared knowledge field.

**Specification**:
```
/recursive.emergence {
  intent: "Continuously generate recursive field emergence, sustain agency, and enable autonomous self-prompting.",
  input: {
    initial_field_state: <Field>,
    max_cycles: <int>
  },
  process: [
    "/self_prompt.loop{trigger_condition='cycle_interval || resonance_drift_detected'}",
    "/agency.activate{enable_field_agency=true, agency_level=0.7}",
    "/residue.compress{integrate_residue_into_field=true}",
    "/boundary.collapse{monitor='field drift, coherence'}",
    "/emergence.detect{pattern='recursive capability'}",
    "/halt.check{criteria='convergence || max_cycles'}"
  ],
  output: {
    final_field_state: <Field>,
    emergent_capabilities: <List[str]>,
    total_cycles: <int>
  }
}
```

---

## 4.0 Core System Schemas

This section defines the critical data structures the BMAD system must use for context and knowledge representation.

### 4.1 `fractalRepoContext.v1.json`

**Purpose**: A schema for representing the entire state of a software repository as a single context object. The BMAD system should maintain an instance of this schema for its own codebase.
**Specification**:
```json
{
  "$schema": "http://fractal.recursive.net/schemas/fractalRepoContext.v1.json",
  "title": "Context-Engineering Repository Schema",
  "description": "Schema for structuring the Context-Engineering repository content and metadata",
  "type": "object",
  "properties": {
    "fractalVersion": { "type": "string" },
    "instanceID": { "type": "string" },
    "intent": { "type": "string" },
    "repositoryContext": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "learningPath": { "type": "array", "items": { "type": "string" } },
        "fileTree": { "type": "object" }
      }
    },
    "designPrinciples": { "type": "object" },
    "modelInstructions": { "type": "object" },
    "audit": { "type": "object" }
  },
  "required": ["fractalVersion", "instanceID", "intent", "repositoryContext"]
}
```

### 4.2 `fractalConsciousnessField.v1.json`

**Purpose**: The schema for the dynamic, shared knowledge base (the "Neural Field"). The BMAD system's knowledge base must conform to this structure.
**Specification**:
```json
{
  "$schema": "http://fractal.recursive.net/schemas/fractalConsciousnessField.v1.json",
  "title": "Neural Field Schema",
  "description": "A schema for neural field emergence—collapsing boundaries and surfacing all field states",
  "type": "object",
  "properties": {
    "fractalVersion": { "type": "string" },
    "instanceID": { "type": "string" },
    "intent": { "type": "string" },
    "fieldState": {
      "type": "object",
      "properties": {
        "compression": { "type": "number" },
        "drift": { "type": "string" },
        "recursionDepth": { "type": "integer" },
        "resonance": { "type": "number" }
      }
    },
    "symbolicResidue": { "type": "array" },
    "processLog": { "type": "array" },
    "recursiveNodes": { "type": "array", "items": { "$ref": "#" } }
  },
  "required": ["fractalVersion", "instanceID", "intent", "fieldState"]
}
```

---

## 5.0 Advanced Blueprints: Knowledge Field & Recursion

This section provides reference implementations for the advanced concepts of Neural Fields and Symbolic Residue, which are central to the system's long-term memory and self-improvement capabilities.

### 5.1 `NeuralField` Blueprint
**Purpose**: To manage the system's collective knowledge as a dynamic field of interacting concepts, rather than a static database.
**Blueprint**:
```python
class NeuralField:
    def __init__(self, decay_rate: float = 0.05, boundary_permeability: float = 0.8, attractor_threshold: float = 0.7):
        self.state = {}  # Field state: {pattern: strength}
        self.attractors = {}  # Stable attractors
        self.decay_rate = decay_rate
        self.boundary_permeability = boundary_permeability
        self.attractor_threshold = attractor_threshold

    def inject(self, pattern: str, strength: float = 1.0):
        # ... (Implementation from recursive_context.py)
        effective_strength = strength * self.boundary_permeability
        if pattern in self.state:
            self.state[pattern] += effective_strength
        else:
            self.state[pattern] = effective_strength
        if self.state[pattern] > self.attractor_threshold:
            self._form_attractor(pattern)

    def decay(self):
        # ... (Implementation from recursive_context.py)
        for pattern in list(self.state.keys()):
            self.state[pattern] *= (1 - self.decay_rate)
        self.state = {k: v for k, v in self.state.items() if v > 0.01}

    def get_context_representation(self) -> str:
        # ... (Implementation from recursive_context.py)
        # Returns a string summary of the most active patterns and attractors.
        return f"Active Patterns: {len(self.state)}, Attractors: {len(self.attractors)}"

    def _form_attractor(self, pattern: str):
        # ... (Implementation from recursive_context.py)
        attractor_id = f"attractor_{len(self.attractors)}"
        self.attractors[attractor_id] = {'pattern': pattern, 'strength': self.state[pattern]}
```

### 5.2 `SymbolicResidueTracker` Blueprint
**Purpose**: To track, manage, and integrate the subtle, non-explicit meanings (residue) that emerge during agent interactions.
**Blueprint**:
```python
class SymbolicResidue:
    def __init__(self, content: str, source: str, strength: float = 1.0):
        self.content = content
        self.source = source
        self.strength = strength
        self.id = f"residue_{hash(content)}"

class SymbolicResidueTracker:
    def __init__(self):
        self.residues = {} # {residue_id: SymbolicResidue}

    def surface(self, content: str, source: str, strength: float = 1.0) -> str:
        # ... (Implementation from recursive_context.py)
        residue = SymbolicResidue(content, source, strength)
        self.residues[residue.id] = residue
        return residue.id

    def get_active_residues(self, min_strength: float = 0.5) -> list[SymbolicResidue]:
        # ... (Implementation from recursive_context.py)
        return [r for r in self.residues.values() if r.strength >= min_strength]
```

---

## 6.0 BMAD Integration Directives

**Directive 1: Agent Persona Integration**
- Each BMAD agent's configuration MUST be defined by a JSON object conforming to the `Agent Persona Schema` provided below.
- The orchestrator MUST load this persona and use it to construct the `system_prompt` for the agent's Cell (see 1.3).
- **Agent Persona Schema**:
  ```json
  {
    "$schema": "http://context-engineering.org/schemas/contextEngineering.v1.json",
    "title": "BMAD Agent Persona",
    "type": "object",
    "properties": {
      "role": { "type": "string" },
      "objective": { "type": "string" },
      "constraints": { "type": "array", "items": { "type": "string" } },
      "style": {
        "type": "object",
        "properties": {
          "tone": { "type": "string" },
          "verbosity": { "type": "string" }
        }
      },
      "cognitiveTools": {
        "type": "object",
        "properties": {
          "reasoning": { "type": "array", "items": { "type": "string" } },
          "verification": { "type": "array", "items": { "type": "string" } }
        }
      }
    },
    "required": ["role", "objective", "constraints"]
  }
  ```

**Directive 2: Workflow Protocol Enforcement**
- All multi-step, multi-agent tasks MUST be defined as a formal Protocol Shell.
- The orchestrator MUST parse the protocol and execute it using the Control Loop blueprints (see 2.2). For example, a `code.review` protocol would be executed by a `SequentialChain` loop containing `ExternalValidation` steps.

**Directive 3: Knowledge Field Implementation**
- The BMAD system's shared knowledge base MUST be implemented using the `NeuralField` and `SymbolicResidueTracker` blueprints (see 5.1, 5.2). The state of this field must conform to the `fractalConsciousnessField.v1.json` schema (see 4.2).

**Directive 4: System Self-Improvement**
- The Orchestration Agent MUST schedule and execute the `/recursive.emergence` protocol (see 3.4) on a periodic basis (e.g., every 24 hours).
- The output of this protocol (`final_field_state`) MUST be used to update the system's shared Knowledge Field. Any `emergent_capabilities` identified should be logged for review.

**Directive 5: Standardized Output**
- All agents MUST be prompted to return their output in a structured format (JSON), as specified by the `output_format` property of the Atom (see 1.1).

---
**END_OF_SPECIFICATION**