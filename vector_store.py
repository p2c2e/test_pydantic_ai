import asyncio
import logging
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any

import asyncpg
import chromadb
import faiss
import numpy as np
import pydantic_core

logger = logging.getLogger(__name__)
if not os.getenv("LOG_ENABLED", "").lower() in ("true", "1", "yes"):
    logger.addHandler(logging.NullHandler())
    logger.setLevel(logging.CRITICAL)

class VectorStore(ABC):
    @abstractmethod
    async def initialize(self, recreate: bool = False) -> None:
        pass

    @abstractmethod
    async def insert(self, url: str, title: str, content: str, embedding: List[float]) -> None:
        pass

    @abstractmethod
    async def search(self, embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

class PostgresVectorStore(VectorStore):
    def __init__(self, dsn: str, database: str):
        self.server_dsn = dsn
        self.database = database
        self.pool = None

    async def initialize(self, recreate: bool = False) -> None:
        if recreate:
            conn = await asyncpg.connect(self.server_dsn)
            try:
                db_exists = await conn.fetchval(
                    'SELECT 1 FROM pg_database WHERE datname = $1', self.database
                )
                if recreate and db_exists:
                    await conn.execute(
                        f"""
                        SELECT pg_terminate_backend(pg_stat_activity.pid)
                        FROM pg_stat_activity
                        WHERE pg_stat_activity.datname = '{self.database}'
                        AND pid <> pg_backend_pid()
                        """
                    )
                    await conn.execute(f'DROP DATABASE {self.database}')
                    db_exists = False
                
                if not db_exists:
                    await conn.execute(f'CREATE DATABASE {self.database}')
            finally:
                await conn.close()

        self.pool = await asyncpg.create_pool(f'{self.server_dsn}/{self.database}')
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("""
                    CREATE EXTENSION IF NOT EXISTS vector;
                    CREATE TABLE IF NOT EXISTS doc_sections (
                        id serial PRIMARY KEY,
                        url text NOT NULL UNIQUE,
                        title text NOT NULL,
                        content text NOT NULL,
                        embedding vector(1536) NOT NULL
                    );
                    CREATE INDEX IF NOT EXISTS idx_doc_sections_embedding 
                    ON doc_sections USING hnsw (embedding vector_l2_ops);
                """)

    async def insert(self, url: str, title: str, content: str, embedding: List[float]) -> None:
        embedding_json = pydantic_core.to_json(embedding).decode()
        await self.pool.execute(
            'INSERT INTO doc_sections (url, title, content, embedding) VALUES ($1, $2, $3, $4)',
            url, title, content, embedding_json
        )

    async def search(self, embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        query = '''
            SELECT url, title, content, 
                   1 / (1 + (embedding <-> $1)) as similarity,
                   embedding <-> $1 as distance
            FROM doc_sections 
            ORDER BY embedding <-> $1 
            LIMIT $2
        '''
        embedding_json = pydantic_core.to_json(embedding).decode()
        logger.info(f"Executing vector search query with limit {limit}")
        logger.debug(f"Vector search query: {query}")
        
        rows = await self.pool.fetch(query, embedding_json, limit)
        results = [dict(row) for row in rows]
        
        for result in results:
            logger.info(f"Found match: {result['title']} (L2 distance: {result['distance']:.4f}, similarity: {result['similarity']:.4f})")
            
        return [{k: v for k, v in r.items() if k not in ['distance', 'similarity']} for r in results]

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()

class FaissVectorStore(VectorStore):
    def __init__(self, path: str = "./faiss"):
        self.path = path
        self.index = None
        self.documents = []
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        """Ensure the FAISS directory exists."""
        os.makedirs(self.path, exist_ok=True)

    async def initialize(self, recreate: bool = False) -> None:
        index_path = os.path.join(self.path, "docs.index")
        docs_path = os.path.join(self.path, "docs.npy")

        logger.info(f"Initializing FAISS vector store at {self.path}")
        logger.info(f"Index path: {index_path}")
        logger.info(f"Documents path: {docs_path}")

        if recreate:
            if os.path.exists(index_path):
                logger.info(f"Removing existing index file: {index_path}")
                os.remove(index_path)
            if os.path.exists(docs_path):
                logger.info(f"Removing existing documents file: {docs_path}")
                os.remove(docs_path)

        if os.path.exists(index_path) and os.path.exists(docs_path):
            logger.info("Loading existing FAISS index and documents")
            try:
                self.index = faiss.read_index(index_path)
                self.documents = list(np.load(docs_path, allow_pickle=True))
                logger.info(f"Successfully loaded FAISS index with {len(self.documents)} documents")
                logger.info(f"Index dimension: {self.index.d}, total vectors: {self.index.ntotal}")
            except Exception as e:
                logger.error(f"Failed to load existing FAISS index: {e}")
                raise RuntimeError(f"FAISS index loading failed: {e}")
        else:
            logger.info("Creating new FAISS index")
            try:
                self.index = faiss.IndexFlatL2(1536)  # 1536 is the dimension of text-embedding-3-small
                self.documents = []
                logger.info("Successfully created new FAISS index with dimension 1536")
            except Exception as e:
                logger.error(f"Failed to create new FAISS index: {e}")
                raise RuntimeError(f"FAISS index creation failed: {e}")

    async def insert(self, url: str, title: str, content: str, embedding: List[float]) -> None:
        logger.info(f"Inserting new document: {title}")
        logger.debug(f"Document URL: {url}")
        logger.debug(f"Content length: {len(content)} characters")
        
        try:
            embedding_array = np.array([embedding], dtype=np.float32)
            logger.debug(f"Embedding shape: {embedding_array.shape}")
            
            self.index.add(embedding_array)
            self.documents.append({"url": url, "title": title, "content": content})
            
            logger.info(f"Successfully added document to index. Total documents: {len(self.documents)}")
            
            # Save after each insert
            index_path = os.path.join(self.path, "docs.index")
            docs_path = os.path.join(self.path, "docs.npy")
            
            logger.info("Saving updated index and documents to disk")
            faiss.write_index(self.index, index_path)
            np.save(docs_path, self.documents)
            logger.info("Successfully saved index and documents")
            
        except Exception as e:
            logger.error(f"Failed to insert document: {e}")
            raise RuntimeError(f"Document insertion failed: {e}")

    async def search(self, embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        logger.info(f"Searching FAISS index with limit={limit}")
        logger.debug(f"Index contains {self.index.ntotal} vectors")
        
        try:
            embedding_array = np.array([embedding], dtype=np.float32)
            logger.debug(f"Search vector shape: {embedding_array.shape}")
            
            distances, indices = self.index.search(embedding_array, limit)
            logger.debug(f"Search returned {len(indices[0])} results")
            logger.debug(f"Distances: {distances[0]}")
            
            results = []
            for i, idx in enumerate(indices[0]):
                if idx != -1:  # FAISS returns -1 for empty slots
                    doc = self.documents[idx]
                    doc['similarity_score'] = float(1 / (1 + distances[0][i]))  # Convert distance to similarity
                    results.append(doc)
                    logger.info(f"Result {i+1}: {doc['title']} (L2 distance: {distances[0][i]:.4f}, similarity: {doc['similarity_score']:.4f})")
                else:
                    logger.debug(f"Result {i+1}: Empty slot")
            
            logger.info(f"Returning {len(results)} matching documents")
            return [{k: v for k, v in r.items() if k != 'similarity_score'} for r in results]
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise RuntimeError(f"FAISS search failed: {e}")

    async def close(self) -> None:
        if self.index is not None:
            faiss.write_index(self.index, os.path.join(self.path, "docs.index"))
            np.save(os.path.join(self.path, "docs.npy"), self.documents)

class ChromaVectorStore(VectorStore):
    MAX_RETRIES = 3  # Class constant for retry attempts
    
    def __init__(self, path: str = "./chromadb", collection: str = "default_collection"):
        self.path = path
        self.client = None
        self.collection = collection
        self._ensure_dir()

    def _print_collection_stats(self) -> None:
        """Print statistics about ChromaDB collections and counts."""
        if self.client:
            collections = self.client.list_collections()
            logger.info(f"ChromaDB contains {len(collections)} collections:")
            for coll in collections:
                count = coll.count()
                logger.info(f"Collection '{coll.name}': {count} embeddings")
                
    def _ensure_dir(self) -> None:
        """Ensure the ChromaDB directory exists and is writable."""
        abs_path = os.path.abspath(self.path)
        try:
            os.makedirs(abs_path, exist_ok=True)
            # Test write permissions by creating and removing a test file
            test_file = os.path.join(abs_path, '.write_test')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            logger.info("Tested recreated folder...")
        except (OSError, IOError) as e:
            logger.error(f"Failed to create/access ChromaDB directory at {abs_path}: {e}")
            raise RuntimeError(f"ChromaDB directory {abs_path} is not accessible: {e}")

    async def initialize(self, recreate: bool = False) -> None:
        abs_path = os.path.abspath(self.path)
        
        try:
            # If recreating and path exists, delete the entire directory
            if recreate and os.path.exists(abs_path):
                logger.info(f"Deleting existing ChromaDB directory: {abs_path}")
                try:
                    for root, dirs, files in os.walk(abs_path, topdown=False):
                        for name in files:
                            os.remove(os.path.join(root, name))
                        for name in dirs:
                            os.rmdir(os.path.join(root, name))
                    os.rmdir(abs_path)
                    self._ensure_dir()  # Recreate the directory
                except Exception as e:
                    logger.error(f"Failed to recreate ChromaDB directory: {e}")
                    raise
            
            logger.info(f"Initializing ChromaDB at: {abs_path}")
            
            # Initialize client with simpler configuration
            try:
                # https://github.com/langchain-ai/langchain/issues/26884
                chromadb.api.client.SharedSystemClient.clear_system_cache()
                settings = chromadb.Settings(
                    is_persistent=True,
                    persist_directory=abs_path,
                    anonymized_telemetry=False
                )
                self.client = chromadb.Client(settings)
                logger.info(f"Successfully initialized ChromaDB client with persist_directory: {abs_path}")
                self._print_collection_stats()
            except Exception as e:
                logger.error(f"Failed to initialize ChromaDB client: {e}")
                raise RuntimeError(f"ChromaDB initialization failed: {e}")
            
            # Handle collection management
            try:
                existing_collections = self.client.list_collections()
                collection_exists = "doc_sections" in [c.name for c in existing_collections]

                if recreate and collection_exists:
                    self.client.delete_collection("doc_sections")
                    logger.info("Deleted existing ChromaDB collection 'doc_sections'")
                    collection_exists = False

                for attempt in range(self.MAX_RETRIES):
                    try:
                        if collection_exists:
                            self.collection = self.client.get_collection("doc_sections")
                            logger.info(f"Retrieved existing ChromaDB collection 'doc_sections' at: {abs_path}")
                        else:
                            self.collection = self.client.create_collection(
                                name="doc_sections",
                                metadata={"hnsw:space": "l2"}
                            )
                            logger.info(f"Created new ChromaDB collection 'doc_sections' at: {abs_path}")
                        self._print_collection_stats()
                        break
                    except Exception as e:
                        if attempt == self.MAX_RETRIES - 1:
                            logger.error(f"Failed to create collection after {self.MAX_RETRIES} attempts: {e}")
                            raise
                        logger.warning(f"Attempt {attempt + 1} failed, retrying collection creation...")
                        await asyncio.sleep(1)
            except Exception as e:
                logger.exception(e)
        except Exception as e:
            logger.error(f"Critical error during ChromaDB initialization: {e}")
            raise RuntimeError(f"Failed to initialize ChromaDB: {e}")

    async def insert(self, url: str, title: str, content: str, embedding: List[float]) -> None:
        self.collection.add(
            embeddings=[embedding],
            documents=[content],
            metadatas=[{"url": url, "title": title}],
            ids=[url]  # Using URL as unique ID
        )

    async def search(self, embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        logger.info("Current ChromaDB statistics before search:")
        self._print_collection_stats()
        
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=limit,
            include_distances=True
        )
        
        documents = []
        for i, (meta, doc, distance) in enumerate(zip(
            results["metadatas"][0], 
            results["documents"][0],
            results["distances"][0]
        )):
            similarity = 1 / (1 + distance)
            logger.info(f"Result {i+1}: {meta['title']} (L2 distance: {distance:.4f}, similarity: {similarity:.4f})")
            documents.append({
                "url": meta["url"],
                "title": meta["title"],
                "content": doc
            })
        return documents

    async def close(self) -> None:
        # ChromaDB handles cleanup automatically
        pass

def get_vector_store(vector_db_type: str = "postgres") -> VectorStore:
    vector_db_type = vector_db_type.lower()
    if vector_db_type == "chromadb":
        return ChromaVectorStore()
    elif vector_db_type == "faiss":
        return FaissVectorStore()
    return PostgresVectorStore(
        dsn='postgresql://postgres:postgres@localhost:54320',
        database='pydantic_ai_rag'
    )
