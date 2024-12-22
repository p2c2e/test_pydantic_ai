import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import chromadb
import asyncpg
import pydantic_core
import logging

logger = logging.getLogger(__name__)

class VectorStore(ABC):
    @abstractmethod
    async def initialize(self, recreate: bool = False) -> None:
        pass

    @abstractmethod
    async def insert(self, url: str, title: str, content: str, embedding: List[float]) -> None:
        pass

    @abstractmethod
    async def search(self, embedding: List[float], limit: int = 8) -> List[Dict[str, Any]]:
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

    async def search(self, embedding: List[float], limit: int = 8) -> List[Dict[str, Any]]:
        query = '''
            SELECT url, title, content, 
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
            logger.info(f"Found match: {result['title']} (distance: {result['distance']:.4f})")
            
        return [{k: v for k, v in r.items() if k != 'distance'} for r in results]

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()

class ChromaVectorStore(VectorStore):
    def __init__(self, path: str = "./chromadb"):
        self.path = path
        self.client = None
        self.collection = None

    async def initialize(self, recreate: bool = False) -> None:
        abs_path = os.path.abspath(self.path)
        
        # If recreating and path exists, delete the entire directory
        if recreate and os.path.exists(abs_path):
            import shutil
            logger.info(f"Deleting existing ChromaDB directory: {abs_path}")
            shutil.rmtree(abs_path)
        
        os.makedirs(abs_path, exist_ok=True)
        logger.info(f"Initializing ChromaDB at: {abs_path}")
        
        self.client = chromadb.PersistentClient(path=abs_path)
        
        # Always try to delete collection if it exists
        try:
            self.client.delete_collection("doc_sections")
            logger.info("Deleted existing ChromaDB collection 'doc_sections'")
        except ValueError:
            logger.info("No existing collection to delete")

        # Create fresh collection
        self.collection = self.client.create_collection(
            name="doc_sections",
            metadata={"hnsw:space": "l2"}
        )
        logger.info(f"Created new ChromaDB collection 'doc_sections' at: {abs_path}")

    async def insert(self, url: str, title: str, content: str, embedding: List[float]) -> None:
        self.collection.add(
            embeddings=[embedding],
            documents=[content],
            metadatas=[{"url": url, "title": title}],
            ids=[url]  # Using URL as unique ID
        )

    async def search(self, embedding: List[float], limit: int = 8) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=limit
        )
        
        return [
            {
                "url": meta["url"],
                "title": meta["title"],
                "content": doc
            }
            for meta, doc in zip(results["metadatas"][0], results["documents"][0])
        ]

    async def close(self) -> None:
        # ChromaDB handles cleanup automatically
        pass

def get_vector_store(vector_db_type: str = "postgres") -> VectorStore:
    if vector_db_type.lower() == "chromadb":
        return ChromaVectorStore()
    return PostgresVectorStore(
        dsn='postgresql://postgres:postgres@localhost:54320',
        database='pydantic_ai_rag'
    )
