# Hybrid Retrieval

**Summary**: Hybrid retrieval combines keyword-based search (BM25) with semantic vector search to achieve both lexical precision and semantic understanding. It is the baseline for high-stakes RAG systems, especially in domains like finance where missing exact terms can be costly.

**Sources**: RAG Primer.docx

**Last updated**: 2026-07-04

---

## Why Hybrid?

Semantic search is great for understanding intent and contextual similarity, but it can miss exact matches. Keyword search (BM25) preserves lexical accuracy but struggles with conceptual queries. Hybrid retrieval balances both (source: RAG Primer.docx).

In enterprise RAG systems, semantic-only retrieval misses exact references, while BM25-only retrieval struggles with conceptual queries. Hybrid retrieval balances both and usually improves recall and grounding quality significantly (source: RAG Primer.docx).

## When BM25 Matters

BM25 becomes critical when queries contain (source: RAG Primer.docx):
- Exact identifiers or specific terms
- Error codes (e.g., "What does error code 429 mean?")
- Clause references (e.g., "What is clause 6A in this document?")
- API names, version numbers, log signatures, product codes

Semantic [[embeddings]] may not prioritize these exact tokens properly, but BM25 handles them well (source: RAG Primer.docx).

## Query-Aware Weighting

Rather than using fixed weights between semantic and keyword retrieval, make it query-aware (source: RAG Primer.docx):

- **Keyword-heavy queries** (numbers, abbreviations, exact phrases) — Increase BM25 contribution
- **Intent-driven queries** (broader, conceptual) — Increase semantic retrieval weight

The final score is dynamically adjusted instead of being fixed. Most teams skip this and then wonder why their RAG feels inconsistent in production (source: RAG Primer.docx).

## Combining Results

The process for merging results from both retrieval systems (source: RAG Primer.docx):

1. **Normalize scores** — BM25 and vector similarity operate on different scales
2. **Merge and deduplicate** candidates
3. **Re-rank** using a cross-encoder or LLM re-ranker to determine final ordering (see [[reranking]])

## Latency Considerations

Both retrievals happen in parallel, so total retrieval time equals the slower retriever rather than the sum of both. Example: if vector search takes 120ms and BM25 takes 80ms, retrieval finishes in roughly 120ms plus a small [[reranking]] overhead (source: RAG Primer.docx).

## Similarity Score Thresholds

The similarity score threshold matters just as much as the retrieval method. A poorly tuned threshold floods the re-ranker with noise regardless of which retriever is used (source: RAG Primer.docx).

Example threshold: cosine >= 0.75 to cut out semantically weak chunks entirely (source: RAG Primer.docx).

## Financial RAG Example

For financial PDFs where missing a single number can cost millions (source: RAG Primer.docx):
- Combine BM25 (keyword) + semantic search for exact numbers + contextual meaning
- Merge results using RRF (Reciprocal Rank Fusion)
- Add a re-ranker (e.g., Cohere Rerank) to push the most relevant chunk to the top
- Use layout-aware [[chunking-strategies|chunking]] (tables intact) and metadata filtering (company, quarter, doc type)
- Apply multi-query expansion to improve recall
- Always cite sources for every number

In finance, retrieval is risk management — hybrid search + [[reranking]] is the minimum bar (source: RAG Primer.docx).

## Related Pages

- [[reranking]]
- [[embeddings]]
- [[vector-databases]]
- [[rag-pipeline-architecture]]
- [[latency-optimization]]
