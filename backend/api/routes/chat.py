from fastapi import APIRouter

from pydantic import BaseModel

from backend.services.rag_service import (
    generate_rag_response
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