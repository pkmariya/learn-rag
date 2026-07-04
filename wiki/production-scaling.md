# Production Scaling

**Summary**: A RAG pipeline that works on a laptop often dies with real users. Production-grade RAG requires separation of concerns — models, API, databases, and tools all scaling independently — plus strategies like parallel processing, semantic caching, and infrastructure as code.

**Sources**: RAG architecture.txt, RAG Primer.docx

**Last updated**: 2026-07-04

---

## The Core Principle

The secret is separation. Your models, your API, your databases, your tools — all independent, all scaling on their own. That's production-grade RAG (source: RAG architecture.txt).

## Testing for Production

Before deploying, mix 95% garbage data with your real documents. If your pipeline can still find the right answers in all that noise, you know it's solid (source: RAG architecture.txt).

## Key Architecture Patterns

### 1. Parallel Document Processing

Process documents in parallel, not one by one. Tools like Ray let you parse thousands of files across multiple machines at the same time (source: RAG architecture.txt).

### 2. Vector Search + Knowledge Graph

Don't use vector search alone. Combine it with a knowledge graph. Vectors give you semantic meaning; the graph gives you relationships between entities. Run both at the same time (source: RAG architecture.txt).

See [[graph-based-rag]] and [[hybrid-retrieval]] for implementation patterns.

### 3. Separate LLM from API Server

Never put your LLM inside your API server. Host your model separately using something like vLLM and Ray Serve so they scale based on GPU demand without killing your web server (source: RAG architecture.txt).

### 4. Polyglot Persistence (Multiple Databases)

Use multiple databases, each for what it's best at (source: RAG architecture.txt):
- One for chat history
- One for caching
- One for vectors (see [[vector-databases]])
- One for entity relationships (knowledge graph)

One database can't do everything well.

### 5. Semantic Caching

If two users ask the same question in different words, recognize it's the same intent and serve a cached answer. Zero GPU cost for repeat queries (source: RAG architecture.txt).

See [[cost-optimization]] for more caching strategies.

### 6. Intelligent Agent Design

Use something like LangGraph to build a state machine where the agent can plan, decide if it needs to search, run code, or answer directly. It can loop and correct itself instead of just going retrieve-then-answer (source: RAG architecture.txt).

See [[agentic-rag]] and [[graph-based-rag]] for agentic pipeline architectures.

### 7. Sandbox Code Execution

If your agent can execute code, sandbox it. No network access, limited memory, hard timeout. One bad prompt shouldn't take down your system (source: RAG architecture.txt).

### 8. Infrastructure as Code

Define your entire cloud infrastructure as code using tools like Terraform. Don't click buttons in a console (source: RAG architecture.txt).

### 9. Auto-Scale to Zero

Use something like Karpenter to scale to zero. When nobody's using it, kill the GPU machines automatically. When traffic comes back, spin them up in seconds. Only pay for what you use (source: RAG architecture.txt).

## Production Checklist

From RAG architecture.txt and RAG Primer.docx:

- [ ] Documents processed in parallel (Ray or equivalent)
- [ ] LLM hosted separately from API server
- [ ] Vector search combined with knowledge graph
- [ ] Separate databases for separate concerns
- [ ] Semantic caching for repeated queries
- [ ] Agent can loop and self-correct (not linear)
- [ ] Code execution sandboxed
- [ ] Infrastructure defined as code
- [ ] Auto-scaling to zero when idle
- [ ] [[observability]] spans on every pipeline stage
- [ ] [[rag-evaluation]] running on production traffic

## Related Pages

- [[rag-pipeline-architecture]]
- [[cost-optimization]]
- [[latency-optimization]]
- [[observability]]
- [[agentic-rag]]
- [[vector-databases]]
