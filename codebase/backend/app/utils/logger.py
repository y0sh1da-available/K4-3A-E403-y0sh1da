import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any
from uuid import uuid4


# backend/logs/eval.log
BACKEND_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = BACKEND_ROOT / "logs"
LOG_FILE = LOG_DIR / "eval.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)

_write_lock = Lock()


def create_request_id() -> str:
    """
    Tạo ID riêng cho mỗi lượt chat để trace khi debug/evaluation.
    """
    return f"req_{uuid4().hex[:8]}"


def log_interaction(
    *,
    request_id: str,
    user_input: str,
    slide_page: int,
    prompt: str,
    raw_llm_response: str,
    parsed_case: str | None,
    latency_ms: float,
    model: str | None = None,
    error: str | None = None,
    extra: dict[str, Any] | None = None,
) -> None:
    """
    Ghi một lượt tương tác AI vào logs/eval.log.

    CP3 cần đặc biệt:
    - prompt đầu vào
    - raw response của LLM
    """

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id,
        "user_input": user_input,
        "slide_page": slide_page,
        "model": model,
        "prompt": prompt,
        "raw_llm_response": raw_llm_response,
        "parsed_case": parsed_case,
        "latency_ms": round(latency_ms, 2),
        "error": error,
    }

    if extra:
        record["extra"] = extra

    line = json.dumps(
        record,
        ensure_ascii=False,
    )

    with _write_lock:
        with LOG_FILE.open(
            "a",
            encoding="utf-8",
        ) as file:
            file.write(line + "\n")