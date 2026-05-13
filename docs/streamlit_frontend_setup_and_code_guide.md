# Streamlit Frontend Design — Life Insurance AI Copilot

This document contains:

1. Frontend architecture
2. Streamlit UI design
3. Project structure
4. Step-by-step setup instructions
5. Complete Streamlit code
6. API integration
7. Session memory handling
8. UI enhancements
9. Docker notes
10. Detailed code explanations

---

# 1. Frontend Goals

The frontend should:

- Provide a clean enterprise-style insurance UI
- Support multi-turn conversations
- Display graph node execution
- Display shared state
- Show citations
- Show human-review status
- Persist chat history
- Be demo-friendly for judges

The frontend does NOT need:
- authentication
- complex animations
- advanced styling
- pixel-perfect design

The evaluation focuses more on:
- graph correctness
- shared state
- traces
- human-in-the-loop

---

# 2. Recommended Frontend Structure

```text
frontend/
│
├── app.py
├── components/
│   ├── chat_panel.py
│   ├── sidebar.py
│   ├── state_panel.py
│   └── trace_panel.py
│
├── services/
│   └── api_service.py
│
├── utils/
│   └── helpers.py
│
├── assets/
│   └── styles.css
│
├── requirements.txt
└── .streamlit/
    └── config.toml
```

---

# 3. Step-by-Step Setup Guide

# Step 1 — Create Virtual Environment

Open terminal:

```bash
python -m venv venv
```

Activate environment:

## Windows

```bash
venv\Scripts\activate
```

## Mac/Linux

```bash
source venv/bin/activate
```

---

# Step 2 — Install Dependencies

Create:

```text
requirements.txt
```

Add:

```text
streamlit
requests
pandas
python-dotenv
```

Install:

```bash
pip install -r requirements.txt
```

---

# Step 3 — Create Streamlit Config

Create:

```text
.streamlit/config.toml
```

Add:

```toml
[theme]
base="dark"
primaryColor="#4F8BF9"
backgroundColor="#0E1117"
secondaryBackgroundColor="#262730"
textColor="#FAFAFA"
```

---

# Step 4 — Create Folder Structure

```bash
mkdir frontend
cd frontend

mkdir components
mkdir services
mkdir utils
mkdir assets
mkdir .streamlit
```

---

# Step 5 — Create Backend URL Environment Variable

Create:

```text
.env
```

Add:

```text
BACKEND_URL=http://localhost:8000
```

---

# 4. Frontend Layout Design

The UI will have:

## Main Chat Area

Contains:
- user messages
- AI responses
- citations

---

## Sidebar

Contains:
- session ID
- graph node executed
- current risk tier
- human review status
- applicant data

---

## Trace Panel

Displays:
- executed nodes
- graph transitions
- routing flow

---

# 5. Backend Response Format (IMPORTANT)

Your FastAPI backend should return:

```json
{
  "response": "...",
  "node_executed": "underwriting",
  "citations": [
    {
      "document": "Product Guide",
      "page": 12
    }
  ],
  "state": {
    "risk_tier": "high"
  },
  "trace": [
    "intent_router",
    "underwriting",
    "human_review"
  ]
}
```

The Streamlit UI depends on this structure.

---

# 6. API Service

Create:

```text
services/api_service.py
```

Code:

```python
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Backend URL from environment variable
BASE_URL = os.getenv("BACKEND_URL")


def send_message(session_id: str, message: str):
    """
    Sends user message to FastAPI backend.

    Args:
        session_id: unique chat session ID
        message: user query

    Returns:
        JSON response from backend
    """

    endpoint = f"{BASE_URL}/chat"

    payload = {
        "session_id": session_id,
        "message": message
    }

    try:
        response = requests.post(endpoint, json=payload)

        # Raise exception if status code is not 200
        response.raise_for_status()

        return response.json()

    except Exception as e:
        return {
            "response": f"Backend connection failed: {str(e)}",
            "node_executed": "error",
            "citations": [],
            "state": {},
            "trace": []
        }
```

---

# 7. Sidebar Component

Create:

```text
components/sidebar.py
```

Code:

```python
import streamlit as st


def render_sidebar(state_data, node_name):
    """
    Renders left sidebar.

    Displays:
    - active node
    - applicant state
    - risk information
    - human review status
    """

    with st.sidebar:
        st.title("Life Insurance AI")

        st.divider()

        st.subheader("Workflow Status")

        st.write(f"Active Node: {node_name}")

        st.divider()

        st.subheader("Applicant State")

        applicant_data = state_data.get("applicant_data", {})

        if applicant_data:
            st.json(applicant_data)
        else:
            st.info("No applicant data collected yet")

        st.divider()

        risk_data = state_data.get("risk_score", {})

        if risk_data:
            st.subheader("Risk Score")
            st.json(risk_data)

        human_review = state_data.get("human_review_required", False)

        if human_review:
            st.error("Human Review Required")
        else:
            st.success("No Human Review Needed")
```

---

# 8. Trace Panel Component

Create:

```text
components/trace_panel.py
```

Code:

```python
import streamlit as st


def render_trace(trace_data):
    """
    Shows graph execution trace.

    Example:
    intent_router -> underwriting -> human_review
    """

    st.subheader("LangGraph Execution Trace")

    if not trace_data:
        st.info("No graph trace available")
        return

    for index, node in enumerate(trace_data):
        st.write(f"{index + 1}. {node}")
```

---

# 9. Main Streamlit App

Create:

```text
app.py
```

Code:

```python
import uuid
import streamlit as st

from services.api_service import send_message
from components.sidebar import render_sidebar
from components.trace_panel import render_trace


# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Life Insurance AI Copilot",
    page_icon="🛡️",
    layout="wide"
)


# ---------------------------------------------------
# SESSION INITIALIZATION
# ---------------------------------------------------

# Create unique session ID only once
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Store backend state
if "state" not in st.session_state:
    st.session_state.state = {}


# Store graph trace
if "trace" not in st.session_state:
    st.session_state.trace = []


# Store last executed node
if "active_node" not in st.session_state:
    st.session_state.active_node = "intent_router"


# ---------------------------------------------------
# APP HEADER
# ---------------------------------------------------

st.title("🛡️ Life Insurance AI Copilot")

st.caption(
    "LangGraph-powered underwriting, policy guidance, beneficiary support, and issuance workflow assistant"
)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

render_sidebar(
    st.session_state.state,
    st.session_state.active_node
)


# ---------------------------------------------------
# DISPLAY EXISTING CHAT HISTORY
# ---------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        # Display citations if available
        if message.get("citations"):

            st.markdown("### Citations")

            for citation in message["citations"]:
                st.write(
                    f"- {citation.get('document')} | Page {citation.get('page')}"
                )


# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------

user_input = st.chat_input("Ask about underwriting, policies, beneficiaries, or issuance...")


# ---------------------------------------------------
# HANDLE USER MESSAGE
# ---------------------------------------------------

if user_input:

    # Add user message to UI history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)


    # Call backend API
    backend_response = send_message(
        st.session_state.session_id,
        user_input
    )


    # Extract response data
    ai_response = backend_response.get("response", "No response")

    citations = backend_response.get("citations", [])

    node_executed = backend_response.get("node_executed", "unknown")

    state_data = backend_response.get("state", {})

    trace_data = backend_response.get("trace", [])


    # Update session state
    st.session_state.state = state_data
    st.session_state.trace = trace_data
    st.session_state.active_node = node_executed


    # Store assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_response,
            "citations": citations
        }
    )


    # Display assistant response
    with st.chat_message("assistant"):

        st.markdown(ai_response)


        # Show citations
        if citations:

            st.markdown("### Citations")

            for citation in citations:
                st.write(
                    f"- {citation.get('document')} | Page {citation.get('page')}"
                )


    # Show graph trace
    st.divider()

    render_trace(trace_data)
```

---

# 10. Running The App

# Start FastAPI Backend

From backend folder:

```bash
uvicorn main:app --reload
```

Backend runs:

```text
http://localhost:8000
```

---

# Start Streamlit Frontend

From frontend folder:

```bash
streamlit run app.py
```

Frontend runs:

```text
http://localhost:8501
```

---

# 11. Expected Demo Flow

## Example Flow

User:
```text
What is the difference between term life and whole life?
```

Expected node:
```text
policy_qa
```

---

User:
```text
I am 45 and diabetic.
```

Expected node:
```text
underwriting
```

---

User:
```text
Can my 10-year-old son be nominee?
```

Expected node:
```text
beneficiary
```

Shared state should still contain:
- age
- medical history
- policy preference

---

# 12. Recommended Improvements

After MVP works, add:

## Better UX
- typing indicator
- streaming responses
- collapsible citations
- graph visualization

---

## Better State Visualization
Display:
- collected applicant fields
- missing fields
- risk score evolution

---

## Better Trace Display
Convert:

```text
intent_router -> underwriting -> human_review
```

into visual workflow blocks.

---

# 13. Docker Notes

## Streamlit Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

# 14. Common Errors

## Backend Connection Refused

Cause:
- FastAPI not running

Fix:
```bash
uvicorn main:app --reload
```

---

## CORS Error

Add to FastAPI:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Session Resetting

Cause:
- browser refresh
- backend state not persisted

Fix:
- use LangGraph MemorySaver
- persist session_id

---

# 15. Final Recommendations

Prioritize:
- stable workflows
- visible state persistence
- trace visibility
- citations
- human-review pause

Avoid spending exce