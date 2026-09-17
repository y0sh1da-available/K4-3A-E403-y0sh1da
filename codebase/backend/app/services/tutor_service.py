from app.schemas import ChatRequest, ChatResponse
from app.services.gemini_service import call_gemini


def handle_chat(
    request: ChatRequest,
) -> ChatResponse:
    return call_gemini(request)