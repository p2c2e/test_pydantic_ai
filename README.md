# Pydantic AI Examples

This repository contains example implementations using Pydantic AI for various AI-powered applications.

## Installation

The recommended way to install dependencies is using the `uv` package manager for its speed and reliability:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies with uv
uv pip install -r requirements.txt
```

## Environment Setup

1. Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

2. Required environment variables:
```
OPENAI_API_KEY=your_key_here
SEARX_URL=your_searx_instance_url  # Optional: for search examples
LOG_ENABLED=true  # Optional: for detailed logging
```

## Examples

### RAG (Retrieval Augmented Generation)

The repository includes multiple implementations of RAG with different vector stores:

```bash
# Build search database (defaults to using ChromaDB)
python rag_agent.py build

# Run a search query
python rag_agent.py search "How do I use vector stores with RAG?"

# Specify vector store type
VECTOR_DB=faiss python rag_agent.py build
VECTOR_DB=postgres python rag_agent.py search "Your query here"
```

### Search and Chat Examples

```bash
# Run SearxNG search agent
python searxng_agent.py

# Run chat interface with search
python user_chat_search.py

# Run dynamic form filler
python form2/user_dyn_form_filler.py
```

### Document Processing

```bash
# Download and process markdown docs
python download_markdown.py

# Test dynamic model generation
python dynamic_model.py
```

## Vector Store Support

`vector_store.py` provides a unified interface for different vector stores:

- **PostgreSQL with pgvector**: Requires PostgreSQL with pgvector extension
- **FAISS**: In-memory/disk vector store, good for smaller datasets
- **ChromaDB**: Embedded vector store with persistence

## Development

To run the examples:

1. Ensure your `.env` file is configured
2. Activate your virtual environment
3. Run specific examples as shown above

## Requirements

See `requirements.txt` for full list of dependencies. Key requirements:

- pydantic
- pydantic_ai
- openai
- chromadb
- faiss-cpu
- asyncpg
- httpx

## Troubleshooting

- If you get embedding errors, ensure your OpenAI API key is valid
- For PostgreSQL examples, ensure PostgreSQL is running and pgvector extension is installed
- For ChromaDB persistence issues, check write permissions in the chromadb directory

## Development

To run the examples:

1. Set up environment variables:
   ```bash
   OPENAI_API_KEY=your_key_here
   SEARX_URL=your_searx_instance_url
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run specific examples:
   ```bash
   python rag.py search "your query"
   python searxng_agent.py
   ```
