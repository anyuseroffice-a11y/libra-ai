"""Build the Libra AI dataset from hand-authored corpus modules.

Every example is a real user question paired with the answer a competent
developer would actually send. Corpus modules expose TRAINING and VALIDATION
lists of (user_message, assistant_message) tuples; validation scenarios are
authored separately from training scenarios.

Generation proceeds in batches of exactly 50. Each batch runs structural and
semantic checks before it is accepted, and any failed example must be fixed in
the corpus before the build completes.
"""

from __future__ import annotations

import importlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

from checks import check_pair

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"

# module name -> category -> quota. Validation scenarios are kept completely
# separate from training scenarios inside each module.
MODULES: dict[str, dict[str, int]] = {
    "corpus.programming_train_a": {"training": 100},
    "corpus.programming_train_b": {"training": 100},
    "corpus.programming_val_a": {"validation": 100},
    "corpus.programming_val_b": {"validation": 100},
    "corpus.research": {"training": 100, "validation": 100},
    "corpus.technical": {"training": 50, "validation": 50},
    "corpus.general": {"training": 75, "validation": 75},
    "corpus.conversation": {"training": 50, "validation": 50},
    "corpus.creative": {"training": 25, "validation": 25},
}

CATEGORY_BY_MODULE: dict[str, str] = {
    "corpus.programming_train_a": "programming",
    "corpus.programming_train_b": "programming",
    "corpus.programming_val_a": "programming",
    "corpus.programming_val_b": "programming",
    "corpus.research": "research",
    "corpus.technical": "technical",
    "corpus.general": "general",
    "corpus.conversation": "conversation",
    "corpus.creative": "creative",
}

BATCH_SIZE = 50


def collect(split: str) -> tuple[list[tuple[dict[str, str], str]], list[str]]:
    pairs: list[tuple[dict[str, str], str]] = []
    errors: list[str] = []
    for module_name, quotas in MODULES.items():
        quota = quotas.get(split, 0)
        if quota == 0:
            continue
        try:
            module = importlib.import_module(module_name)
        except ImportError as exc:
            errors.append(f"cannot import {module_name}: {exc}")
            continue
        items = list(getattr(module, "TRAINING" if split == "training" else "VALIDATION", []))
        if len(items) < quota:
            errors.append(f"{module_name} provides {len(items)} {split} examples, expected at least {quota}")
            continue
        category = CATEGORY_BY_MODULE[module_name]
        pairs.extend(
            ({"role": "user", "content": user}, {"role": "assistant", "content": assistant}, category)
            for user, assistant in items[:quota]
        )
    return pairs, errors


def check_batch(split: str, batch: list[tuple[dict[str, str], dict[str, str], str]], batch_number: int) -> list[str]:
    problems: list[str] = []
    prompts = [item["content"] for item, _, _ in batch]
    responses = [item["content"] for item, _, _ in batch]
    if len(prompts) != len(set(prompts)):
        problems.append(f"duplicate user prompt inside {split} batch {batch_number}")
    if len(responses) != len(set(responses)):
        problems.append(f"duplicate assistant response inside {split} batch {batch_number}")
    for position, (user, assistant, category) in enumerate(batch, start=1):
        for problem in check_pair(category, user["content"], assistant["content"]):
            problems.append(f"{split} batch {batch_number} example {position}: {problem}")
    return problems


def main() -> int:
    train, train_errors = collect("training")
    validation, validation_errors = collect("validation")
    errors = train_errors + validation_errors
    if errors:
        print("Corpus errors:")
        for error in errors:
            print(f"- {error}")
        print("Build aborted. Fix the corpus modules before building.")
        return 1

    all_train_prompts = [user["content"] for user, _, _ in train]
    all_val_prompts = [user["content"] for user, _, _ in validation]
    if len(all_train_prompts) != len(set(all_train_prompts)):
        errors.append("duplicate user prompt within training pool")
    if len(all_val_prompts) != len(set(all_val_prompts)):
        errors.append("duplicate user prompt within validation pool")
    if len(set(all_train_prompts) & set(all_val_prompts)):
        errors.append("user prompt overlap between training and validation")
    all_train_responses = [assistant["content"] for _, assistant, _ in train]
    all_val_responses = [assistant["content"] for _, assistant, _ in validation]
    if len(all_train_responses) != len(set(all_train_responses)):
        errors.append("duplicate assistant response within training pool")
    if len(all_val_responses) != len(set(all_val_responses)):
        errors.append("duplicate assistant response within validation pool")
    if len(set(all_train_responses) & set(all_val_responses)):
        errors.append("assistant response overlap between training and validation")
    if errors:
        print("Pool errors:")
        for error in errors:
            print(f"- {error}")
        print("Build aborted. Fix the corpus modules before building.")
        return 1

    for split, pairs in (("training", train), ("validation", validation)):
        if len(pairs) != 500:
            print(f"{split}: expected 500 examples, found {len(pairs)}")
            return 1
        for batch_number, start in enumerate(range(0, 500, BATCH_SIZE), start=1):
            batch = pairs[start:start + BATCH_SIZE]
            problems = check_batch(split, batch, batch_number)
            if problems:
                print(f"Failure in {split} batch {batch_number}:")
                for problem in problems:
                    print(f"- {problem}")
                print("Build aborted. Fix the corpus examples before building.")
                return 1
            print(f"{split} batch {batch_number}: 50 examples checked")

    train_records = [
        {"messages": [{"role": "user", "content": user["content"]}, {"role": "assistant", "content": assistant["content"]}]}
        for user, assistant, _ in train
    ]
    validation_records = [
        {"messages": [{"role": "user", "content": user["content"]}, {"role": "assistant", "content": assistant["content"]}]}
        for user, assistant, _ in validation
    ]
    DATASET.mkdir(parents=True, exist_ok=True)
    for path, records in ((DATASET / "train.jsonl", train_records), (DATASET / "validation.jsonl", validation_records)):
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    metadata = {
        "batch": 2,
        "training_categories": dict(Counter(category for _, _, category in train)),
        "validation_categories": dict(Counter(category for _, _, category in validation)),
        "note": "Hand-authored real user/answer pairs. Category metadata is separate so each JSONL record keeps the exact messages-only fine-tuning schema.",
    }
    (DATASET / "batch1_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Wrote dataset/train.jsonl and dataset/validation.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
