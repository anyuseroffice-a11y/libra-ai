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

TRAINING_SCENARIOS = [
    "a local booking service", "an internal finance tool", "a community forum", "a small online shop",
    "a volunteer scheduling app", "a course platform", "a clinic dashboard", "a delivery portal",
]


def realistic_question(topic: str, category: str, mode: int, context: str, holdout: bool) -> str:
    lower = topic.lower()
    if category == "programming":
        if "safe delete" in lower:
            return f"I need to remove cancelled orders from {context}. What transaction and WHERE clause would make a MySQL delete safe, and how can I verify the affected rows?"
        if "deadlock" in lower:
            return f"Two workers in {context} occasionally deadlock while updating orders. How should I diagnose the MySQL deadlock and change the transaction?"
        if "slow quer" in lower or "search" in lower:
            return f"A query in {context} became slow after the table grew. How should I use EXPLAIN and indexes to find the MySQL bottleneck?"
        if "logout" in lower:
            return f"How should {context} implement PHP logout so the session is actually invalidated on the server?"
        if "session timeout" in lower:
            return f"Users stay signed in too long on {context}. How can I implement an idle timeout with PHP sessions?"
        if "file upload" in lower:
            return f"I’m adding document uploads to {context}. What should the PHP endpoint validate before saving a file, and can you show the safe part of the handler?"
        if "registration" in lower:
            return f"For {context}, I need a PHP registration endpoint. How should I validate the email, hash the password, and handle a duplicate account?"
        if "login" in lower:
            return f"Users of {context} can log in, but the session setup feels unsafe. What would a secure PDO login flow look like?"
        if "csrf" in lower:
            return f"A POST form in {context} changes state without a CSRF token. How should I add and verify a token in PHP?"
        if "validation errors" in lower:
            return f"In {context}, the form only shows 'invalid input' even when several fields are wrong. How should the PHP endpoint return useful field-level validation errors?"
        if "transaction" in lower:
            return f"Creating an invoice in {context} writes an invoice row and stock update. How do I make those PHP/PDO writes atomic?"
        if "pagination" in lower:
            return f"The {context} admin list needs pagination. How should I validate page and limit values and bind them safely in PDO?"
        if "race condition" in lower:
            return f"The search box in {context} sends a request per keystroke and old results sometimes win. How should I fix that in JavaScript?"
        if "debounce" in lower:
            return f"The product search in {context} calls the API on every keypress. Show a small JavaScript debounce implementation and explain where to put it."
        if "api error" in lower:
            return f"The frontend for {context} shows a blank screen when the API returns 401, 422, or 500. How should the fetch error handling distinguish them?"
        if "composite index" in lower:
            return f"In {context}, the orders query filters tenant_id and status and sorts by created_at. Which MySQL index fits that query, and how would I check it?"
        if "json api" in lower or "json validation" in lower:
            return f"My PHP endpoint for {context} sometimes emits an HTML error page. How can I validate JSON input and return consistent JSON errors?"
        if "password reset" in lower:
            return f"I’m implementing password reset for {context}. What should the token table store, and how do I make the link single-use?"
        if "fetch" in lower:
            return f"A dashboard in {context} treats a 500 response as successful JSON. What is a robust fetch() error path?"
        if "deployment" in lower or "linux" in lower:
            return f"The {context} service works in my shell but fails under systemd. What should I inspect in the logs and service environment?"
        if "rag" in lower:
            return f"I’m adding document search to {context}. How should I chunk, retrieve, and expose evidence without letting retrieved text override system instructions?"
        return f"I’m working on {context}, specifically {topic.lower()}. What implementation would you use here, and what would you test first?"
    if category == "research":
        return f"I’m making a decision for {context}: what should I know about {topic.lower()}, and which assumptions could change the recommendation?"
    if category == "general":
        return f"Could you explain {topic.lower()} in plain language, with one concrete example from {context}?"
    if category == "conversation":
        return [
            f"Hey Libra, I’ve got a half-formed idea for {context} and need someone to think it through with me. It is mainly about {topic.lower()}.",
            f"I’m frustrated with the {context} project. The part about {topic.lower()} is getting nowhere. Can you help me find a sensible next step?",
            f"I finally fixed a bug in {context}. It involved {topic.lower()}. What should I record so I don’t repeat the whole investigation later?",
            f"Can I get a quick outside opinion on a {topic.lower()} decision I’m making for {context}?",
            f"I have ten things to do for {context}, including {topic.lower()}, and no clear order. Help me choose the first one.",
        ][(mode + len(context) + (1 if holdout else 0)) % 5]
    if category == "technical":
        return f"I keep seeing the term {topic.lower()} in engineering discussions about {context}. What is actually happening under the hood?"
    return f"I’m planning {context} and want to think clearly about this: {topic.lower()}. Where would you start?"


def realistic_answer(topic: str, guidance: str, category: str, mode: int, context: str, holdout: bool) -> str:
    if category == "programming":
        return programming_answer(topic, guidance, mode, context)
    if category == "research":
        return [
            f"For {context}, {topic.lower()} is a conditional choice. {guidance} Test the stated workload before committing.",
            f"The evidence for {topic.lower()} should be separated from preference in {context}. {guidance} Note what observation would change the recommendation.",
            f"When {context} considers {topic.lower()}, compare the actual failure modes. {guidance} A small representative test is more useful than a slogan.",
            f"The budget and growth assumptions for {context} matter to {topic.lower()}. {guidance} Revisit the choice when those assumptions change.",
            f"Before choosing {topic.lower()} for {context}, measure the factors that dominate the decision. {guidance}",
        ][mode]
    if category == "general":
        return [
              f"{topic} is easiest to understand in simple terms: {guidance} That is why it matters in {context}.",
              f"For {topic}, a useful picture is this: {guidance} Think of {context} as a concrete case.",
            f"{topic} has one important distinction: {guidance} It prevents a common misunderstanding in {context}.",
            f"{topic} can be explained compactly: {guidance} The same idea applies when reasoning about {context}.",
              f"One caveat about {topic} is worth keeping in mind. {guidance} The context of {context} can change the practical answer.",
        ][mode]
    if category == "conversation":
        return [
            f"About {topic.lower()} in {context}: absolutely, tell me the rough idea, who it is for, and what you have already tried; we can shape it without pretending the first version is final.",
            f"For {topic.lower()} in {context}, let’s make the next move small: name the visible problem, write down the constraint that matters most, and ignore the rest until that is clear.",
            f"The {topic.lower()} fix in {context} is worth capturing: write down the symptom, the actual cause, and the check that would catch it next time.",
            f"On {topic.lower()} in {context}, I’ll give you a view and label the assumption behind it, so you can disagree with the premise instead of arguing with a vague conclusion.",
            f"For {topic.lower()} in {context}, start with the task that either unblocks someone else or teaches you the most. Give it a short time box, then reassess with evidence.",
        ][mode]
    if category == "technical":
        return [
            f"In {context}, {topic} works through a mechanism you can observe: {guidance}",
            f"For {context}, treat {topic} as a contract between concurrent parts: {guidance}",
            f"Follow one request through {context} to understand {topic}: {guidance}",
            f"At production scale in {context}, {topic} changes the cost of the tradeoff: {guidance}",
            f"A practical mental model for {topic} in {context} is: {guidance}",
        ][mode]
    return [
            f"For {context}, start {topic.lower()} by naming the user outcome and the first test. {guidance}",
            f"Before choosing tools for {topic.lower()} in {context}, write down the failure you want to prevent. {guidance}",
            f"The first useful experiment for {topic.lower()} in {context} is: {guidance}",
            f"For {topic.lower()} in {context}, trade scope against feedback speed. {guidance}",
            f"Keep the {topic.lower()} plan for {context} reversible while the evidence is thin. {guidance}",
        ][mode]


def programming_answer(topic: str, guidance: str, mode: int, context: str) -> str:
    lower = topic.lower()
    code = code_for_topic(topic)
    if "safe delete" in lower:
        answer = f"For {context}, {topic} should not be deleted by status alone. First select the exact rows inside a transaction, inspect the count, then delete with the same tenant and status predicate."
        code = """$pdo->beginTransaction();
$check = $pdo->prepare("SELECT id FROM orders WHERE tenant_id = ? AND status = ? LIMIT 100");
$check->execute([$tenantId, 'cancelled']);
$ids = $check->fetchAll(PDO::FETCH_COLUMN);
if (count($ids) > 100) {
    $pdo->rollBack();
    throw new RuntimeException('Review deletion scope');
}
$delete = $pdo->prepare("DELETE FROM orders WHERE tenant_id = ? AND status = ?");
$delete->execute([$tenantId, 'cancelled']);
$pdo->commit();"""
        return answer + " This protects against an accidental cross-tenant delete and gives you an affected-row check.\n\n```sql\n" + code + "\n```"
    if "race condition" in lower:
        return f"In {context}, {topic} has an ordering bug: the old response wins because requests finish in a different order from the keystrokes. Abort the previous request and ignore AbortError; the newest request then owns the result.\n\n```javascript\n" + """let controller;

async function search(query) {
    controller?.abort();
    controller = new AbortController();
    const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`, {
        signal: controller.signal,
    });
    if (!response.ok) throw new Error(`Search failed: ${response.status}`);
    return response.json();
}

searchInput.addEventListener('input', async (event) => {
    try {
        renderResults(await search(event.target.value));
    } catch (error) {
        if (error.name !== 'AbortError') showSearchError(error);
    }
});""" + "\n```\nThe abort is the important part: an obsolete response cannot update the UI after a newer query starts."
    if "debounce" in lower:
        return f"For {context}, debouncing delays the call until typing pauses, which reduces traffic without making the search feel sluggish. Keep the timer around the fetch call, not inside the result renderer.\n\n```javascript\n" + """function debounce(callback, wait) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => callback(...args), wait);
    };
}

const requestSearch = debounce(async (query) => {
    const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    if (!response.ok) throw new Error(`Search failed: ${response.status}`);
    renderResults(await response.json());
}, 250);""" + "\n```"
    if "logout" in lower:
        return f"For {context}, destroy the server-side session and expire the session cookie. Redirect after the response so a stale browser page cannot be mistaken for an authenticated session.\n\n```php\n" + """session_start();
$_SESSION = [];
if (ini_get('session.use_cookies')) {
        $params = session_get_cookie_params();
        setcookie(session_name(), '', time() - 42000, $params['path'], $params['domain'], $params['secure'], $params['httponly']);
}
session_destroy();
header('Location: /login');
exit;""" + "\n```"
    if "session timeout" in lower:
        return f"For {context}, store the last activity time in the session and rotate or destroy the session after the idle limit. Check this on every authenticated request, not only on the dashboard.\n\n```php\n" + """session_start();
$idleLimit = 1800;
if (isset($_SESSION['last_activity']) && time() - $_SESSION['last_activity'] > $idleLimit) {
        $_SESSION = [];
        session_destroy();
        http_response_code(401);
        exit('Session expired');
}
$_SESSION['last_activity'] = time();""" + "\n```"
    if "deadlock" in lower:
        return f"For {context}, use the deadlock report to identify the lock order, then make every worker update shared tables in the same order. Keep transactions short and retry a deadlock victim with bounded backoff.\n\n```sql\nSHOW ENGINE INNODB STATUS;\n```"
    if "slow quer" in lower or "search" in lower:
        return f"For {context}, investigate {topic} with the exact query and its parameters, then run EXPLAIN ANALYZE. Look for a full scan, an unexpectedly large row estimate, or a filesort before adding an index."
    if mode == 0 or any(word in lower for word in ("implement", "upload", "registration", "login", "api", "crud", "transaction")):
        return f"For {context}, {topic}: {guidance}\n\n```text\n" + code + "\n```"
    if mode == 1:
        return f"In {context}, reproduce the reported {topic} input first, then inspect the value crossing the boundary. {guidance} Check the failing branch with a focused test."
    if mode == 2:
        return f"For {context}, {topic}: {guidance} I would test the successful path, invalid input, and the state after a failed write."
    if mode == 3:
        return f"For {context}, {topic}: {guidance} Choose the simpler implementation until measurements show that the extra moving parts solve a real bottleneck."
    return f"For {context}, {topic}: {guidance} The most useful edge test is the one that exercises malformed input or a retry while the operation is partially complete."


def question_suffix(category: str, mode: int) -> str:
    suffixes = {
        "programming": [
            " Show the smallest practical example.",
            " The failure is intermittent, so explain how you would reproduce it.",
            " I want to review the design before it reaches production.",
            " I’m weighing a simple approach against a more scalable one.",
            " Include the boundary case most developers miss.",
        ],
        "research": [
            " I need a recommendation, not just definitions.",
            " What evidence would change your view?",
            " Please distinguish established facts from judgment.",
            " The decision has a small budget and a growing workload.",
            " What would you measure before committing?",
        ],
        "general": [
            " Start with the intuition.",
            " A short analogy would help.",
            " What is the common misunderstanding here?",
            " How does this show up in everyday life?",
            " What assumption makes the explanation incomplete?",
        ],
        "technical": [
            " Use a request-level example if possible.",
            " I’m trying to understand the failure mode.",
            " Which part of the mental model is easiest to get wrong?",
            " How does the tradeoff appear at scale?",
            " What observation would confirm that explanation?",
        ],
        "creative": [
            " Give me a concrete first milestone.",
            " I have one week to test the idea.",
            " Help me avoid building the wrong thing.",
            " Include one alternative direction.",
            " What would make the idea easier to validate?",
        ],
    }
    return suffixes.get(category, [""] * 5)[mode]


def bangla_pair(topic: str, guidance: str, category: str, mode: int, context: str) -> tuple[str, str]:
    label = topic.split(" ", 1)[-1]
    prompt = f"{context}-এর জন্য {label} নিয়ে সাহায্য দরকার। বাস্তব কাজে এটা কীভাবে ব্যবহার করব, আর কোন ভুলগুলো আগে ধরব?"
    lower = topic.lower()
    if "registration" in lower:
        response = "Registration-এর ক্ষেত্রে আগে email validate করুন, password_hash() দিয়ে password সংরক্ষণ করুন এবং PDO prepared statement ব্যবহার করুন। একই email আবার এলে database-এর unique constraint ধরে পরিষ্কার error দিন।"
    elif "file upload" in lower:
        response = "File upload-এ শুধু extension বিশ্বাস করবেন না। Upload error, size এবং MIME type যাচাই করে random filename ব্যবহার করুন এবং public folder-এর বাইরে ফাইল রাখুন।"
    elif "login" in lower:
        response = "Login-এর সময় password_verify() দিয়ে hash মিলিয়ে নিন, সফল হলে session_regenerate_id(true) চালান এবং session-এ শুধু প্রয়োজনীয় user id রাখুন।"
    elif "csrf" in lower:
        response = "CSRF ঠেকাতে session-এ random token রাখুন, form-এ পাঠান এবং POST-এর সময় hash_equals() দিয়ে মিলিয়ে নিন। Token না মিললে state change করবেন না।"
    elif "validation errors" in lower:
        response = "প্রতিটি field আলাদা করে validate করে errors array-তে field name অনুযায়ী message রাখুন। HTTP 422 JSON response পাঠালে frontend প্রতিটি input-এর পাশে error দেখাতে পারবে।"
    elif "transaction" in lower:
        response = "Invoice insert আর stock update একই PDO transaction-এর মধ্যে রাখুন। সব query সফল হলে commit করুন; exception হলে rollback করে partial state আটকান।"
    elif "pagination" in lower:
        response = "page আর limit integer হিসেবে parse করে maximum দিন। LIMIT ও OFFSET bindValue() দিয়ে PDO::PARAM_INT হিসেবে bind করুন; input সরাসরি SQL string-এ বসাবেন না।"
    elif "json" in lower or "api" in lower:
        response = "API boundary-তে JSON_THROW_ON_ERROR দিয়ে input parse করুন, required field ও type যাচাই করুন এবং সব failure-এর জন্য একই JSON error format ফেরত দিন।"
    elif "index" in lower:
        response = "Index বাছাই করার আগে query-র WHERE এবং ORDER BY দেখুন। tenant_id, status ও created_at একসঙ্গে ব্যবহার হলে composite index পরীক্ষা করুন, তারপর EXPLAIN দিয়ে plan মিলিয়ে নিন।"
    elif "safe delete" in lower:
        response = "Cancelled order delete করার আগে একই tenant_id ও status দিয়ে SELECT করে row count দেখুন। Transaction-এর মধ্যে parameterized DELETE চালান, count অস্বাভাবিক হলে rollback করুন, তারপর commit করুন।"
    elif "race condition" in lower:
        response = "পুরনো search response যেন নতুন ফলকে overwrite না করে, তাই আগের request AbortController দিয়ে cancel করুন। AbortError আলাদা করে ধরুন এবং নতুন response-টাই render করুন।"
    elif "debounce" in lower:
        response = "প্রতিটি keypress-এ API call না করে ২৫০ মিলিসেকেন্ড অপেক্ষা করুন। নতুন keypress এলে আগের timer clear করে তারপর search function চালান।"
    else:
        response = f"{label} নিয়ে {context}-এর ক্ষেত্রে input validation, failure handling এবং একটি ছোট test—এই তিনটি আগে নিশ্চিত করুন।"
    prompt += [" একটি ছোট উদাহরণও দিন।", " সমস্যাটা কীভাবে পরীক্ষা করব?", " production-এর আগে কী review করব?", " সহজ আর scalable পদ্ধতির পার্থক্য কী?", " কোন boundary case-টি ভুলে যাওয়া সহজ?"][mode]
    response += [" ছোট একটি উদাহরণ দিয়ে শুরু করুন।", " আগে একটি reproducible test লিখুন।", " production-এর আগে failure path পরীক্ষা করুন।", " workload অনুযায়ী পদ্ধতিটি বেছে নিন।", " malformed input-ও test করুন।"][mode]
    response += f" {label} নিয়ে {context}-এর বাস্তব ব্যবহারে এই ফলটি একটি ছোট test দিয়ে যাচাই করুন।"
    if category == "programming" and mode == 0:
        response += "\n\nউদাহরণ:\n```text\n" + code_for_topic(topic) + "\n```"
    if category == "conversation":
        prompt = f"লিব্রা, {context}-এর {topic} নিয়ে আজকে কাজের চাপ অনেক। কোন কাজটা আগে শুরু করব বুঝতে পারছি না?"
        response = f"{context}-এর {topic} নিয়ে কাজগুলোকে প্রভাব আর জরুরিতার ভিত্তিতে সাজাই। যে কাজটি অন্য কাজ খুলে দেয়, সেটি আগে নিন এবং ছোট সময়ের মধ্যে শেষ করার মতো অংশ বেছে নিন।"
    return prompt, response


def banglish_pair(topic: str, guidance: str, category: str, mode: int, context: str) -> tuple[str, str]:
    prompt = f"{context} er jonno {topic} niye amar project-e jhamela hocche. Practical bhabe ki korbo?"
    lower = topic.lower()
    if "registration" in lower:
        response = "Registration-er jonno email validate kore password_hash() diye password store korun, ar PDO prepared statement use korun. Same email hole unique constraint-er error handle korun."
    elif "file upload" in lower:
        response = "File upload-e extension trust korben na. Upload error, size ar MIME type check kore random filename din, ebong public folder-er baire rakhun."
    elif "login" in lower:
        response = "Login-e password_verify() diye hash check korun, success hole session_regenerate_id(true) call korun, ar session-e shudhu user id rakhun."
    elif "csrf" in lower:
        response = "CSRF prevent korte session-e random token rakhun, form-e pathan, ar POST-er shomoy hash_equals() diye verify korun. Token mismatch hole state change korben na."
    elif "validation errors" in lower:
        response = "Prottek field alada validate kore errors array-te field name onujayi message rakhun. HTTP 422 JSON response dile frontend input-er pashe error dekhate parbe."
    elif "transaction" in lower:
        response = "Invoice insert ar stock update ekta PDO transaction-er moddhe rakhun. Sob query success hole commit, exception hole rollback korun."
    elif "pagination" in lower:
        response = "page ar limit integer hisebe parse kore maximum din. LIMIT ar OFFSET bindValue() diye PDO::PARAM_INT kore bind korun; input SQL string-e boshaben na."
    elif "json" in lower or "api" in lower:
        response = "API boundary-te JSON input parse kore required field ar type validate korun. Error hole sob path-e consistent JSON response din."
    elif "index" in lower:
        response = "Index choose korar age WHERE ar ORDER BY dekhen. tenant_id, status, created_at ekshathe thakle composite index test kore EXPLAIN diye verify korun."
    elif "safe delete" in lower:
        response = "Cancelled order delete korar age same tenant_id ar status diye SELECT kore count dekhen. Transaction-er moddhe parameterized DELETE chalan, count odd hole rollback korun, tarpor commit korun."
    elif "race condition" in lower:
        response = "Purono search response jeno notun result overwrite na kore, tai ager request AbortController diye cancel korun. AbortError alada kore dhore shudhu latest result render korun."
    elif "debounce" in lower:
        response = "Prottek keypress-e API call na kore 250 millisecond wait korun. Notun keypress hole ager timer clear kore tarpor search function chalan."
    else:
        response = f"{topic.lower()} er khetre input validation, failure handling, ar ekta chhoto test age nishchit korun."
    prompt += [" Ekta chhoto example dekhaw.", " Reproduce korar step bolben?", " Production-er age ki review korbo?", " Simple ar scalable approach-er tradeoff ki?", " Kon edge case ta miss kora easy?"][mode]
    response += [" Chhoto example diye start korun.", " Age reproducible test likhun.", " Production-er age failure path test korun.", " Workload dekhe approach choose korun.", " Malformed input-o test korun."][mode]
    response += f" {topic} niye {context}-er real use case-e ei result ekta chhoto test diye verify korun."
    if category == "programming" and mode == 0:
        response += "\n\nExample:\n```text\n" + code_for_topic(topic) + "\n```"
    if category == "conversation":
        prompt = f"Libra, {context}-er {topic} niye amar khub frustrated lagche. Ekhon ki pathabo?"
        response = f"{context}-er {topic} er error message, relevant code, ar expected behavior pathan. Guess na kore actual failure point theke debug korbo."
    return prompt, response

MODES = [
    ("implementation", "How would you implement {topic}? Give a practical approach and a small working example where code is useful.", "Implementation plan: {guidance}"),
    ("debugging", "I have a problem involving {topic}. How would you diagnose it, and what fix would you apply first?", "Start by checking the symptom against the boundary described in the question. The likely root cause is addressed by this fix: {guidance}"),
    ("review", "Review this design concern: {topic}. What would you keep, change, and test before shipping?", "Keep the core idea, but verify these risks before shipping: {guidance} Add a focused test for the failure mode, not only the happy path."),
    ("tradeoff", "Explain the important tradeoffs when choosing an approach for {topic}.", "The tradeoff is between simplicity, correctness, and operational cost. For this case: {guidance} Choose based on the workload and failure tolerance rather than a universal rule."),
    ("edge cases", "What edge cases matter for {topic}, and how should the response handle them?", "Cover invalid input, retries, concurrency, partial failure, and authorization where relevant. The central handling is: {guidance}"),
]


def code_for_topic(topic: str) -> str:
    topic = topic.rsplit(": ", 1)[-1].lower()
    if "file upload" in topic:
        return """$file = $_FILES['document'] ?? null;
if (!$file || $file['error'] !== UPLOAD_ERR_OK || $file['size'] > 5_000_000) {
    throw new InvalidArgumentException('Invalid upload');
}
$finfo = new finfo(FILEINFO_MIME_TYPE);
if (!in_array($finfo->file($file['tmp_name']), ['application/pdf', 'image/png'], true)) {
    throw new InvalidArgumentException('Unsupported file type');
}
$name = bin2hex(random_bytes(16));
move_uploaded_file($file['tmp_name'], __DIR__ . '/../private_uploads/' . $name);"""
    if "registration" in topic:
        return """$hash = password_hash($password, PASSWORD_DEFAULT);
$statement = $pdo->prepare('INSERT INTO users (email, password_hash) VALUES (:email, :hash)');
$statement->execute(['email' => $email, 'hash' => $hash]);"""
    if "login" in topic or "password reset" in topic:
        return """$statement = $pdo->prepare('SELECT id, password_hash FROM users WHERE email = :email');
$statement->execute(['email' => $email]);
$user = $statement->fetch(PDO::FETCH_ASSOC);
if (!$user || !password_verify($password, $user['password_hash'])) {
    throw new RuntimeException('Invalid credentials');
}
session_regenerate_id(true);
$_SESSION['user_id'] = $user['id'];"""
    if "csrf" in topic:
        return """if (!isset($_SESSION['csrf'])) {
    $_SESSION['csrf'] = bin2hex(random_bytes(32));
}
if (!hash_equals($_SESSION['csrf'], $_POST['csrf'] ?? '')) {
    http_response_code(419);
    exit('Invalid CSRF token');
}"""
    if "validation errors" in topic:
        return """$errors = [];
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors['email'] = 'Enter a valid email address.';
    }
    if (strlen($password) < 12) {
        $errors['password'] = 'Use at least 12 characters.';
    }
if ($errors) {
    http_response_code(422);
    header('Content-Type: application/json');
    echo json_encode(['errors' => $errors], JSON_THROW_ON_ERROR);
    exit;
}"""
    if "dependency" in topic:
        return """final class UserRepository {
    public function __construct(private PDO $pdo) {}

    public function findByEmail(string $email): ?array {
        $query = $this->pdo->prepare('SELECT id, email FROM users WHERE email = :email');
        $query->execute(['email' => $email]);
        return $query->fetch(PDO::FETCH_ASSOC) ?: null;
    }
}"""
    if "safe delete" in topic:
        return """START TRANSACTION;
SELECT id FROM orders WHERE tenant_id = ? AND status = 'cancelled' LIMIT 100;
DELETE FROM orders WHERE tenant_id = ? AND status = 'cancelled';
COMMIT;"""
    if "transaction" in topic:
        return """$pdo->beginTransaction();
try {
    $insert->execute($insertParams);
    $update->execute($updateParams);
    $pdo->commit();
} catch (Throwable $error) {
    $pdo->rollBack();
    throw $error;
}"""
    if "pagination" in topic:
        return """$page = max(1, min((int)($_GET['page'] ?? 1), 10000));
$limit = 25;
$statement = $pdo->prepare('SELECT id, title FROM posts ORDER BY created_at DESC LIMIT :limit OFFSET :offset');
$statement->bindValue(':limit', $limit, PDO::PARAM_INT);
$statement->bindValue(':offset', ($page - 1) * $limit, PDO::PARAM_INT);
$statement->execute();"""
    if "composite index" in topic or "schema indexes" in topic:
        return "CREATE INDEX idx_orders_tenant_status_created ON orders (tenant_id, status, created_at);\nEXPLAIN SELECT * FROM orders WHERE tenant_id = ? AND status = ? ORDER BY created_at DESC;"
    if "aggregate" in topic or "reporting join" in topic:
        return """SELECT customer_id, COUNT(*) AS order_count
FROM orders
WHERE status = ?
GROUP BY customer_id
HAVING COUNT(*) > ?;"""
    if "javascript" in topic:
        return """const controller = new AbortController();
const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`, {
  signal: controller.signal,
});
if (!response.ok) throw new Error(`Search failed: ${response.status}`);
const results = await response.json();"""
    if "html" in topic:
        return '<label for="email">Email</label>\n<input id="email" name="email" type="email" required aria-describedby="email-error">\n<p id="email-error" role="alert"></p>'
    if "css" in topic or "tailwind" in topic:
        return ".results {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));\n    gap: 1rem;\n}"
    if "ai api" in topic or "llm" in topic or "rag" in topic:
        return """const result = await client.responses.create({
  model: process.env.AI_MODEL,
  input: [{ role: 'user', content: prompt }],
  timeout: 15_000,
});
if (!result.output_text) throw new Error('Model returned no text');"""
    if "api" in topic or "json" in topic:
        return """$payload = json_decode(file_get_contents('php://input'), true, 512, JSON_THROW_ON_ERROR);
if (!is_string($payload['email'] ?? null) || !filter_var($payload['email'], FILTER_VALIDATE_EMAIL)) {
    http_response_code(422);
    echo json_encode(['error' => 'A valid email is required']);
    exit;
}"""
    if "git" in topic or "linux" in topic:
        return 'git status\ngit diff --check\ngit add path/to/resolved-file\ngit commit -m "Resolve configuration conflict"'
    return "const started = performance.now();\nconst result = await runOperation();\nlogger.info({ durationMs: performance.now() - started }, 'operation complete');"


def make_examples(tasks: list[tuple[str, str]], category: str, start_index: int, holdout: bool = False) -> list[tuple[dict, str]]:
    result: list[tuple[dict, str]] = []
    for task_index, (topic, guidance) in enumerate(tasks):
        for mode_index, (_, prompt_template, response_template) in enumerate(MODES):
            context = VALIDATION_SCENARIOS[(task_index + mode_index * 2) % len(VALIDATION_SCENARIOS)] if holdout else TRAINING_SCENARIOS[(task_index + mode_index) % len(TRAINING_SCENARIOS)]
            prompt = realistic_question(topic, category, mode_index, context, holdout)
            prompt += question_suffix(category, mode_index)
            response = realistic_answer(topic, guidance, category, mode_index, context, holdout)
            if category == "programming":
                response += [
                    " The example is the implementation starting point; wire it to your actual input and error path.",
                    " Reproduce the failure with the smallest input before changing surrounding code.",
                    " Before shipping, test rejected input and confirm that state stays unchanged.",
                    " Keep this simple until latency, traffic, or failure data justifies extra machinery.",
                    " Try malformed input and a repeated request, not only the successful case.",
                ][mode_index]
            language_marker = (start_index + task_index * 5 + mode_index) % 13
            if language_marker == 0:
                prompt, response = bangla_pair(topic, guidance, category, mode_index, context)
            elif language_marker == 1:
                prompt, response = banglish_pair(topic, guidance, category, mode_index, context)
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
        ([(topic, guidance) for topic, guidance in tasks], category, offset, quota)
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
    all_pairs = train_pairs + validation_pairs
    for batch_start in range(0, len(all_pairs), 50):
        batch = all_pairs[batch_start:batch_start + 50]
        if len(batch) != 50:
            raise ValueError(f"generation batch {batch_start // 50 + 1} is not exactly 50 examples")
        prompts = [item["messages"][0]["content"] for item, _ in batch]
        if len(prompts) != len(set(prompts)):
            raise ValueError(f"duplicate prompt inside generation batch {batch_start // 50 + 1}")
        for item, category in batch:
            user = item["messages"][0]["content"].lower()
            assistant = item["messages"][1]["content"].lower()
            if category == "programming" and "safe delete" in user and not any(token in assistant for token in ("delete", "transaction", "rollback", "mysql")):
                raise ValueError(f"safe-delete semantic check failed in batch {batch_start // 50 + 1}")
            if category == "programming" and "race condition" in user and not any(token in assistant for token in ("abortcontroller", "abort", "stale", "request")):
                raise ValueError(f"race-condition semantic check failed in batch {batch_start // 50 + 1}")
        print(f"Generation batch {batch_start // 50 + 1}: 50 examples checked")
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