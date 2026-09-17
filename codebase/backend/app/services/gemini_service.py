from pathlib import Path

from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.schemas import ChatRequest, ChatResponse


client = genai.Client(api_key=GEMINI_API_KEY)


PROMPT_PATH = (
    Path(__file__).resolve().parents[2]
    / "prompts"
    / "system_prompt.txt"
)


def load_system_prompt() -> str:
    return PROMPT_PATH.read_text(
        encoding="utf-8"
    ).strip()


def build_user_prompt(request: ChatRequest) -> str:
    return f"""
CURRENT SLIDE PAGE:
{request.slide_page}

CURRENT LESSON CONTEXT:
<lesson_context>
{request.slide_context}
</lesson_context>

LEARNER QUESTION:
<user_input>
{request.user_input}
</user_input>

Classify this interaction and produce the required Grounded Tutor response.
""".strip()


def call_gemini(
    request: ChatRequest,
) -> ChatResponse:
    system_prompt = load_system_prompt()
    user_prompt = build_user_prompt(request)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.1,
            response_mime_type="application/json",
            response_schema=ChatResponse,
        ),
    )

    # google-genai có thể parse structured response
    # trực tiếp từ Pydantic schema.
    if response.parsed is not None:
        return response.parsed

    # Fallback nếu SDK không populate response.parsed.
    return ChatResponse.model_validate_json(
        response.text
    )