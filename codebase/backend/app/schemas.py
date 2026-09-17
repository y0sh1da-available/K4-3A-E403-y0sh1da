from typing import Literal, Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_input: str
    slide_context: str
    slide_page: int


class Citation(BaseModel):
    has_citation: bool
    source: Optional[str] = None
    exact_quote: Optional[str] = None


class ChatResponse(BaseModel):
    case: Literal["A", "B", "C"]

    action: Literal[
        "ANSWER_WITH_CITATION",
        "ASK_CLARIFICATION",
        "REFUSE_AND_GUIDE",
    ]

    reply_text: str

    citation: Citation

    clarification_question: Optional[str] = None

    next_action_hint: Optional[str] = None