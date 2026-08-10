"""Extend the Libra AI dataset with new categories.

This script merges existing high-quality examples with new targeted examples
for identity, mathematics, algorithms, system design, AI/ML, and more.

DO NOT train the model until all audits pass and flags are reviewed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"
TRAIN_PATH = DATASET / "train.jsonl"
VAL_PATH = DATASET / "validation.jsonl"
METADATA_PATH = DATASET / "batch1_metadata.json"

sys.path.insert(0, str(ROOT / "training"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def make_row(user: str, assistant: str) -> dict:
    return {"messages": [{"role": "user", "content": user}, {"role": "assistant", "content": assistant}]}


def run_semantic_audit() -> list[str]:
    """Run the semantic audit and return flags."""
    try:
        from semantic_audit import audit
        from pathlib import Path as P
        flags = []
        for p in [DATASET / "train.jsonl", DATASET / "validation.jsonl"]:
            flags.extend(audit(p))
        return flags
    except Exception as e:
        print(f"Warning: Could not run semantic audit: {e}")
        return []


def filter_existing(existing: list[dict]) -> list[dict]:
    """Remove examples that would fail the semantic audit."""
    filtered = []
    for row in existing:
        user = next((m["content"] for m in row["messages"] if m["role"] == "user"), "")
        assistant = next((m["content"] for m in row["messages"] if m["role"] == "assistant"), "")
        user_lower = user.lower()

        # Skip MySQL questions with JavaScript-only answers
        if "mysql" in user_lower and not any(tok in assistant.lower() for tok in ("select", "insert", "update", "delete", "index", "sql")):
            if any(tok in assistant.lower() for tok in ("const ", "let ", "function", "fetch(")):
                continue
        # Skip RAG questions without proper signals
        if "rag" in user_lower and not any(tok in assistant.lower() for tok in ("chunk", "retriev", "embedding", "vector")):
            continue

        filtered.append(row)
    return filtered


def deduplicate(train: list[dict], val: list[dict]) -> tuple[list[dict], list[dict]]:
    """Remove duplicates within and across splits."""
    seen_users = set()
    deduped_train = []
    for row in train:
        user = next((m["content"] for m in row["messages"] if m["role"] == "user"), "")
        if user not in seen_users:
            seen_users.add(user)
            deduped_train.append(row)

    deduped_val = []
    for row in val:
        user = next((m["content"] for m in row["messages"] if m["role"] == "user"), "")
        if user not in seen_users:
            seen_users.add(user)
            deduped_val.append(row)

    return deduped_train, deduped_val


def main() -> None:
    print("=" * 60)
    print("Libra AI Dataset Extension")
    print("=" * 60)

    # Load existing data
    existing_train = load_jsonl(TRAIN_PATH)
    existing_val = load_jsonl(VAL_PATH)
    print(f"\nLoaded: {len(existing_train)} train, {len(existing_val)} val")

    # Filter out failing examples
    filtered_train = filter_existing(existing_train)
    filtered_val = filter_existing(existing_val)
    removed = (len(existing_train) - len(filtered_train)) + (len(existing_val) - len(filtered_val))
    print(f"Removed {removed} failing examples")
    print(f"After filtering: {len(filtered_train)} train, {len(filtered_val)} val")

    # Load new examples from modules
    new_examples = []

    from examples.identity import IDENTITY_TRAIN, IDENTITY_VAL
    new_examples.append(("identity", IDENTITY_TRAIN, IDENTITY_VAL))

    from examples.mathematics import MATH_TRAIN, MATH_VAL
    new_examples.append(("mathematics", MATH_TRAIN, MATH_VAL))

    from examples.algorithms import ALGO_TRAIN, ALGO_VAL
    new_examples.append(("algorithms", ALGO_TRAIN, ALGO_VAL))

    from examples.system_design import SYS_TRAIN, SYS_VAL
    new_examples.append(("system_design", SYS_TRAIN, SYS_VAL))

    from examples.ai_ml import ML_TRAIN, ML_VAL
    new_examples.append(("ai_ml", ML_TRAIN, ML_VAL))

    from examples.research import RESEARCH_TRAIN, RESEARCH_VAL
    new_examples.append(("research_deep", RESEARCH_TRAIN, RESEARCH_VAL))

    from examples.programming_deep import PROG_TRAIN, PROG_VAL
    new_examples.append(("programming_deep", PROG_TRAIN, PROG_VAL))

    # Add new examples to splits
    train_rows = list(filtered_train)
    val_rows = list(filtered_val)

    train_counts = {}
    val_counts = {}
    for cat, train_exs, val_exs in new_examples:
        for ex in train_exs:
            train_rows.append(make_row(ex[0], ex[1]))
        for ex in val_exs:
            val_rows.append(make_row(ex[0], ex[1]))
        train_counts[cat] = len(train_exs)
        val_counts[cat] = len(val_exs)
        print(f"Added {len(train_exs)} train + {len(val_exs)} val for {cat}")

    # Deduplicate
    train_rows, val_rows = deduplicate(train_rows, val_rows)
    print(f"\nAfter dedup: {len(train_rows)} train, {len(val_rows)} val")

    # Write
    write_jsonl(TRAIN_PATH, train_rows)
    write_jsonl(VAL_PATH, val_rows)
    print(f"\nWrote {TRAIN_PATH}")
    print(f"Wrote {VAL_PATH}")

    # Update metadata
    metadata = {
        "batch": 1,
        "training_categories": train_counts,
        "validation_categories": val_counts,
        "total_training": len(train_rows),
        "total_validation": len(val_rows),
        "note": "Extended dataset with identity, mathematics, algorithms, system design, AI/ML, and deeper examples."
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {METADATA_PATH}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total training: {len(train_rows)}")
    print(f"Total validation: {len(val_rows)}")
    print("\nTraining category breakdown:")
    for cat, count in sorted(train_counts.items()):
        print(f"  {cat}: {count}")
    print("\nValidation category breakdown:")
    for cat, count in sorted(val_counts.items()):
        print(f"  {cat}: {count}")

    print("\nDone. Run audits before training.")
    print("  python training/validate_dataset.py")
    print("  python training/quality_audit.py")
    print("  python training/semantic_audit.py")


if __name__ == "__main__":
    main()
