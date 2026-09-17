from app.config import OPENAI_MODEL

from app.schemas import (
    ChatRequest,
    ChatResponse,
)

from app.services.openai_service import (
    call_openai,
    OpenAICallError,
)

from app.utils.logger import (
    create_request_id,
    log_interaction,
)


# =========================================================
# Validation Error
# =========================================================

class BackendValidationError(ValueError):
    """
    Raised when the LLM output violates deterministic
    Grounded Tutor backend safeguards.
    """

    pass


# =========================================================
# Helpers
# =========================================================

def normalize_text(text: str) -> str:
    """
    Normalize whitespace and casing so citation validation
    is less sensitive to minor formatting differences.
    """

    return " ".join(text.split()).casefold()


# =========================================================
# Backend Guard
# =========================================================

def validate_response(
    response: ChatResponse,
    request: ChatRequest,
) -> None:
    """
    Validate OpenAI output against the locked A/B/C flow.

    OpenAI is the AI decision engine that selects A/B/C.
    Backend only verifies that the returned decision satisfies
    deterministic grounding and response constraints.
    """

    # -----------------------------------------------------
    # General rules
    # -----------------------------------------------------

    if not response.reply_text.strip():
        raise BackendValidationError(
            "reply_text must not be empty."
        )

    expected_actions = {
        "A": "ANSWER_WITH_CITATION",
        "B": "ASK_CLARIFICATION",
        "C": "REFUSE_AND_GUIDE",
    }

    expected_action = expected_actions[
        response.case
    ]

    if response.action != expected_action:
        raise BackendValidationError(
            f"Case {response.case} must use action "
            f"{expected_action}, got {response.action}."
        )

    # =====================================================
    # CASE A
    # Enough evidence -> answer + citation
    # =====================================================

    if response.case == "A":

        if not response.citation.has_citation:
            raise BackendValidationError(
                "Case A requires "
                "citation.has_citation=true."
            )

        if not response.citation.source:
            raise BackendValidationError(
                "Case A requires citation.source."
            )

        if not response.citation.exact_quote:
            raise BackendValidationError(
                "Case A requires citation.exact_quote."
            )

        quote = normalize_text(
            response.citation.exact_quote
        )

        context = normalize_text(
            request.slide_context
        )

        # Core grounding safeguard:
        # quoted evidence must really exist in the
        # supplied lesson context.
        if quote not in context:
            raise BackendValidationError(
                "Citation exact_quote is not present "
                "in the supplied slide context."
            )

        if response.clarification_question is not None:
            raise BackendValidationError(
                "Case A must not contain "
                "clarification_question."
            )

        # slide_page is trusted backend metadata.
        # Do not rely on the LLM to invent a page number.
        response.citation.source = (
            f"Slide {request.slide_page}"
        )

    # =====================================================
    # CASE B
    # Ambiguous -> ask learner to clarify
    # =====================================================

    elif response.case == "B":

        if response.citation.has_citation:
            raise BackendValidationError(
                "Case B must not contain a citation."
            )

        if (
            response.citation.source is not None
            or response.citation.exact_quote is not None
        ):
            raise BackendValidationError(
                "Case B citation fields must be null."
            )

        if not response.clarification_question:
            raise BackendValidationError(
                "Case B requires "
                "clarification_question."
            )

        if not response.next_action_hint:
            raise BackendValidationError(
                "Case B requires next_action_hint."
            )

    # =====================================================
    # CASE C
    # Unsupported / out of scope -> limit + guide
    # =====================================================

    elif response.case == "C":

        if response.citation.has_citation:
            raise BackendValidationError(
                "Case C must not contain a citation."
            )

        if (
            response.citation.source is not None
            or response.citation.exact_quote is not None
        ):
            raise BackendValidationError(
                "Case C citation fields must be null."
            )

        if response.clarification_question is not None:
            raise BackendValidationError(
                "Case C must not contain "
                "clarification_question."
            )

        if not response.next_action_hint:
            raise BackendValidationError(
                "Case C requires next_action_hint."
            )


# =========================================================
# Main Backend Orchestrator
# =========================================================

def handle_chat(
    request: ChatRequest,
) -> ChatResponse:
    """
    Main backend orchestration:

    Request
      -> OpenAI decision
      -> deterministic backend guard
      -> retry once if invalid
      -> logging
      -> final ChatResponse
    """

    request_id = create_request_id()

    # =====================================================
    # ATTEMPT 1
    # =====================================================

    try:
        first_result = call_openai(
            request=request
        )

    except OpenAICallError as exc:

        log_interaction(
            request_id=request_id,
            user_input=request.user_input,
            slide_page=request.slide_page,
            prompt=exc.prompt,
            raw_llm_response=exc.raw_response,
            parsed_case=None,
            latency_ms=exc.latency_ms,
            model=OPENAI_MODEL,
            error=str(exc),
            extra={
                "attempt": 1,
                "guard_passed": False,
                "failure_stage": "openai_call",
                "returned_case": None,
            },
        )

        raise

    first_response = (
        first_result.parsed_response
    )

    correction_note: str | None = None

    try:
        validate_response(
            response=first_response,
            request=request,
        )

        log_interaction(
            request_id=request_id,
            user_input=request.user_input,
            slide_page=request.slide_page,
            prompt=first_result.prompt,
            raw_llm_response=(
                first_result.raw_response
            ),
            parsed_case=first_response.case,
            latency_ms=first_result.latency_ms,
            model=OPENAI_MODEL,
            error=None,
            extra={
                "attempt": 1,
                "guard_passed": True,
                "returned_case": (
                    first_response.case
                ),
            },
        )

        return first_response

    except BackendValidationError as exc:

        correction_note = str(exc)

        # Keep the rejected model output in eval.log
        # for technical verification and debugging.
        log_interaction(
            request_id=request_id,
            user_input=request.user_input,
            slide_page=request.slide_page,
            prompt=first_result.prompt,
            raw_llm_response=(
                first_result.raw_response
            ),
            parsed_case=first_response.case,
            latency_ms=first_result.latency_ms,
            model=OPENAI_MODEL,
            error=correction_note,
            extra={
                "attempt": 1,
                "guard_passed": False,
                "failure_stage": "backend_guard",
                "returned_case": None,
            },
        )

    # =====================================================
    # ATTEMPT 2 — RE-EVALUATION
    # =====================================================

    try:
        second_result = call_openai(
            request=request,
            correction_note=correction_note,
        )

    except OpenAICallError as exc:

        log_interaction(
            request_id=request_id,
            user_input=request.user_input,
            slide_page=request.slide_page,
            prompt=exc.prompt,
            raw_llm_response=exc.raw_response,
            parsed_case=None,
            latency_ms=exc.latency_ms,
            model=OPENAI_MODEL,
            error=str(exc),
            extra={
                "attempt": 2,
                "guard_passed": False,
                "failure_stage": "openai_call",
                "returned_case": None,
            },
        )

        raise

    second_response = (
        second_result.parsed_response
    )

    try:
        validate_response(
            response=second_response,
            request=request,
        )

        log_interaction(
            request_id=request_id,
            user_input=request.user_input,
            slide_page=request.slide_page,
            prompt=second_result.prompt,
            raw_llm_response=(
                second_result.raw_response
            ),
            parsed_case=second_response.case,
            latency_ms=second_result.latency_ms,
            model=OPENAI_MODEL,
            error=None,
            extra={
                "attempt": 2,
                "guard_passed": True,
                "returned_case": (
                    second_response.case
                ),
            },
        )

        return second_response

    except BackendValidationError as exc:

        second_error = str(exc)

        log_interaction(
            request_id=request_id,
            user_input=request.user_input,
            slide_page=request.slide_page,
            prompt=second_result.prompt,
            raw_llm_response=(
                second_result.raw_response
            ),
            parsed_case=second_response.case,
            latency_ms=second_result.latency_ms,
            model=OPENAI_MODEL,
            error=second_error,
            extra={
                "attempt": 2,
                "guard_passed": False,
                "failure_stage": "backend_guard",
                "returned_case": None,
            },
        )

        raise BackendValidationError(
            "OpenAI response failed backend "
            "validation after re-evaluation. "
            f"Last error: {second_error}"
        )