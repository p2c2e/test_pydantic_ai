from typing import Any, Callable

from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel


def get_model():
    # return OpenAIModel(
    #     'deepseek-chat',
    #     base_url='https://api.deepseek.com',
    #     api_key=os.environ['DEEPSEEK_API_KEY']
    # )
    return "openai:gpt-4o"

def register_agent_as_tool(caller: Agent, new_agent: Agent, deps_fn: Callable[[], Any]) -> None:
    """
    Register the run_sync method of new_agent as a tool in the caller agent.

    Args:
        caller: The agent instance that will have the new tool registered.
        new_agent: The agent whose run_sync method will be registered as a tool.
        deps_fn: function to call for creating a deps object
    """

    # Determine the tool name
    tool_name = new_agent.name or new_agent.__class__.__name__ or f"new_agent_tool_{uuid.uuid4()}"

    # Create the docstring by combining the system prompt and tool docstrings
    all_tool_docstrings = "\n".join(
        tool.description for tool in new_agent._function_tools.values()
    )

    agent_docstring = "\n".join(new_agent._system_prompts)
    tools_docstring = f"And I can help you with the following types of tasks:\n{all_tool_docstrings}"
    new_agent_tools_docstring = (f"{agent_docstring}\n\n"+tools_docstring)

    def create_tool_closure():
        deps = deps_fn()
        async def new_agent_tool(ctx: RunContext[Any], user_prompt: str) -> str:
            """{new_agent_tool_docstring}"""
            print(f"{tool_name} wrapper function called ..........{user_prompt}")
            result = await new_agent.run(user_prompt, deps=deps)
            return result.data
        return new_agent_tool

    new_agent_tool = create_tool_closure()

    # Set the docstring for the new_agent_tool function
    new_agent_tool.__doc__ = new_agent_tools_docstring
    print(new_agent)
    print(new_agent.name)
    print(agent_docstring)
    print(tools_docstring)
    # print(new_agent.system_prompt())
    print("#"*50)
    # Create a Tool instance using the new_agent's metadata
    import uuid



    tool = Tool(
        # takes_ctx=False,
        function=new_agent_tool,
        name=tool_name,
        description=agent_docstring
    )
    print(tool)
    print("~"*50)

    # Register the tool with the caller agent
    caller._register_tool(tool)
