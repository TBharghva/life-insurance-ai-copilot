# Mock API service to simulate backend responses for the frontend application.
# TODO: Replace with real API calls to FastAPI backend once implemented.
def send_message(session_id: str, message: str):
    """
    Mock backend response.
    Replace later with FastAPI API call.
    """

    message_lower = message.lower()

    if "diabetes" in message_lower or "smoker" in message_lower:

        return {
            "response": (
                "Based on the disclosed medical information, "
                "additional underwriting review may be required."
            ),
            "node_executed": "underwriting",
            "citations": [
                {
                    "document": "Underwriting Guidelines",
                    "page": 14
                }
            ],
            "state": {
                "applicant_data": {
                    "medical_conditions": ["Diabetes"],
                    "smoker": True
                },
                "risk_score": {
                    "risk_tier": "High Risk"
                },
                "human_review_required": True
            },
            "trace": [
                "intent_router",
                "underwriting",
                "human_review"
            ]
        }

    elif "nominee" in message_lower:

        return {
            "response": (
                "A minor nominee requires a guardian/trustee."
            ),
            "node_executed": "beneficiary",
            "citations": [
                {
                    "document": "Beneficiary Guide",
                    "page": 9
                }
            ],
            "state": {
                "human_review_required": False
            },
            "trace": [
                "intent_router",
                "beneficiary"
            ]
        }

    return {
        "response": (
            "Term insurance covers a fixed duration "
            "while whole life provides lifelong coverage."
        ),
        "node_executed": "policy_qa",
        "citations": [
            {
                "document": "Product Guide",
                "page": 12
            }
        ],
        "state": {
            "human_review_required": False
        },
        "trace": [
            "intent_router",
            "policy_qa"
        ]
    }