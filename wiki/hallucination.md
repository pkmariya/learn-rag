# Hallucination

**Summary**: Hallucination is when an AI model generates information that sounds convincing but is incorrect, made up, or unsupported by facts. It occurs because the model predicts the most likely next words instead of verifying truth. Detecting and minimizing hallucinations is essential for reliable production AI.

**Sources**: RAG Primer.docx, RAG failure situations.pdf, Agentic_RAG_Architecture_1741260286.pdf

**Last updated**: 2026-07-04

---

## What is Hallucination?

Hallucination occurs when an LLM generates information that sounds convincing but is actually incorrect, made up, or unsupported by facts. It happens because the model predicts the most likely next words instead of verifying the truth (source: RAG Primer.docx).

An LLM can read the right documents and still confidently generate information that is not present in the context. So evaluation needs to focus on grounding, not just retrieval (source: RAG Primer.docx).

## Why RAG Systems Still Hallucinate

Even with correct documents in the knowledge base, RAG chatbots can hallucinate because (source: RAG Primer.docx):
- Retrieved context may be related but not actually relevant to the question
- The model generates a faithful answer based on the *wrong* documents
- The prompt does not instruct the model to be selective about which parts of context to use

## Techniques for Reducing Hallucination

Five approaches, each suited to different scenarios (source: RAG Primer.docx):

1. **Better Prompting** — Instruct the model to only use provided context, cite sources, and say "I don't know" when appropriate
2. **RAG** — Ground responses in retrieved external knowledge
3. **Fine-tuning** — Train the model on domain-specific data
4. **Function Calling** — Use structured tool outputs rather than free-form generation
5. **Guardrails** — Post-processing validation and safety checks

## Measuring Hallucination

Key evaluation approaches (source: RAG Primer.docx):

- **Faithfulness metrics (RAGAS)** — Check if claims are supported by retrieved passages
- **LLM-as-a-Judge** — Use a stronger model to evaluate grounding
- **Attribution/Citations** — Require the model to cite supporting spans
- **Human evaluation** — Periodic review for real-world quality
- **Regression testing** — Benchmark set of questions with expected answers

See [[rag-evaluation]] for detailed evaluation strategies.

## Validation and Guardrails

Production RAG systems need a validation layer (source: RAG Primer.docx):
- Check grounding of generated answers
- Detect hallucinations
- Block unsafe outputs
- Post-process for formatting, safety, and citations

## Designing for "I Don't Know"

A well-designed system should admit when it does not have an answer rather than generating misleading information. This requires designing the system architecture, not just the prompt, to handle out-of-scope queries gracefully (source: RAG Primer.docx).

## Architectural Solutions to Hallucination

Several [[rag-types|RAG architecture variants]] are specifically designed to combat hallucination:

- **Corrective RAG** — Grades retrieved documents for relevance; falls back to web search when confidence is low. Uses a Decompose-Then-Recompose algorithm to filter irrelevant content (source: Agentic_RAG_Architecture_1741260286.pdf).
- **Self-Reflective RAG** — Uses reflection tokens to evaluate output quality, with hallucination checks before delivering answers. Can trigger query rewrites and restart the process (source: Agentic_RAG_Architecture_1741260286.pdf).
- **Adaptive RAG** — Includes self-reflection steps that iteratively check if answers meet requirements and detect inaccuracies (source: Agentic_RAG_Architecture_1741260286.pdf).

Domain mismatch is a particularly common cause of hallucination: if the knowledge base covers medical data but the user asks about cricket, the system may fabricate answers rather than admitting ignorance (source: RAG failure situations.pdf). See [[rag-failure-modes]] for all 10 failure cases.

## Related Pages

- [[rag-evaluation]]
- [[rag-pipeline-architecture]]
- [[observability]]
- [[agentic-rag]]
- [[rag-types]]
- [[rag-failure-modes]]
