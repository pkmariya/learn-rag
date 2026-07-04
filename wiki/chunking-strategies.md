# Chunking Strategies

**Summary**: Chunking is how documents are split into smaller pieces for embedding and retrieval. The choice of chunking strategy is one of the most common failure points in RAG systems, and there is no single "best" strategy — only the right one for your data and query type.

**Sources**: RAG Primer.docx, RAG Chunking Techniques.pdf, Chunking Types.pdf, RAG with Langchain.pdf

**Last updated**: 2026-07-04

---

## Why Chunking Matters

Most RAG systems fail not because of the LLM, but because of bad chunking. If retrieval feels random, hallucinated, or incomplete, the chunking strategy is often the real bottleneck (source: RAG Primer.docx).

### The Fixed-Size Chunking Problem

With fixed-size chunking, related information can be split across chunks and never retrieved together. Example: a query about "side effects of medication X when combined with Y" fails because medication X details end up in Chunk 1 and interaction details in Chunk 2 (source: RAG Primer.docx).

The solution is to implement context-aware chunking based on semantic boundaries with domain-specific entity preservation (source: RAG Primer.docx).

## 10 Chunking Types

Every RAG builder should know these 10 types (source: RAG Primer.docx):

| # | Type | Description |
|---|------|-------------|
| 1 | **Fixed-Size Chunking** | Simple token splits. Fast, but often breaks meaning. |
| 2 | **Overlapping Chunking** | Adds context continuity across boundaries. A strong baseline. |
| 3 | **Sentence-Based Chunking** | Keeps semantic coherence. Better retrieval quality than raw tokens. |
| 4 | **Paragraph-Based Chunking** | Great for blogs, reports, and structured text. |
| 5 | **Semantic Chunking** | Splits on meaning shifts using embeddings. High quality, higher compute. |
| 6 | **Recursive Chunking** | Section -> subsection -> paragraph. Perfect for nested documents. |
| 7 | **Section-Based Chunking** | Uses headings and clauses. Excellent for PDFs, RFPs, policies. |
| 8 | **Sliding Window Chunking** | Guarantees zero information loss in long documents. |
| 9 | **Hierarchical Chunking** | Store summaries + detailed chunks together. Best for multi-level retrieval. |
| 10 | **Metadata-Aware Chunking** | Titles, sections, sources = smarter filtering + [[reranking]]. |

## Early Chunking vs Late Chunking

Most RAG systems use **early chunking** (source: RAG Primer.docx):
1. Cut a long document into chunks
2. Embed each chunk in isolation
3. Retrieve the best-matching chunk

The problem: when you cut first, each chunk forgets what is happening in the rest of the document. This causes failures on long policies, specs, or research-style writing.

**Late chunking** flips the order (source: RAG Primer.docx):
1. Embed the entire document at the token level (using a long-context model)
2. Apply chunk boundaries on top of those token embeddings
3. Build each chunk's final embedding by pooling the tokens inside it

In other words:
- **Early chunking** = read a paragraph, forget the rest
- **Late chunking** = read the whole page, then summarize each section with that context in mind

### Benefits of Late Chunking

- Chunks "remember" surrounding context, leading to better retrieval on long, relationship-heavy docs
- Fewer broken references ("it", "they", "the above section") because the model saw the full picture
- Still produces short, clean chunks for retrieval, but vectors are richer and more coherent

### When to Consider Late Chunking

- Failures are clearly cross-context (answer depends on multiple sections)
- Already using long-context embedding models
- Treating chunking as an engineering lever, not just a pre-processing detail

## Additional Chunking Techniques

Beyond the core 10, several additional techniques are worth considering:

### Query-Aware Chunking

Creates chunks optimized for expected questions. Analyzes typical user queries, identifies question patterns, and chunks content to align with expected queries. Best for known use cases (FAQ, customer support) with repetitive query patterns. Avoid for open-ended exploration (source: RAG Chunking Techniques.pdf).

### LLM-Based Chunking

Uses an LLM to intelligently identify logical breakpoints in documents. The LLM analyzes content structure and semantics, generating chunks with natural boundaries. Can include summaries or key points per chunk. Best for complex, unstructured documents. Avoid for large-scale processing (expensive and slow) (source: RAG Chunking Techniques.pdf).

### Agentic Chunking

An AI agent analyzes each document's type and structure, selects the best chunking strategy (or combines multiple), and adjusts strategy based on retrieval performance feedback. Best for diverse document types and advanced RAG pipelines. Overkill for simple use cases (source: RAG Chunking Techniques.pdf).

### Context-Enriched Chunking

Combines surrounding sentences with each chunk to add context. Uses a sliding window (e.g., window_size=2) to include neighboring sentences. Helps preserve context that would otherwise be lost at chunk boundaries (source: Chunking Types.pdf).

### Advanced Semantic Chunking (Clustering)

Uses SentenceTransformer embeddings + KMeans clustering to group semantically similar sentences into chunks, regardless of their position in the document. Results in topically coherent chunks even from unstructured text (source: Chunking Types.pdf).

## Choosing the Right Technique

Start simple, then upgrade based on results (source: RAG Chunking Techniques.pdf):

1. **Start** — Begin with Fixed-Size or Recursive chunking. Test with actual queries, measure retrieval accuracy.
2. **Upgrade when needed**:
   - Poor retrieval -> Try Semantic chunking
   - Need filtering -> Add Metadata-aware
   - Specific queries -> Use Query-aware
   - Complex docs -> Consider LLM-based
3. **Combine techniques**:
   - Recursive + Metadata = structured + searchable
   - Semantic + Query-aware = precise retrieval
   - Document-based + Metadata = organized knowledge base

## Recommended Starting Parameters

From RAG with Langchain.pdf:
- **chunk_size**: 200-1000 characters (300 is optimal starting point)
- **chunk_overlap**: 10-20% of chunk_size (50-100 characters)
- **separators**: `["\n\n", "\n", ".", " "]` (paragraph -> sentence -> word)

## Chunking and Cost

Chunk size and overlap directly affect (source: RAG Primer.docx):
- Recall vs precision tradeoffs
- Token consumption and [[cost-optimization|cost]]
- [[latency-optimization|Latency]] through the pipeline

## Related Pages

- [[rag-pipeline-architecture]]
- [[embeddings]]
- [[hybrid-retrieval]]
- [[latency-optimization]]
- [[cost-optimization]]
- [[rag-failure-modes]]
- [[langchain-rag]]
