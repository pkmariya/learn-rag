# Reranking

**Summary**: Reranking is the process of reordering retrieved documents to push the most relevant results to the top. It bridges the gap between initial retrieval and final context assembly, removing noise before it reaches the LLM.

**Sources**: RAG Primer.docx

**Last updated**: 2026-07-04

---

## Why Reranking?

Raw retrieval results are not enough. Initial retrieval (whether keyword, semantic, or hybrid) returns candidates that are related to the query but not necessarily the most relevant. Reranking ensures only the most relevant context reaches the LLM (source: RAG Primer.docx).

Retrieval quality matters more than model size — and reranking is a key lever for improving that quality (source: RAG Primer.docx).

## How Reranking Works

After initial retrieval returns candidates, a reranker scores each candidate more carefully against the query (source: RAG Primer.docx):

1. Initial retrieval returns top-k candidates
2. A cross-encoder or LLM-based reranker evaluates each candidate against the query
3. Results are reordered by relevance score
4. Only the top results proceed to context assembly

## Reranking Methods

Methods mentioned in the source (source: RAG Primer.docx):
- **Cross-encoder rerankers** — Score query-document pairs together for higher accuracy
- **LLM rerankers** — Use an LLM to judge relevance
- **Cohere Rerank** — A specific reranking service, recommended for financial RAG

## Reciprocal Rank Fusion (RRF)

When combining results from multiple retrieval systems (e.g., [[hybrid-retrieval]]), RRF merges ranked lists by computing a combined score based on each result's rank across the different systems (source: RAG Primer.docx).

## Latency vs Accuracy Tradeoff

Reranking adds a processing step, which increases latency. However (source: RAG Primer.docx):
- The overhead is typically small compared to LLM generation time
- It reduces the amount of irrelevant context sent to the LLM, which can actually reduce generation latency
- For high-stakes applications (finance, legal), the accuracy gain justifies the cost

Unnecessary reranking should be avoided when [[latency-optimization|latency]] is the primary concern and retrieval quality is already sufficient (source: RAG Primer.docx).

## Related Pages

- [[hybrid-retrieval]]
- [[rag-pipeline-architecture]]
- [[latency-optimization]]
- [[rag-evaluation]]
