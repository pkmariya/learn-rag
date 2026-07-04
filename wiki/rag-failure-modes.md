# RAG Failure Modes

**Summary**: RAG systems can fail in at least 10 distinct ways, from wrong data retrieval to context overflow. Understanding these failure modes is essential for building robust systems and choosing the right [[rag-types|RAG architecture]].

**Sources**: RAG failure situations.pdf, RAG Vs CAG Vs MAG.pdf, RAG Cheatsheet.pdf

**Last updated**: 2026-07-04

---

## The Two Failure Points

RAG = Retrieval + Generation. If either step fails, the output is wrong (source: RAG failure situations.pdf).

## 10 RAG Failure Cases

### 1. Wrong Data Retrieved

The retriever returns semantically similar but factually irrelevant documents. Searching "Lion diet" returns results for "Lionel Messi diet" (source: RAG failure situations.pdf).

If correct retrieval probability R = 0.7, then 30% of answers may fail due to bad data.

**Mitigation**: Better [[embeddings]], [[reranking]], query reformulation.

### 2. Incomplete Information

The knowledge base has only partial coverage. Asking "What causes rain?" retrieves only "clouds hold water" but misses "water vapor condenses and falls" (source: RAG failure situations.pdf).

If dataset has only 60% coverage, expected accuracy drops to ~60%.

**Mitigation**: Audit knowledge base coverage, use [[hybrid-retrieval]] to cast a wider net.

### 3. Poor Question Understanding

The system misinterprets ambiguous or vague queries. "Why do planes fly higher than birds?" is misunderstood as "difference between birds and planes" (source: RAG failure situations.pdf).

**Mitigation**: Query reformulation, HyDE (see [[rag-types]]), clarification prompts.

### 4. Failure to Connect Facts (Multi-hop Reasoning)

The retriever finds all relevant pieces but the LLM can't join them logically. To answer "Why does ice float?" requires connecting: (A) ice is less dense than water, and (B) lower density causes floating (source: RAG failure situations.pdf).

If both facts are retrieved (probability 0.9) but connection fails (probability 0.7), total success = 0.9 x 0.7 = 63%.

**Mitigation**: [[agentic-rag]] with reasoning chains, Adaptive RAG, better prompt engineering. Multi-hop reasoning is one of RAG's hardest challenges (source: RAG Vs CAG Vs MAG.pdf).

### 5. Outdated Knowledge

The knowledge base contains stale information. Asking "Who is India's current president?" returns the wrong name if data is from 2020 (source: RAG failure situations.pdf).

**Mitigation**: Regular knowledge base updates, timestamp-aware retrieval, metadata filtering. This is where RAG has an advantage over fine-tuning — documents can be updated without retraining (source: RAG Vs CAG Vs MAG.pdf).

### 6. Domain Mismatch

The system is trained on medical data but receives cricket questions. It may hallucinate rather than admit ignorance (source: RAG failure situations.pdf).

**Mitigation**: Domain detection, "I don't know" responses (see [[hallucination]]), query routing to appropriate knowledge sources.

### 7. Poor Chunking or Embedding Quality

Chunks that are too large contain mostly irrelevant text. Chunks too small lose context. If each chunk has only 10% relevant info, retrieval accuracy drops to ~10% (source: RAG failure situations.pdf).

**Mitigation**: Optimize [[chunking-strategies]], test different chunk sizes (start with 300-500 characters), use chunk overlap.

### 8. Low Vector Similarity

The cosine similarity between query vector and document vector is too low for meaningful retrieval. "Capital of USA" and "Washington D.C. is a city" may have low similarity if not phrased properly (source: RAG failure situations.pdf).

Similarity = cos(theta). At 90 degrees = 0 (no match), at 0 degrees = 1 (perfect match).

**Mitigation**: Better [[embeddings]] models, query expansion, HyDE (see [[rag-types]]).

### 9. Context Window Overflow

LLMs can only process a limited number of tokens. If retrieved data exceeds the context window, older information is lost (source: RAG failure situations.pdf).

**Mitigation**: [[chunking-strategies]] to control context size, reduce top-k, use summarization of retrieved chunks (see [[latency-optimization]]).

### 10. Storage or Indexing Errors

Files not saved or indexed properly cause the retriever to return nothing or wrong data. Like saving homework in "Downloads" but searching in "Documents" (source: RAG failure situations.pdf).

**Mitigation**: Automated ingestion pipelines, index validation, [[observability]] to monitor retrieval health.

## Prevention Checklist

From RAG failure situations.pdf:
- Keep knowledge base updated regularly
- Clean and organize data before indexing
- Encourage clear, specific questions
- Use balanced chunking (not too large, not too small)
- Monitor retrieval accuracy with quantitative metrics

## Cascading Failures

Retrieval failures cascade: wrong chunk = wrong answer. A single bad retrieval can undermine an otherwise correct generation pipeline (source: RAG Vs CAG Vs MAG.pdf).

Corrective RAG and Self-Reflective RAG (see [[rag-types]]) are specifically designed to detect and recover from these failures.

## Related Pages

- [[rag-types]]
- [[hallucination]]
- [[chunking-strategies]]
- [[embeddings]]
- [[rag-evaluation]]
- [[observability]]
