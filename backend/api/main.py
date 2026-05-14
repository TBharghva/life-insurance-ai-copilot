from fastapi import FastAPI

from backend.api.routes.chat import router as chat_router


# ---------------------------------------------------
# CREATE FASTAPI APP
# ---------------------------------------------------

app = FastAPI(
    title="Life Insurance AI Copilot",
    version="1.0.0"
)


# ---------------------------------------------------
# REGISTER ROUTES
# ---------------------------------------------------

app.include_router(chat_router)