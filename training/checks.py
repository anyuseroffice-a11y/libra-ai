"""Shared semantic checks for the Libra AI dataset builder.

These are heuristic rules that verify the strongest topic-answer, code-language,
and language-consistency signals. They are fail-fast guards during generation and
are meant to be supplemented with the standalone semantic audit and human review.
"""

from __future__ import annotations

import re

BANGLA_RE = re.compile(r"[\u0980-\u09ff]")
BANGLISH_MARKERS = re.compile(r"\b(niye|kivabe|korbo|bujhaiyen|dorkar|jhamela|hocche|korte|pathan|dekhaw|likhun|rakhun)\b", re.IGNORECASE)
BANGLISH_ANSWER_MARKERS = re.compile(r"\b(ei|prothome|dorkar|pathan|korbo|bujhte|kore|korun|koren|din|ache|rakhun|dekhen|hobe|jonno|er)\b", re.IGNORECASE)
PHP_TOKENS = ("<?php", "$pdo", "$_SESSION", "password_hash", "password_verify", "session_regenerate_id",
              "session_destroy", "hash_equals", "move_uploaded_file", "finfo", "$_FILES", "bindValue",
              "beginTransaction", "http_response_code", "filter_var", "$statement", "$errors", "PDO::")
JS_TOKENS = ("const ", "let ", "function", "fetch(", "AbortController", "addEventListener", "querySelector",
             "getElementById", "setTimeout", "clearTimeout", "localStorage", "performance.now", "=>")
SQL_TOKENS = ("SELECT", "INSERT", "UPDATE", "DELETE", "JOIN", "CREATE INDEX", "EXPLAIN", "WHERE", "TRANSACTION",
              "COMMIT", "ROLLBACK", "GROUP BY", "ORDER BY", "FULLTEXT")


def has_bangla(text: str) -> bool:
    return bool(BANGLA_RE.search(text))


def is_banglish(text: str) -> bool:
    return bool(BANGLISH_MARKERS.search(text))


def has_code(text: str) -> bool:
    return "```" in text


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


# Ordered keyword -> required answer tokens (any-of). Order matters: specific first.
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
    ("deployment", ("systemd", "journalctl", "service", "log", "systemctl")),
    ("git merge", ("merge", "conflict", "git", "branch")),
    ("permissions", ("chmod", "chown", "permission", "rwx", "umask")),
    ("rag", ("chunk", "retriev", "embedding", "vector", "index")),
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

OLD_TEMPLATE_SIGNATURES = (
    "the question about",
    "hides two decisions",
    "becomes workable when one assumption is measurable",
    "connect it to what you can see",
    "deserves the smallest design i would ship",
    "keep the core idea",
    "the important boundary is clear",
    "implementation plan:",
    "i have a problem involving",
    "review this design concern:",
    "the tradeoff is between simplicity, correctness, and operational cost",
    "start by checking the symptom against the boundary",
    "cover invalid input, retries, concurrency, partial failure",
)


def topic_violations(user: str, answer: str) -> list[str]:
    """Return a list of topic-answer consistency problems (English prompts only)."""
    problems: list[str] = []
    if has_bangla(user):
        return problems
    user_lower = user.lower()
    answer_lower = answer.lower()
    for keyword, required in TOPIC_REQUIREMENTS:
        if keyword in user_lower and not any(token in answer_lower for token in required):
            problems.append(f"topic '{keyword}' in prompt has no matching answer signal ({', '.join(required)})")
    return problems


def code_language_violations(user: str, answer: str) -> list[str]:
    """Return code-language mismatch problems when the prompt requests a specific language."""
    problems: list[str] = []
    if not has_code(answer):
        return problems
    user_lower = user.lower()
    languages = code_language(answer)
    if "mysql" in user_lower and not (languages & {"sql", "php"}):
        if languages & {"js"}:
            problems.append("MySQL prompt answered with JavaScript-only code")
        else:
            problems.append("MySQL prompt has code with no SQL/PHP")
    if "php" in user_lower and languages & {"js"} and not (languages & {"php"}):
        problems.append("PHP prompt answered with JavaScript-only code")
    if re.search(r"\b(javascript|js)\b", user_lower) and languages & {"php"} and not (languages & {"js"}):
        problems.append("JavaScript prompt answered with PHP-only code")
    return problems


def language_violations(user: str, answer: str) -> list[str]:
    """Return language-consistency problems for Bangla and Banglish prompts."""
    problems: list[str] = []
    if has_bangla(user) and not has_bangla(answer):
        problems.append("Bangla prompt has no Bangla-script answer")
    if is_banglish(user) and not has_bangla(answer) and not BANGLISH_ANSWER_MARKERS.search(answer.lower()):
        problems.append("Banglish prompt has no natural Banglish/Bangla answer")
    return problems


def check_pair(category: str, user: str, answer: str) -> list[str]:
    """Full per-pair check used by the batch builder."""
    problems: list[str] = []
    if not answer.strip():
        problems.append("empty assistant response")
    elif len(answer.strip()) < 40:
        problems.append("assistant response is shorter than 40 characters")
    if category == "programming":
        problems.extend(topic_violations(user, answer))
        problems.extend(code_language_violations(user, answer))
    problems.extend(language_violations(user, answer))
    lowered = answer.lower()
    for signature in OLD_TEMPLATE_SIGNATURES:
        if signature in lowered:
            problems.append(f"old template signature: '{signature}'")
            break
    return problems
