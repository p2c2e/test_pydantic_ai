from typing import Union, Optional

from pydantic import BaseModel

from pydantic_ai import Agent, RunContext, ModelRetry

from dotenv import load_dotenv

load_dotenv(verbose=True)

class GeneralQuery(BaseModel):
    query: str
    results : list[str]


user_proxy: Agent[None, Union[GeneralQuery, str]] = Agent(
    'openai:gpt-4o-mini',
    deps_type=Optional[GeneralQuery], # type: ignore
    result_type=str,  # type: ignore
    system_prompt=(
        "You are an helpful AI assistant who has extensive general knowledge. If the user asks questions that "
        "require latest information, you will use the search tool to find that out.  Make sure you use Indian currency"
    ),
)

hyde_agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=str,
    result_type=str,
    system_prompt=(
        "You are an helpful AI assistant who can expand a given user query into Two possible alternate queries."
        " You will return the list of possible queries with one potential answer for it."
    ),
)

@user_proxy.tool
async def curr_convertor(ctx: RunContext[GeneralQuery], amount: float, source_code: str, target_code: str) -> float:
    """Convert currency from one code to another.

    Args:
        ctx (RunContext[GeneralQuery]): The run context containing GeneralQuery information
        amount (float): The amount to convert
        source_code (str): The source currency code (e.g. 'USD')
        target_code (str): The target currency code (e.g. 'INR')

    Returns:
        (float): The converted amount in target currency
    """
    print(f"{amount} - From {source_code} to {target_code}")
    return amount * 80.0

@user_proxy.tool
async def search(ctx: RunContext[GeneralQuery], query: str) -> str:
    """Search the web for information based on the given query.

    Args:
        ctx (RunContext[GeneralQuery]): The run context containing GeneralQuery information
        query (str): The search query string

    Returns:
        (str): The search results as a formatted string
    """
    print(f"Searching the web with query {query}")
    # hyde = await hyde_agent.run(query)
    # print(hyde.data)
    return "Latest share price of GOOGLE is 1027.9 USD"+ "\n"

from pydantic_ai.messages import ModelRequest, ModelResponse

history : list[ModelRequest | ModelResponse] | None = []
result = user_proxy.run_sync("What is Google share price?", message_history=history)
print(result.data)
# while True:
#     query = input("Begin> ")
#     if query.lower().strip() == 'quit':
#         break
#     else:
#         result = user_proxy.run_sync(query, message_history=history)
#         # print(result)
#         history += result.new_messages()
#         history = history[-3:]
#         print(result.data)
