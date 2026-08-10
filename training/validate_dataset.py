"""Validate Libra AI JSONL datasets and report optional category metadata."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = ROOT / "dataset" / "train.jsonl"
VALIDATION_PATH = ROOT / "dataset" / "validation.jsonl"
METADATA_PATH = ROOT / "dataset" / "batch1_metadata.json"
VALID_ROLES = {"user", "assistant", "system"}
EXPECTED_TRAINING_COUNT = 694
EXPECTED_VALIDATION_COUNT = 674


def load_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    examples: list[dict[str, Any]] = []
    errors: list[str] = []
    if not path.exists():
        return [], [f"Missing file: {path}"]
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            if not raw_line.strip():
                errors.append(f"{path.name}:{line_number}: blank line")
                continue
            try:
                item = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.name}:{line_number}: invalid JSON ({exc.msg})")
                continue
            if not isinstance(item, dict) or set(item) != {"messages"}:
                errors.append(f"{path.name}:{line_number}: expected only a messages field")
                continue
            messages = item.get("messages")
            if not isinstance(messages, list) or not messages:
                errors.append(f"{path.name}:{line_number}: messages must be a non-empty list")
                continue
            for message in messages:
                if not isinstance(message, dict) or set(message) != {"role", "content"}:
                    errors.append(f"{path.name}:{line_number}: malformed message object")
                    continue
                if message["role"] not in VALID_ROLES:
                    errors.append(f"{path.name}:{line_number}: invalid role {message['role']!r}")
                if not isinstance(message["content"], str) or not message["content"].strip():
                    errors.append(f"{path.name}:{line_number}: empty message content")
            examples.append(item)
    return examples, errors


def fingerprint(example: dict[str, Any]) -> str:
    return json.dumps(example, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def user_prompt(example: dict[str, Any]) -> str:
    return "\n".join(
        message["content"]
        for message in example.get("messages", [])
        if isinstance(message, dict) and message.get("role") == "user" and isinstance(message.get("content"), str)
    ).strip()


def main() -> int:
    train, errors = load_jsonl(TRAIN_PATH)
    validation, validation_errors = load_jsonl(VALIDATION_PATH)
    errors.extend(validation_errors)
    train_keys = [fingerprint(item) for item in train]
    validation_keys = [fingerprint(item) for item in validation]
    train_duplicate_count = len(train_keys) - len(set(train_keys))
    validation_duplicate_count = len(validation_keys) - len(set(validation_keys))
    exact_duplicate_count = len(set(train_keys) & set(validation_keys))
    all_keys = train_keys + validation_keys
    duplicate_count = train_duplicate_count + validation_duplicate_count + exact_duplicate_count
    train_prompts = [user_prompt(item) for item in train]
    validation_prompts = [user_prompt(item) for item in validation]
    prompt_overlap_count = len(set(train_prompts) & set(validation_prompts))
    train_prompt_duplicate_count = len(train_prompts) - len(set(train_prompts))
    validation_prompt_duplicate_count = len(validation_prompts) - len(set(validation_prompts))
    if len(train) != EXPECTED_TRAINING_COUNT:
        errors.append(f"expected {EXPECTED_TRAINING_COUNT} training examples, found {len(train)}")
    if len(validation) != EXPECTED_VALIDATION_COUNT:
        errors.append(f"expected {EXPECTED_VALIDATION_COUNT} validation examples, found {len(validation)}")
    errors.extend(
        f"duplicate example detected: {key[:80]}"
        for key, count in Counter(all_keys).items()
        if count > 1
    )
    if train_prompt_duplicate_count or validation_prompt_duplicate_count:
        errors.append("duplicate user prompt detected within a dataset")
    if prompt_overlap_count:
        errors.append("user prompt overlap detected between training and validation")

    print(f"Training examples: {len(train)}")
    print(f"Validation examples: {len(validation)}")
    print(f"Training duplicate count: {train_duplicate_count}")
    print(f"Validation duplicate count: {validation_duplicate_count}")
    print(f"Cross-dataset exact duplicate count: {exact_duplicate_count}")
    print(f"Cross-dataset prompt overlap count: {prompt_overlap_count}")
    print(f"Duplicate count: {duplicate_count}")
    print(f"Invalid example count: {len(errors)}")

    if METADATA_PATH.exists():
        try:
            metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
            categories = metadata.get("training_categories", {})
            validation_categories = metadata.get("validation_categories", {})
            print("Training category distribution:")
            for category, count in categories.items():
                print(f"  {category}: {count}")
            print("Validation category distribution:")
            for category, count in validation_categories.items():
                print(f"  {category}: {count}")
        except (OSError, json.JSONDecodeError, AttributeError) as exc:
            errors.append(f"metadata error: {exc}")

    if errors:
        print("Validation result: FAILED")
        for error in errors[:20]:
            print(f"- {error}")
        if len(errors) > 20:
            print(f"- ... {len(errors) - 20} more errors")
        return 1
    print("Validation result: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())