#!/usr/bin/env python3
"""Generate all example modules for dataset extension."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# We'll write each module file
def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Wrote {path}")

# ============ ALGORITHMS ============
algo_train = [
    ("Implement binary search in Python.", "Time: O(log n), Space: O(1). Works on sorted arrays. Compare mid with target, eliminate half each step."),
    ("Time complexity of binary search?", "O(log n). Each comparison halves the search space."),
    ("Explain BFS vs DFS.", "BFS uses a queue, explores level by level, finds shortest paths in unweighted graphs. DFS uses stack/recursion, goes deep first, good for topological sort and cycle detection."),
    ("What is dynamic programming?", "Solves overlapping subproblems by storing results. Example: Fibonacci with memo is O(n) vs O(2^n) naive."),
    ("Stack vs Queue?", "Stack is LIFO (push/pop same end). Queue is FIFO (enqueue back, dequeue front)."),
    ("What is a heap?", "Complete binary tree where parent dominates children. Used for priority queues. Insert/extract O(log n)."),
    ("Explain Dijkstra algorithm.", "Finds shortest paths from source in weighted graph with non-negative edges. Uses priority queue. O((V+E) log V)."),
    ("BST vs hash table?", "BST: sorted data, range queries O(log n). Hash: O(1) average lookup, no ordering."),
    ("Time complexity of quicksort?", "Average O(n log n), worst O(n^2) with bad pivots. Space O(log n) for recursion stack."),
    ("What is a trie?", "Prefix tree storing strings character by character. O(m) insert/search where m is key length. Used for autocomplete and spell checking."),
    ("Explain union-find.", "Tracks disjoint sets. Find and union nearly O(1) amortized with path compression and union by rank."),
    ("Implement BFS on a graph.", "O(V+E) time. Use queue, track visited, process level by level."),
    ("Topological sorting?", "Orders DAG vertices so edge (u,v) means u before v. DFS post-order reversed or Kahn algorithm with in-degree tracking."),
    ("Two pointers technique?", "Two indices moving through data. Used for: two sum sorted array, palindrome check, finding middle of linked list."),
    ("Kruskal vs Prim for MST?", "Kruskal: sort edges, add non-cycle edges using union-find, O(E log E). Prim: grow tree from vertex using heap, O(E log V)."),
    ("What is amortized analysis?", "Averages cost over a sequence. Dynamic array insert is O(1) amortized despite occasional O(n) resize."),
    ("Linked list vs array?", "Array: O(1) random access, O(n) insert/delete. Linked list: O(1) insert at head, O(n) search, no random access."),
    ("Explain sliding window.", "Maintains window over data. O(n) for problems like max sum subarray, longest substring without repeats."),
    ("What is a priority queue?", "Serves highest-priority element first. Binary heap: insert O(log n), extract O(log n), peek O(1)."),
    ("Implement a stack.", "Use list: push = append, pop = pop(). Both O(1) amortized."),
    ("Explain merge sort.", "Divide array in half, recursively sort halves, merge sorted halves. O(n log n) always, O(n) space, stable."),
    ("What is a graph?", "Vertices connected by edges. Directed vs undirected. Weighted vs unweighted. Represented by adjacency list or matrix."),
    ("Implement DFS.", "O(V+E) time. Use recursion or explicit stack, track visited."),
    ("What is a hash collision?", "Two keys map to same hash bucket. Resolved by chaining (linked list at bucket) or open addressing (probe next slot)."),
    ("Explain Bellman-Ford algorithm.", "Shortest paths from source, handles negative edges. O(VE). Can detect negative cycles."),
]

algo_val = [
    ("What is Big O notation?", "Upper bound on growth rate. Describes worst-case time/space as input grows. O(1) < O(log n) < O(n) < O(n log n) < O(n^2)."),
    ("Implement quicksort.", "Pick pivot, partition array into elements less/greater than pivot, recurse on both halves. Average O(n log n)."),
    ("What is a hash table?", "Maps keys to values via hash function. Average O(1) lookup/insert. Worst O(n) with many collisions."),
    ("Explain binary search tree.", "Each node has left < parent < right. Search/insert average O(log n), worst O(n) if unbalanced."),
    ("What is graph coloring?", "Assign colors to vertices so no adjacent vertices share same color. Chromatic number is minimum colors needed."),
    ("Explain knapsack problem.", "Given items with weights and values, maximize value within weight limit. 0/1 knapsack is O(nW) with DP. Fractional is greedy O(n log n)."),
    ("What is memoization?", "Cache results of expensive function calls. Trade space for time. Top-down DP approach."),
    ("Explain Bellman-Ford.", "Shortest paths from source with negative edges. O(VE) time. Detects negative cycles."),
    ("What is a red-black tree?", "Self-balancing BST with O(log n) operations. Nodes colored red/black with balancing rules to maintain height log n."),
    ("Explain Floyd-Warshall.", "All-pairs shortest paths in O(V^3). Works with negative edges but not negative cycles."),
    ("What is backtracking?", "Explore all solutions, abandon invalid ones early. Used for N-queens, Sudoku, permutations. Exponential worst case."),
    ("Explain greedy algorithms.", "Make locally optimal choices at each step. Works for activity selection, Huffman coding. Not always globally optimal."),
    ("What is divide and conquer?", "Split problem into subproblems, solve recursively, combine results. Examples: merge sort, quicksort, binary search."),
    ("What is a bloom filter?", "Probabilistic set: O(1) insert/lookup, may have false positives, no false negatives. Space efficient."),
    ("BFS shortest path properties?", "In unweighted graph, BFS from source gives shortest paths to all reachable vertices. O(V+E) time."),
    ("What is the Master theorem?", "Solves recurrences T(n) = aT(n/b) + f(n). Compare f(n) to n^(log_b(a)) to determine complexity class."),
    ("Explain dynamic arrays.", "Resizable arrays like Python list. Amortized O(1) append, double capacity when full. O(n) worst-case resize."),
    ("What is a skip list?", "Layered linked list for O(log n) search. Probabilistic balancing alternative to balanced BSTs."),
    ("Explain stable matching.", "Gale-Shapley algorithm produces stable matching between two sets in O(n^2). No pair prefers someone else over their match."),
    ("What is cycle detection?", "Floyd tortoise and hare algorithm detects cycle in O(n) time, O(1) space. Also: topological sort for directed graphs."),
]

write_file('training/examples/algorithms.py', '"""Algorithm and data structure examples."""\n\nALGO_TRAIN = ' + repr(algo_train) + '\n\nALGO_VAL = ' + repr(algo_val) + '\n')

# ============ SYSTEM DESIGN ============
sys_train = [
    ("Design a URL shortener.", "Hash or base62 encode a counter. Store mapping in Redis for speed, MySQL for persistence. Use 301 redirects. Consider collision handling and custom slugs."),
    ("Design a chat system.", "WebSocket for real-time messages. Store messages in database with conversation ID. Use message queue for fan-out. Presence via heartbeat. Read receipts with ACK."),
    ("How would you design rate limiting?", "Token bucket or sliding window. Redis for distributed counters. Return 429 with Retry-After header. Different limits per endpoint and user tier."),
    ("Design a notification system.", "Event-driven: producers emit events, notification service consumes them. Support push, email, SMS via separate workers. Use priority queue for urgent notifications."),
    ("Design a file storage service.", "Object storage with content-addressable hashing. Store metadata in MySQL, files in S3-compatible storage. Chunk large files. Pre-signed URLs for access."),
    ("Design a search system.", "Inverted index for full-text search. Elasticsearch or custom implementation. Rank by relevance (TF-IDF or BM25). Support autocomplete with trie."),
    ("How would you design an e-commerce backend?", "Product catalog in MySQL with Redis cache. Cart in Redis session. Orders with ACID transactions. Payment via Stripe/PayPal integration. Inventory with optimistic locking."),
    ("Design an authentication system.", "JWT access tokens with short expiry, refresh token rotation. Password hashing with bcrypt. OAuth2 for social login. Rate limit login attempts."),
    ("Design a payment processing architecture.", "Idempotent payment requests with unique keys. Webhook for async confirmation. Two-phase: authorize then capture. Reconciliation job. PCI compliance."),
    ("How would you implement caching?", "Cache-aside pattern: check cache first, fallback to DB. Use Redis with TTL. Cache invalidation on write. Consider stampede with locks."),
    ("Design a URL shortener at scale.", "Base62 encoding of auto-increment ID. Bloom filter for existence check. Redis for hot mappings. MySQL for persistence. Analytics via write-behind."),
    ("Design a real-time leaderboard.", "Redis sorted set for O(log N) rank updates. Shards by game ID. Periodic snapshot to MySQL for persistence. Handle ties with secondary sort."),
    ("How would you design a news feed?", "Pull model: fan-out on read, query followees posts. Push model: fan-out on write to followers inbox. Hybrid: push for users with few followers, pull for celebrities."),
    ("Design a webhook delivery system.", "Queue-based with retry. Exponential backoff. Dead letter queue for permanent failures. Signature verification. Delivery logs for debugging."),
    ("How would you design a task scheduler?", "Job queue with Redis or RabbitMQ. Workers poll for jobs. Support cron expressions. Priority levels. Dead letter for failed jobs. Monitoring dashboard."),
    ("Design a content delivery strategy.", "CDN for static assets with cache headers. Origin server for dynamic content. Edge caching with invalidation. Consider cache-busting with versioned filenames."),
    ("How would you design a logging system?", "Structured logging to stdout. Log collector (Fluentd/Logstash). Centralized storage (Elasticsearch). Alerting on patterns. Retention policies."),
    ("Design a notification preference system.", "User preferences stored per notification type and channel. Check preferences before sending. Support do-not-disturb windows. Audit trail."),
    ("How would you design a multi-tenant system?", "Shared database with tenant_id column. Row-level security. Separate schemas for isolation. Resource quotas per tenant. Connection pooling."),
    ("Design a real-time collaboration tool.", "Operational Transformation or CRDT for concurrent edits. WebSocket for real-time sync. Version history with conflict resolution. Presence indicators."),
]

sys_val = [
    ("Design a simple cache.", "LRU cache with O(1) lookup and eviction. Use HashMap + doubly linked list. Set TTL for expiry. Consider size limits."),
    ("How would you design a URL validator?", "Regex for format, DNS lookup for domain existence, HTTP check for accessibility. Handle international domains with IDN encoding."),
    ("Design a rate limiter for an API.", "Token bucket algorithm. Redis for distributed state. Key by API key or IP. Return remaining quota in headers. Support different limits per endpoint."),
    ("How would you design a feature flag system?", "Toggle stored in database, cached in Redis. Evaluation at application level. Gradual rollout by percentage. A/B testing support."),
    ("Design a simple search autocomplete.", "Trie with frequency counts. Update counts on search. Return top-k suggestions. Cache popular queries. Consider typo tolerance."),
    ("How would you design audit logging?", "Append-only table recording who did what and when. Store old and new values for mutations. Queryable by actor, time range, and action type."),
    ("Design a session management system.", "Server-side sessions stored in Redis. Random session IDs. Automatic expiry. Regeneration on privilege change. Secure cookie flags."),
    ("How would you design a configuration management system?", "Hierarchical config with environment overrides. Version controlled. Hot reload via file watcher or API. Validate config on startup."),
    ("Design a simple message queue.", "Circular buffer with producers and consumers. Support multiple consumer groups. Persistent storage for durability. Dead letter for failed messages."),
    ("How would you design a health check endpoint?", "Check database connectivity, Redis, external services. Return 200 if healthy, 503 if not. Include dependency status in response body."),
    ("Design a database migration system.", "Versioned SQL files applied in order. Track applied migrations in a meta table. Support up and down migrations. Dry-run mode."),
    ("How would you design a file upload system?", "Stream to temp file, validate type and size, move to permanent storage. Generate unique filename. Return URL. Support chunked uploads for large files."),
    ("Design a simple CDN.", "Reverse proxy with caching. Cache static assets by URL. Respect Cache-Control headers. Purge by tag or URL pattern. Origin fallback."),
    ("How would you design a task queue?", "Redis list with BRPOPLPUSH for reliable processing. Worker pool consuming jobs. Retry with exponential backoff. Priority queue support."),
    ("Design a simple load balancer.", "Round-robin or least-connections algorithm. Health checks on backends. Session affinity option. Weighted distribution. Connection draining on shutdown."),
    ("How would you design API versioning?", "URL path versioning (/v1/, /v2/). Deprecation headers. Backward-compatible changes preferred. Documentation for breaking changes."),
    ("Design a webhook system.", "Outgoing HTTP calls with retry. Signature header for verification. Event filtering per subscriber. Delivery logs with response codes."),
    ("How would you design a data pipeline?", "ETL: Extract from sources, Transform in processing layer, Load to destination. Use message queue for decoupling. Monitor lag and failures."),
    ("Design a simple distributed lock.", "Redis SET NX EX for acquire, Lua script for release. Fencing token to prevent stale locks. Consider Redlock for multi-node."),
    ("How would you design an API gateway?", "Single entry point for all APIs. Handle auth, rate limiting, request routing. Transform responses. Log all requests. Support WebSocket upgrade."),
]

write_file('training/examples/system_design.py', '"""System design examples."""\n\nSYS_TRAIN = ' + repr(sys_train) + '\n\nSYS_VAL = ' + repr(sys_val) + '\n')

# ============ AI/ML ============
ml_train = [
    ("What is a transformer?", "Architecture using self-attention to process sequences. Encoder-decoder with multi-head attention. Replaced RNNs for most NLP tasks. Foundation of modern LLMs."),
    ("Explain attention mechanism.", " Computes relevance scores between query and keys. Scaled dot-product: softmax(QK^T/sqrt(d))V. Allows model to focus on relevant parts of input."),
    ("What is tokenization?", "Converting text to numerical tokens. BPE merges frequent character pairs. WordPiece for BERT. SentencePiece for multilingual. Determines vocabulary size and input representation."),
    ("Explain embeddings.", "Dense vector representations of discrete items. Word2Vec, GloVe for words. Sentence transformers for text. Capture semantic relationships in continuous space."),
    ("What is RAG?", "Retrieval-Augmented Generation: retrieve relevant documents, inject into LLM context. Combines knowledge base with generative model. Reduces hallucination, enables current knowledge."),
    ("Explain LoRA fine-tuning.", "Low-Rank Adaptation: freeze base model, train low-rank decomposition matrices. Reduces trainable parameters by 100-1000x. Applied to attention layers."),
    ("What is QLoRA?", "Quantized LoRA: combine 4-bit quantization with LoRA fine-tuning. Enables fine-tuning 65B models on single 48GB GPU. NF4 quantization."),
    ("Explain transformer attention math.", "Attention(Q,K,V) = softmax(QK^T/sqrt(d_k))V. Multi-head: concat multiple attention heads. Each head learns different relationship patterns."),
    ("What is temperature in LLM sampling?", "Controls randomness in token selection. T=1: standard sampling. T<1: more deterministic, peaked distribution. T>1: more random, flatter distribution."),
    ("Explain top-p sampling.", "Nucleus sampling: sample from smallest set of tokens whose cumulative probability >= p. Dynamically adjusts vocabulary size. Balances coherence and diversity."),
    ("What is context window?", "Maximum number of tokens an LLM can process. Includes input + output. GPT-4: 128K. Limited by attention mechanism quadratic cost."),
    ("Explain overfitting.", "Model memorizes training data instead of learning patterns. Signs: low train loss, high val loss. Fixes: more data, regularization, dropout, early stopping."),
    ("What is a neural network?", "Layers of connected neurons with learnable weights. Forward pass computes output. Backpropagation computes gradients. Loss function measures error."),
    ("Explain gradient descent.", "Optimization by updating parameters in negative gradient direction. Learning rate controls step size. Variants: SGD, Adam, AdaGrad. Converges to local minimum."),
    ("What is a CNN?", "Convolutional Neural Network: applies learnable filters to detect patterns. Pooling reduces spatial dimensions. Effective for images, also text classification."),
    ("Explain RNN and LSTM.", "RNN processes sequences with hidden state. LSTM adds gates (forget, input, output) to handle long-range dependencies. GRU simplifies LSTM with fewer gates."),
    ("What is batch normalization?", "Normalize layer inputs to zero mean, unit variance. Speeds training, allows higher learning rates. Applied before activation function."),
    ("Explain dropout.", "Randomly zero neurons during training. Prevents co-adaptation, acts as ensemble. Usually 20-50% rate. Disabled during inference."),
    ("What is Adam optimizer?", "Adaptive learning rate method combining momentum and RMSProp. Maintains per-parameter learning rates. Good default for most problems."),
    ("Explain backpropagation.", "Compute gradients of loss w.r.t. parameters using chain rule. Forward pass computes activations. Backward pass propagates error gradients. O(n) per layer."),
    ("What is fine-tuning?", "Continue training pre-trained model on specific task. Lower learning rate than pre-training. Freeze early layers, train later layers. Adapt general model to domain."),
    ("Explain token limits in LLMs.", "LLMs have fixed context window. Input tokens + output tokens must fit. Exceeding causes truncation. Strategies: chunking, sliding window, summarization."),
    ("What is prompt engineering?", "Designing input text to get desired LLM output. Techniques: few-shot examples, chain-of-thought, role prompting, constrained output."),
    ("Explain hallucination in LLMs.", "Model generates plausible but false information. Caused by: training data gaps, pattern matching without understanding. Mitigation: RAG, fact-checking, constrained decoding."),
    ("What is model quantization?", "Reduce precision of model weights (FP16, INT8, INT4). Reduces memory and speeds inference. Trade-off: slight accuracy loss. Enables deployment on edge devices."),
]

ml_val = [
    ("What is self-attention?", "Mechanism where each token attends to all other tokens. Computes pairwise relevance. O(n^2) in sequence length. Enables parallel processing of sequences."),
    ("Explain BERT.", "Bidirectional encoder, pre-trained with masked language modeling and next sentence prediction. Good for classification, NER, question answering."),
    ("What is GPT architecture?", "Decoder-only transformer. Auto-regressive: predict next token. Pre-trained on next token prediction. Generates text sequentially."),
    ("Explain transfer learning.", "Use knowledge from one task to improve another. Pre-train on large corpus, fine-tune on small dataset. Foundation of modern NLP."),
    ("What is a language model?", "Probability distribution over token sequences. P(w1,w2,...,wn). Can be autoregressive (GPT) or masked (BERT). Trained to predict next/masked tokens."),
    ("Explain multi-head attention.", "Multiple attention heads in parallel, each learning different relationships. Concatenate outputs, project with linear layer. Allows attending to different positions simultaneously."),
    ("What is positional encoding?", "Inject sequence order information since transformers lack recurrence. Sinusoidal (fixed) or learned embeddings. Added to token embeddings before attention."),
    ("Explain encoder-decoder architecture.", "Encoder processes input into representation. Decoder generates output conditioned on encoder. Used in translation, summarization. Cross-attention connects them."),
    ("What is beam search?", "Keep top-k (beam width) most probable sequences at each step. More thorough than greedy, less random than sampling. Used in translation and summarization."),
    ("Explain knowledge distillation.", "Train smaller student model to mimic larger teacher. Soft targets from teacher provide more information than hard labels. Reduces model size with minimal accuracy loss."),
    ("What is a data pipeline for ML?", "Sequence: data collection, cleaning, feature engineering, splitting, training, evaluation. Needs versioning, reproducibility, monitoring."),
    ("Explain ROC-AUC.", "Receiver Operating Characteristic curve plots TPR vs FPR at various thresholds. AUC = area under curve. 0.5 = random, 1.0 = perfect. Threshold-independent metric."),
    ("What is cross-validation?", "Split data into k folds. Train on k-1, validate on 1. Rotate. Average metrics. More reliable estimate of generalization performance."),
    ("Explain feature engineering.", "Transform raw data into model inputs. Categorical encoding, scaling, interaction terms, text vectorization. Domain knowledge improves model performance."),
    ("What is a confusion matrix?", "Table of TP, FP, TN, FN. From this: accuracy, precision, recall, F1. Shows types of errors model makes."),
    ("Explain precision vs recall.", "Precision = TP/(TP+FP) - of predicted positives, how many correct. Recall = TP/(TP+FN) - of actual positives, how many found. Trade-off between them."),
    ("What is regularization?", "Techniques to prevent overfitting: L1/L2 weight penalty, dropout, early stopping, data augmentation. Adds constraint to model complexity."),
    ("Explain batch vs stochastic gradient descent.", "Batch GD uses all data per update - stable but slow. SGD uses one sample - noisy but fast. Mini-batch is compromise. Most common in practice."),
    ("What is a loss function?", "Measures prediction error. MSE for regression, cross-entropy for classification, contrastive loss for similarity. Minimized during training."),
    ("Explain learning rate scheduling.", "Adjust learning rate during training. Start high for fast convergence, decay for fine-tuning. Cosine annealing, warm-up, step decay."),
    ("What is an embedding layer?", "Lookup table mapping discrete tokens to dense vectors. Learnable during training. Output dimension is embedding size. Foundation of NLP models."),
    ("Explain chain-of-thought prompting.", "Ask model to show reasoning steps before final answer. Improves accuracy on multi-step problems. Mimics human problem-solving process."),
    ("What is few-shot learning?", "Provide a few examples in the prompt to guide model behavior. No fine-tuning needed. Leverages in-context learning ability of large models."),
    ("Explain model evaluation metrics.", "Classification: accuracy, precision, recall, F1, AUC. Regression: MSE, MAE, R-squared. NLP: BLEU, ROUGE, perplexity. Choose metric aligned with goal."),
    ("What is neural network initialization?", "Random weight initialization breaks symmetry. Xavier/He initialization maintains variance across layers. Poor initialization causes vanishing/exploding gradients."),
]

write_file('training/examples/ai_ml.py', '"""AI/ML examples."""\n\nML_TRAIN = ' + repr(ml_train) + '\n\nML_VAL = ' + repr(ml_val) + '\n')

# ============ RESEARCH (deeper) ============
research_train = [
    ("Compare PostgreSQL vs MySQL for a SaaS.", "PostgreSQL: better JSON support, stricter types, advanced features. MySQL: simpler ops, wider hosting. For SaaS: PostgreSQL if you need JSONB, complex queries. MySQL if team knows it."),
    ("REST vs GraphQL tradeoffs.", "REST: simpler, cacheable, good for public APIs. GraphQL: flexible queries, no over-fetching, good for complex client needs. GraphQL adds server complexity."),
    ("Evaluate microservices vs monolith.", "Monolith: simpler deploy, easier debugging, good for small teams. Microservices: independent scaling, team autonomy, but adds operational complexity. Start monolith, split when justified."),
    ("How do you evaluate a technology?", "Consider: problem fit, team expertise, ecosystem maturity, community support, operational cost, migration path. Avoid hype-driven decisions."),
    ("Compare SQL vs NoSQL databases.", "SQL: structured data, ACID, complex queries. NoSQL: flexible schema, horizontal scaling, eventual consistency. Choose based on data model and consistency needs."),
    ("Evaluate RAG vs fine-tuning for knowledge.", "RAG: add knowledge without retraining, updatable, transparent sources. Fine-tune: deeper behavior change, better for style/format. Combine for best results."),
    ("How do you assess ML model quality?", "Hold-out test set, cross-validation, multiple metrics (not just accuracy). Check for bias, fairness, robustness. Compare against baseline. Consider inference cost."),
    ("Evaluate caching strategies.", "Cache-aside: flexible, application-managed. Write-through: consistent but slower writes. Write-behind: fast writes, risk of data loss. CDN for static, Redis for dynamic."),
    ("Compare message queues: RabbitMQ vs Kafka.", "RabbitMQ: traditional queue, routing, good for task distribution. Kafka: log-based, replay, high throughput, event streaming. Kafka for event sourcing, RabbitMQ for work queues."),
    ("Evaluate serverless vs containers.", "Serverless: no ops, auto-scale, pay-per-use, cold starts. Containers: consistent env, more control, predictable cost at scale. Serverless for variable workloads."),
    ("How do you evaluate API design quality.", "Consistency, naming, error handling, versioning, documentation, security. Follow conventions (REST: nouns, HTTP methods). Test with clients before finalizing."),
    ("Compare testing strategies.", "Unit: fast, isolated. Integration: real dependencies. E2E: full stack, slow. TDD vs BDD. Balance: many unit tests, some integration, few E2E."),
    ("Evaluate observability approaches.", "Logs: detailed events. Metrics: aggregates over time. Traces: request flow across services. All three needed. Structured logging enables better analysis."),
    ("Compare deployment strategies.", "Blue-green: zero downtime, two environments. Canary: gradual rollout, risk mitigation. Rolling: update instances one by one. Choose based on risk tolerance."),
    ("Evaluate data modeling approaches.", "Normalization: reduce redundancy, ensure consistency. Denormalization: optimize reads. Star schema for analytics. Choose based on read/write patterns."),
    ("How do you evaluate security tradeoffs.", "Defense in depth, principle of least privilege. Balance security with usability. Consider threat model. Regular audits. Don't over-engineer for unlikely threats."),
    ("Compare frontend frameworks.", "React: ecosystem, flexibility. Vue: simplicity, learning curve. Angular: structure, TypeScript. Svelte: compiler, performance. Choose based on team and project needs."),
    ("Evaluate database scaling options.", "Read replicas: scale reads. Sharding: scale writes. Vertical scaling: simplest but limited. Connection pooling: reduce overhead. Cache layer: reduce DB load."),
    ("How do you approach code review.", "Focus on correctness, readability, maintainability. Check edge cases, security, performance. Be constructive. Automated checks first, human review for design."),
    ("Evaluate technical debt.", "Identify hot spots (frequent changes, many bugs). Measure impact on velocity. Prioritize by frequency and severity. Balance with feature work. Refactor incrementally."),
]

research_val = [
    ("Compare Python vs JavaScript for backend.", "Python: cleaner syntax, ML ecosystem, Django/Flask. JavaScript: full-stack with Node, async I/O, npm ecosystem. Python for data-heavy, JS for real-time."),
    ("Evaluate NoSQL for a chat application.", "Document store (MongoDB) good for message history. Key-value (Redis) for real-time. Wide-column for time-series. Consider query patterns and consistency needs."),
    ("How do you evaluate open source licenses.", "Permissive (MIT, Apache): allow commercial use. Copyleft (GPL): derivatives must be open. LGPL: linking only. Match license to distribution model."),
    ("Compare cloud providers.", "AWS: largest ecosystem. Azure: Microsoft integration. GCP: data/ML strengths. Compare pricing, services, support, compliance needs."),
    ("Evaluate API versioning strategies.", "URL versioning: explicit but creates many routes. Header versioning: clean URLs but harder to test. Query param: simple but messy. Choose what works for your clients."),
    ("Compare CI/CD approaches.", "Jenkins: self-hosted, flexible. GitHub Actions: integrated, YAML. GitLab CI: built-in. Consider: cost, maintenance, integration, scalability."),
    ("How do you evaluate code quality.", "Static analysis, test coverage, complexity metrics, code review. Balance metrics with judgment. High coverage with bad tests is misleading."),
    ("Evaluate container orchestration.", "Kubernetes: powerful but complex. Docker Swarm: simpler but limited. Nomad: flexible. Managed services (ECS, Cloud Run) for less ops."),
    ("Compare search engines.", "Elasticsearch: full-featured, heavy. Meilisearch: lightweight, fast. Algolia: SaaS, easy. Solr: mature. Choose based on scale and features needed."),
    ("Evaluate event sourcing patterns.", "Events as source of truth. Replay capability, audit trail. Complexity in querying current state. Use when history matters (finance, collaboration)."),
    ("How do you evaluate a research paper.", "Check methodology, sample size, statistical significance. Reproducibility. Related work context. Limitations section. Conflict of interest."),
    ("Compare static site generators.", "Next.js: React, SSR/SSG. Hugo: fast, Go templates. Gatsby: GraphQL, plugins. Astro: islands. Choose based on complexity needs."),
    ("Evaluate database migration tools.", "Flyway: SQL-based, simple. Liquibase: changelog, rollback. Alembic: Python. Consider: rollback support, team familiarity, integration."),
    ("Compare monitoring solutions.", "Prometheus + Grafana: metrics, open source. Datadog: SaaS, comprehensive. New Relic: APM. Consider cost, features, self-hosted vs SaaS."),
    ("How do you approach architecture decisions.", "ADRs (Architecture Decision Records). Document context, options, tradeoffs, decision. Review with team. Revisit when assumptions change."),
    ("Evaluate real-time frameworks.", "WebSockets: bidirectional, persistent. SSE: server-to-client. Socket.IO: abstraction over both. Consider: scale, fallback, protocol."),
    ("Compare build tools.", "Webpack: configurable, complex. Vite: fast, ESM. esbuild: fastest, limited features. Turbopack: incremental. Choose based on project needs."),
    ("Evaluate database indexing strategies.", "Index selective columns used in WHERE/JOIN. Composite index order matters. Covering indexes avoid table lookups. Too many indexes slow writes."),
    ("How do you evaluate API performance.", "Latency percentiles (p50, p95, p99), throughput, error rate. Load testing with realistic patterns. Monitor after deployment."),
    ("Evaluate state management.", "Local state: simplest. Context: simple shared. Redux: predictable. Zustand: minimal. Jotai: atomic. Choose based on complexity and team preference."),
]

write_file('training/examples/research.py', '"""Deeper research examples."""\n\nRESEARCH_TRAIN = ' + repr(research_train) + '\n\nRESEARCH_VAL = ' + repr(research_val) + '\n')

# ============ PROGRAMMING (deeper) ============
prog_train = [
    ("Implement JWT authentication in Node.js.", "Use jsonwebtoken library. Sign token with secret and expiry. Verify on protected routes. Store in httpOnly cookie or Authorization header."),
    ("How to prevent SQL injection in PHP.", "Always use prepared statements with PDO. Never interpolate user input into SQL. Use bindParam or bindValue with typed parameters."),
    ("Implement CSRF protection in a web app.", "Generate random token per session. Include in forms as hidden field. Verify on POST requests. Use SameSite cookie attribute."),
    ("Build a REST API with proper error handling.", "Use consistent JSON error format. Return appropriate HTTP status codes. Log errors server-side. Validate input. Handle not-found, unauthorized, validation errors."),
    ("How to implement rate limiting in PHP.", "Use Redis to store request counts per IP/API key. Sliding window algorithm. Return 429 with Retry-After header. Different limits per endpoint."),
    ("Implement file upload validation in PHP.", "Check $_FILES errors, file size, MIME type with finfo, extension against whitelist. Generate random filename. Store outside web root."),
    ("Build a WebSocket chat server.", "Use ws library in Node.js. Handle connection, message, disconnect events. Broadcast to room members. Store message history. Handle reconnection."),
    ("How to implement pagination in PHP/MySQL.", "Use LIMIT/OFFSET with prepared statements. Calculate total count separately. Return metadata: page, per_page, total, has_next."),
    ("Implement a secure login system.", "Hash password with password_verify. Rate limit login attempts. Use httpOnly cookies. Implement session fixation protection. Add account lockout."),
    ("Build a JSON API with PHP.", "Set Content-Type header. Validate JSON input. Use http_response_code for errors. Return consistent response format. Handle CORS."),
    ("How to implement soft deletes.", "Add deleted_at timestamp column. Filter queries by deleted_at IS NULL. Restore by setting deleted_at to NULL. Cascade to related records."),
    ("Implement image processing in PHP.", "Use GD library or Imagick. Resize, crop, compress. Validate image dimensions and type. Generate thumbnails. Store in private directory."),
    ("Build a real-time notification system.", "Event-driven architecture. WebSocket for push. Store in database for persistence. Batch notifications. Support multiple channels."),
    ("How to implement optimistic locking.", "Add version column to database. Include version in UPDATE WHERE clause. If affected rows is 0, someone else updated first. Retry or inform user."),
    ("Implement a search feature with MySQL.", "Use FULLTEXT index for text search. LIKE for simple patterns. Consider Elasticsearch for complex search. Add filters and sorting."),
    ("Build a file sharing system.", "Generate unique file ID. Store file metadata in DB. Support access control (owner, shared users). Generate time-limited download links."),
    ("How to handle concurrent API requests.", "Use idempotency keys for POST requests. Deduplicate by key. Return cached response for duplicate requests. Implement request deduplication."),
    ("Implement a webhook receiver.", "Verify signature with HMAC. Validate payload schema. Process asynchronously via queue. Return 200 quickly. Retry on failure."),
    ("Build a role-based access control system.", "Define roles and permissions. Assign roles to users. Check permissions at middleware level. Cache permission checks."),
    ("How to implement a caching strategy.", "Cache-aside with Redis. Cache database query results. Set appropriate TTL. Invalidate on data change. Handle cache stampede."),
    ("Implement a background job processor.", "Use Redis queue with worker processes. Support retries with exponential backoff. Dead letter queue for failed jobs. Monitor queue depth."),
    ("Build a logging and monitoring system.", "Structured JSON logging. Different log levels. Centralized log aggregation. Alert on error patterns. Performance metrics."),
    ("How to implement database migrations.", "Version-controlled SQL files. Track applied migrations. Support up/down operations. Test on copy of production data."),
    ("Implement a payment integration.", "Use Stripe/PayPal SDK. Idempotent requests. Webhook for async events. Handle failures gracefully. PCI compliance considerations."),
    ("Build a dashboard with real-time data.", "WebSocket or Server-Sent Events for updates. Aggregate metrics server-side. Cache expensive queries. Update charts incrementally."),
    ("How to optimize slow database queries.", "Use EXPLAIN to analyze query plan. Add appropriate indexes. Avoid SELECT *. Optimize JOINs. Consider query rewriting."),
    ("Implement error tracking and alerting.", "Global error handler. Send errors to tracking service (Sentry). Alert on error rate spikes. Stack traces and context."),
    ("Build a multi-language support system.", "Use i18n library. Extract strings to resource files. Support pluralization. Date/number formatting by locale. RTL support."),
    ("How to implement data validation.", "Server-side validation for all inputs. Client-side for UX. Whitelist approach. Validate types, lengths, ranges. Return specific error messages."),
    ("Build a notification preference system.", "Store per-user, per-notification-type preferences. Support channels: email, push, in-app. Respect do-not-disturb windows."),
]

prog_val = [
    ("How to implement JWT refresh tokens.", "Short-lived access token (15 min), long-lived refresh token (7 days). Rotate refresh token on use. Store refresh tokens in database. Revoke on logout."),
    ("Build a rate limiter with Redis.", "Token bucket: store tokens per key. Refill at fixed rate. Decrement on request. Return 429 when empty. Use Lua script for atomicity."),
    ("Implement API authentication.", "API keys in headers. HMAC signatures for request verification. OAuth2 for delegated access. Rate limit per key."),
    ("How to handle CORS in a web API.", "Set Access-Control-Allow-Origin. Handle preflight OPTIONS requests. Allow specific methods and headers. Credentials require explicit origin."),
    ("Build a real-time collaboration feature.", "Operational Transform or CRDT for conflict resolution. WebSocket for sync. Version tracking. Presence indicators."),
    ("Implement data encryption at rest.", "Use AES-256 for database encryption. Encrypt sensitive fields. Key management with KMS. Envelope encryption for performance."),
    ("How to build a feature flag system.", "Store flags in database with Redis cache. Evaluate at middleware level. Support gradual rollout by percentage. A/B testing."),
    ("Implement a search autocomplete.", "Trie data structure with frequency counts. Update on each search. Return top-k suggestions. Cache popular queries."),
    ("Build a webhook delivery system.", "Queue-based with retry logic. Exponential backoff. Dead letter queue. Signature verification. Delivery logs."),
    ("How to implement logging best practices.", "Structured JSON logs. Correlation IDs across requests. Appropriate log levels. Separate access and application logs."),
    ("Build a notification system.", "Event-driven architecture. Multiple channels (email, push, in-app). Priority queue. User preferences. Delivery tracking."),
    ("Implement a caching layer.", "Redis with TTL. Cache-aside pattern. Invalidation on write. Cache warming for cold starts. Monitor hit rate."),
    ("How to handle database failover.", "Read replicas for read scaling. Automatic failover with health checks. Connection pooling. Retry logic for transient failures."),
    ("Build an API gateway.", "Single entry point. Authentication, rate limiting, request routing. Response caching. Logging and monitoring."),
    ("Implement a task scheduler.", "Cron-like scheduling. Job priority. Retry with backoff. Dead letter for failures. Dashboard for monitoring."),
    ("How to optimize API response time.", "Database query optimization, response caching, compression, pagination, field selection. Monitor p95 latency."),
    ("Build a content management system.", "Flexible schema for content types. Version control. Workflow (draft, review, publish). Media management. Access control."),
    ("Implement audit logging.", "Track all data mutations. Store before/after values. Queryable by user, time, action. Compliance requirements."),
    ("How to handle API versioning.", "URL path versioning (/v1/). Backward-compatible changes. Deprecation headers. Documentation for breaking changes."),
    ("Build a monitoring dashboard.", "Real-time metrics with Prometheus/Grafana. Key indicators: latency, error rate, throughput. Alert rules."),
    ("Implement a testing framework.", "Unit tests for logic. Integration tests for APIs. E2E tests for critical paths. Test data factories. CI/CD integration."),
    ("How to manage environment configuration.", "Separate config from code. Environment variables. .env files for development. Secrets management (Vault, AWS SSM)."),
    ("Build a health check system.", "Check all dependencies (DB, cache, external services). Return status code and details. Include in load balancer config."),
    ("Implement a data pipeline.", "ETL processes. Data validation. Schema evolution. Monitoring. Error handling and retry."),
    ("How to handle graceful shutdown.", "Stop accepting new requests. Wait for in-flight requests to complete. Close database connections. Exit cleanly."),
    ("Build a multi-tenant system.", "Shared database with tenant_id. Row-level security. Resource quotas. Separate schemas for isolation."),
    ("Implement a CI/CD pipeline.", "Build, test, deploy stages. Automated testing. Staging environment. Blue-green or canary deployment. Rollback capability."),
    ("How to handle file uploads at scale.", "Chunked uploads. Direct-to-S3 presigned URLs. Progress tracking. Resumable uploads. Virus scanning."),
    ("Build an error tracking system.", "Global error handler. Error grouping. Alert rules. Stack traces with context. User impact tracking."),
    ("Implement a real-time dashboard.", "WebSocket for live updates. Server-Sent Events for one-way. Efficient data serialization. Connection management."),
]

write_file('training/examples/programming_deep.py', '"""Deeper programming examples."""\n\nPROG_TRAIN = ' + repr(prog_train) + '\n\nPROG_VAL = ' + repr(prog_val) + '\n')

print("All example modules generated!")
print("Run: python training/extend_dataset.py")
