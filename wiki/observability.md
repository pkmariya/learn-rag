# Observability

**Summary**: Observability in RAG systems means tracking every step of the pipeline through span-level tracing. AI systems degrade over time, and without visibility into each component, problems cannot be diagnosed or fixed.

**Sources**: RAG Primer.docx

**Last updated**: 2026-07-04

---

## Why Observability Matters

If you are deploying LLM-powered apps to real users, you need to know what is happening inside your pipeline at every step. A user asks a question, it flows through multiple components, and eventually a response comes out. Each step takes time, each can fail, and each has its own cost. Looking only at input and output gives no visibility (source: RAG Primer.docx).

AI systems degrade over time. What worked last month might not work today. Span-level metrics let you catch drift early and tune each component independently (source: RAG Primer.docx).

## The Five Spans

Each RAG request can be traced through five spans (source: RAG Primer.docx):

### 1. Query Span
User submits a question. This is where the trace begins. Captures raw input, timestamp, and session info.

### 2. Embedding Span
The query hits the [[embeddings|embedding]] model and becomes a vector. Tracks token count and latency. If the embedding API is slow or hitting rate limits, this span catches it.

### 3. Retrieval Span
The vector goes to the [[vector-databases|vector database]] for similarity search. **This is where most RAG problems hide.** Common reasons: bad chunks, low relevance scores, wrong top-k values. The retrieval span exposes all of it.

### 4. Context Span
Retrieved chunks get assembled with the system prompt. Shows exactly what is being fed to the LLM. If the context is too long, it shows up here.

### 5. Generation Span
The LLM produces a response. Usually the longest and most expensive span. Input tokens, output tokens, latency, reasoning — everything is logged for [[cost-optimization|cost tracking]] and debugging.

## Governance and Observability

Production RAG requires logs, traces, metrics, and audits. If you cannot see it, you cannot trust it (source: RAG Primer.docx).

## Model Drift Detection

RAG answers can degrade even without code changes when the LLM provider silently updates the model. Strategies to catch model drift (source: RAG Primer.docx):

1. **Pin the model version** — Use specific version strings, not aliases. Log the exact version on every call.
2. **Golden test set** — Pick 100 real questions with known good answers. Run them nightly. Compare scores.
3. **LLM-as-judge** — Sample 2-5% of live answers. Score with a stronger model on faithfulness and relevance. Plot the trend.
4. **User signals** — Thumbs down, regenerate clicks, follow-up questions, abandonment. These shift before complaints arrive.
5. **Monitor structural metrics** — Answer length, refusal rate, hedging phrases ("I'm not sure"). Structural drift shows up first.

## Related Pages

- [[rag-evaluation]]
- [[rag-pipeline-architecture]]
- [[latency-optimization]]
- [[hallucination]]
