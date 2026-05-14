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

        st.divider()

        # ---------------------------------------------------
        # CLEAR CHAT BUTTON
        # ---------------------------------------------------

        if st.button(
            "Clear Chat",
            use_container_width=True
        ):

            # Clear chat history
            st.session_state.messages = []

            # Clear workflow state
            st.session_state.state = {}

            # Clear graph trace
            st.session_state.trace = []

            # Reset active node
            st.session_state.active_node = (
                "intent_router"
            )

            # Optional: new session ID
            # Creates fresh conversation
            import uuid

            st.session_state.session_id = str(
                uuid.uuid4()
            )

            # Refresh UI immediately
            st.rerun()