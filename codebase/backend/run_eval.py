import json
import time
from pathlib import Path

from app.schemas import ChatRequest
from app.services.tutor_service import handle_chat


# =========================================================
# Paths
# =========================================================

BACKEND_ROOT = Path(__file__).resolve().parent
REPO_ROOT = BACKEND_ROOT.parents[1]

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
            f"Golden set not found: {GOLDEN_SET_PATH}"
        )

    with GOLDEN_SET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "golden_set.json must contain a JSON array."
        )

    return data


# =========================================================
# Run one test case
# =========================================================

def run_case(test_case: dict) -> dict:

    request = ChatRequest(
        user_input=test_case["user_input"],
        slide_context=test_case["slide_context"],
        slide_page=test_case.get(
            "slide_page",
            1,
        ),
    )

    expected_case = test_case[
        "expected_case"
    ]

    expected_action = test_case.get(
        "expected_action"
    )

    start_time = time.perf_counter()

    try:
        response = handle_chat(request)

        elapsed_ms = (
            time.perf_counter() - start_time
        ) * 1000

        case_pass = (
            response.case
            == expected_case
        )

        action_pass = (
            expected_action is None
            or response.action
            == expected_action
        )

        passed = (
            case_pass
            and action_pass
        )

        return {
            "id": test_case["id"],
            "taxonomy": test_case.get(
                "taxonomy",
                test_case.get(
                    "layer",
                    "UNKNOWN",
                ),
            ),
            "source": test_case.get(
                "source",
                "UNKNOWN",
            ),
            "expected_case": (
                expected_case
            ),
            "actual_case": (
                response.case
            ),
            "expected_action": (
                expected_action
            ),
            "actual_action": (
                response.action
            ),
            "passed": passed,
            "latency_ms": round(
                elapsed_ms,
                2,
            ),
            "error": None,
        }

    except Exception as exc:

        elapsed_ms = (
            time.perf_counter() - start_time
        ) * 1000

        return {
            "id": test_case["id"],
            "taxonomy": test_case.get(
                "taxonomy",
                test_case.get(
                    "layer",
                    "UNKNOWN",
                ),
            ),
            "source": test_case.get(
                "source",
                "UNKNOWN",
            ),
            "expected_case": (
                expected_case
            ),
            "actual_case": "ERROR",
            "expected_action": (
                expected_action
            ),
            "actual_action": None,
            "passed": False,
            "latency_ms": round(
                elapsed_ms,
                2,
            ),
            "error": (
                f"{type(exc).__name__}: {exc}"
            ),
        }


# =========================================================
# Markdown report
# =========================================================

def write_results(
    results: list[dict],
) -> None:

    total = len(results)

    passed = sum(
        result["passed"]
        for result in results
    )

    failed = total - passed

    pass_rate = (
        passed / total * 100
        if total
        else 0
    )

    avg_latency = (
        sum(
            r["latency_ms"]
            for r in results
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
        (
            f"- Pass rate: "
            f"**{pass_rate:.2f}%**"
        ),
        (
            f"- Average latency: "
            f"**{avg_latency:.2f} ms**"
        ),
        "",
        "## Detailed Results",
        "",
        (
            "| ID | Taxonomy | Expected | "
            "Actual | Pass | Latency (ms) |"
        ),
        (
            "|---|---|---|---|---|---:|"
        ),
    ]

    for result in results:

        mark = (
            "✅"
            if result["passed"]
            else "❌"
        )

        lines.append(
            f"| {result['id']} "
            f"| {result['taxonomy']} "
            f"| {result['expected_case']} "
            f"| {result['actual_case']} "
            f"| {mark} "
            f"| {result['latency_ms']} |"
        )

    failures = [
        result
        for result in results
        if not result["passed"]
    ]

    if failures:

        lines.extend([
            "",
            "## Failed Cases",
            "",
        ])

        for result in failures:

            lines.append(
                f"### {result['id']}"
            )

            lines.append("")

            lines.append(
                f"- Expected case: "
                f"`{result['expected_case']}`"
            )

            lines.append(
                f"- Actual case: "
                f"`{result['actual_case']}`"
            )

            if result["error"]:
                lines.append(
                    f"- Error: "
                    f"`{result['error']}`"
                )

            lines.append("")

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

    golden_set = load_golden_set()

    print(
        f"Running {len(golden_set)} "
        f"Golden Set cases...\n"
    )

    results = []

    for index, test_case in enumerate(
        golden_set,
        start=1,
    ):

        case_id = test_case["id"]

        print(
            f"[{index}/{len(golden_set)}] "
            f"{case_id}...",
            end=" ",
            flush=True,
        )

        result = run_case(
            test_case
        )

        results.append(result)

        if result["passed"]:
            print(
                f"PASS "
                f"({result['actual_case']})"
            )
        else:
            print(
                f"FAIL "
                f"(expected "
                f"{result['expected_case']}, "
                f"got "
                f"{result['actual_case']})"
            )

    write_results(results)

    passed = sum(
        r["passed"]
        for r in results
    )

    total = len(results)

    print("\n====================")
    print("Evaluation completed")
    print("====================")

    print(
        f"Passed: {passed}/{total}"
    )

    print(
        f"Pass rate: "
        f"{passed / total * 100:.2f}%"
        if total
        else "Pass rate: N/A"
    )

    print(
        f"Report: {RESULTS_PATH}"
    )


if __name__ == "__main__":
    main()