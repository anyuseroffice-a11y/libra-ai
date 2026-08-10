"""Heuristic quality audit for Libra AI instruction data."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"
PATHS = {"train": DATASET / "train.jsonl", "validation": DATASET / "validation.jsonl"}
OLD_TEMPLATE_SIGNATURES = (
    "Implementation plan:",
    "Start by checking the symptom against the boundary",
    "Keep the core idea, but verify these risks",
    "Cover invalid input, retries, concurrency, partial failure",
    "I have a problem involving",
    "Review this design concern:",
    "The question about",
    "becomes workable when one assumption is measurable",
    "Connect it to what you can see",
    "deserves the smallest design I would ship",
    "The important boundary is clear",
    "Compare the first safe baseline",
)


def read_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def messages(row: dict) -> tuple[str, str]:
    user = next((m["content"] for m in row["messages"] if m["role"] == "user"), "")
    assistant = next((m["content"] for m in row["messages"] if m["role"] == "assistant"), "")
    return user, assistant


def opening(text: str) -> str:
    words = re.findall(r"[\w’'-]+", text.lower())
    return " ".join(words[:5])


def is_identity_question(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in ("your name", "who are you", "libra ai", "who created", "who owns", "kaidoct", "chatgpt", "gemini", "qwen", "identity", "assistant name", "project identity"))


def is_concise_math_answer(user: str, response: str) -> bool:
    lowered = user.lower()
    math_terms = ("sum", "log_", "derivative", "integral", "probability", "gcd", "inverse", "mod", "sin(", "cos(", "eigen", "second derivative", "term of", "orthogonal", "prime", "area", "series", "arrangements", "edges in", "complex")
    arithmetic_shape = any(symbol in user for symbol in ("=", "+", "-", "<", ">", "^", "|", "sqrt", "x")) and any(char.isdigit() for char in user)
    return (any(term in lowered for term in math_terms) or arithmetic_shape) and ("=" in response or "->" in response or "therefore" in response.lower() or "!" in response)


def audit_split(name: str, rows: list[dict]) -> tuple[list[str], Counter, Counter]:
    issues: list[str] = []
    users = [messages(row)[0] for row in rows]
    responses = [messages(row)[1] for row in rows]
    duplicate_responses = Counter(responses)
    repeated_openings = Counter(opening(text) for text in responses)
    if len(responses) != len(set(responses)):
        issues.append(f"{name}: duplicate assistant responses = {len(responses) - len(set(responses))}")
    for index, (user, response) in enumerate(zip(users, responses), start=1):
        lowered = user.lower()
        if len(response.strip()) < 40 and not is_identity_question(user) and not is_concise_math_answer(user, response):
            issues.append(f"{name}:{index}: very short assistant response")
        if not response.strip():
            issues.append(f"{name}:{index}: empty assistant response")
        if any(signature.lower() in response.lower() or signature.lower() in user.lower() for signature in OLD_TEMPLATE_SIGNATURES):
            issues.append(f"{name}:{index}: old template signature")
        if any(word in lowered for word in ("file upload", "upload a file", "document upload")) and not any(word in response.lower() for word in ("upload", "move_uploaded_file", "finfo", "$_files")):
            issues.append(f"{name}:{index}: upload question lacks upload-specific answer")
        if "password reset" in lowered and not any(word in response.lower() for word in ("reset", "token", "password")):
            issues.append(f"{name}:{index}: password-reset question lacks reset-specific answer")
        if any(word in lowered for word in ("race condition", "older response", "old results")) and not any(word in response.lower() for word in ("abortcontroller", "stale", "request", "race")):
            issues.append(f"{name}:{index}: race-condition question lacks concurrency-specific answer")
        if "composite index" in lowered and not any(word in response.lower() for word in ("index", "tenant_id", "created_at", "explain")):
            issues.append(f"{name}:{index}: index question lacks index-specific answer")
        if re.search(r"[\u0980-\u09ff]", user) and not re.search(r"[\u0980-\u09ff]", response):
            issues.append(f"{name}:{index}: Bangla prompt has no Bangla-script response")
        if re.search(r"\b(niye|kivabe|ki korbo|bujhaiyen|dorkar|pathan)\b", user.lower()) and not re.search(r"\b(ei|prothome|dorkar|pathan|korbo|bujhte|kore|korun|din)\b", response.lower()):
            issues.append(f"{name}:{index}: Banglish prompt has no natural Banglish response")
    return issues, duplicate_responses, repeated_openings


def main() -> int:
    all_issues: list[str] = []
    all_responses: list[str] = []
    opening_counts: Counter[str] = Counter()
    for name, path in PATHS.items():
        rows = read_rows(path)
        issues, responses, openings = audit_split(name, rows)
        all_issues.extend(issues)
        all_responses.extend(responses)
        opening_counts.update(openings)
        print(f"{name.title()} rows: {len(rows)}")
        print(f"{name.title()} duplicate assistant responses: {sum(count - 1 for count in responses.values() if count > 1)}")
        print(f"{name.title()} repeated opening groups: {sum(1 for count in openings.values() if count > 1)}")
    print(f"All-split duplicate assistant responses: {len(all_responses) - len(set(all_responses))}")
    print(f"Quality issue count: {len(all_issues)}")
    print("Top 20 assistant opening phrases:")
    for phrase, count in opening_counts.most_common(20):
        print(f"  {count:>3}  {phrase}")
    if all_issues:
        print("Quality audit result: FAILED")
        for issue in all_issues[:30]:
            print(f"- {issue}")
        if len(all_issues) > 30:
            print(f"- ... {len(all_issues) - 30} more issues")
        return 1
    print("Quality audit result: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
