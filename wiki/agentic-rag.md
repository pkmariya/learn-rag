# Agentic RAG

**Summary**: Agentic RAG moves beyond passive document retrieval by introducing reasoning, planning, memory, and multi-agent coordination into the RAG pipeline. It transforms RAG from a simple lookup into an active, adaptive workflow.

**Sources**: RAG Primer.docx, Agentic_RAG_Architecture_1741260286.pdf, RAG Cheatsheet.pdf, RAG Types.pdf

**Last updated**: 2026-07-04

---

## Traditional RAG vs Agentic RAG

**Traditional RAG** is passive and static — "You ask, I fetch" (source: RAG Primer.docx):
- User sends a query -> vector search -> top documents picked -> handed to LLM -> generation
- Works for FAQ bots or simple text processing from PDFs
- Static and passive

**Agentic RAG** is active and adaptive (source: RAG Primer.docx):
- Brings actual reasoning and planning into the loop
- An agent can rephrase queries, look deeper, summarize chunks before proceeding
- Multiple agents work together: one to search, one to verify, one to answer, one to reflect
- Can say "this answer doesn't look correct, let me keep retrying"

> "Traditional RAG is a lookup; Agentic RAG is a workflow" (source: RAG Primer.docx)

## Key Capabilities

Agentic RAG adds these capabilities beyond traditional RAG (source: RAG Primer.docx):

- **Memory** — Remembers the last conversation and prior context
- **Conditional Logic** — Knows when to stop, when to ask again, when to escalate
- **Query Rewriting** — Rephrases queries for better retrieval
- **Multi-step Retrieval** — Goes beyond single-pass retrieval
- **Recovery Logic** — Retries and fallback strategies
- **Reflection** — Evaluates whether its own answers are correct

## Where Traditional RAG Breaks

Traditional RAG feels fine until you need (source: RAG Primer.docx):
- Multi-step retrieval
- Query rewriting
- [[Reranking]]
- Memory
- Recovery logic

That is where linear pipelines start collapsing. See also [[graph-based-rag]].

## 7 Agentic RAG Architectures

Agentic RAG is not a single pattern but a family of architectures (source: Agentic_RAG_Architecture_1741260286.pdf):

### 1. Agentic RAG Router

Routes user queries to appropriate tools or data sources. The Retrieval Agent evaluates query intent and type, then a Router dispatches to Vector Search, Web Search, Recommendation System, or Text-to-SQL as needed (source: Agentic_RAG_Architecture_1741260286.pdf).

### 2. Query Planning Agentic RAG

Handles complex queries by breaking them into parallelizable subqueries across diverse data sources. A Query Planner interprets the query, generates prompts for downstream query engines, and synthesizes results into a coherent answer (source: Agentic_RAG_Architecture_1741260286.pdf).

### 3. Adaptive RAG

A Query Analyzer classifies queries by complexity and routes them to the appropriate path: direct LLM (no retrieval), single-step retrieval, or multi-step reasoning chain. Includes self-reflection and hallucination checking (source: Agentic_RAG_Architecture_1741260286.pdf).

See [[rag-types]] for more detail on Adaptive RAG.

### 4. Corrective RAG

Self-corrects retrieval results. A Retrieval Evaluator assigns confidence scores; low-confidence results trigger web searches for augmentation. Uses a Decompose-Then-Recompose algorithm to extract key info while filtering irrelevant content (source: Agentic_RAG_Architecture_1741260286.pdf).

### 5. Self-Reflective RAG

Uses special "reflection tokens" to decide when retrieval is needed and to evaluate output quality. The system can critique its own response, trigger query rewrites, and restart the process if the answer is unsatisfactory (source: Agentic_RAG_Architecture_1741260286.pdf).

### 6. Speculative RAG

A smaller specialist LM generates multiple answer drafts in parallel from different document subsets, then a larger generalist LM verifies the best draft. Achieves up to 12.97% accuracy improvement and 51% latency reduction (source: Agentic_RAG_Architecture_1741260286.pdf).

### 7. Self-Route Agentic RAG

Autonomously determines the best retrieval path. If a query is answerable with given context, it processes immediately. Otherwise, it routes to a long-context model with additional context. Balances cost-efficiency with accuracy (source: Agentic_RAG_Architecture_1741260286.pdf).

## Key Features of Agentic RAG

Beyond traditional RAG, agentic systems offer (source: Agentic_RAG_Architecture_1741260286.pdf):
- **AI Agents** — Autonomous agents performing complex tasks beyond simple query handling
- **Dynamic Query Handling** — Adjustments based on user queries for complex, nuanced questions
- **Enhanced Problem-Solving** — Agents navigate multiple documents, compare info, generate summaries
- **Tool Utilization** — Integration with databases, APIs, web search, recommendation systems
- **Continuous Learning** — Adapts strategies based on feedback and new data
- **Improved Accuracy** — Combining retrieval with generation reduces errors

## Engineering Principles

Agentic RAG is where real AI engineering comes in — not just prompts, but systems with (source: RAG Primer.docx):
- Memory and state
- Limits and boundaries
- Fallback options
- Responsibility by design

"We're no longer testing for intelligence; we're designing for responsibility" (source: RAG Primer.docx).

## Related Pages

- [[rag-overview]]
- [[rag-types]]
- [[graph-based-rag]]
- [[rag-pipeline-architecture]]
- [[hallucination]]
- [[rag-failure-modes]]
- [[production-scaling]]
