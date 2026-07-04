# Embeddings

**Summary**: Embeddings turn human language into numerical vectors where distance equals similarity. They are the foundation of semantic search, RAG retrieval, and modern AI — without them, these systems cannot function.

**Sources**: RAG Primer.docx

**Last updated**: 2026-07-04

---

## Why Embeddings?

Computers do not understand words — they understand numbers. Embeddings turn messy human language into clean numerical maps of meaning. Each word, sentence, or document becomes a vector with position and distance. Distance equals similarity (source: RAG Primer.docx).

This is how large language models work at scale (source: RAG Primer.docx):
- They scan millions of documents in milliseconds
- They find meaning without exact keyword matches
- They compare ideas even when the wording is different
- They retrieve the right context before generating an answer

Without embeddings, semantic search does not exist. Without embeddings, RAG pipelines break. Without embeddings, models do not understand what you mean (source: RAG Primer.docx).

## Static vs Contextual Embeddings

### Static Embeddings (Word2Vec, GloVe, FastText)

Static embeddings are context-blind — they collapse every meaning of a word into a single point in space. This causes **polysemy collapse**: a word like "Washington" pulls both "State" and "D.C." results into the same cluster, destroying search precision (source: RAG Primer.docx).

### Contextual Embeddings (BERT, RoBERTa, Transformers)

Transformer-based models generate an embedding based on surrounding tokens. "Washington is a state" and "Washington is the capital" produce two distinct vectors because the attention mechanism looks at neighbor words (source: RAG Primer.docx).

## Solving Semantic Ambiguity

Three approaches to resolve polysemy without losing transfer learning benefits (source: RAG Primer.docx):

1. **Contextual Embeddings** — Shift from static models to transformer-based models (BERT/RoBERTa) that generate dynamic, context-dependent embeddings.

2. **Sense Disambiguation (WSD)** — If stuck with static vectors, implement a Sense-Aware layer. Map ambiguous words to different "sense centroids" based on trigger keywords in the query.

3. **The Projection Trick** — Learn a small projection matrix that stretches the vector space along specific dimensions to separate clusters, keeping pre-trained weights frozen. No retraining required.

## Embedding Model Selection

When choosing an embedding model, consider (source: RAG Primer.docx):
- Vector dimensions and cost trade-offs
- ANN algorithms (HNSW, IVF)
- Similarity metrics (cosine, dot product)
- Domain-specific vs general-purpose models

## NLP Pipeline Foundation

Before jumping into prompting LLMs, understanding the NLP pipeline is essential (source: RAG Primer.docx):

1. **Basic Pre-processing** — Tokenization, lemmatization, stemming, stop-word removal
2. **Word Embeddings** — Word2Vec (CBOW vs Skip-Gram), GloVe, FastText, transformer-based
3. **Sequence Models** — RNNs, LSTMs, GRUs, then BERT's bidirectional context breakthrough
4. **Core NLP Tasks** — NER, POS tagging, sentiment analysis, machine translation

## Related Pages

- [[rag-pipeline-architecture]]
- [[chunking-strategies]]
- [[vector-databases]]
- [[hybrid-retrieval]]
- [[cost-optimization]]
