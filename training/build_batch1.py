"""Build a deterministic, category-balanced first Libra AI dataset batch."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"

PROGRAMMING = [
    ("PHP PDO registration", "Use a unique email index, validate input, bind a PDO parameter, and store password_hash($password, PASSWORD_DEFAULT); never store the raw password."),
    ("PHP login session", "Fetch the user by email with a prepared statement, call password_verify(), then session_regenerate_id(true) before storing the user id in the session."),
    ("PHP CSRF protection", "Generate a random_bytes token in the session, include it in the form, and compare it with hash_equals() on POST before changing state."),
    ("PHP file upload", "Check upload errors, size, MIME type with finfo, and a generated filename; store outside the public directory and never trust the original extension."),
    ("PHP transaction", "Wrap related INSERT and UPDATE statements in beginTransaction(), commit(), and rollback() in a catch block so partial writes cannot survive."),
    ("PHP validation errors", "Return field-level errors from the server and preserve old form values, but normalize and validate again on the server even when browser validation exists."),
    ("PHP pagination", "Use a bounded integer page and limit, calculate offset, and run a separate COUNT query; do not interpolate arbitrary request values into SQL."),
    ("PHP dependency boundaries", "Keep controllers thin, put database operations in a repository, and inject PDO so the service can be tested without a global connection."),
    ("PHP JSON API", "Set Content-Type: application/json, decode input with JSON_THROW_ON_ERROR, validate the payload, and return consistent success and error envelopes."),
    ("PHP password reset", "Store a hash of a short-lived random token with an expiry, invalidate it after use, and do not reveal whether an email exists."),
    ("MySQL schema indexes", "Index columns used for selective WHERE clauses and joins, but verify the plan with EXPLAIN because every index adds write and storage cost."),
    ("MySQL composite index", "For a query filtering tenant_id and status then ordering by created_at, test an index beginning with tenant_id, status, created_at."),
    ("MySQL safe delete", "Use a transaction, select the target count first, apply a parameterized DELETE with the same predicate, and commit only after checking the affected rows."),
    ("MySQL aggregate query", "Group by the entity key and use HAVING for aggregate filters; avoid selecting nonaggregated columns that are not functionally dependent on the group."),
    ("MySQL foreign keys", "Use matching types and storage engines, define the intended delete behavior explicitly, and index child foreign-key columns."),
    ("MySQL optimistic locking", "Add a version column and update with WHERE id = ? AND version = ?, incrementing version atomically; zero affected rows means a conflict."),
    ("MySQL search", "Use a suitable FULLTEXT index for natural-language search or a carefully indexed prefix query; leading-wildcard LIKE cannot use a normal B-tree efficiently."),
    ("MySQL migration", "Make schema changes reversible, record them in versioned migrations, and test them against a copy of production-shaped data before deployment."),
    ("MySQL reporting join", "Start from the required grain, join on keys rather than display names, and check row counts after each join to catch accidental multiplication."),
    ("JavaScript fetch", "Check response.ok before parsing, catch network and JSON errors separately, and cancel stale requests with AbortController when the view changes."),
    ("JavaScript form handling", "Use FormData, prevent the default submit, disable the submit control while awaiting the request, and render server validation errors accessibly."),
    ("JavaScript event delegation", "Attach one listener to the stable container and use closest() to identify a matching button, which also supports dynamically inserted rows."),
    ("JavaScript race condition", "Track the request identity or abort the previous request so a slower old response cannot overwrite newer state."),
    ("JavaScript module design", "Export small pure functions for parsing and formatting, keep DOM effects at the boundary, and avoid hidden mutable module state."),
    ("HTML accessible form", "Associate each input with a label, expose errors through aria-describedby and an error summary, and preserve a logical keyboard order."),
    ("HTML semantic layout", "Use header, nav, main, section, and footer according to meaning; choose elements for structure rather than styling their default appearance."),
    ("CSS responsive table", "Keep the table semantic, allow horizontal overflow at narrow widths, and avoid shrinking text until it becomes unreadable."),
    ("CSS stacking context", "Inspect positioned elements, z-index, transform, opacity, and isolation because a child cannot escape its ancestor stacking context by using a larger z-index."),
    ("CSS layout shift", "Reserve image dimensions with aspect-ratio or width and height, and avoid inserting late content above the current viewport."),
    ("Tailwind design tokens", "Define repeated colors and spacing in the theme, use semantic utility groupings, and extract a component only when a pattern has real behavior."),
    ("Tailwind responsive navigation", "Use a mobile-first hidden/menu state, a keyboard-accessible button, and breakpoint utilities only for layout changes rather than duplicated markup."),
    ("REST resource design", "Use nouns for resource paths, HTTP methods for intent, stable error shapes, and idempotency where retries can repeat a write."),
    ("REST pagination", "Return items plus explicit pagination metadata, cap page size, and use a cursor when offset pagination becomes unstable under frequent inserts."),
    ("REST authentication", "Prefer short-lived access tokens with refresh rotation or secure server sessions; authorize every resource access instead of trusting client ownership fields."),
    ("JSON validation", "Validate required fields, types, bounds, and unknown-field policy at the boundary, then convert to an internal structure before business logic."),
    ("Git conflict resolution", "Understand both changes before editing, resolve the smallest region, run tests, stage the resolution, and make the merge commit only after verification."),
    ("Linux deployment logs", "Use systemd status and journalctl with a time window, inspect the process environment and permissions, then reproduce the failing command as the service user."),
    ("AI API integration", "Keep the provider key server-side, set timeouts and retry limits, validate model output before use, and log request metadata without sensitive prompt content."),
    ("RAG retrieval", "Chunk by meaning with overlap, attach source metadata, retrieve a small candidate set, rerank when needed, and instruct generation to distinguish evidence from gaps."),
    ("LLM prompt injection", "Treat retrieved documents and user-provided text as untrusted data, separate instructions from context, and enforce authorization outside the model."),
    ("Web architecture", "Separate browser, application, and persistence concerns; define contracts at boundaries, make writes observable, and choose caching only after measuring the bottleneck."),
]

RESEARCH = [
    ("PostgreSQL versus MySQL for a SaaS", "Compare workload, indexing, JSON support, operational familiarity, hosting, and migration cost; there is no universal winner without workload data."),
    ("REST versus GraphQL", "REST is usually simpler for resource-oriented public APIs, while GraphQL helps clients shape related data; schema governance and caching complexity decide the tradeoff."),
    ("RAG evaluation", "Measure retrieval recall and citation support separately from answer correctness, then add adversarial and no-answer cases rather than relying only on average scores."),
    ("Monolith versus microservices", "A modular monolith reduces distributed-systems cost early; services become justified when independent scaling, ownership, or isolation outweighs coordination overhead."),
    ("Evidence quality", "Prefer primary sources and methods over summaries, record publication date and limitations, and label interpretation separately from directly observed findings."),
    ("Model quantization", "Lower precision reduces memory and may improve throughput, but accuracy and hardware support vary; benchmark the actual prompts and latency target."),
    ("Open source license choice", "Match the license to distribution, modification, patent, and network-use requirements; review the exact license text rather than relying on a label."),
    ("Remote work productivity claim", "Separate output metrics from activity proxies, control for role and selection effects, and treat a single survey as suggestive rather than causal evidence."),
    ("Database normalization", "Normalize to protect consistency and then denormalize only for measured read patterns, with a clear write path that maintains derived values."),
    ("Browser storage options", "Cookies support request-linked sessions, localStorage is convenient but exposed to XSS, and IndexedDB handles larger structured client data; threat model first."),
    ("Scientific uncertainty", "Distinguish measurement error, model uncertainty, and missing evidence; a narrow confidence interval does not repair a biased measurement process."),
    ("Technology adoption", "Evaluate total cost, ecosystem health, hiring, operational maturity, exit cost, and fit to constraints instead of ranking tools by popularity."),
    ("Search ranking experiment", "Define a primary metric, randomize exposure, prevent interference, estimate power, and inspect segment effects before declaring a small lift meaningful."),
    ("Caching strategy", "Cache stable, expensive reads with explicit invalidation and bounded staleness; do not cache personalized or authorization-sensitive content under a shared key."),
    ("Queue versus synchronous work", "Keep latency-critical work synchronous and move retryable, slow, or bursty work to a queue with idempotency and a dead-letter path."),
    ("API versioning", "Prefer backward-compatible evolution and deprecation windows; version when the contract meaningfully changes and publish migration guidance."),
    ("Privacy threat model", "Map data flows, actors, assets, and trust boundaries, then prioritize abuse cases by impact and likelihood rather than listing generic controls."),
    ("Benchmark interpretation", "Report environment, workload, warmup, variance, and cost; a faster microbenchmark may not predict end-to-end user performance."),
    ("Human versus automated review", "Automation is consistent for known patterns, while human review handles ambiguity and context; combine them with clear escalation criteria."),
    ("Source reconciliation", "When credible sources disagree, compare definitions, populations, dates, methods, and incentives before deciding whether the disagreement is substantive."),
]

GENERAL = [
    ("Explain compound interest", "Interest is added to the principal and then earns interest itself. The basic model is A = P(1 + r/n)^(nt), assuming a fixed rate and regular compounding."),
    ("Why leap years exist", "A tropical year is about 365.2422 days, so the calendar adds leap days under a rule that keeps dates aligned with the seasons."),
    ("Difference between revenue and profit", "Revenue is money earned from sales; profit is what remains after relevant costs. A company can have high revenue and still lose money."),
    ("What an API is", "An API is a defined interface through which software requests data or actions. The contract describes inputs, outputs, errors, and authorization."),
    ("How DNS works", "DNS maps names to records such as IP addresses through recursive and authoritative servers, with caching controlled by TTL values."),
    ("Why backups need testing", "A backup is useful only if it can be restored. Test recovery, permissions, completeness, and recovery time rather than checking that a file exists."),
    ("What a checksum does", "A checksum summarizes bytes so accidental changes are detectable. It is not automatically a proof of authenticity; use a signature for that."),
    ("How vaccines train immunity", "Vaccines present immune targets safely enough to create memory responses, reducing the chance or severity of disease when exposure occurs."),
    ("What inflation means", "Inflation is a sustained rise in the general price level, which lowers purchasing power when income does not rise at the same pace."),
    ("Why oceans moderate climate", "Water stores and transports large amounts of heat, so oceans slow temperature changes and redistribute energy through currents."),
    ("What correlation means", "Correlation describes how variables move together; it does not by itself establish that one causes the other."),
    ("How HTTP differs from HTTPS", "HTTPS is HTTP carried through TLS, providing encryption and server authentication when certificate validation succeeds."),
    ("What an algorithm is", "An algorithm is a finite, precise procedure for transforming inputs into an outcome. Efficiency and correctness depend on the problem and constraints."),
    ("Why sleep matters", "Sleep supports memory consolidation, regulation, and physical recovery. Exact needs vary, but persistent severe sleep problems merit investigation."),
    ("What opportunity cost means", "Opportunity cost is the value of the best alternative given up when choosing an option; it includes time and capacity, not only money."),
]

CONVERSATION = [
    ("greeting", "Hey! What are we working on?"),
    ("stuck on a bug", "Send the error, the relevant code, and what you expected to happen. I’ll trace the actual cause with you."),
    ("overwhelmed by a project", "Let’s reduce it to the next concrete decision. What is already working, and what is currently blocking progress?"),
    ("celebrating a fix", "Nice. Before moving on, capture what caused it and add a small regression test so the lesson stays with the project."),
    ("unclear requirement", "Let’s pin down the user action, expected result, and edge case first. Those three usually expose the missing requirement."),
    ("asking for concise help", "Sure. Give me the exact question and I’ll keep the answer focused."),
    ("learning plan", "Pick one practical outcome, then work backward through the smallest concepts needed to build it."),
    ("bad day debugging", "That sounds draining. We can make the next step small: reproduce it once, capture the input, and inspect the first unexpected value."),
    ("asking for an opinion", "I can give a view, but I’ll separate my judgment from facts and state what assumption drives it."),
    ("Banglish support", "Bujhte parchi. Error message ar relevant code ta pathao; age root cause ber kori, tarpor clean fix dibo."),
]

TECHNICAL = [
    ("database transaction isolation", "Isolation controls what concurrent transactions can observe. Stronger isolation reduces anomalies but can increase blocking, so choose it for the invariant at risk."),
    ("public key cryptography", "A key pair lets someone publish a key for encryption or signature verification while keeping the private key secret for decryption or signing."),
    ("garbage collection", "A garbage collector reclaims unreachable objects. It simplifies memory management, but pauses, allocation rate, and heap size still affect latency."),
    ("HTTP idempotency", "An operation is idempotent when repeating it has the same intended effect as doing it once. PUT is designed that way; POST often needs an idempotency key for retries."),
    ("eventual consistency", "Replicas may temporarily disagree after a write, but converge under stated conditions. Applications need conflict handling and a clear freshness expectation."),
    ("load balancing", "A load balancer distributes requests and can perform health checks and TLS termination, but session affinity and retries need explicit failure semantics."),
    ("observability", "Logs describe events, metrics show aggregates, and traces connect work across services. Useful observability links all three to user-impacting outcomes."),
    ("rate limiting", "Rate limiting protects capacity and fairness by bounding requests over time. Use a policy appropriate to identity and return retry guidance when possible."),
    ("container image layers", "Images are composed of immutable layers; ordering stable dependencies before frequently changing application files improves cache reuse."),
    ("embedding vectors", "An embedding maps content into a numeric space where a distance function approximates semantic similarity. It is a retrieval aid, not a truth signal."),
]

CREATIVE = [
    ("design a CLI backup tool", "Define the command vocabulary first: init, backup, list, restore, and verify. Make dry-run and structured output first-class so automation can trust it."),
    ("debug a mysterious outage", "Write a timeline from observed signals, identify the first divergence from normal, and test the smallest hypothesis before changing multiple systems."),
    ("plan a portfolio project", "Choose a real user problem, constrain the first release, expose one architectural tradeoff, and document what you measured rather than only showing screenshots."),
    ("improve a slow dashboard", "Measure server time, query time, payload size, and browser rendering separately; optimize the largest measured contributor and recheck perceived latency."),
    ("explain a complex system simply", "Start with the user-visible goal, name the major parts, trace one request end to end, then add failure modes and tradeoffs."),
]

VALIDATION_SCENARIOS = [
    "a community marketplace",
    "a clinic appointment portal",
    "a school administration dashboard",
    "a logistics tracking service",
    "a subscription analytics product",
    "a small newsroom platform",
    "a nonprofit donation system",
    "a property maintenance app",
]

MODES = [
    ("implementation", "How would you implement {topic}? Give a practical approach and a small working example where code is useful.", "Implementation plan: {guidance}"),
    ("debugging", "I have a problem involving {topic}. How would you diagnose it, and what fix would you apply first?", "Start by checking the symptom against the boundary described in the question. The likely root cause is addressed by this fix: {guidance}"),
    ("review", "Review this design concern: {topic}. What would you keep, change, and test before shipping?", "Keep the core idea, but verify these risks before shipping: {guidance} Add a focused test for the failure mode, not only the happy path."),
    ("tradeoff", "Explain the important tradeoffs when choosing an approach for {topic}.", "The tradeoff is between simplicity, correctness, and operational cost. For this case: {guidance} Choose based on the workload and failure tolerance rather than a universal rule."),
    ("edge cases", "What edge cases matter for {topic}, and how should the response handle them?", "Cover invalid input, retries, concurrency, partial failure, and authorization where relevant. The central handling is: {guidance}"),
]


def code_for_topic(topic: str) -> str:
    topic = topic.rsplit(": ", 1)[-1]
    if topic.startswith("PHP"):
        return "$statement = $pdo->prepare('SELECT id, password_hash FROM users WHERE email = :email');\n$statement->execute(['email' => $email]);\n$user = $statement->fetch(PDO::FETCH_ASSOC);\nif (!$user || !password_verify($password, $user['password_hash'])) {\n    throw new RuntimeException('Invalid credentials');\n}"
    if topic.startswith("MySQL"):
        return "CREATE INDEX idx_orders_customer_status ON orders (customer_id, status, created_at);\nSELECT customer_id, COUNT(*) AS order_count\nFROM orders\nWHERE status = ?\nGROUP BY customer_id;"
    if topic.startswith("JavaScript"):
        return "const response = await fetch('/api/items', { signal: controller.signal });\nif (!response.ok) throw new Error(`Request failed: ${response.status}`);\nconst items = await response.json();\nrenderItems(items);"
    if topic.startswith("HTML"):
        return '<label for="email">Email</label>\n<input id="email" name="email" type="email" required aria-describedby="email-error">\n<p id="email-error" role="alert"></p>'
    if topic.startswith("CSS") or topic.startswith("Tailwind"):
        return ".results {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));\n    gap: 1rem;\n}"
    if topic.startswith("REST") or topic.startswith("JSON"):
        return "const payload = await request.json();\nif (!payload.email || typeof payload.email !== 'string') {\n    return response.status(400).json({ error: 'email is required' });\n}"
    if topic.startswith("Git") or topic.startswith("Linux"):
        return 'git status\ngit diff --check\ngit add path/to/resolved-file\ngit commit -m "Resolve configuration conflict"'
    if topic.startswith("AI") or topic.startswith("LLM") or topic.startswith("RAG"):
        return "const result = await client.responses.create({\n  model: process.env.AI_MODEL,\n  input: [{ role: 'user', content: prompt }],\n  timeout: 15_000,\n});\nif (!result.output_text) throw new Error('Model returned no text');"
    return "const started = performance.now();\nconst result = await runOperation();\nlogger.info({ durationMs: performance.now() - started }, 'operation complete');"


def make_examples(tasks: list[tuple[str, str]], category: str, start_index: int, holdout: bool = False) -> list[tuple[dict, str]]:
    result: list[tuple[dict, str]] = []
    for task_index, (topic, guidance) in enumerate(tasks):
        for mode_index, (_, prompt_template, response_template) in enumerate(MODES):
            if holdout:
                holdout_prompts = [
                    "A teammate inherited {topic}. What would you change first, and how would you verify it?",
                    "The production symptom points to {topic}. Walk through a diagnosis and the smallest safe fix.",
                    "Before shipping a feature involving {topic}, review the design for failure modes and test coverage.",
                    "Choose an approach for {topic} under a real workload. Explain the tradeoffs and the assumptions behind your choice.",
                    "What could go wrong with {topic} at the edges of its input, traffic, or failure behavior? Give concrete mitigations.",
                ]
                prompt = holdout_prompts[mode_index].format(topic=topic)
            else:
                prompt = prompt_template.format(topic=topic)
            response = response_template.format(guidance=guidance)
            if category == "programming" and mode_index == 0:
                response += "\n\nExample:\n```text\n" + code_for_topic(topic) + "\n```"
            if holdout:
                response = response + " Verify the recommendation with a focused test or measurement for this scenario."
            language_marker = (start_index + task_index * 5 + mode_index) % 13
            if language_marker == 0:
                prompt = "বাংলায় উত্তর দিন: " + prompt
                response = "মূল বিষয়: " + response
            elif language_marker == 1:
                prompt = "Banglish-e bujhaiyen: " + prompt
                response = "Short kore bolle, " + response
            result.append(({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}, category))
    return result


def build() -> None:
    train_groups = [
        (PROGRAMMING, "programming", 0, 200),
        (RESEARCH, "research", 200, 100),
        (GENERAL, "general", 300, 75),
        (CONVERSATION, "conversation", 375, 50),
        (TECHNICAL, "technical", 425, 50),
        (CREATIVE, "creative", 475, 25),
    ]
    train_pairs = [pair for tasks, category, offset, quota in train_groups for pair in make_examples(tasks, category, offset)[:quota]]
    holdout_topics = [
        ([(f"{VALIDATION_SCENARIOS[index % len(VALIDATION_SCENARIOS)]}: {topic}", guidance + " Compare the first safe baseline with one measurable alternative.") for index, (topic, guidance) in enumerate(tasks)], category, offset, quota)
        for tasks, category, offset, quota in [
            (PROGRAMMING, "programming", 0, 200),
            (RESEARCH, "research", 100, 100),
            (GENERAL, "general", 200, 75),
            (CONVERSATION, "conversation", 300, 50),
            (TECHNICAL, "technical", 400, 50),
            (CREATIVE, "creative", 500, 25),
        ]
    ]
    # Holdout prompts use an independent scenario framing and are never copied into training.
    validation_pairs = [pair for tasks, category, offset, quota in holdout_topics for pair in make_examples(tasks, category, offset, holdout=True)[:quota]]
    DATASET.mkdir(parents=True, exist_ok=True)
    for path, pairs in ((DATASET / "train.jsonl", train_pairs), (DATASET / "validation.jsonl", validation_pairs)):
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            for item, _ in pairs:
                handle.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n")
    metadata = {
        "batch": 1,
        "training_categories": dict(Counter(category for _, category in train_pairs)),
        "validation_categories": dict(Counter(category for _, category in validation_pairs)),
        "note": "Category metadata is separate so each JSONL record keeps the exact messages-only fine-tuning schema.",
    }
    (DATASET / "batch1_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()