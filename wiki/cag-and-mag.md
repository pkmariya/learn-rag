# CAG and MAG

**Summary**: CAG (Cache-Augmented Generation) and MAG (Memory-Augmented Generation) are alternative augmentation paradigms alongside RAG. CAG eliminates retrieval latency by preloading all knowledge into the context window. MAG adds persistent, evolving memory across sessions for personalization.

**Sources**: RAG Vs CAG Vs MAG.pdf

**Last updated**: 2026-07-04

---

## The Core Problem

LLMs are powerful but frozen — they know nothing beyond their training cutoff and nothing about your business. A user asking "What's the current pricing for the Pro plan?" gets an answer from 18-month-old training data. Three paradigms address this differently (source: RAG Vs CAG Vs MAG.pdf).

## CAG (Cache-Augmented Generation)

Preloads all knowledge into the LLM's context window at startup, precomputes KV (key-value) cache states, then answers queries without any retrieval step (source: RAG Vs CAG Vs MAG.pdf).

**How it works**:
1. **Load Docs (startup)** — Load all documents into LLM context window
2. **Precompute KV Cache** — Save attention states to memory (done once)
3. **Query Time (fast path)** — Append query to cache, generate answer (no retrieval)

**Strengths** (source: RAG Vs CAG Vs MAG.pdf):
- Reduced latency (eliminates real-time retrieval)
- No chunking errors (full documents in context)
- Enhanced multi-hop reasoning (all info processed upfront)
- Simpler architecture (no embedding pipeline, no vector DB)

**Weaknesses** (source: RAG Vs CAG Vs MAG.pdf):
- Limited by context window size for large datasets
- Stale cache problem (requires full rebuild when knowledge changes)
- Initial overhead to precompute KV cache
- Not multi-tenant (one shared context)

**When to use**: Stable, bounded knowledge bases that fit in the context window. Example: HR policy chatbot with 80 stable docs totaling 200K tokens (source: RAG Vs CAG Vs MAG.pdf).

**Frameworks**: vLLM, HF Transformers, Anthropic prompt caching (source: RAG Vs CAG Vs MAG.pdf).

## MAG (Memory-Augmented Generation)

Adds dynamic, evolving memory that persists, updates, and improves across sessions — giving the system continuity and personalization (source: RAG Vs CAG Vs MAG.pdf).

**How it works**:
1. **Current Session** — Working memory + episodic/semantic memory retrieval
2. **Memory Update & Consolidation** — Important facts/preferences written back to memory store
3. **Next Session Continuity** — Memory retrieved for same user, providing full continuity

**Strengths** (source: RAG Vs CAG Vs MAG.pdf):
- True continuity (remembers preferences, decisions, history)
- Self-improving (gets richer the more the system is used)
- Personalization at scale (each user has their own evolving memory layer)
- Combines multiple memory types (episodic, semantic, procedural)

**Weaknesses** (source: RAG Vs CAG Vs MAG.pdf):
- Memory staleness (old memories can contradict new facts)
- Privacy risk (stores contain sensitive personal information)
- Write strategy complexity (deciding what to remember/forget is non-trivial)
- Highest infrastructure complexity of the three paradigms

**When to use**: Long-running agents, personal assistants, multi-session systems where users return. Example: Executive assistant AI used daily that remembers goals, preferences, and decisions (source: RAG Vs CAG Vs MAG.pdf).

**Frameworks**: Mem0, Zep, MemGPT, LangGraph (source: RAG Vs CAG Vs MAG.pdf).

## Decision Framework

| Factor | RAG | CAG | MAG |
|---|---|---|---|
| Corpus size | Any (scales to millions) | Must fit in context window | Any |
| Change frequency | Daily updates OK | Stable for months | Evolves with user |
| Multi-session | No (stateless) | No (stateless) | Yes (persistent memory) |
| Latency priority | Medium | Lowest | Medium |
| Always-fresh info | Yes | No (stale cache risk) | Partial |
| Personalization | No | No | Yes |
| Infrastructure complexity | Medium | Low | Highest |

(source: RAG Vs CAG Vs MAG.pdf)

## Scenario-Based Selection

- **Telecom support bot** (10M customers, 500 product docs updating weekly) -> **RAG**. Corpus too large for CAG, queries vary widely (source: RAG Vs CAG Vs MAG.pdf).
- **HR policy chatbot** (80 stable policy docs, 200K tokens) -> **CAG**. Docs fit in context, policies don't change daily (source: RAG Vs CAG Vs MAG.pdf).
- **Executive assistant** (personal AI used daily) -> **MAG**. Needs to remember goals, preferences, decisions, style (source: RAG Vs CAG Vs MAG.pdf).

## Hybrid Approach

High-performance systems can combine paradigms: CAG for core identity/stable knowledge + RAG for long-tail search over large, changing corpora (source: RAG Vs CAG Vs MAG.pdf).

## Related Pages

- [[rag-overview]]
- [[rag-vs-fine-tuning]]
- [[rag-types]]
- [[cost-optimization]]
- [[latency-optimization]]
