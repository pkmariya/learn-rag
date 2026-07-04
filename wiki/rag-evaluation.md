# RAG Evaluation

**Summary**: RAG evaluation goes beyond simple accuracy to measure faithfulness, context relevance, answer relevance, and retrieval quality. Without proper evaluation, hallucinations slip into production even when retrieval looks perfect.

**Sources**: RAG Primer.docx

**Last updated**: 2026-07-04

---

## Why Evaluation Matters

If you do not measure it, you cannot trust it (source: RAG Primer.docx). Production RAG is about reliability, not demos. Automated and human feedback loops are essential.

## Key Metrics

Evaluation metrics for production RAG systems (source: RAG Primer.docx):

- **Faithfulness** — Are the claims in the generated answer supported by the retrieved passages?
- **Context Relevance** — Was the retrieved context actually relevant to the question?
- **Answer Relevance** — Does the answer address the question?
- **Recall@K** — Of all relevant documents, how many were retrieved?
- **Precision@K** — Of the retrieved documents, how many were relevant?
- **MRR (Mean Reciprocal Rank)** — How high is the first relevant result?
- **nDCG (Normalized Discounted Cumulative Gain)** — Quality of the ranking order

## Faithfulness vs Context Relevance

A common trap: faithfulness of 0.83 means 83% of the generated answer is grounded in the retrieved context. That sounds good, but it tells you nothing about whether the retrieved context was the *right* context (source: RAG Primer.docx).

The retrieval step may pull documents that are related but not actually relevant. The model then generates a faithful answer — faithfully based on the wrong documents (source: RAG Primer.docx).

To debug this, evaluate context relevance and answer relevance separately, not just faithfulness. If context relevance is low, the [[chunking-strategies|chunking strategy]] or [[embeddings|embedding model]] is the culprit. If context relevance is fine but answer relevance is low, it is a generation/prompt issue (source: RAG Primer.docx).

## Evaluation Techniques

### 1. RAGAS Framework
Metrics like faithfulness check whether claims in the generated answer are supported by retrieved passages. Flags potential [[hallucination]] when the model introduces facts not present in context (source: RAG Primer.docx).

### 2. LLM-as-a-Judge
Provide the question, retrieved context, and generated answer to another LLM. Ask it to evaluate whether the answer is supported by the evidence. The judge looks for unsupported claims and reasoning outside the provided documents (source: RAG Primer.docx).

### 3. Attribution and Citations
Require the model to generate answers with citations or supporting spans from retrieved chunks. Makes it easier to verify whether each part of the answer is grounded in the source (source: RAG Primer.docx).

### 4. Human Evaluation
Automated metrics help scale evaluation, but periodic human review is still important to validate real-world answer quality (source: RAG Primer.docx).

### 5. Regression Testing
Maintain a benchmark set of questions with expected grounded answers. Every time the retrieval pipeline, prompts, or models change, run these tests to ensure the system has not silently degraded (source: RAG Primer.docx).

## Evaluation Frameworks

Tools for benchmarking and iterating (source: RAG Primer.docx):
- **RAGAS** — Retrieval Augmented Generation Assessment
- **Grouse** — Grounded evaluation
- **DeepEval** — Deep evaluation metrics

## Cross-Channel Consistency

For enterprise chatbots that give different answers across channels, evaluation should include cross-channel consistency tests using golden questions and tracking semantic similarity of responses (source: RAG Primer.docx).

## Related Pages

- [[hallucination]]
- [[observability]]
- [[rag-pipeline-architecture]]
- [[hybrid-retrieval]]
