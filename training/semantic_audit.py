"""Heuristic semantic audit for topic and code consistency."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = (ROOT / "dataset" / "train.jsonl", ROOT / "dataset" / "validation.jsonl")


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def pair(row: dict) -> tuple[str, str]:
    user = next(message["content"] for message in row["messages"] if message["role"] == "user")
    assistant = next(message["content"] for message in row["messages"] if message["role"] == "assistant")
    return user, assistant


def has_code(text: str) -> bool:
    return "```" in text or bool(re.search(r"\b(SELECT|INSERT|DELETE|UPDATE|const |function |session_start|password_hash)\b", text))


def audit(path: Path) -> list[str]:
    flags: list[str] = []
    for number, row in enumerate(rows(path), start=1):
        user, assistant = pair(row)
        user_lower = user.lower()
        answer_lower = assistant.lower()
        location = f"{path.name}:{number}"
        if "mysql" in user_lower or "sql query" in user_lower:
            if "safe delete" in user_lower and not any(token in answer_lower for token in ("delete", "transaction", "rollback", "where")):
                flags.append(f"{location}: MySQL safe-delete question lacks DELETE/transaction handling")
            if "index" in user_lower and not any(token in answer_lower for token in ("index", "explain", "where", "created_at")):
                flags.append(f"{location}: MySQL index question lacks index reasoning")
            if "javascript" in answer_lower and not any(token in answer_lower for token in ("sql", "mysql", "query", "index", "delete")):
                flags.append(f"{location}: MySQL question contains JavaScript-only answer")
        if "php file upload" in user_lower or "document uploads" in user_lower:
            if not any(token in answer_lower for token in ("upload", "$_files", "finfo", "move_uploaded_file")):
                flags.append(f"{location}: PHP upload question lacks upload implementation")
            if "password_verify" in answer_lower and "upload" not in answer_lower:
                flags.append(f"{location}: PHP upload answer appears to be login code")
        if "php" in user_lower and "```" in assistant:
            has_php = any(token in assistant for token in ("<?php", "$pdo", "$statement", "$_SESSION", "password_", "http_response_code"))
            has_js = any(token in assistant for token in ("const ", "let ", "fetch(", "performance.now", "logger.info"))
            if has_js and not has_php:
                flags.append(f"{location}: PHP question contains JavaScript-only code")
        if "registration" in user_lower and not any(token in answer_lower for token in ("password_hash", "insert into", "registration", "duplicate")):
            flags.append(f"{location}: registration question lacks registration implementation")
        if "login" in user_lower and not any(token in answer_lower for token in ("password_verify", "session", "credentials")):
            flags.append(f"{location}: login question lacks login handling")
        if any(token in user_lower for token in ("race condition", "older response", "old results")):
            if not any(token in answer_lower for token in ("abortcontroller", "abort", "stale", "request")):
                flags.append(f"{location}: JavaScript race question lacks a cancellation/order fix")
            if "javascript" in answer_lower and "fetch" not in answer_lower and has_code(assistant):
                flags.append(f"{location}: race-condition code lacks fetch implementation")
        if re.search(r"[\u0980-\u09ff]", user) and not re.search(r"[\u0980-\u09ff]", assistant):
            flags.append(f"{location}: Bangla user message has no Bangla-script answer")
        if re.search(r"\b(niye|kivabe|korbo|bujhaiyen|dorkar)\b", user_lower) and not re.search(r"\b(korun|koren|korbo|dekhen|chalan|din|ache)\b", answer_lower):
            flags.append(f"{location}: Banglish answer lacks detectable natural Banglish wording")
    return flags


def main() -> int:
    flags = [flag for path in PATHS for flag in audit(path)]
    print(f"Semantic audit flags: {len(flags)}")
    print(f"Code-topic mismatch flags: {sum('code' in flag or 'JavaScript-only' in flag for flag in flags)}")
    print(f"Language mismatch flags: {sum('Bangla' in flag or 'Banglish' in flag for flag in flags)}")
    if flags:
        print("Semantic audit result: FAILED")
        for flag in flags[:50]:
            print(f"- {flag}")
        return 1
    print("Semantic audit result: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
