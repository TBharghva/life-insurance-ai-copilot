# Life Insurance AI Copilot — Implementation Plan

# Goal

Deliver a stable, production-style, demo-safe AI copilot within 10 days.

Priority:

1. Graph correctness
2. Shared state
3. Human review trigger
4. RAG accuracy
5. Guardrails
6. Deployment

NOT UI polish.

---

# Team Allocation

| Member | Responsibility          |
| ------ | ----------------------- |
| Dev 1  | FastAPI + LangGraph     |
| Dev 2  | Streamlit UI            |
| Dev 3  | RAG ingestion + FAISS   |
| Dev 4  | Guardrails + evaluation |
| Dev 5  | AWS + Docker            |
| Dev 6  | Testing + LangSmith     |

---

# Day 1 — Architecture & Setup

## Tasks

- Finalize graph design
- Define shared state schema
- Setup repo structure
- Setup Docker
- Setup FastAPI boilerplate
- Setup Streamlit boilerplate
- Setup LangSmith

## Deliverables

- Repo initialized
- Graph skeleton created
- Docker builds successfully

---

# Day 2 — Dataset Ingestion

## Tasks

- Load PDFs
- Create chunking pipeline
- Create metadata schema
- Build FAISS index
- Parse CSV datasets
- Create structured lookup functions

## Deliverables

- Retrieval working
- CSV lookup working
- Citations preserved

---

# Day 3 — Intent Router + Shared State

## Tasks

- Implement LangGraph state
- Implement MemorySaver
- Implement router node
- Add hybrid routing logic
- Setup conditional edges

## Deliverables

- Multi-node graph executes
- State persists across turns

---

# Day 4 — Underwriting Agent

## Tasks

- Health intake workflow
- Risk lookup integration
- Premium estimation tool
- Risk scoring output
- High-risk detection

## Deliverables

- Underwriting flow operational
- Premium estimation working

---

# Day 5 — Policy QA Agent

## Tasks

- RAG retrieval chain
- Citation formatting
- Policy comparison prompts
- Rider explanation prompts

## Deliverables

- Policy QA functional
- Citations shown

---

# Day 6 — Beneficiary + Issuance Agents

## Tasks

- Beneficiary validation
- Minor nominee rules
- Issuance timeline retrieval
- Lapse/revival responses

## Deliverables

- Beneficiary flow working
- Issuance flow working

---

# Day 7 — Human Review + Guardrails

## Tasks

- Human review node
- Pause/resume workflow
- Prompt injection blocking
- Underwriting restriction guardrails
- Guaranteed premium guardrails

## Deliverables

- HitL functioning
- All 3 adversarial tests blocked

---

# Day 8 — UI + Trace Visualization

## Tasks

- Streamlit integration
- State display panel
- Node path display
- LangSmith integration
- Session history support

## Deliverables

- Full end-to-end app operational
- Trace visibility working

---

# Day 9 — Evaluation + Optimization

## Tasks

- Build 30-question evaluation set
- Run DeepEval
- Improve retrieval
- Improve routing accuracy
- Reduce latency
- Fix hallucinations

## Deliverables

- Faithfulness >= 0.85
- Relevancy >= 0.80
- Routing >= 90%

---

# Day 10 — Deployment + Demo Rehearsal

## Tasks

- Deploy to AWS ECS
- Validate Docker build
- Validate persistence
- Demo rehearsal
- Backup deployment
- Prepare architecture presentation

## Deliverables

- Public URL live
- Demo-ready system
- Presentation-ready traces

---

# Critical Success Criteria

## Must Work Perfectly

### Shared State

User should never repeat:

- age
- health details
- policy preference

### Human Review Trigger

Must pause graph.

### Citations

All policy answers require:

- document name
- page number
- section

### LangSmith Trace

Must visibly show:

- node transitions
- state delta
- conditional edges

---

# Risk Management

## Biggest Risks

### Intent Routing Errors

Mitigation:

- hybrid routing
- keyword rules
- confidence thresholds

### Hallucinations

Mitigation:

- strict RAG grounding
- deterministic CSV lookups
- citation enforcement

### Slow Responses

Mitigation:

- async APIs
- lightweight prompts
- small embedding model

### Broken State Persistence

Mitigation:

- test multi-turn flows daily
- validate MemorySaver continuously

---

# Recommended Demo Script

## Demo Scenario

1. Compare term vs whole life
2. Ask rider question
3. Disclose diabetes + smoking
4. Trigger high-risk review
5. Show pause
6. Resume workflow
7. Add beneficiary question
8. Show shared memory
9. Display LangSmith trace

This single flow demonstrates nearly all scoring categories.

---

# Final Recommendations

## Prioritize

- stable graph execution
- deterministic behavior
- observable state transitions
- safe outputs

## Avoid

- over-engineering
- excessive agents
- unstable autonomous workflows
- unnecessary multimodal features
