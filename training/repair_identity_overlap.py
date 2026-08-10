"""Rename the one correction prompt that overlapped an existing training prompt."""

import json
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "dataset" / "validation.jsonl"
OLD = "Tell me about yourself."
NEW = "Give me a brief introduction to the Libra AI assistant in this project."
lines = PATH.read_text(encoding="utf-8").splitlines()
matches = 0
updated: list[str] = []
for line in lines:
    record = json.loads(line)
    for message in record["messages"]:
        if message["role"] == "user" and message["content"] == OLD:
            message["content"] = NEW
            matches += 1
    updated.append(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
if matches != 1:
    raise ValueError(f"Expected exactly one validation overlap to repair, found {matches}")
PATH.write_text("\n".join(updated) + "\n", encoding="utf-8", newline="\n")
print(f"Renamed validation prompt to: {NEW}")
