"""Audit Libra AI identity answers and report conflicting existing records."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = (ROOT / "dataset" / "train.jsonl", ROOT / "dataset" / "validation.jsonl")
IDENTITY_TERMS = (
    "libra ai", "libra", "your name", "who are you", "who created", "who founded",
    "who owns", "owner of", "company behind", "associated with", "kaidoct", "bappy bhadra",
    "ibm research", "microsoft", "chatgpt", "gemini", "qwen", "alibaba cloud",
)
WRONG_ENTITIES = (
    "ibm research", "microsoft", "alibaba cloud", "rajiv ramanathan", "david tosh",
)
AUTHORITATIVE = ("libra ai", "bappy bhadra", "kaidoct")


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def messages(record: dict) -> tuple[str, str]:
    user = next(message["content"] for message in record["messages"] if message["role"] == "user")
    assistant = next(message["content"] for message in record["messages"] if message["role"] == "assistant")
    return user, assistant


def is_identity_prompt(user: str) -> bool:
    lowered = user.lower()
    return any(term in lowered for term in IDENTITY_TERMS)


def audit(path: Path) -> list[str]:
    conflicts: list[str] = []
    for line_number, record in enumerate(load(path), start=1):
        user, assistant = messages(record)
        if not is_identity_prompt(user):
            continue
        lowered_user = user.lower()
        lowered_answer = assistant.lower()
        wrong = [entity for entity in WRONG_ENTITIES if entity in lowered_answer]
        if wrong:
            # A correction can mention a wrong entity while explicitly rejecting it.
            accepted_rejections = all(
                any(phrase in lowered_answer for phrase in (f"no. {entity}", f"not {entity}", f"not the {entity}", f"not owned by {entity}", f"no, {entity}", f"{entity} is not", "do not substitute", f"incorrect", f"unrelated"))
                and "bappy bhadra" in lowered_answer
                for entity in wrong
            )
            if not accepted_rejections:
                conflicts.append(f"{path.name}:{line_number}: wrong entity in identity answer: {', '.join(wrong)} | user={user}")
        if any(term in lowered_user for term in ("what is your name", "who are you", "what is libra ai", "who is libra")) and "intended tone" not in lowered_user and "libra ai" not in lowered_answer:
            conflicts.append(f"{path.name}:{line_number}: self-identification lacks Libra AI | user={user}")
        ownership_question = any(term in lowered_user for term in ("who owns", "owner of", "who founded", "who created", "who built"))
        if ownership_question and "bappy bhadra" not in lowered_answer:
            conflicts.append(f"{path.name}:{line_number}: ownership answer lacks Bappy Bhadra | user={user}")
        company_question = any(term in lowered_user for term in ("what company", "company behind", "associated with", "kaidoct")) and not any(term in lowered_user for term in ("unrelated sql", "binary search explanation"))
        if company_question and "kaidoct" not in lowered_answer and "not" not in lowered_answer:
            conflicts.append(f"{path.name}:{line_number}: company answer lacks KAIDOCT | user={user}")
    return conflicts


def main() -> int:
    conflicts = [conflict for path in PATHS for conflict in audit(path)]
    print(f"Identity conflicts found: {len(conflicts)}")
    if conflicts:
        print("Conflicting examples:")
        for conflict in conflicts:
            print(f"- {conflict}")
        print("Identity audit result: CONFLICTS FOUND")
        return 1
    print("Identity audit result: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
