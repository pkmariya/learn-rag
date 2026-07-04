# RAG Pipeline Architecture

**Summary**: A production RAG system consists of 12 core components spanning data ingestion, retrieval, generation, and evaluation. Each stage influences the final answer quality.

**Sources**: RAG Primer.docx, RAG architecture.txt, RAG Cheatsheet.pdf

**Last updated**: 2026-07-04

---

## The 12 Core Components

Every production RAG system includes these components (source: RAG Primer.docx):

1. **Document Ingestion** — How knowledge enters the system (PDFs, text files, web pages, CSVs, APIs, databases)
2. **Data Pre-processing** — Cleaning noise, headers, footers, formatting. Quality here directly affects retrieval accuracy.
3. **Chunking Strategy** — Deciding how knowledge is split. Chunk size and overlap decide recall vs precision. See [[chunking-strategies]].
4. **Embedding Generation** — Turning meaning into vectors. Model choice impacts speed, cost, and semantic quality. See [[embeddings]].
5. **Vector Database** — Storing embeddings for fast similarity search. See [[vector-databases]].
6. **Retriever** — Finding relevant information. Similarity vs MMR changes diversity of results. See [[hybrid-retrieval]].
7. **Reranking** — Selecting the best results from initial retrieval. See [[reranking]].
8. **Context Assembly** — Building the prompt context from retrieved chunks.
9. **Prompt Engineering** — Guiding the LLM response with rules, roles, and boundaries.
10. **LLM Generator** — Producing the final answer. The LLM operates inside constraints, not free-thinking.
11. **Post-processing** — Formatting, safety checks, citations.
12. **Feedback & Evaluation** — Measuring quality and improving the system. See [[rag-evaluation]].

## The Simple Version First

When designing a RAG system, start with the simplest version (source: RAG Primer.docx):

Document Store -> Chunking -> Embedding Model -> Vector DB -> Retrieval -> LLM -> Response

## Where It Breaks

The three places this breaks in production (source: RAG Primer.docx):

1. **Chunking strategy** — Cuts context at wrong boundaries
2. **Retrieval quality** — Top-k is not always the best chunk
3. **Prompt design** — Context window order affects the answer

## What Matters Most

The quality of a RAG system often depends more on (source: RAG Primer.docx):

- How intelligently you chunk the data
- How well your retriever finds the right context
- Whether [[reranking]] removes noise
- How the context window is constructed
- How you measure [[hallucination]] and [[latency-optimization|latency]]
- How responses are refined after generation

## Building a Robust System — Blueprint

A complete RAG blueprint covers (source: RAG Primer.docx):

- **Indexing** — Semantic splits, ColBERT embeddings, Multi-Representation Indexing, RAPTOR hierarchical clustering
- **Query Construction** — Translate natural language into the right format: SQL for relational DBs, traversal for graph DBs, embeddings for vector stores
- **RAG Types** — Multi-Query RAG Fusion, HyDE Decomposition
- **Routing** — Logical routing picks the right database; semantic routing picks the right prompt
- **Retrieval** — Refinement and [[reranking]] ensure only the most relevant context reaches the LLM
- **Generation** — Active retrieval, Self-RAG, and RRR patterns let the model decide *when* to retrieve
- **Evals** — RAGAS, Grouse, and DeepEval for benchmarking. See [[rag-evaluation]].

## Design Interview Approach

When asked to design a production RAG system (source: RAG Primer.docx):

1. **Clarify** — What kind of documents? Structured or unstructured? Acceptable latency?
2. **Draw the simplest version** — The basic pipeline
3. **Talk through failure modes** — Chunking, retrieval quality, prompt design
4. **End with evaluation** — Answer faithfulness, context precision, end-to-end latency

## Production Scaling

For scaling this architecture to real users, see [[production-scaling]] which covers parallel processing, LLM separation from API servers, polyglot persistence, semantic caching, infrastructure as code, and auto-scaling to zero (source: RAG architecture.txt).

## Common Challenges and Solutions

| Challenge | Solution |
|---|---|
| Hallucination | Fact-checking and source validation (see [[hallucination]]) |
| Retrieval Latency | Approximate nearest neighbor algorithms (see [[vector-indexing]]) |
| Context Length Limits | Recursive summarization of retrieved chunks |
| Irrelevant Retrieval | Filtering and pre-processing of documents |
| Response Consistency | Conversation history as part of context |

(source: RAG Cheatsheet.pdf)

## Related Pages

- [[rag-overview]]
- [[rag-types]]
- [[chunking-strategies]]
- [[embeddings]]
- [[vector-databases]]
- [[vector-indexing]]
- [[hybrid-retrieval]]
- [[reranking]]
- [[rag-evaluation]]
- [[observability]]
- [[production-scaling]]
- [[rag-failure-modes]]
