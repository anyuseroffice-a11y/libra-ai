"""Hand-authored example corpus for the Libra AI dataset.

Each module exposes EXAMPLES: a list of (user_message, assistant_message)
tuples. The builder in training/build_dataset.py reads these, splits them
into batches of 50, runs per-batch semantic checks, and writes the JSONL
files. Every pair is written as a real user question followed by the answer
a competent developer would actually send; no template substitution.
"""
