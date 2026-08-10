"""Consolidated final quality report for the Libra AI dataset.

Combines structural validation, quality audit, and semantic audit numbers into
one report, printed to stdout and written to training/quality_report.txt.

The model must NOT be trained until semantic audit flags are reviewed.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

from quality_audit import OLD_TEMPLATE_SIGNATURES, audit_split, read_rows
from semantic_audit import audit
from validate_dataset import load_jsonl, user_prompt

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"
TRAIN_PATH = DATASET / "train.jsonl"
VALIDATION_PATH = DATASET / "validation.jsonl"
REPORT_PATH = ROOT / "training" / "quality_report.txt"


def main() -> int:
    train, train_errors = load_jsonl(TRAIN_PATH)
    validation, validation_errors = load_jsonl(VALIDATION_PATH)
    train_pairs, val_pairs = read_rows(TRAIN_PATH), read_rows(VALIDATION_PATH)
    train_prompts = [user_prompt(item) for item in train]
    validation_prompts = [user_prompt(item) for item in validation]
    all_responses = [next(m["content"] for m in row["messages"] if m["role"] == "assistant") for row in train_pairs + val_pairs]

    exact_duplicates = len(set(json_fingerprint(item) for item in train + validation))
    train_dup = len(train) - len(set(json_fingerprint(item) for item in train))
    validation_dup = len(validation) - len(set(json_fingerprint(item) for item in validation))
    cross_dup = len(set(json_fingerprint(item) for item in train) & set(json_fingerprint(item) for item in validation))
    prompt_overlap = len(set(train_prompts) & set(validation_prompts))
    duplicate_responses = len(all_responses) - len(set(all_responses))

    openings = Counter()
    for name, rows in (("train", train_pairs), ("validation", val_pairs)):
        _, _, counts = audit_split(name, rows)
        openings.update(counts)
    repeated_openings = sum(1 for count in openings.values() if count > 1)

    semantic_flags = [flag for path in (TRAIN_PATH, VALIDATION_PATH) for flag in audit(path)]
    code_topic_mismatch = sum(1 for flag in semantic_flags if "code" in flag or "JavaScript-only" in flag or "PHP-only" in flag or "implementation" in flag)
    language_mismatch = sum(1 for flag in semantic_flags if "Bangla" in flag or "Banglish" in flag)

    template_signature_hits = 0
    for row in train_pairs + val_pairs:
        text = row["messages"][0]["content"] + " " + row["messages"][1]["content"]
        lowered = text.lower()
        if any(signature.lower() in lowered for signature in OLD_TEMPLATE_SIGNATURES):
            template_signature_hits += 1

    lines = [
        "Libra AI dataset final quality report",
        "====================================",
        f"Training count: {len(train)}",
        f"Validation count: {len(validation)}",
        f"Exact duplicates (within+between splits): {train_dup + validation_dup + cross_dup}",
        f"  Training duplicates: {train_dup}",
        f"  Validation duplicates: {validation_dup}",
        f"  Cross-dataset exact duplicates: {cross_dup}",
        f"Exact duplicates (all 1000, set count): {exact_duplicates}",
        f"Prompt overlap (train vs validation): {prompt_overlap}",
        f"Duplicate responses (all splits): {duplicate_responses}",
        f"Repeated opening groups: {repeated_openings}",
        f"Old template signature hits: {template_signature_hits}",
        f"Semantic audit flags: {len(semantic_flags)}",
        f"Code-topic mismatch flags: {code_topic_mismatch}",
        f"Language mismatch flags: {language_mismatch}",
        "",
    ]
    metadata_path = DATASET / "batch1_metadata.json"
    if metadata_path.exists():
        import json
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            lines.append("Training category distribution:")
            for category, count in metadata.get("training_categories", {}).items():
                lines.append(f"  {category}: {count}")
            lines.append("Validation category distribution:")
            for category, count in metadata.get("validation_categories", {}).items():
                lines.append(f"  {category}: {count}")
        except (OSError, json.JSONDecodeError) as exc:
            lines.append(f"(metadata unavailable: {exc})")

    print("\n".join(lines))
    report = "\n".join(lines) + "\n"
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"\nReport written to {REPORT_PATH}")
    print("\nTop 15 assistant opening phrases:")
    for phrase, count in openings.most_common(15):
        print(f"  {count:>3}  {phrase}")
    if semantic_flags:
        print(f"\n{len(semantic_flags)} semantic flags must be reviewed before any training run:")
        for flag in semantic_flags[:40]:
            print(f"- {flag}")
        return 1
    return 0


def json_fingerprint(item: dict) -> str:
    import json
    return json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


if __name__ == "__main__":
    sys.exit(main())
