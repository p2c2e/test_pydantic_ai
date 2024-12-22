from typing import Union, Optional

from pydantic import BaseModel

from pydantic_ai import Agent, RunContext, ModelRetry

from dotenv import load_dotenv

load_dotenv()

class Box(BaseModel):
    width: int
    height: int
    depth: int
    units: str


user_proxy: Agent[None, Union[Box, str]] = Agent(
    'openai:gpt-4o-mini',
    deps_type=Optional[str], # type: ignore
    result_type=str,  # type: ignore
    system_prompt=(
        "You are an helpful AI assistant who has extensive general knowledge"
    ),
    result_retries=10,
)


@user_proxy.result_validator
async def validate_result(ctx: RunContext[str], agent_result: str) -> Box:
    if agent_result.lower().strip() == "quit":
        exit(0)
    print(agent_result)
    query = input("User> ")
    raise ModelRetry(f'{query}')

query = input("Begin> ")
result = user_proxy.run_sync(query)
print(result.data)