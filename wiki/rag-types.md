# RAG Types

**Summary**: There are at least 10 distinct RAG architecture patterns, ranging from simple Standard RAG to advanced Agentic and Adaptive variants. Each optimizes for different tradeoffs between accuracy, latency, complexity, and cost.

**Sources**: RAG Cheatsheet.pdf, RAG Types.pdf, Agentic_RAG_Architecture_1741260286.pdf

**Last updated**: 2026-07-04

---

## Taxonomy Overview

RAG architectures can be organized by increasing sophistication (source: RAG Cheatsheet.pdf):

| Architecture | Complexity | Best For |
|---|---|---|
| Standard (Naive) RAG | Beginner | Basic Q&A with external knowledge |
| Corrective RAG | Intermediate | High-precision use cases (medical, legal) |
| Speculative RAG | Intermediate | Balancing speed and accuracy |
| Fusion RAG | Intermediate | Multiple data sources of varying formats |
| Self RAG | Intermediate | Conversational systems requiring consistency |
| Fine-tuned RAG | Intermediate | Specialized domains needing expert responses |
| HyDE | Intermediate | Improving retrieval for vague queries |
| Hierarchical RAG | Advanced | Large, structured document hierarchies |
| Multi-modal RAG | Advanced | Information spanning text, images, audio, video |
| Adaptive RAG | Advanced | Diverse query types and user needs |
| [[agentic-rag]] | Advanced | Complex queries requiring multiple information types |

## Standard (Naive) RAG

The basic pipeline: query embedding, vector similarity search, prompt augmentation, LLM generation (source: RAG Types.pdf).

Flow: User Query -> Embedding -> Vector DB Search -> Prompt Augmentation -> LLM Generation -> Output

**When to use**: Basic question-answering systems. Start with chunk sizes of 512-1024 tokens and adjust based on performance (source: RAG Cheatsheet.pdf).

## Corrective RAG

Adds a self-correction loop: retrieved documents are graded for relevance. If irrelevant, the system searches alternative sources (e.g., web) and corrects before generating (source: RAG Types.pdf, Agentic_RAG_Architecture_1741260286.pdf).

Key components (source: Agentic_RAG_Architecture_1741260286.pdf):
- **Retrieval Evaluator** — Assigns confidence scores to retrieved documents
- **Triggered Actions** — Categorized as Correct, Ambiguous, or Incorrect
- **Web Search Augmentation** — Falls back to web search when confidence is low
- **Decompose-Then-Recompose** — Extracts key info while filtering irrelevant content
- **Plug-and-Play** — Integrates with existing RAG systems without major modifications

**When to use**: Medical information systems, legal documentation — anywhere accuracy is critical (source: RAG Cheatsheet.pdf).

## Speculative RAG

Uses a smaller specialist LM to generate multiple answer drafts in parallel from different document subsets, then a larger generalist LM verifies the best draft (source: Agentic_RAG_Architecture_1741260286.pdf).

Performance: up to 12.97% accuracy improvement and 51% latency reduction compared to conventional RAG on benchmarks like TriviaQA and PubHealth (source: Agentic_RAG_Architecture_1741260286.pdf).

This is related to [[cost-optimization]] via speculative decoding — using a small LLM for drafting and a large LLM for verification.

## Fusion RAG

Runs multiple retrieval methods simultaneously and fuses their results. Useful when dealing with heterogeneous data sources (articles, patents, databases). Weight different sources based on reliability and relevance (source: RAG Cheatsheet.pdf).

See also: [[hybrid-retrieval]] for combining BM25 with semantic search.

## Self RAG (Self-Reflective RAG)

Uses special "reflection tokens" to determine when retrieval is needed and to evaluate generated output quality (source: Agentic_RAG_Architecture_1741260286.pdf):

1. Query arrives — system decides if retrieval is needed
2. If yes: retrieve, evaluate relevance, filter irrelevant docs
3. LLM generates response
4. Hallucination check validates answer against context
5. Self-critique evaluates quality; rewrites query if unsatisfactory

**Benefits**: Reduced [[hallucination]], enhanced versatility, dynamic adaptation (source: Agentic_RAG_Architecture_1741260286.pdf).

## HyDE (Hypothetical Document Embeddings)

Instead of embedding the raw query, the system first generates a hypothetical answer/document, then embeds that for retrieval. This captures more semantic detail than the original query alone (source: RAG Types.pdf).

Flow: User Query -> Generate Hypothetical Document -> Embed Hypothetical -> Vector DB Search -> Prompt Augmentation -> Generation -> Output

**When to use**: When user queries are vague or short, and direct query embedding yields poor retrieval results.

## Graph RAG

Combines vector retrieval with a knowledge graph. A Graph Generator creates entity-relationship structures from retrieved data. Both vector similarity results (Context 1) and graph-based relationship results (Context 2) are merged for richer prompt augmentation (source: RAG Types.pdf).

See [[graph-based-rag]] for more detail on graph-based pipeline architectures.

## Hybrid RAG

Extends Graph RAG by using both vector DB and graph DB as parallel retrieval paths from the start, merging semantic similarity context with relational/structural context (source: RAG Types.pdf).

See [[hybrid-retrieval]] for BM25 + semantic combinations.

## Adaptive RAG

A Query Analyzer classifies incoming queries by complexity and routes them to the appropriate processing path (source: RAG Types.pdf, Agentic_RAG_Architecture_1741260286.pdf):

- **Direct** — Simple queries go straight to LLM (no retrieval)
- **Single Step** — One round of retrieval from vector DB
- **Multi Step** — Multi-hop reasoning via a Reasoning Chain before retrieval

Includes self-reflection: checks if the answer meets requirements, runs hallucination detection, and rewrites queries if necessary (source: Agentic_RAG_Architecture_1741260286.pdf).

## RAG Performance Comparison

Approximate comparison across architectures (source: RAG Cheatsheet.pdf):

| Architecture | Response Time | Accuracy | Memory Usage | Implementation Complexity |
|---|---|---|---|---|
| Standard RAG | High | Medium | Medium | Low |
| Corrective RAG | Low | Very High | High | High |
| Speculative RAG | High | Very High | Low | Very High |
| Fusion RAG | Low | High | Low | Very High |
| Agentic RAG | Low | Very High | Very High | Very High |

## Choosing the Right Architecture

Start with Standard RAG, then upgrade based on pain points (source: RAG Cheatsheet.pdf):

- Poor accuracy -> Corrective RAG or Self RAG
- Slow responses -> Speculative RAG
- Multiple data formats -> Fusion RAG
- Complex multi-step queries -> [[agentic-rag]] or Adaptive RAG
- Structured document hierarchies -> Hierarchical RAG
- Need for personalization across sessions -> Consider [[cag-and-mag]]

## Related Pages

- [[agentic-rag]]
- [[graph-based-rag]]
- [[hybrid-retrieval]]
- [[rag-pipeline-architecture]]
- [[hallucination]]
- [[cag-and-mag]]
