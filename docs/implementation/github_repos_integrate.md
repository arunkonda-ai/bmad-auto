# BMAD Project — Recommended GitHub Repos (Claude-Readable Guide)

This document lists carefully selected GitHub repositories useful for building the BMAD multi-agent system for AI application development. It is written in a **Claude-readable, structured format** with clear WHAT, WHY, WHERE, STRENGTH, and WHY-NOT sections so Claude can load and reason over them.

---

## 1. inngest/inngest
**Url:** https://github.com/inngest/inngest
**Category:** Must-Have  
**What:** Serverless workflow orchestrator  
**Why Use:** Triggers stateful, event-driven pipelines with retries and error handling  
**Where to Use:** Core engine for PRD → Story → PR → Deploy flows  
**Strength:** Production-ready, low-latency, integrates with GitHub Actions  
**Why Not Use:** Adds infra complexity if GitHub Actions alone is sufficient
**Huma Decision:** Implement only if you recommend in Phase 1 or move it to later phase.

---

## 2. protocolbuffers/protobuf
**Url:** https://github.com/protocolbuffers/protobuf
**Category:** Must-Have  
**What:** Data serialization and schema enforcement  
**Why Use:** Define strict agent-to-agent message contracts; cross-language, versionable  
**Where to Use:** Architect defines schema contracts, Dev + QA enforce in CI  
**Strength:** Reliable, fast, widely supported  
**Why Not Use:** Schema maintenance overhead if JSON/YAML is sufficient



---

## 4. OpenBMB/RepoAgent
**Url:** https://github.com/OpenBMB/RepoAgent
**Category:** Good-to-Have  
**What:** LLM agent to explore repos & generate documentation  
**Why Use:** Automatically enrich KB, summarize repos, discover APIs  
**Where to Use:** Analyst + Architect for onboarding new tech stacks  
**Strength:** Context-rich summaries, speeds up discovery  
**Why Not Use:** Early-stage, may need tuning for accuracy and stability

---

## 5. SciPhi-AI/agent-search
**Url:** https://github.com/SciPhi-AI/agent-search
**Category:** Experimental  
**What:** Semantic search powered by LLM agents  
**Why Use:** Build semantic search over KB, docs, and external sources  
**Where to Use:** Analyst + Dev for rapid knowledge lookup  
**Strength:** Hybrid of LLM + search, better recall than keyword search  
**Why Not Use:** Higher latency/cost, not production hardened

---

## 7. context-engineering/context-engineering (Optional Addition)
**Url:** https://github.com/context-engineering/context-engineering
**Category:** Good-to-Have  
**What:** Framework for context design & prompt architecture  
**Why Use:** Strengthens agent prompts, improves precision, reduces hallucinations  
**Where to Use:** Shared common-instructions layer, prompt templates  
**Strength:** Adds systematic context strategy across all BMAD agents  
**Why Not Use:** Adds complexity if LangGraph context control alone is sufficient


---

## 8. LangFuse (Observability)
**Url:** https://github.com/inngest/inngest
**Category:** Must-Have (Observability Layer)  
**What:** Open-source LLM observability & tracing  
**Why Use:** Track agent calls, latency, cost, errors, and success rate  
**Where to Use:** BMAD Orchestrator, QA, Architect to monitor system health  
**Strength:** Self-hostable, integrates with LangChain/LangGraph  
**Why Not Use:** Requires infra setup (DB + UI); overhead if project is very small

---


### Key Principle:
Use **Inngest + Protobuf + LangFuse** as your foundation. Layer **PostHog, RepoAgent, Context-Engineering** as enablers. Use **agent-search + agent-os** for experimentation.

---

### Decision Logic:
- **Keep table current** — when adding new repos, include WHAT/WHY/WHERE/WHY-NOT so BMAD agents can reason about adoption.
- **Use this file as /kb/repos-decision.md** so Orchestrator agent can check before suggesting adoption of any tool.
