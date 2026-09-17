import json
import time
from pathlib import Path
import sys


# =========================================================
# Paths
# =========================================================

BACKEND_DIR = Path(__file__).resolve().parent

# repo/
# ├── codebase/
# │   └── backend/
# │       └── run_eval.py
# └── eval/
REPO_ROOT = BACKEND_DIR.parents[1]

sys.path.insert(
    0,
    str(BACKEND_DIR),
)


from app.schemas import ChatRequest
from app.services.tutor_service import handle_chat


GOLDEN_SET_PATH = (
    REPO_ROOT
    / "eval"
    / "golden_set.json"
)

RESULTS_PATH = (
    REPO_ROOT
    / "eval"
    / "run_results.md"
)


# =========================================================
# Load Golden Set
# =========================================================

def load_golden_set() -> list[dict]:

    if not GOLDEN_SET_PATH.exists():
        raise FileNotFoundError(
            f"Không tìm thấy Golden Set: "
            f"{GOLDEN_SET_PATH}"
        )

    with GOLDEN_SET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        cases = json.load(file)

    if not isinstance(cases, list):
        raise ValueError(
            "golden_set.json phải là một JSON array."
        )

    return cases


# =========================================================
# Run One Case
# =========================================================

def run_case(
    case: dict,
) -> dict:

    request = ChatRequest(
        user_input=case["user_input"],
        slide_context=case["slide_context"],
        slide_page=case["slide_page"],
    )

    start_t = time.perf_counter()

    try:
        response = handle_chat(request)

        latency_ms = round(
            (
                time.perf_counter()
                - start_t
            )
            * 1000,
            2,
        )

        case_match = (
            response.case
            == case["expected_case"]
        )

        action_match = (
            response.action
            == case["expected_action"]
        )

        passed = (
            case_match
            and action_match
        )

        return {
            "id": case["id"],
            "layer": case.get(
                "layer",
                case.get(
                    "taxonomy",
                    "UNKNOWN",
                ),
            ),
            "source": case.get(
                "source",
                "UNKNOWN",
            ),
            "expected_case": (
                case["expected_case"]
            ),
            "actual_case": response.case,
            "expected_action": (
                case["expected_action"]
            ),
            "actual_action": response.action,
            "reply_text": response.reply_text,
            "latency_ms": latency_ms,
            "passed": passed,
            "error": None,
        }

    except Exception as exc:

        latency_ms = round(
            (
                time.perf_counter()
                - start_t
            )
            * 1000,
            2,
        )

        return {
            "id": case["id"],
            "layer": case.get(
                "layer",
                case.get(
                    "taxonomy",
                    "UNKNOWN",
                ),
            ),
            "source": case.get(
                "source",
                "UNKNOWN",
            ),
            "expected_case": (
                case["expected_case"]
            ),
            "actual_case": "ERROR",
            "expected_action": (
                case["expected_action"]
            ),
            "actual_action": None,
            "reply_text": "",
            "latency_ms": latency_ms,
            "passed": False,
            "error": (
                f"{type(exc).__name__}: "
                f"{exc}"
            ),
        }


# =========================================================
# Generate Markdown Report
# =========================================================

def write_report(
    results: list[dict],
) -> None:

    total = len(results)

    passed = sum(
        1
        for result in results
        if result["passed"]
    )

    failed = total - passed

    pass_rate = (
        passed / total * 100
        if total
        else 0
    )

    avg_latency = (
        sum(
            result["latency_ms"]
            for result in results
        )
        / total
        if total
        else 0
    )

    lines = [
        "# Golden Set Evaluation Results",
        "",
        "## Summary",
        "",
        f"- Total cases: **{total}**",
        f"- Passed: **{passed}**",
        f"- Failed: **{failed}**",
        f"- Pass rate: **{pass_rate:.1f}%**",
        (
            "- Average end-to-end latency: "
            f"**{avg_latency:.2f} ms**"
        ),
        "",
        "## Detailed Results",
        "",
        (
            "| ID | Layer | Source | Expected | "
            "Actual | Result | Latency |"
        ),
        (
            "|---|---|---|---|---|---|---:|"
        ),
    ]

    for result in results:

        status = (
            "✅ PASS"
            if result["passed"]
            else "❌ FAIL"
        )

        expected = (
            f"{result['expected_case']} / "
            f"{result['expected_action']}"
        )

        actual = (
            f"{result['actual_case']} / "
            f"{result['actual_action']}"
        )

        lines.append(
            f"| {result['id']} "
            f"| {result['layer']} "
            f"| {result['source']} "
            f"| {expected} "
            f"| {actual} "
            f"| {status} "
            f"| {result['latency_ms']:.2f} ms |"
        )

    failures = [
        result
        for result in results
        if not result["passed"]
    ]

    lines.extend([
        "",
        "## Failed Cases",
        "",
    ])

    if not failures:

        lines.append(
            "No failed cases in this run."
        )

    else:
        for result in failures:

            lines.extend([
                f"### {result['id']}",
                "",
                (
                    "- Expected: "
                    f"`{result['expected_case']} / "
                    f"{result['expected_action']}`"
                ),
                (
                    "- Actual: "
                    f"`{result['actual_case']} / "
                    f"{result['actual_action']}`"
                ),
            ])

            if result["error"]:
                lines.append(
                    f"- Error: `{result['error']}`"
                )
            else:
                lines.append(
                    "- Model reply: "
                    f"{result['reply_text']}"
                )

            lines.extend([
                "- Failure analysis: "
                "_To be reviewed by the team._",
                "",
            ])

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    RESULTS_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


# =========================================================
# Main
# =========================================================

def main():

    cases = load_golden_set()

    print("=" * 80)
    print(
        "🚀 BẮT ĐẦU GOLDEN SET EVALUATION "
        f"({len(cases)} CASES)"
    )
    print("=" * 80)

    results = []

    for index, case in enumerate(
        cases,
        start=1,
    ):

        result = run_case(case)

        results.append(result)

        status = (
            "✅ PASS"
            if result["passed"]
            else "❌ FAIL"
        )

        print(
            f"[{index:02d}/{len(cases)}] "
            f"{status} | "
            f"{case['id']} | "
            f"{result['expected_case']} "
            f"→ {result['actual_case']} | "
            f"{result['latency_ms']} ms"
        )

    write_report(results)

    total = len(results)

    passed = sum(
        1
        for result in results
        if result["passed"]
    )

    failed = total - passed

    pass_rate = (
        passed / total * 100
        if total
        else 0
    )

    print("=" * 80)
    print("📊 KẾT QUẢ")
    print(f"Total : {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(
        f"Pass rate: {pass_rate:.1f}%"
    )
    print(
        f"Report: {RESULTS_PATH}"
    )
    print("=" * 80)


if __name__ == "__main__":
    main()