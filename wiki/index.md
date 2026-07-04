# Wiki Index

**Summary**: Table of contents for the Learn RAG wiki.

**Last updated**: 2026-07-04

---

## Core Concepts

- [[rag-overview]] — What RAG is, how AI systems have progressed, and common challenges
- [[rag-pipeline-architecture]] — The 12 core components of a production RAG system
- [[rag-types]] — 10+ RAG architecture patterns from Standard to Agentic, with tradeoffs
- [[agentic-rag]] — Active, adaptive RAG with 7 architecture variants (Router, Adaptive, Corrective, etc.)
- [[graph-based-rag]] — Stateful, branching pipelines; Graph RAG and Hybrid RAG architectures
- [[rag-vs-fine-tuning]] — When to choose RAG, fine-tuning, or a hybrid approach
- [[cag-and-mag]] — CAG (Cache-Augmented Generation) and MAG (Memory-Augmented Generation) paradigms

## Retrieval

- [[embeddings]] — How text becomes vectors, static vs contextual embeddings, solving semantic ambiguity
- [[vector-databases]] — Chroma, Pinecone, Milvus, Qdrant, Faiss, Weaviate compared
- [[vector-indexing]] — HNSW, IVF, PQ, and TurboQuant/TurboWek for training-free indexing
- [[hybrid-retrieval]] — Combining BM25 keyword search with semantic vector search
- [[reranking]] — Reordering retrieved results to push the most relevant to the top
- [[chunking-strategies]] — 15+ chunking types, early vs late chunking, and choosing the right technique

## Production

- [[production-scaling]] — Scaling RAG for real users: parallel processing, separation of concerns, auto-scaling
- [[rag-evaluation]] — Faithfulness, context relevance, RAGAS, LLM-as-judge, regression testing
- [[rag-failure-modes]] — 10 specific ways RAG systems fail and how to prevent each
- [[hallucination]] — Causes, detection, mitigation, and architectural solutions (Corrective/Self-Reflective RAG)
- [[observability]] — Span-level tracing, model drift detection, and governance
- [[latency-optimization]] — Root causes of latency and strategies to cut response time by 2-5x
- [[cost-optimization]] — Prompt caching, model routing, semantic caching, and team best practices

## Implementation

- [[langchain-rag]] — LangChain and LangGraph implementation reference for RAG pipelines
