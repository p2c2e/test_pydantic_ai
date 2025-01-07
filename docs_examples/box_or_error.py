from typing import Union

from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel

from pydantic_ai import Agent, RunContext, ModelRetry




class Box(BaseModel):
    width: int
    height: int
    depth: int
    units: str


agent: Agent[None, Union[Box, str]] = Agent(
    'openai:gpt-4o-mini',
    deps_type=str, # type: ignore
    result_type=Union[Box, str],  # type: ignore
    system_prompt=(
        "Extract me the dimensions of a box, "
        "if you can't extract all data, ask the user to try again."
    ),
    result_retries=2,
)

@agent.result_validator
async def validate_result(ctx: RunContext[Union[Box, str]], agent_result: Box) -> Box:
    if isinstance(agent_result, Box):
        return agent_result
    else:
        print(f"{ctx.deps}")
        for msg in ctx.messages:
            print(type(msg))
            # ctx.messages.append(Message(content=""))
            print(msg)
        print('.'*50)
        ctx.deps = "The box is 20x30x40 cm in size"
        raise ModelRetry(f'he box is 20x30x40 cm')

result = agent.run_sync('The box is 10x20x30')
print(result.data)
#> Please provide the units for the dimensions (e.g., cm, in, m).

result = agent.run_sync('The box is 10x20x30 cm')
print(result.data)
#> width=10 height=20 depth=30 units='cm'
