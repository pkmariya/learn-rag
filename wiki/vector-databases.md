# Vector Databases

**Summary**: Vector databases store embeddings and enable fast similarity search for RAG retrieval. The choice of vector store affects retrieval speed, accuracy, memory usage, query cost, and even how you chunk data and write prompts.

**Sources**: RAG Primer.docx

**Last updated**: 2026-07-04

---

## Why the Choice Matters

Vector databases are not interchangeable. Your vector store quietly decides (source: RAG Primer.docx):
- How fast retrieval feels
- How accurate responses stay
- How much memory you burn
- How expensive every query becomes
- How you chunk data
- How you even write prompts

In real systems, retrieval is the architecture (source: RAG Primer.docx).

## Vector Database Comparison

### Chroma — Fast to Start
- Lightweight and local-first
- Simple HNSW-based indexing
- Tight embedding integrations
- **Use when**: prototyping, notebooks, or small applications (source: RAG Primer.docx)

### Pinecone — The Managed Default
- No infrastructure to run
- Real-time updates and metadata filtering
- Production-grade availability
- **Use when**: you want reliability at scale without owning ops (source: RAG Primer.docx)

### Milvus — Built for Volume
- Distributed and GPU-accelerated
- Multiple indexing strategies (IVF, PQ, HNSW)
- Designed for billions of vectors
- **Use when**: throughput and scale dominate everything else (source: RAG Primer.docx)

### Qdrant — Filters Matter
- Rust-based and performance-focused
- Optimized HNSW with quantization
- Strong payload + conditional search
- **Use when**: retrieval has strict constraints and real-time needs (source: RAG Primer.docx)

### Faiss — The Engine Under Many Systems
- Ultra-fast similarity search
- CPU and GPU support
- Complete control, zero abstraction
- **Use when**: building custom pipelines or benchmarking retrieval (source: RAG Primer.docx)

### Weaviate — Semantic-First by Design
- Open-source and multimodal
- HNSW indexing with built-in vectorizers
- Keyword + vector [[hybrid-retrieval|hybrid search]]
- **Use when**: search spans text, images, and structured metadata (source: RAG Primer.docx)

## Indexing Strategies

Common ANN (Approximate Nearest Neighbor) algorithms used in vector databases (source: RAG Primer.docx):
- **HNSW** (Hierarchical Navigable Small World) — Used by Chroma, Qdrant, Weaviate
- **IVF** (Inverted File Index) — Used by Milvus, Faiss
- **PQ** (Product Quantization) — Used by Milvus for compression

## Related Pages

- [[embeddings]]
- [[hybrid-retrieval]]
- [[rag-pipeline-architecture]]
- [[latency-optimization]]
