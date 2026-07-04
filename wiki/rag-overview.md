# RAG Overview

**Summary**: Retrieval Augmented Generation (RAG) is a technique that enhances LLM outputs by retrieving relevant external knowledge before generating a response, grounding answers in real data rather than relying solely on the model's training.

**Sources**: RAG Primer.docx

**Last updated**: 2026-07-04

---

## What is RAG?

RAG combines an LLM's generation capabilities with real-time retrieval from external knowledge sources. Instead of relying purely on what the model learned during training, RAG fetches relevant documents and uses them as context for generating more accurate, up-to-date responses (source: RAG Primer.docx).

The basic pipeline is: User query -> Embedding -> Vector search -> Top-k documents retrieved -> Assembled into prompt context -> LLM generates response (source: RAG Primer.docx).

## How AI Systems Have Progressed

RAG sits in a progression of increasingly capable AI system architectures (source: RAG Primer.docx):

1. **LLM** — Context-free generation from prompt input without external retrieval. Fast and simple but limited in context understanding.
2. **RAG** — Knowledge-enhanced. Combines LLM output with real-time retrieval from external sources for more accurate, up-to-date responses.
3. **AI Agent** — Autonomous task execution using planning, reasoning, memory, and tool integrations to complete workflows requiring decision-making.
4. **Agentic AI** — Multi-agent collaboration where specialized agents coordinate, share memory, and divide tasks to solve complex problems together.

## Common Challenges

Five common challenges cause RAG systems to fail (source: RAG Primer.docx):

1. **Poor Chunking** — Use context-aware, semantic chunking instead of fixed-size chunking
2. **Weak Embeddings** — Use domain-specific embedding models
3. **Bloated Prompts** — Keep prompts clean and structured
4. **Lack of Metadata** — Add metadata filters to control what gets retrieved
5. **No Feedback Loop** — Build a feedback loop to learn which retrievals actually helped

## RAG is a System, Not a Feature

Most explanations simplify RAG to "Documents -> Embeddings -> Vector DB -> Retrieve -> LLM." In reality, a production-grade RAG system is a multi-layer architecture where every stage influences the final answer (source: RAG Primer.docx).

The 12 core components of a production RAG system are covered in [[rag-pipeline-architecture]].

## RAG is a Pipeline Problem

Most teams obsess over the model, but RAG is not a model problem — it is a pipeline problem. You can use the most powerful LLM in the world and still get poor answers if your retrieval layer is weak. RAG in production is less about AI magic and more about system design (source: RAG Primer.docx).

## Related Pages

- [[rag-pipeline-architecture]]
- [[chunking-strategies]]
- [[embeddings]]
- [[vector-databases]]
- [[hybrid-retrieval]]
- [[reranking]]
- [[agentic-rag]]
- [[graph-based-rag]]
- [[rag-evaluation]]
- [[hallucination]]
- [[observability]]
- [[latency-optimization]]
- [[cost-optimization]]
