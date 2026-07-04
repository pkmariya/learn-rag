# LangChain RAG

**Summary**: LangChain is a framework for building LLM-powered applications with modular components for document loading, text splitting, embeddings, vector stores, retrievers, and chains. LangGraph extends it with stateful, graph-based agent workflows.

**Sources**: RAG with Langchain.pdf, RAG Bundle.pdf, RAG Cheatsheet.pdf

**Last updated**: 2026-07-04

---

## LangChain Overview

LangChain provides modular, pre-built components for building RAG pipelines (source: RAG with Langchain.pdf):

1. **Document Loaders** — Load data from PDFs, text files, websites, CSVs, Wikipedia
2. **Text Splitters** — Break documents into chunks (see [[chunking-strategies]])
3. **Embeddings** — Convert text to vectors (see [[embeddings]])
4. **Vector Stores** — Store and search embeddings (see [[vector-databases]])
5. **Retrievers** — Find relevant documents
6. **LLMs** — Generate responses
7. **Evaluation** — Assess performance (see [[rag-evaluation]])

## Pipeline with Plain Python

A minimal RAG pipeline without frameworks (source: RAG Bundle.pdf):

1. **File Upload** — Load text from files (TXT, PDF, docs)
2. **Chunking** — Split into smaller parts (embedding models + LLMs have token limits)
3. **Embeddings** — Convert chunks into vectors (similar meaning = closer vectors)
4. **Vector Database** — Store embeddings with ChromaDB (lightweight, runs locally)
5. **User Query** — Convert query to embedding, find most similar chunks
6. **Generation** — GPT answers based ONLY on retrieved context

Key tips (source: RAG Bundle.pdf):
- Keep chunks small enough for precision; increase size if answers feel incomplete
- Try top_k = 3 to 5 for better coverage
- Keep temperature low for factual answers

## LangChain Implementation

### Document Loading and Preprocessing

LangChain doesn't provide built-in preprocessing — you must write custom code to clean headers, footers, page numbers, and standardize text format (source: RAG with Langchain.pdf).

Available loaders: PyPDFLoader, TextLoader, WebBaseLoader, CSVLoader, WikipediaLoader (source: RAG with Langchain.pdf).

### Text Chunking Parameters

Recommended starting configuration (source: RAG with Langchain.pdf):
- **chunk_size**: 200-1000 characters (300 is optimal starting point)
- **chunk_overlap**: 10-20% of chunk_size (50-100 characters)
- **separators**: `["\n\n", "\n", ".", " "]` (paragraph, sentence, word)

### Embedding Models

Popular choices (source: RAG with Langchain.pdf):
- **all-mpnet-base-v2** — Best balance of quality and speed
- **all-MiniLM-L6-v2** — Fastest, good for large datasets
- **text-embedding-ada-002** — OpenAI's high-quality model

### Vector Database Options

FAISS is highlighted for LangChain use (source: RAG with Langchain.pdf):
- Fast: Optimized for similarity search
- Scalable: Handles millions of vectors
- Free: Open-source (Facebook AI)
- GPU Support: Faster processing with CUDA

Alternatives: Pinecone (managed cloud), Chroma (simple/lightweight), Qdrant (high-performance). See [[vector-databases]] for full comparison.

### Retrieval Settings

Key retrieval parameters (source: RAG with Langchain.pdf):
- **k**: Number of chunks to retrieve (3-10)
- **search_type**: `"similarity"` or `"mmr"` (maximal marginal relevance for diversity)
- **score_threshold**: Minimum similarity score

### Chain Types

Three chain types for generation (source: RAG with Langchain.pdf):
- **stuff** — Fast, limited context. Puts all retrieved chunks into one prompt.
- **map_reduce** — Handles more context. Processes each chunk separately, then combines.
- **refine** — Most thorough but slow. Iteratively refines the answer with each chunk.

## LangGraph (Stateful Agents)

LangGraph extends LangChain for building stateful, graph-based RAG workflows (source: RAG Bundle.pdf):

1. Create LangGraph state
2. Build Retrieve Node (vector search)
3. Build Generate Node (LLM response)
4. Connect nodes into a graph
5. Run the application

This enables the agent to loop, self-correct, and make conditional decisions rather than following a linear retrieve-then-answer pipeline. See [[graph-based-rag]] and [[agentic-rag]].

## Evaluation

Key metrics (source: RAG with Langchain.pdf):
- **Faithfulness** — Answer stays true to source documents
- **Relevance** — Answer addresses the question
- **Retrieval Quality** — Retrieved chunks are relevant

Evaluation approaches: Automated (BLEU, ROUGE, BERTScore), Human (ratings, comparative analysis), Continuous (A/B testing, feedback loops). See [[rag-evaluation]].

## Key Success Tips

From RAG with Langchain.pdf:
- **Chunk Size**: Start with 300 characters, adjust based on your data
- **Overlap**: Use 50-100 characters for context preservation
- **Retrieval**: Experiment with k=3 to k=10 based on query complexity
- **Temperature**: Keep at 0 for factual responses
- **Caching**: Store frequently accessed embeddings
- **Monitoring**: Track query performance and user feedback
- **Error Handling**: Graceful failures and fallbacks
- **Security**: Protect API keys and sensitive data

## Related Pages

- [[rag-pipeline-architecture]]
- [[chunking-strategies]]
- [[embeddings]]
- [[vector-databases]]
- [[graph-based-rag]]
- [[rag-evaluation]]
