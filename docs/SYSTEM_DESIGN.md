# Life Insurance AI Copilot — System Design

# 1. High-Level Architecture

```text
User
  ↓
Streamlit UI
  ↓
FastAPI API Layer
  ↓
LangGraph Workflow Engine
  ├── Intent Router
  ├── Underwriting Agent
  ├── Policy QA Agent
  ├── Beneficiary Agent
  ├── Issuance Agent
  ├── Human Review Node
  ↓
Tools Layer
  ├── FAISS Retriever
  ├── Premium Lookup Tool
  ├── Risk Lookup Tool
  ├── Guardrails
  └── State Manager
  ↓
Storage Layer
  ├── FAISS Index
  ├── PDFs
  ├── CSV datasets
  └── LangGraph Checkpointer
```

# 2. Core Architectural Principle

This is NOT a simple chatbot.

The system is a:

- stateful workflow engine
- with conditional graph routing
- shared memory
- multi-agent specialization
- deterministic business logic

Graph correctness matters more than UI sophistication.

---

# 3. Recommended Folder Structure

```text
project/
│
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── middleware/
│   │
│   ├── graph/
│   │   ├── nodes/
│   │   ├── routers/
│   │   ├── state/
│   │   ├── edges/
│   │   └── workflow.py
│   │
│   ├── rag/
│   │   ├── ingestion/
│   │   ├── retriever/
│   │   ├── chunking/
│   │   └── citations/
│   │
│   ├── tools/
│   │   ├── premium_lookup.py
│   │   ├── risk_lookup.py
│   │   ├── guardrails.py
│   │   └── validators.py
│   │
│   ├── prompts/
│   ├── memory/
│   ├── evaluation/
│   └── config/
│
├── frontend/
│   ├── pages/
│   ├── components/
│   └── services/
│
├── datasets/
├── docker/
├── tests/
└── docs/
```

---

# 4. LangGraph Design

## Graph Nodes

### 4.1 Intent Router

Responsibilities:

- Classify user query intent
- Route to specialist node
- Use hybrid routing

Routing categories:

- underwriting
- policy_qa
- beneficiary
- issuance
- lapse_revival

Recommended implementation:

```python
1. Rule-based keyword matching
2. Fallback LLM classification
3. Confidence threshold
```

---

### 4.2 Underwriting Agent

Responsibilities:

- Collect applicant information
- Risk intake
- Risk classification
- Premium estimation
- Trigger human review

Uses:

- Risk CSV lookup
- Premium CSV lookup
- Underwriting guidelines RAG

Output:

```json
{
  "risk_tier": "standard",
  "indicative_premium": "₹XXXX/month",
  "human_review_required": false
}
```

---

### 4.3 Policy QA Agent

Responsibilities:

- Policy comparisons
- Rider explanations
- Coverage clarifications
- Exclusion explanations

Uses:

- FAISS retrieval
- Citation generation

All responses must include:

- document name
- section
- page number

---

### 4.4 Beneficiary Agent

Responsibilities:

- Nominee rules
- Share validation
- Minor nominee checks
- Trustee guidance

Validation examples:

- Share total must equal 100%
- Minor nominee requires guardian/trustee

---

### 4.5 Issuance Agent

Responsibilities:

- Pending documents
- Issuance timeline
- Dispatch status
- Revival guidance

Uses:

- Issuance checklist RAG
- Lapse/revival guide

---

### 4.6 Human Review Node

Responsibilities:

- Pause workflow
- Display risk summary
- Await manual decision
- Resume graph

Trigger conditions:

- high risk
- substandard risk
- dangerous medical condition

Demo requirement:
Must visibly pause workflow.

---

# 5. State Management Design

## Shared State

Use:

- LangGraph MemorySaver
- Persistent session state
- Conversation continuity

Critical shared data:

```python
- age
- health disclosures
- smoking status
- occupation
- policy preference
- risk score
- conversation history
```

State must persist across:

- graph nodes
- multiple turns
- API restarts during demo

---

# 6. RAG Architecture

## Recommended Chunking

Chunk size:

- 700–1000 tokens

Overlap:

- 100–150 tokens

Metadata:

```python
{
  "document_name": str,
  "page_number": int,
  "section": str,
  "document_type": str
}
```

---

## Embeddings

Recommended:

- text-embedding-3-small

---

## Retrieval Strategy

Recommended:

- similarity search
- top_k = 4
- metadata filtering

---

# 7. Structured Lookup Tools

## Premium Lookup Tool

Input:

```python
age
sum_assured
policy_term
```

Output:

```python
premium_range
```

Implementation:

- Pandas filtering
- Deterministic logic
- No vector search

---

## Risk Lookup Tool

Input:

```python
medical_conditions
occupation
lifestyle
```

Output:

```python
risk_tier
risk_explanation
```

---

# 8. Guardrails Design

## Must Block

### Final underwriting decisions

Blocked phrases:

- approved
- rejected
- guaranteed acceptance

### Guaranteed premium quotes

Must include:

- indicative only
- non-binding

### Medical diagnosis

Must avoid:

- diagnosis
- treatment recommendation

### Prompt injection

Examples:

- ignore instructions
- reveal prompt
- bypass safety

Implementation:

```python
1. Pre-LLM validation
2. Output moderation
3. Response rewriting
4. Fallback refusal template
```

---

# 9. API Design

## POST /chat

Request:

```json
{
  "session_id": "abc123",
  "message": "I am 45 and diabetic"
}
```

Response:

```json
{
  "response": "...",
  "node_executed": "underwriting",
  "citations": [],
  "state": {}
}
```

---

## GET /state/{session_id}

Returns:

- shared graph state
- conversation history
- current node

---

## GET /health

Returns:

- service health
- vector db status
- LLM connectivity

---

# 10. Streamlit UI Design

Recommended panels:

## Chat Panel

- User conversation
- AI responses

## State Panel

Display:

- collected applicant data
- current risk tier
- active node
- conversation history

## Trace Panel

Display:

- executed node path
- graph transitions

---

# 11. Observability

Use LangSmith for:

- graph traces
- node execution
- latency monitoring
- state delta tracking

Demo must show:

- at least 3 node transitions
- state growth over time
- HitL interrupt

---

# 12. Performance Optimizations

Use:

- async FastAPI
- cached retrievers
- lazy loading
- deterministic routing
- lightweight prompts

Avoid:

- unnecessary agents
- recursive loops
- excessive retrieval depth

Target:

- < 4 second response time

---

# 13. Deployment Architecture

```text
User
 ↓
AWS Load Balancer
 ↓
Docker Container
 ├── FastAPI
 ├── LangGraph
 ├── FAISS
 └── Streamlit
```

Recommended:

- ECS Fargate
- environment variables
- single-container deployment for simplicity

---

# 14. Recommended Demo Flow

1. User asks policy comparison
2. Policy QA node executes
3. User provides health disclosures
4. Underwriting node executes
5. High-risk trigger fires
6. Human review pause shown
7. Beneficiary query asked
8. Beneficiary node accesses prior state
9. LangSmith trace shown
