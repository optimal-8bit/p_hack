# RAG Module

## Purpose
This module provides a full Retrieval-Augmented Generation pipeline through helper functions only.

It is designed for fast hackathon development:
- no route coupling
- clean abstraction per concern
- provider fallback for reliability
- Neo4j vector search for retrieval

## What This Module Solves
1. Ingest large text and split it into chunks.
2. Convert chunks into embeddings.
3. Store embeddings with metadata in Neo4j.
4. Retrieve top-matching chunks for a user query.
5. Generate an answer grounded in retrieved context.
6. Handle provider failures via fallback.

## File-by-File Breakdown

### functions.py
Entry-point helpers that other modules should call.

- index_document(document_id, content, metadata, chunk_size, chunk_overlap)
  - Splits text
  - Generates embeddings with fallback
  - Ensures vector index exists
  - Upserts all chunks into Neo4j

- answer_query(query, top_k)
  - Retrieves relevant chunks
  - Builds context block
  - Calls grounded generation
  - Returns answer plus chunk evidence

- remove_document(document_id)
  - Deletes all chunks for a document

### chunking.py
Pure text chunking utility.

- chunk_text(text, chunk_size, chunk_overlap)
- Uses overlap to preserve context continuity across chunks.

### embeddings.py
Embedding generation and fallback routing.

- get_embedding(provider, text)
- get_embedding_with_fallback(text)

Provider order is controlled by env configuration.
Primary default order is Google AI Studio, then OpenRouter, then Ollama.

### vector_store.py
Neo4j vector index and persistence operations.

- ensure_vector_index(vector_dimensions)
- upsert_chunk(chunk_id, document_id, content, embedding, metadata)
- similarity_search(embedding, top_k)
- delete_document(document_id)

### retrieval.py
Retrieval orchestration.

- retrieve_chunks(query, top_k)
- build_context(chunks)

Maps raw vector hits into strongly-typed chunk models and context string blocks.

### generation.py
Final answer generation from retrieved context.

- generate_grounded_answer(query, context)

Uses LLM fallback order from configuration and returns provider/model metadata.

### cache.py
Simple in-memory TTL cache used by embeddings and retrieval layers.

### retry.py
Async retry utility with linear backoff for external API calls.

### schemas.py
Typed models for retrieval and final RAG answer output.

## Main Helper API for Other Modules
Use these from controllers/services:

1. index_document
2. answer_query
3. remove_document

## High-Level Flow

### Indexing Flow
1. Receive document text.
2. Split into chunks.
3. Create embedding per chunk with fallback provider chain.
4. Ensure Neo4j vector index exists.
5. Upsert chunks and metadata.

### Query Flow
1. Receive user query.
2. Embed query with fallback provider chain.
3. Run Neo4j vector similarity search.
4. Build context from top chunks.
5. Generate grounded answer using LLM fallback.
6. Return answer with evidence chunks.

## Provider Fallback Strategy

### Embeddings
RAG_EMBEDDING_PROVIDER_ORDER controls fallback.

Example:
- google_ai_studio,openrouter,ollama

### Generation
RAG_GENERATION_PROVIDER_ORDER controls fallback.

Example:
- google_ai_studio,openrouter,ollama

If one provider fails, next provider is attempted automatically.

## Neo4j Data Model
Each chunk is stored as one node with:
- chunk_id
- document_id
- content
- embedding
- metadata_json
- updated_at

Vector search uses a Neo4j vector index defined by:
- RAG_VECTOR_INDEX_NAME
- RAG_CHUNK_LABEL

## Important Environment Variables

### Neo4j
- NEO4J_URI
- NEO4J_USERNAME
- NEO4J_PASSWORD
- NEO4J_DATABASE

### Chunking and Retrieval
- RAG_CHUNK_SIZE
- RAG_CHUNK_OVERLAP
- RAG_TOP_K

### Reliability and Performance
- RAG_CACHE_TTL_SECONDS
- RAG_RETRY_ATTEMPTS
- RAG_RETRY_BASE_DELAY_SECONDS

### Embedding Models
- RAG_EMBEDDING_PROVIDER_ORDER
- RAG_GOOGLE_EMBEDDING_MODEL
- RAG_OPENROUTER_EMBEDDING_MODEL
- RAG_OLLAMA_EMBEDDING_MODEL

### Generation Models
- RAG_GENERATION_PROVIDER_ORDER
- RAG_GENERATION_TEMPERATURE
- RAG_GENERATION_MAX_TOKENS

## Usage Example (Controller)

Pseudo-flow for indexing:
1. Receive uploaded text.
2. Call index_document.
3. Return chunks_indexed.

Pseudo-flow for answering:
1. Receive query.
2. Call answer_query.
3. Return answer and supporting chunks.

## Performance Notes
1. Caching helps repeated query and embedding requests.
2. Keep chunk_size tuned for your dataset.
3. Increase top_k for more context, lower for speed.
4. Use Ollama fallback for local/offline resilience.

## Troubleshooting
1. Empty retrieval results:
	- Confirm documents were indexed successfully.
	- Verify Neo4j connection and vector index settings.

2. Provider failures:
	- Check API keys and base URLs.
	- Validate fallback order env values are non-empty.

3. Slow responses:
	- Reduce top_k.
	- Reduce max token generation size.
	- Increase cache TTL for repeated workloads.

4. Bad answer quality:
	- Adjust chunk size and overlap.
	- Improve source document cleanliness.
	- Tune generation model and temperature.

## Design Principles Followed
1. Route-free helper design.
2. Strict separation of concerns.
3. Async-first execution.
4. Provider-agnostic with fallback.
5. Hackathon-friendly iteration speed.
