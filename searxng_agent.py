"""SearxNG search agent implementation."""
import os
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import asyncio
import httpx
from urllib.parse import urlencode
from typing import Union, Optional
import json

from dotenv import load_dotenv
load_dotenv(verbose=True)

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext


class SearxNGSearchParams(BaseModel):
    """Search parameters for SearxNG API."""
    q: str  # Required: search query
    categories: Optional[List[str]] = None  # Optional: comma-separated list of categories
    engines: Optional[List[str]] = None  # Optional: comma-separated list of engines
    lang: str = "all"  # Default: all
    pageno: int = 1  # Default: 1
    time_range: Optional[str] = None  # Optional: day, month, year
    format: str = "json"  # Default: json (json, csv, rss)
    safesearch: Optional[int] = None  # Optional: 0, 1, 2 (0=None, 1=Moderate, 2=Strict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "q": "python programming",
                "categories": ["it", "science"],
                "time_range": "month",
                "safesearch": 1
            }
        }

async def search_searxng(
    query: str,
    host_url: str = "https://searx.be",  # Default public instance
    **kwargs
) -> Dict[str, Any]:
    """
    Search using SearxNG API.
    
    Args:
        query: Search query string
        host_url: SearxNG instance URL
        **kwargs: Additional search parameters matching SearxNGSearchParams fields
        
    Returns:
        Dict containing search results and metadata
    """
    # Create search params object with query and any overrides
    params = SearxNGSearchParams(q=query)
    for k, v in kwargs.items():
        if hasattr(params, k):
            setattr(params, k, v)
            
    # Build query parameters
    query_params = {"q": params.q, "format": params.format}
    
    if params.categories:
        query_params["categories"] = ",".join(params.categories)
    if params.engines:
        query_params["engines"] = ",".join(params.engines)
    if params.lang:
        query_params["lang"] = params.lang
    if params.pageno:
        query_params["pageno"] = params.pageno
    if params.time_range:
        query_params["time_range"] = params.time_range
    if params.safesearch is not None:
        query_params["safesearch"] = params.safesearch

    # Ensure host URL doesn't end with slash
    host_url = host_url.rstrip("/")
    
    # Make request to SearxNG instance
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{host_url}/search",
            params=query_params,
            headers={
                "User-Agent": "searxng-python-client/1.0",
                "Accept": "application/json"
            }
        )
        response.raise_for_status()
        return response.json()

searx_agent: Agent[Union[SearxNGSearchParams], List] = Agent(
    'openai:gpt-4o', # 'openai:gpt-4o-mini'
    # deps_type=Optional[GeneralQuery], # type: ignore
    # result_type=str,  # type: ignore
    system_prompt=(
        "You are an helpful AI Search assistant who can help people find more information from variety of sources."
        "You will use the searx tool to find relevant results and then take the top 5 results to share further."
        "While the q (query) in the param object is mandatory, all other fields are optional"
    ),
)

@searx_agent.tool
async def searx_tool(ctx: RunContext[SearxNGSearchParams], query: str) -> Dict:
    try:
        # Example search with some parameters
        results = await search_searxng(
            query=query,
            host_url=os.getenv("SEARX_URL", "http://localhost:58080"),
            categories=ctx.deps.categories if ctx.deps.categories else [],
            time_range=ctx.deps.time_range if ctx.deps.time_range else "month",
            safesearch=1
        )

        # Pretty print results
        print("Search Results:")
        print(json.dumps(results, indent=2))
        return results
    except httpx.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        raise e
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e



# def create_agent_with_tools():
#     searx_agent: Agent[Union[SearxNGSearchParams], List] = Agent(
#         'openai:gpt-4o', # 'openai:gpt-4o-mini'
#         # deps_type=Optional[GeneralQuery], # type: ignore
#         # result_type=str,  # type: ignore
#         system_prompt=(
#             "You are an helpful AI Search assistant who can help people find more information from variety of sources."
#             "You will use the searx tool to find relevant results and then take the top 5 results to share further."
#             "While the q (query) in the param object is mandatory, all other fields are optional"
#         ),
#     )
#
#     async def searx_tool(ctx: RunContext[SearxNGSearchParams], query: str) -> Dict:
#         try:
#             # Example search with some parameters
#             results = await search_searxng(
#                 query=query,
#                 host_url=os.getenv("SEARX_URL", "http://localhost:58080"),
#                 categories=ctx.deps.categories if ctx.deps.categories else [],
#                 time_range=ctx.deps.time_range if ctx.deps.time_range else "month",
#                 safesearch=1
#             )
#
#             # Pretty print results
#             print("Search Results:")
#             print(json.dumps(results, indent=2))
#             return results
#         except httpx.HTTPError as e:
#             print(f"HTTP error occurred: {e}")
#             raise e
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             raise e
#
#     # Add the tool to the agent
#     searx_agent.add_tool(searx_tool)
#
#     return searx_agent




async def main():
    """Example usage of SearxNG search."""
    import json
    import asyncio
    
    try:
        # Example search with some parameters
        results = await search_searxng(
            query="python programming",
            host_url="http://localhost:58080",
            categories=["it", "science"],
            time_range="month",
            safesearch=1
        )
        
        # Pretty print results
        print("Search Results:")
        print(json.dumps(results, indent=2))
        
    except httpx.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


async def main_agent():
    args = SearxNGSearchParams(q="IGNORED")
    results = await searx_agent.run("Who were the top 3 medalists in the 2024 olympics 100m mens running? GIve me just the names", deps=args)
    print(results.data)


if __name__ == "__main__":
    # asyncio.run(main())
    asyncio.run(main_agent())
