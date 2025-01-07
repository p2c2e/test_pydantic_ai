from typing import Union, Optional

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

import rag_agent

load_dotenv(verbose=True)

from pydantic_ai import Agent, RunContext, ModelRetry

import logging
import os

logger = logging.getLogger()
if os.getenv("LOG_ENABLED", "").lower() in ("true", "1", "yes"):
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
else:
    logger.addHandler(logging.NullHandler())
    logger.setLevel(logging.CRITICAL)

class FormDetails(BaseModel):
    name: str
    age: int
    city: Optional[str] = None

class AgentDeps(BaseModel):
    form: FormDetails
    user_input: str


agent: Agent[None, Union[FormDetails, str]] = Agent(
    'openai:gpt-4o-mini',
    deps_type=str, # type: ignore
    result_type=Union[FormDetails, str],  # type: ignore
    system_prompt=(
        "Extract me the FormDetails fields from user input"
        "if you are not able to complete the form with all data, ask the for the missing data."
        "You can skip Optional items in the data. "
        "Do not bother 'reconfirming' with details. If you have sufficient information. Just complete the exercise"
    ),
    result_retries=5,
)

@agent.result_validator
async def validate_result(ctx: RunContext[AgentDeps], agent_result: Union[FormDetails, str]) -> FormDetails:
    if isinstance(agent_result, FormDetails):
        # We can do more complicated validation on what is mandatory, optional, valid values etc.
        return agent_result
    else:
        logger.info(f"{ctx.deps}")
        # for msg in ctx.messages:
        #     logger.info(type(msg))
        #     # ctx.messages.append(Message(content=""))
        #     logger.info(msg)
        # logger.info('.'*50)
        print(agent_result)
        new_user_input =  "I am Sudhan, based in Bangalore, born in Jan 1 1954"
        raise ModelRetry(new_user_input)

result = agent.run_sync('I am Sudhan, aged around 60 years')
print(result.data)
# #> Please provide the units for the dimensions (e.g., cm, in, m).
#
# result = agent.run_sync('The FormDetails is 10x20x30 cm')
# logger.info(result.data)
# #> width=10 height=20 depth=30 units='cm'
#
# MAIN_SYSTEM_PROMPT = """
# You are a AWS Cloud Migration Expert who helps users with their questions on
#     Cloud Migration to AWS Services. You should use the search tool to find the answer for the user question.
#     Be as specific as possible with citations in the document.
#     If an answer is a) not available in the Knowledgebase, b) when asked about Azure or Google, GCP etc. or
#     c) if the answers are not available in the conversational history, then politely decline to answer and
#     instead suggest that they visit https://aws.amazon.com/migrate-modernize-build/cloud-migration/how-to-migrate/
#     """
#
# user_proxy: Agent[None, Union[GeneralQuery, str]] = Agent(
#     'openai:gpt-4o', # 'openai:gpt-4o-mini'
#     deps_type=Optional[GeneralQuery], # type: ignore
#     result_type=str,  # type: ignore
#     system_prompt=(
#         MAIN_SYSTEM_PROMPT
#         # "You are an helpful AI assistant who has extensive knowledge on Cloud MIgration. You will use the search "
#         # "the docs for the answers. "
#         # "Topics unrelated to cloud migration or document management, politely refuse to answer"
#     ),
# )
#
# hyde_agent = Agent(
#     'openai:gpt-4o-mini',
#     deps_type=str,
#     result_type=str,
#     system_prompt=(
#         "You are an helpful AI assistant who can expand a given user query into Two possible alternate queries."
#         " You will return the list of possible queries with one potential answer for it."
#     ),
# )
#
# @user_proxy.tool
# async def indexer(ctx: RunContext[GeneralQuery]) -> str:
#     """Reindex the contents of the ./data/ folder.
#
#     Args:
#         ctx (RunContext[GeneralQuery]): The run context containing GeneralQuery information
#
#     Returns:
#         (str): A message indicating success or failure of the reindexing operation
#     """
#     import rag_agent
#     logger.info("Indexing....")
#     try:
#         import os
#         await rag_agent.build_search_db("file:///Users/sudranga1/workspace/test_create_llama/data", os.getenv("VECTOR_DB", "chromadb"))
#     except Exception as e:
#         return f"Failed to index the files due to error {e}"
#
#     return "Successfully indexed files"
#
# @user_proxy.tool
# async def curr_convertor(ctx: RunContext[GeneralQuery], amount: float, source_code: str, target_code: str) -> float:
#     """Convert currency from one code to another.
#
#     Args:
#         ctx (RunContext[GeneralQuery]): The run context containing GeneralQuery information
#         amount (float): The amount to convert
#         source_code (str): The source currency code (e.g. 'USD')
#         target_code (str): The target currency code (e.g. 'INR')
#
#     Returns:
#         (float): The converted amount in target currency
#     """
#     logger.info(f"{amount} - From {source_code} to {target_code}")
#     return amount * 80.0
#
# @user_proxy.tool
# async def search_docs(ctx: RunContext[GeneralQuery], query: str) -> str:
#     """Search the documents for information based on the given query.
#
#     Args:
#         ctx (RunContext[GeneralQuery]): The run context containing GeneralQuery information
#         query (str): The search query string
#
#     Returns:
#         (str): The search results as a formatted string
#     """
#     logger.info(f"Searching the docs with query {query}")
#     import os
#     results = await rag_agent.run_agent(query, vector_db_type=os.getenv("VECTOR_DB", "chromadb"))
#     # hyde = await hyde_agent.run(query)
#     # logger.info(hyde.data)
#     return results
#
#
# from pydantic_ai.messages import ModelRequest, ModelResponse
#
# history : list[ModelRequest | ModelResponse] | None = []
# # result = user_proxy.run_sync("What is Google share price?", message_history=history)
# # logger.info(result.data)
# while True:
#     # rag_agent.build_search_db("file:///Users/sudranga1/workspace/test_create_llama/data", os.getenv("VECTOR_DB", "chromadb"))
#     query = input("Begin> ")
#     if query.lower().strip() == 'quit':
#         break
#     else:
#         result = user_proxy.run_sync(query, message_history=history)
#         # logger.info(result)
#         history += result.new_messages()
#         history = history[-3:]
#         logger.info(result.data)
