# Graph-Based RAG

**Summary**: Graph-based RAG replaces fragile linear pipelines with stateful, branching architectures where every step holds context and nodes decide what happens next. It enables multi-hop retrieval, conditional reasoning, and retry logic.

**Sources**: RAG Primer.docx, RAG Types.pdf, RAG architecture.txt

**Last updated**: 2026-07-04

---

## Linear RAG is Fragile

Linear RAG pipelines suffer from (source: RAG Primer.docx):
- Single pass retrieval
- No memory of previous steps
- No retry logic
- No conditional reasoning
- Retrieval failures = bad output

## Graph-Based RAG Changes the Architecture

With graph-based RAG (source: RAG Primer.docx):
- The flow becomes **stateful**
- Every step holds context
- Nodes decide what happens next
- The system can **branch, loop, retry, or stop**

## Why This Matters in Production

Graph-based RAG makes production systems more robust (source: RAG Primer.docx):
- Multi-hop retrieval becomes manageable
- Query rewriting can be inserted cleanly
- [[Reranking]] becomes modular
- Memory can persist across steps
- Tool usage becomes structured

## Key Architecture Principles

The shift from linear to graph-based RAG represents a fundamental change (source: RAG Primer.docx):
- **Control > randomness** — Explicit decision points instead of hoping the pipeline works
- **State > stateless** — Each step knows what came before
- **Architecture > prompt hacks** — System design instead of prompt engineering workarounds

## Graph RAG Architecture

Graph RAG combines vector retrieval with a knowledge graph (source: RAG Types.pdf):

1. User query is embedded into vectors
2. A **Graph Generator** analyzes retrieved data and constructs a knowledge graph (entities as nodes, relationships as edges)
3. The knowledge graph is stored in a **Graph Database**
4. Both vector similarity results (Context 1) and graph-based relationship results (Context 2) are merged in prompt augmentation
5. The LLM generates a response using this enriched context

This provides richer answers than vector-only retrieval because the graph captures structured connections between concepts (source: RAG Types.pdf).

## Hybrid RAG (Vector + Graph)

Hybrid RAG extends Graph RAG by feeding data sources into both Vector DB and Graph Generator from the start (source: RAG Types.pdf):

- **Context 1** — Information retrieved based on semantic similarity (Vector DB)
- **Context 2** — Information retrieved based on relational structures, entity-relationship context (Graph DB)
- Both contexts are merged for comprehensive prompt augmentation

This is the architecture recommended for production: don't use vector search alone, combine it with a knowledge graph. Vectors give you semantic meaning; the graph gives you relationships between entities. Run both at the same time (source: RAG architecture.txt).

## Frameworks

- **LangGraph** — Framework for building graph-based RAG pipelines where RAG is "no longer a straight line" but "a decision system" (source: RAG Primer.docx). See [[langchain-rag]].
- **Neo4j** — Graph database commonly used for knowledge graphs in RAG systems.

## Related Pages

- [[agentic-rag]]
- [[rag-pipeline-architecture]]
- [[rag-overview]]
- [[rag-types]]
- [[hybrid-retrieval]]
- [[langchain-rag]]
- [[production-scaling]]
