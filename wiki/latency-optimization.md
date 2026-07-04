# Latency Optimization

**Summary**: RAG latency is a pipeline optimization problem, not just an LLM problem. Most delay comes from the entire pipeline — retrieval, context assembly, and generation — not just the model. Optimizing retrieval, reducing context size, caching, and using faster models can cut response time by 2-5x.

**Sources**: RAG Primer.docx

**Last updated**: 2026-07-04

---

## Root Causes of Latency

Why latency happens in RAG systems (source: RAG Primer.docx):

| Root Cause | Problem |
|-----------|---------|
| Huge Knowledge Base | Search Overhead |
| Slow Retrieval Pipeline | Retrieval Bottleneck |
| Heavy Embedding Model | Embedding Latency |
| Large LLM Inference | Inference Delay |
| Excessive Context | Token Explosion |
| Poor [[chunking-strategies\|Chunking]] Strategy | Irrelevant Retrieval |
| Sequential Tool Calls | Blocking Execution |
| Network/API Latency | External Delay |

## Quick Optimization Strategies

Six strategies for immediate improvement (source: RAG Primer.docx):

1. **Stream responses** — Show output as it is generated; feels fast instantly
2. **Cache results** — Store answers + [[embeddings]] (use Redis); repeat queries = instant
3. **Use smaller models** — Use fast models for simple tasks; do not overkill
4. **Send fewer chunks** — Top 3-5 chunks only; less input = faster
5. **Parallel retrieval** — Fetch from multiple sources at once; faster than one big query
6. **Add cache at database level** — Store simple questions, FAQs as primary lookup before hitting the main database

## Optimization Checklist

Full checklist for reducing latency (source: RAG Primer.docx):

| Optimization | Benefit |
|-------------|---------|
| Stream Responses | Perceived Speed |
| Cache Results | Faster Reuse |
| Use Smaller Models | Fast Inference |
| Send Fewer Chunks | Reduced Tokens |
| Parallel Retrieval | Concurrent Fetching |
| Better Chunking | Efficient Retrieval |
| ANN Vector Search | Fast Search |
| Quantization | Model Compression |
| Async Execution | Non-Blocking Calls |
| Context Compression | Prompt Reduction |

## Diagnosing a Slow RAG Chatbot

If a RAG chatbot takes ~15 seconds for a simple query, the delay is usually caused by (source: RAG Primer.docx):
- Oversized chunks
- Too many retrieved documents
- [[hybrid-retrieval|Hybrid search]] overhead
- [[Reranking]] overhead
- Irrelevant context forcing the LLM to process more than needed

### Fixes
- Reduce chunk size (if accuracy holds)
- Retrieve only the top few relevant chunks
- Avoid unnecessary hybrid/reranking steps
- **Profile each stage** (embedding, retrieval, reranking, generation) to find the real bottleneck

## Profiling Checklist

Things to check for latency issues (source: RAG Primer.docx):
1. Chunk size / overlap size, lesser top-k values
2. Which retrieval mechanism is used — semantic / keyword / hybrid — and which gives quicker results
3. Changing the model if it gets answers quicker
4. Vector-based search for unstructured documents vs page-index-based search for structured documents

## Two-Stage Pipeline

A two-stage pipeline is a high-leverage pattern for both latency and [[cost-optimization|cost]] (source: RAG Primer.docx):
1. Cheap BM25 or ANN retrieval pass narrows the candidate set
2. Lightweight cross-encoder re-ranks before anything reaches the frontier LLM

Pair with a score threshold (e.g., cosine >= 0.75) to cut out semantically weak chunks entirely.

## Related Pages

- [[cost-optimization]]
- [[rag-pipeline-architecture]]
- [[hybrid-retrieval]]
- [[reranking]]
- [[observability]]
