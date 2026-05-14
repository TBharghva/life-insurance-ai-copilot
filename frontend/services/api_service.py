import requests
import json



# ---------------------------------------------------
# BACKEND URL
# ---------------------------------------------------

BASE_URL = "http://127.0.0.1:8000"


# ---------------------------------------------------
# SEND MESSAGE
# ---------------------------------------------------

def send_message(
    session_id: str,
    message: str
):
    """
    Send chat message to backend API.
    """
    payload = {
        "session_id": session_id,
        "message": message
    }

    response = requests.post(
        f"{BASE_URL}/chat",
        json=payload
    )

    return response.json()

def stream_message(
    session_id: str,
    message: str
):

    payload = {
        "session_id": session_id,
        "message": message
    }

    response = requests.post(
        f"{BASE_URL}/chat/stream",
        json=payload,
        stream=True
    )

    for line in response.iter_lines():

        if line:

            yield json.loads(
                line.decode("utf-8")
            )