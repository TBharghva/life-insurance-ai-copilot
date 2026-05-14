import uuid
import streamlit as st

from components.sidebar import render_sidebar

# TODO: Replace with real API call to FastAPI backend
# Mock response is currently in services/api_service.py
# from services.api_service import send_message
from services.api_service import ( stream_message)


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

# Store loading state
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

if "pending_user_input" not in st.session_state:
    st.session_state.pending_user_input = None


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
                source_document = citation.get(
                    "source_document",
                    "Unknown Document"
                )

                section = citation.get(
                    "section",
                    "Unknown Section"
                )

                st.write(
                    f"- {source_document} | Section: {section}"
                )


# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------

user_input = st.chat_input(
    "Ask about underwriting, policies, beneficiaries, or issuance...",
    disabled=st.session_state.is_loading
)


# ---------------------------------------------------
# HANDLE USER MESSAGE
# ---------------------------------------------------

if user_input and not st.session_state.is_loading:

    st.session_state.pending_user_input = user_input

    st.session_state.is_loading = True

    st.rerun()

# ---------------------------------------------------
# PROCESS PENDING INPUT
# ---------------------------------------------------

if (
    st.session_state.is_loading
    and st.session_state.pending_user_input
):
    try:

        user_input = st.session_state.pending_user_input

        # Add user message to history
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        # Show user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Assistant response
        with st.chat_message("assistant"):

            response_placeholder = st.empty()

            full_response = ""

            citations = []

            with st.spinner(
                "Generating AI underwriting response..."
            ):

                for chunk in stream_message(
                    st.session_state.session_id,
                    user_input
                ):

                    # Final metadata payload
                    if chunk.get("done"):

                        citations = chunk.get(
                            "citations",
                            []
                        )

                        break

                    token = chunk.get("token", "")

                    full_response += token

                    response_placeholder.markdown(
                        full_response + "▌"
                    )

            # Display citations
            if citations:

                st.markdown("### Sources")

                for citation in citations:

                    source_document = citation.get(
                        "source_document",
                        "Unknown Document"
                    )

                    section = citation.get(
                        "section",
                        "Unknown Section"
                    )

                    st.caption(
                        f"📄 {source_document} — {section}"
                    )
        
        response_placeholder.markdown(full_response)

        # Store assistant message
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response,
                "citations": citations
            }
        )

    finally:

        st.session_state.is_loading = False

        st.session_state.pending_user_input = None

        st.rerun()
