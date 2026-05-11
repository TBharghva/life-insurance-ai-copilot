# Life Insurance AI Copilot — Compact AI Context

## Project Summary

Production-grade Life Insurance AI Copilot using LangGraph stateful workflow.

Primary goal:

- Build a multi-node AI workflow with conditional routing, shared memory, RAG retrieval, structured CSV lookups, and Human-in-the-Loop underwriting escalation.

## Stack

- Backend: Python + FastAPI
- Workflow Engine: LangGraph
- LLM Framework: LangChain
- UI: Streamlit
- Vector Store: FAISS
- Deployment: Docker + AWS ECS
- Observability: LangSmith
- Evaluation: DeepEval

## Domain

Life Insurance

## User Personas

- Insurance Applicant
- Underwriter
- Policy Advisor
- Beneficiary

## Required Specialist Nodes

1. Intent Router
2. Underwriting Agent
3. Policy Q&A Agent
4. Beneficiary Agent
5. Issuance Agent
6. Human Review Node (HitL)

## Core Requirements

- Intent routing accuracy >= 90%
- Shared state persistence across nodes
- High-risk underwriting must trigger human review
- All policy/document answers require citations
- Premium estimates must be labelled non-binding
- No final underwriting decision allowed
- Prompt injection must be blocked
- Conversation history persistence required

## Shared State Schema

```python
state = {
  "session_id": str,
  "conversation_history": list,
  "applicant_data": {
      "name": str,
      "age": int,
      "gender": str,
      "occupation": str,
      "smoker": bool,
      "medical_conditions": list,
      "desired_sum_assured": int,
      "policy_type_preference": str
  },
  "risk_score": {
      "risk_tier": str,
      "score": float,
      "explanation": str
  },
  "node_outputs": dict,
  "current_node": str,
  "human_review_required": bool,
  "human_review_status": str
}
```

## Dataset Design

### PDFs → RAG + FAISS

Use vector retrieval for:

- Product Guide
- Terms & Conditions
- Underwriting Guidelines
- Beneficiary Guide
- Issuance Guide
- Lapse/Reinstatement Guide
- Riders Catalogue
- Glossary

### CSVs → Deterministic Lookup Tools

Do NOT vectorize CSVs.

Use:

- Pandas lookup
- Structured filtering
- Rule-based retrieval

CSV datasets:

- Premium Rate Reference Tables
- Risk Score Classification Table

## Mandatory Functional Requirements

- Policy comparison guidance
- Underwriting intake
- Risk classification lookup
- Indicative premium estimation
- Human-in-the-loop escalation
- Beneficiary nomination validation
- Issuance timeline guidance
- Shared state persistence
- Guardrails

## Guardrails

Must block:

- Final underwriting decisions
- Guaranteed premium quotes
- Medical diagnosis
- Prompt injection
- PHI leakage

## Performance Constraints

- P95 latency < 4 seconds
- Dockerized app
- Public AWS URL
- LangSmith traces visible

## Evaluation Priorities

1. Graph correctness
2. Stateful execution
3. Human review trigger
4. RAG faithfulness
5. Observability
6. Guardrails

## Recommended Model Strategy

Primary model:

- Gemini 2.5 Flash

Optional premium reasoning:

- Claude Sonnet
- GPT-4.1-mini

## Recommended Routing Strategy

Hybrid routing:

1. Keyword/rule-based routing first
2. LLM fallback classification second

## Demo Strategy

Demo must show:

1. Multi-turn conversation
2. Multiple graph nodes executed
3. Shared memory across nodes
4. High-risk underwriting escalation
5. LangSmith trace
6. Source citations

## Bonus Feature Recommendation

Implement:

- Policy Comparison Subgraph

Avoid:

- OCR
- Voice input
- Complex predictive systems

## AWS Deployment

- Dockerized FastAPI
- ECS deployment
- Streamlit frontend
- Environment variables for secrets
- LangSmith tracing enabled

## Team Responsibilities

- FastAPI + LangGraph
- Streamlit UI
- RAG ingestion
- Guardrails + evaluation
- AWS deployment
- Testing + LangSmith
