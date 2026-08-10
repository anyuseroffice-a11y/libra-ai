"""Make two concise validation identity answers distinct."""

import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "dataset" / "validation.jsonl"
records = []
changed = 0
for line in path.read_text(encoding="utf-8").splitlines():
    record = json.loads(line)
    user = next(message["content"] for message in record["messages"] if message["role"] == "user")
    for message in record["messages"]:
        if message["role"] == "assistant" and user == "Is this assistant ChatGPT?" and message["content"] == "No. This assistant is Libra AI.":
            message["content"] = "No. This project’s assistant is Libra AI, not ChatGPT."
            changed += 1
    records.append(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
if changed != 1:
    raise ValueError(f"Expected one ChatGPT correction to update, found {changed}")
path.write_text("\n".join(records) + "\n", encoding="utf-8", newline="\n")
print("Updated one duplicate identity correction response.")
