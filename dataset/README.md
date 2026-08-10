# Libra AI Dataset

## Purpose

This directory contains instruction/chat data for fine-tuning `Qwen/Qwen2.5-1.5B-Instruct` into Libra AI, a direct, friendly programming and research assistant. The current target is exactly 1,000 examples: 500 training and 500 validation records.

## Format

Every JSONL line is an object with exactly one field, `messages`. Each message has a `role` (`user` or `assistant`) and non-empty `content`. Category labels are kept in `batch1_metadata.json` so the fine-tuning files remain compatible with the requested messages-only format.

## Batch 1

- Training examples: exactly 500
- Validation examples: exactly 500
- Training and validation scenarios are kept separate.
- Exact duplicate count across both splits: 0

Training category distribution:

| Category | Count | Share |
| --- | ---: | ---: |
| Programming & software development | 200 | 40% |
| Research & analysis | 100 | 20% |
| General knowledge & Q&A | 75 | 15% |
| Friendly conversation | 50 | 10% |
| Technical explanations | 50 | 10% |
| Creative/problem solving | 25 | 5% |

The batch includes English, Bangla-script prompts/responses, and Banglish prompts/responses. Programming coverage includes PHP, MySQL, JavaScript, HTML, CSS, Tailwind CSS, APIs, authentication, databases, debugging, security, Git/GitHub, Linux, deployment, AI APIs, LLMs, RAG, and web architecture.

## Validation

Run from the repository root:

```text
python training/validate_dataset.py
```

The validator checks JSON syntax, the exact messages-only record shape, valid roles, non-empty content, exact record counts, duplicate records, duplicate user prompts, cross-dataset exact duplicates, cross-dataset prompt overlap, and the category metadata report.

The replacement builder at `training/build_batch1.py` uses independent realistic scenario banks, topic-aware answer branches, exact programming-topic code examples, and native Bangla/Banglish responses. It validates generated records in 50-example batches before writing the files. Training and validation use different scenario pools and intent wording; the builder does not create later batches.

Run the quality audit after generation:

```text
python training/quality_audit.py
```

The audit reports duplicate assistant responses, repeated opening phrases, old template signatures, likely topic/code mismatches, language mismatches, short responses, and the top 20 assistant opening phrases.

Run the semantic audit as the final review:

```text
python training/semantic_audit.py
```

It flags likely programming-topic mismatches, unrelated code languages, missing implementation details for explicit coding requests, and detectable Bangla/Banglish response mismatches. These are heuristics and should be supplemented with manual sample review before training.
