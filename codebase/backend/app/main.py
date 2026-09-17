# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
#
# from app.schemas import ChatRequest, ChatResponse
# from app.services.tutor_service import handle_chat
#
#
# app = FastAPI(
#     title="Grounded Tutor API",
#     version="0.4.0",
# )
#
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Dev / hackathon
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
#
# @app.get("/health")
# def health():
#     return {
#         "status": "ok",
#         "service": "grounded-tutor-backend",
#     }
#
#
# @app.post(
#     "/api/chat",
#     response_model=ChatResponse,
# )
# def chat(request: ChatRequest):
#     try:
#         return handle_chat(request)
#
#     except Exception as exc:
#         print(
#             f"[CHAT ERROR] "
#             f"{type(exc).__name__}: {exc}"
#         )
#
#         raise HTTPException(
#             status_code=500,
#             detail="AI service failed to process the request.",
#         ) from exc




import traceback

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ChatRequest, ChatResponse
from app.services.tutor_service import handle_chat


app = FastAPI(
    title="Grounded Tutor API",
    version="0.4.0",
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
    try:
        return handle_chat(request)

    except Exception as exc:
        print(
            f"[CHAT ERROR] "
            f"{type(exc).__name__}: {exc}"
        )

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="AI service failed to process the request.",
        ) from exc