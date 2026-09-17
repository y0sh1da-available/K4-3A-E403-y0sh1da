from dataclasses import dataclass
from pathlib import Path
import time

from openai import OpenAI

from app.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
)
from app.schemas import (
    ChatRequest,
    ChatResponse,
)


@dataclass
class OpenAIResult:
    parsed_response: ChatResponse
    prompt: str
    raw_response: str
    latency_ms: float


class OpenAICallError(RuntimeError):
    """
    OpenAI/API/parsing error carrying metadata
    for CP3 logging.
    """

    def __init__(
        self,
        message: str,
        prompt: str,
        latency_ms: float,
        raw_response: str = "",
    ):
        super().__init__(message)

        self.prompt = prompt
        self.latency_ms = latency_ms
        self.raw_response = raw_response


client = OpenAI(
    api_key=OPENAI_API_KEY,
)


PROMPT_PATH = (
    Path(__file__).resolve().parents[2]
    / "prompts"
    / "system_prompt.txt"
)


def load_system_prompt() -> str:
    return PROMPT_PATH.read_text(
        encoding="utf-8"
    ).strip()


def build_user_prompt(
    request: ChatRequest,
) -> str:

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

Return the Grounded Tutor decision and response.
""".strip()


def call_openai(
    request: ChatRequest,
    correction_note: str | None = None,
) -> OpenAIResult:

    system_prompt = load_system_prompt()
    user_prompt = build_user_prompt(request)

    if correction_note:
        user_prompt += "\n\n" + f"""
IMPORTANT:
Your previous response violated a backend validation rule:

{correction_note}

Re-evaluate the learner request from the beginning.

Follow the original A/B/C decision flow exactly:
- A: enough evidence to answer with citation
- B: ambiguous/incomplete but can be clarified
- C: unsupported or outside the available lesson context

Do not assume the previous case was correct.
""".strip()

    full_prompt = (
        f"SYSTEM PROMPT:\n"
        f"{system_prompt}\n\n"
        f"USER PROMPT:\n"
        f"{user_prompt}"
    )

    start_time = time.perf_counter()

    raw_response = ""

    try:
        response = client.responses.parse(
            model=OPENAI_MODEL,
            instructions=system_prompt,
            input=user_prompt,
            text_format=ChatResponse,
        )

        raw_response = response.output_text or ""

        if not raw_response:
            raise RuntimeError(
                "OpenAI returned an empty response."
            )

        parsed_response = response.output_parsed

        if parsed_response is None:
            raise RuntimeError(
                "OpenAI returned no parsed structured response."
            )

    except Exception as exc:
        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        raise OpenAICallError(
            message=(
                f"{type(exc).__name__}: {exc}"
            ),
            prompt=full_prompt,
            raw_response=raw_response,
            latency_ms=latency_ms,
        ) from exc

    latency_ms = (
        time.perf_counter() - start_time
    ) * 1000

    return OpenAIResult(
        parsed_response=parsed_response,
        prompt=full_prompt,
        raw_response=raw_response,
        latency_ms=latency_ms,
    )