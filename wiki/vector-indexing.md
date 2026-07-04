# Vector Indexing

**Summary**: Vector indexes are the data structures that make similarity search fast over large embedding collections. The dominant index type today is FAISS/IVF, which requires training on your data before use. TurboQuant, a Google research breakthrough, eliminates this requirement through random rotation of vectors.

**Sources**: vector index.txt, RAG Primer.docx

**Last updated**: 2026-07-04

---

## Why Vector Indexes Matter

Raw brute-force similarity search over millions of vectors is too slow for production. Vector indexes trade small accuracy losses for dramatic speed gains. The choice of index directly impacts retrieval latency, memory usage, and whether the index needs rebuilding as data changes (source: RAG Primer.docx).

See [[vector-databases]] for database-level comparisons (Chroma, Pinecone, etc.). This page focuses on the underlying index algorithms.

## Common Index Types

From RAG Primer.docx:

| Index Type | Approach | Pros | Cons |
|---|---|---|---|
| **HNSW** (Hierarchical Navigable Small World) | Graph-based proximity navigation | Fast queries, good recall | High memory usage |
| **IVF** (Inverted File Index) | Cluster-based partitioning | Scalable, lower memory | Requires training on data |
| **PQ** (Product Quantization) | Vector compression | Very low memory | Lower accuracy |
| **FAISS** | Facebook's IVF+PQ implementation | Industry standard, GPU support | Needs training step |

## The FAISS Training Problem

FAISS (and IVF-based indexes generally) cannot search anything until they study your data first (source: vector index.txt):

1. Sample your documents
2. Group them into clusters
3. Build a lookup structure from clusters
4. Only then can you start searching

If your data grows or shifts significantly, you may need to redo the entire process (source: vector index.txt).

## TurboQuant: Training-Free Indexing

Google Research published TurboQuant, which discovered that applying a random rotation to document vectors before compressing them makes their statistical distribution predictable. The math can figure out the shape of your data without ever seeing it (source: vector index.txt).

### How TurboQuant/TurboWek Works

- **Random rotation** makes vector distributions predictable regardless of the actual data
- **No training required** — add a document and it gets indexed immediately
- **No rebuild needed** — corpus can grow or shift without rebuilding the index
- **Aggressive compression** — 10 million document embeddings go from 31GB down to 4GB (source: vector index.txt)

### Implementation

TurboWek (the implementation of TurboQuant) is built in Rust with Python wrappers already available for LangChain, LlamaIndex, and Haystack (source: vector index.txt).

## Index Selection Guidelines

| Scenario | Recommended Index | Reason |
|---|---|---|
| Prototype / small data (<100K docs) | Flat (brute force) | Simple, exact results |
| Medium scale, high recall needed | HNSW | Best accuracy-speed tradeoff |
| Large scale, memory constrained | IVF+PQ (FAISS) | Proven, scalable |
| Rapidly growing/changing corpus | TurboQuant/TurboWek | No rebuild needed |
| Very large scale + low memory | TurboQuant | 8x compression ratio |

## Related Pages

- [[vector-databases]]
- [[embeddings]]
- [[latency-optimization]]
- [[rag-pipeline-architecture]]
