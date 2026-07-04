# Cost Optimization

**Summary**: Minimizing LLM and token cost requires optimization across every layer: data, orchestration, generation, and application. The most impactful strategies include prompt caching, model routing, semantic response caching, and structured outputs.

**Sources**: RAG Primer.docx, RAG Vs Fine-Tuning.pdf, RAG architecture.txt, RAG Vs CAG Vs MAG.pdf

**Last updated**: 2026-07-04

---

## Cost Optimization by Layer

### Data Layer

**Prompt Design** (source: RAG Primer.docx):
- Compress system prompts — tighten/minimize the wording
- Remove stop-words, duplicates, adjectives
- Use structure, not prose (JSON, markdown)
- Use prompt caching for repeated, generic prompts
- Use local DB for greetings and deterministic responses
- Start with zero-shot prompts; add examples only when accuracy drops

**[[Chunking Strategies]]** (source: RAG Primer.docx):
- Document-based chunking vs semantic chunking
- Reduce top-k to send fewer chunks

**Caching Strategies** (source: RAG Primer.docx):
- **Prompt caching** — Cache static system prompts and docs. Cached input tokens cost up to 90% less.
- **Semantic response caching** — Store past LLM answers as vectors and serve them for near-duplicate incoming queries. This is the most powerful lever when query distribution has meaningful repetition.
- **Embedding cache** — Persist chunk [[embeddings]]; avoid re-embedding unchanged documents.

### Orchestration Layer

- **Homogeneous embedding and LLM models** — Reduce complexity (source: RAG Primer.docx)
- **Two-stage pipeline** — Cheap BM25 or ANN retrieval narrows candidates, then lightweight cross-encoder re-ranks before reaching the frontier LLM. See [[latency-optimization]].
- **Model re-routing / model harnessing** — Use appropriate models (foundational vs frontier) for respective tasks based on complexity (source: RAG Primer.docx)

### Generation Layer

- **Constrain output** — Use structured output (JSON, markdown) (source: RAG Primer.docx)
- **Set output response length limits** (source: RAG Primer.docx)
- **Forbid preamble** — Do not restate the question, do not add commentary (source: RAG Primer.docx)
- **Compress agent memory** — Summarize completed steps; do not pass full history every turn (source: RAG Primer.docx)
- **Self-hosting** open-source models for high-volume or data-sensitive paths removes per-call API spend entirely (source: RAG Primer.docx)

### Application Layer

- **TOON (Token-Oriented Object Notation)** — Format for input and output token optimization (source: RAG Primer.docx)

## Team Best Practices

Recommended practices for all projects (source: RAG Primer.docx):

1. **Hybrid Architecture** — Use deterministic logic for structured tasks; reserve LLMs for reasoning and generation
2. **Primary and Fallback LLM** — Define a provider chain (e.g., Anthropic -> OpenAI) with automatic failover
3. **Concept Engineering over Prompt Engineering** — Structure data, context, and instructions at the architecture level rather than crafting long, fragile prompts
4. **Prompt Caching** — Up to 90% cost reduction on repeated system prompts
5. **Batch API** — 50% cost reduction for non-real-time workloads (bulk generation, offline summarization)
6. **Reserve Paid APIs for Production** — Use open-source models during development and unit testing
7. **Avoid Redundant Context** — Only include strictly necessary context; pre-process and summarize
8. **Log Everything** — Provider, model, input tokens, output tokens, cache status per request

## Speculative Decoding

Combining the strengths of small and large LLM models: use a small LLM for inferencing and a large LLM for verification. This reduces cost while maintaining quality (source: RAG Primer.docx).

## RAG vs Fine-Tuning Cost Comparison

The choice between RAG and fine-tuning has significant cost implications (source: RAG Vs Fine-Tuning.pdf):

| Approach | Typical Cost | When Cost-Effective |
|---|---|---|
| RAG | ~$300/month | Frequently changing information, multiple domains |
| Fine-tuning | ~$15-25K upfront | Stable domain knowledge, specific style/behavior |
| Hybrid | Highest combined | Complex requirements justifying both investments |

See [[rag-vs-fine-tuning]] for the full decision framework.

## CAG as a Cost Alternative

For small, stable knowledge bases that fit in the context window, [[cag-and-mag|CAG (Cache-Augmented Generation)]] eliminates the entire embedding pipeline, vector DB, and retrieval infrastructure — replacing it with a one-time KV cache precomputation. Simpler architecture = lower infrastructure cost (source: RAG Vs CAG Vs MAG.pdf).

## Zero-Cost Queries via Semantic Caching

If two users ask the same question in different words, recognize it's the same intent and serve a cached answer. Zero GPU cost for repeat queries. This is particularly impactful when query distribution has meaningful repetition (source: RAG architecture.txt).

## Related Pages

- [[latency-optimization]]
- [[rag-pipeline-architecture]]
- [[chunking-strategies]]
- [[embeddings]]
- [[hybrid-retrieval]]
- [[rag-vs-fine-tuning]]
- [[cag-and-mag]]
- [[production-scaling]]
