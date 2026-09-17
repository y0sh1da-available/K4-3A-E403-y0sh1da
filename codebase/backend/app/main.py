from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import (
    ChatRequest,
    ChatResponse,
    Citation,
)


app = FastAPI(
    title="Grounded Tutor API",
    version="0.2.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "grounded-tutor-backend",
    }


@app.post(
    "/api/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    text = request.user_input.strip().lower()

    # MOCK CASE B
    if text in {
        "cái này",
        "cái này là gì?",
        "tại sao",
        "why",
    }:
        return ChatResponse(
            case="B",
            action="ASK_CLARIFICATION",
            reply_text=(
                "Mình chưa xác định được bạn đang hỏi "
                "về phần nào."
            ),
            citation=Citation(
                has_citation=False,
                source=None,
                exact_quote=None,
            ),
            clarification_question=(
                "Bạn đang muốn hỏi về khái niệm, "
                "ví dụ hay cách áp dụng của phần nào?"
            ),
            next_action_hint=(
                "Vui lòng nhập câu hỏi cụ thể hơn."
            ),
        )

    # MOCK CASE C
    if "bài tập" in text or "deadline" in text:
        return ChatResponse(
            case="C",
            action="REFUSE_AND_GUIDE",
            reply_text=(
                "Mình không tìm thấy thông tin này "
                "trong bài giảng hiện tại."
            ),
            citation=Citation(
                has_citation=False,
                source=None,
                exact_quote=None,
            ),
            clarification_question=None,
            next_action_hint=(
                "Bạn có thể kiểm tra mục Bài tập "
                "trên hệ thống học tập."
            ),
        )

    # MOCK CASE A
    return ChatResponse(
        case="A",
        action="ANSWER_WITH_CITATION",
        reply_text=(
            "Data Lake là một kho lưu trữ dữ liệu "
            "tập trung, quy mô lớn."
        ),
        citation=Citation(
            has_citation=True,
            source=f"Slide {request.slide_page}",
            exact_quote=request.slide_context,
        ),
        clarification_question=None,
        next_action_hint=(
            f"Xem nội dung tại Slide {request.slide_page}."
        ),
    )