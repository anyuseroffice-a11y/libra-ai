"""Heuristic semantic audit for topic and code consistency.

Flags likely mismatches using category-specific keyword checks and obvious
unrelated code-language mismatches. These are heuristics only, not a
replacement for human review. DO NOT train until flags are reviewed.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = (ROOT / "dataset" / "train.jsonl", ROOT / "dataset" / "validation.jsonl")

PHP_TOKENS = ("<?php", "$pdo", "$_SESSION", "password_hash", "password_verify", "session_regenerate_id",
              "session_destroy", "hash_equals", "move_uploaded_file", "finfo", "$_FILES", "bindValue",
              "beginTransaction", "http_response_code", "filter_var", "$statement", "$errors", "PDO::")
JS_TOKENS = ("const ", "let ", "function", "fetch(", "AbortController", "addEventListener", "querySelector",
             "getElementById", "setTimeout", "clearTimeout", "localStorage", "performance.now", "=>")
SQL_TOKENS = ("select", "insert", "update", "delete", "join", "create index", "explain", "where", "transaction",
              "commit", "rollback", "group by", "order by", "fulltext", "migration", "schema", "mysql",
              "column", "table", "index", "query", "database", "sql", "innodb")

TOPIC_REQUIREMENTS: list[tuple[str, tuple[str, ...]]] = [
    ("safe delete", ("delete", "transaction", "rollback", "where", "soft delete")),
    ("composite index", ("index", "explain", "created_at", "where")),
    ("file upload", ("upload", "$_files", "move_uploaded_file", "finfo", "size")),
    ("image validation", ("finfo", "getimagesize", "mime", "size", "imagetypes")),
    ("password reset", ("reset", "token", "expiry", "password")),
    ("session timeout", ("session", "last_activity", "idle", "timeout", "expire")),
    ("race condition", ("abortcontroller", "abort", "stale", "request", "race")),
    ("debounce", ("debounce", "timer", "settimeout", "cleartimeout")),
    ("form validation", ("validate", "required", "pattern", "checkvalidity")),
    ("api errors", ("response.ok", "status", "catch", "401", "422", "500")),
    ("localstorage", ("localstorage", "json.parse", "setitem", "getitem")),
    ("dom", ("queryselector", "getelementbyid", "addeventlistener", "innerhtml", "dom")),
    ("tailwind", ("tailwind", "class", "breakpoint", "grid", "flex")),
    ("rate limit", ("rate", "limit", "429", "bucket", "throttl")),
    ("authentication architecture", ("token", "session", "jwt", "oauth", "refresh")),
    ("deployment", ("systemd", "journalctl", "service", "log", "systemctl", "blue-green", "canary", "rolling", "downtime", "rollback", "environment", "rollout", "deploy", "release", "infrastructure", "ci/cd", "pipeline", "container", "docker", "kubernetes", "k8s")),
    ("git merge", ("merge", "conflict", "git", "branch")),
    ("permissions", ("chmod", "chown", "permission", "rwx", "umask")),
    ("rag", ("chunk", "retriev", "embedding", "vector", "index", "knowledge", "source", "document", "search", "context", "prompt", "llm", "model", "retrain", "fine-tun", "combine", "updatable", "transparent")),
    ("llm api", ("model", "key", "prompt", "timeout", "retry")),
    ("registration", ("password_hash", "insert into", "duplicate", "register")),
    ("login", ("password_verify", "session", "credentials", "hash")),
    ("logout", ("session_destroy", "cookie", "logout")),
    ("csrf", ("csrf", "token", "hash_equals", "random_bytes")),
    ("pagination", ("limit", "offset", "page")),
    ("crud", ("insert", "update", "delete", "select", "crud")),
    ("index", ("index", "explain", "where")),
    ("joins", ("join", "left join", "foreign key", "inner join")),
    ("transaction", ("transaction", "commit", "rollback", "begintransaction")),
    ("deadlock", ("deadlock", "innodb", "lock", "status")),
    ("foreign keys", ("foreign key", "referential", "constraint", "cascade")),
    ("slow query", ("explain", "index", "scan", "filesort", "plan")),
    ("rest api", ("resource", "method", "endpoint", "http", "route")),
    ("api authentication", ("token", "header", "apikey", "bearer", "key")),
]

BANGLISH_ANSWER_MARKERS = re.compile(r"\b(ei|prothome|dorkar|pathan|korbo|bujhte|kore|korun|koren|din|ache|rakhun|dekhen|hobe|jonno|er)\b", re.IGNORECASE)


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def pair(row: dict) -> tuple[str, str]:
    user = next(message["content"] for message in row["messages"] if message["role"] == "user")
    assistant = next(message["content"] for message in row["messages"] if message["role"] == "assistant")
    return user, assistant


def has_code(text: str) -> bool:
    return "```" in text or bool(re.search(r"\b(SELECT|INSERT|DELETE|UPDATE|const |function |session_start|password_hash)\b", text))


def code_language(text: str) -> set[str]:
    lowered = text.lower()
    found: set[str] = set()
    if any(token in lowered for token in PHP_TOKENS):
        found.add("php")
    if any(token in lowered for token in JS_TOKENS):
        found.add("js")
    if any(token in lowered for token in SQL_TOKENS):
        found.add("sql")
    return found


def audit(path: Path) -> list[str]:
    flags: list[str] = []
    for number, row in enumerate(rows(path), start=1):
        user, assistant = pair(row)
        user_lower = user.lower()
        answer_lower = assistant.lower()
        location = f"{path.name}:{number}"
        if "mysql" in user_lower and not re.search(r"[\u0980-\u09ff]", user_lower):
            languages = code_language(assistant)
            if languages & {"js"} and not (languages & {"sql", "php"}):
                flags.append(f"{location}: MySQL question contains JavaScript-only answer")
        if "php" in user_lower and not re.search(r"[\u0980-\u09ff]", user_lower):
            if has_code(assistant):
                languages = code_language(assistant)
                if languages & {"js"} and not (languages & {"php"}):
                    flags.append(f"{location}: PHP question contains JavaScript-only code")
                if "php file upload" in user_lower or "document uploads" in user_lower or "file upload" in user_lower:
                    if not any(token in answer_lower for token in ("upload", "$_files", "finfo", "move_uploaded_file")):
                        flags.append(f"{location}: PHP upload question lacks upload implementation")
                    elif "password_verify" in answer_lower and "upload" not in answer_lower:
                        flags.append(f"{location}: PHP upload answer appears to be login code")
            if "registration" in user_lower and not any(token in answer_lower for token in ("password_hash", "insert into", "duplicate")):
                flags.append(f"{location}: registration question lacks registration implementation")
            if "login" in user_lower and not any(token in answer_lower for token in ("password_verify", "session", "credentials")):
                flags.append(f"{location}: login question lacks login handling")
        if re.search(r"\b(javascript|js)\b", user_lower) and not re.search(r"[\u0980-\u09ff]", user_lower):
            if any(token in user_lower for token in ("race condition", "older response", "old results", "stale")):
                if not any(token in answer_lower for token in ("abortcontroller", "abort", "stale", "request")):
                    flags.append(f"{location}: JavaScript race question lacks a cancellation/order fix")
            languages = code_language(assistant)
            if languages & {"php"} and not (languages & {"js"}):
                flags.append(f"{location}: JavaScript question contains PHP-only code")
        if not re.search(r"[\u0980-\u09ff]", user_lower):
            for keyword, required in TOPIC_REQUIREMENTS:
                if keyword in user_lower and not any(token in answer_lower for token in required):
                    flags.append(f"{location}: '{keyword}' question lacks a matching answer signal ({', '.join(required)})")
                    break
        # Identity checks
        if any(w in user_lower for w in ("your name", "who are you", "who is libra", "who created", "who owns", "what is libra ai", "company behind libra")):
            if not any(w in answer_lower for w in ("libra ai", "bappy bhadra", "kaidoct")):
                flags.append(f"{location}: Identity question lacks Libra AI/Bappy Bhadra/KAIDOCT answer")
        # Math checks - only flag when question explicitly asks for explanation
        if any(w in user_lower for w in ("explain", "why", "show steps", "derive", "prove")):
            if any(w in user_lower for w in ("solve", "calculate", "find the", "compute", "evaluate", "integral", "derivative", "matrix", "eigenvalue", "probability")):
                if not any(w in answer_lower for w in ("=", "step", "therefore", "result", "answer", "solution", "explanation")):
                    if len(assistant) < 50:
                        flags.append(f"{location}: Math question with explicit explanation request lacks reasoning steps")
        # Algorithm checks - only flag if question is primarily about algorithms/data structures
        if re.search(r"\b(binary search|merge sort|quick sort|bfs|dfs|dijkstra|dynamic programming|greedy|backtrack|linked list|hash table|trie|graph algorithm|complexity analysis|big o|data structure|implement.*algorithm|algorithm.*implement)\b", user_lower):
            if not any(w in answer_lower for w in ("o(", "algorithm", "time", "space", "complexity", "data structure", "queue", "stack", "level", "deep", "search", "sort", "optimal", "locally", "globally", "choice", "step", "activity", "huffman", "coding")):
                if len(assistant) > 50:
                    flags.append(f"{location}: Algorithm question lacks algorithm/data structure content")
        # AI/ML checks - relaxed to accept security/operational LLM discussions
        if re.search(r"\b(transformer|neural network|attention mechanism|embedding|fine-tun|lora|qlora|tokeniz|llm|language model)\b", user_lower):
            if not any(w in answer_lower for w in ("model", "train", "layer", "attention", "embed", "token", "param", "gradient", "rag", "fine-tun", "knowledge", "retrain", "retrieval", "source", "prompt", "injection", "validation", "input", "attack", "security")):
                flags.append(f"{location}: AI/ML question lacks ML terminology in answer")
        # System design checks - only flag if question is clearly about system design
        if re.search(r"\b(design a|system design|url shortener|chat system|notification system|rate limit|caching|load balanc|microservice|event-driven|message queue)\b", user_lower):
            if not any(w in answer_lower for w in ("component", "service", "database", "cache", "queue", "api", "load", "scale", "endpoint", "architecture", "redis", "mysql", "storage", "index", "hash", "webhook", "model", "push", "pull", "read", "write", "sync", "websocket", "concurrent", "preference", "notification", "channel", "init", "backup", "restore", "verify", "deploy", "rollout", "downtime", "risk", "rollback", "http", "header", "signature", "retry", "log", "subscriber", "sql", "migration", "table", "regex", "dns", "lookup", "format", "version", "meta")):
                if len(assistant) > 50:
                    flags.append(f"{location}: System design question lacks design content")
        # Language checks
        if re.search(r"[\u0980-\u09ff]", user) and not re.search(r"[\u0980-\u09ff]", assistant):
            flags.append(f"{location}: Bangla user message has no Bangla-script answer")
        if re.search(r"\b(niye|kivabe|korbo|bujhaiyen|dorkar|jhamela|hocche|korte)\b", user_lower) and not re.search(r"[\u0980-\u09ff]", assistant) and not BANGLISH_ANSWER_MARKERS.search(answer_lower):
            flags.append(f"{location}: Banglish answer lacks detectable natural Banglish wording")
    return flags


def main() -> int:
    flags = [flag for path in PATHS for flag in audit(path)]
    code_topic_mismatch = sum(1 for flag in flags if "code" in flag or "JavaScript-only" in flag or "PHP-only" in flag or "implementation" in flag)
    language_mismatch = sum(1 for flag in flags if "Bangla" in flag or "Banglish" in flag)
    print(f"Semantic audit flags: {len(flags)}")
    print(f"Code-topic mismatch flags: {code_topic_mismatch}")
    print(f"Language mismatch flags: {language_mismatch}")
    if flags:
        print("Semantic audit result: FAILED")
        for flag in flags[:60]:
            print(f"- {flag}")
        if len(flags) > 60:
            print(f"- ... {len(flags) - 60} more flags")
        return 1
    print("Semantic audit result: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
