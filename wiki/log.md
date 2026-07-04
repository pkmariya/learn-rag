# Wiki Log

Append-only record of all wiki operations.

---

## 2026-07-04 — Initial ingest of RAG Primer.docx

**Source**: RAG Primer.docx

**Pages created** (14 pages):
- `rag-overview.md` — Main RAG overview and AI system progression
- `rag-pipeline-architecture.md` — 12 core components of production RAG
- `chunking-strategies.md` — 10 chunking types, early vs late chunking
- `embeddings.md` — Static vs contextual embeddings, polysemy, NLP pipeline
- `vector-databases.md` — Chroma, Pinecone, Milvus, Qdrant, Faiss, Weaviate
- `hybrid-retrieval.md` — BM25 + semantic search, query-aware weighting, RRF
- `reranking.md` — Cross-encoder reranking, RRF, latency tradeoffs
- `agentic-rag.md` — Traditional vs agentic RAG, memory, reasoning, multi-agent
- `graph-based-rag.md` — Stateful pipelines, branching, LangGraph
- `observability.md` — Five spans, model drift detection, governance
- `rag-evaluation.md` — RAGAS, faithfulness, LLM-as-judge, regression testing
- `hallucination.md` — Causes, detection, mitigation techniques
- `latency-optimization.md` — Root causes, optimization checklist, profiling
- `cost-optimization.md` — Prompt caching, model routing, team best practices

**Pages updated**:
- `index.md` — Created with full table of contents

---

## 2026-07-04 — Ingest of 13 new sources

**Sources** (13 files):
- Agentic_RAG_Architecture_1741260286.pdf
- RAG Vs Fine-Tuning.pdf
- RAG Architectures.pdf (image-based, limited text extraction)
- RAG Cheatsheet.pdf
- RAG Types.pdf
- RAG Bundle.pdf
- RAG Chunking Techniques.pdf
- Chunking Types.pdf
- RAG failure situations.pdf
- RAG with Langchain.pdf
- RAG Vs CAG Vs MAG.pdf
- RAG architecture.txt
- vector index.txt

**Pages created** (7 pages):
- `rag-types.md` — 10+ RAG architecture patterns (Standard, Corrective, Speculative, Fusion, Self-RAG, HyDE, Adaptive, etc.)
- `rag-vs-fine-tuning.md` — RAG vs fine-tuning comparison, hybrid approach, cost analysis
- `cag-and-mag.md` — CAG (Cache-Augmented Generation) and MAG (Memory-Augmented Generation) paradigms
- `rag-failure-modes.md` — 10 specific RAG failure cases and prevention strategies
- `vector-indexing.md` — HNSW, IVF, PQ index types and TurboQuant training-free indexing
- `production-scaling.md` — Scaling RAG for real users: parallel processing, LLM separation, semantic caching, IaC
- `langchain-rag.md` — LangChain and LangGraph implementation reference

**Pages updated** (6 pages):
- `agentic-rag.md` — Added 7 agentic RAG architecture subtypes, key features from Agentic_RAG_Architecture PDF
- `chunking-strategies.md` — Added query-aware, LLM-based, agentic, context-enriched, and clustering-based chunking; recommended starting parameters
- `graph-based-rag.md` — Added Graph RAG and Hybrid RAG architecture details from RAG Types PDF
- `hallucination.md` — Added architectural solutions (Corrective RAG, Self-Reflective RAG, Adaptive RAG)
- `rag-pipeline-architecture.md` — Added production scaling reference and common challenges table
- `cost-optimization.md` — Added RAG vs fine-tuning cost comparison, CAG alternative, semantic caching detail
- `index.md` — Reorganized with new sections (Implementation), added all 7 new pages
