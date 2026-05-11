import uuid
import streamlit as st

from components.sidebar import render_sidebar

# TODO: Replace with real API call to FastAPI backend
# Mock response is currently in services/api_service.py
from services.api_service import send_message

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
