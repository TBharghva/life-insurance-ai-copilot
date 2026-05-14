from fastapi import APIRouter

from pydantic import BaseModel

from fastapi.responses import StreamingResponse

import json

from backend.services.rag_service import (
    generate_rag_response, stream_rag_response
)


# ---------------------------------------------------
# ROUTER
# ---------------------------------------------------

router = APIRouter()


# ---------------------------------------------------
# REQUEST MODEL
# ---------------------------------------------------

class ChatRequest(BaseModel):

    session_id: str

    message: str


# ---------------------------------------------------
# RESPONSE MODEL
# ---------------------------------------------------

class ChatResponse(BaseModel):

    response: str

    citations: list


# ---------------------------------------------------
# CHAT ENDPOINT
# ---------------------------------------------------

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):

    rag_response = generate_rag_response(
        request.message
    )

    return ChatResponse(
        response=rag_response["answer"],
        citations=rag_response["citations"]
    )

@router.post("/chat/stream")
def stream_chat(request: ChatRequest):

    rag_response = stream_rag_response(
        request.message
    )

    citations = rag_response["citations"]


    def generate():

        full_response = ""

        for token in rag_response["stream"]:

            full_response += token

            yield json.dumps(
                {
                    "token": token
                }
            ) + "\n"

        # Send citations at end
        yield json.dumps(
            {
                "done": True,
                "citations": citations
            }
        ) + "\n"


    return StreamingResponse(
        generate(),
        media_type="application/json"
    )