from pydantic_ai import Agent, RunContext, Tool
from typing import Any

def register_agent_as_tool(caller: Agent, new_agent: Agent) -> None:
    """
    Register the run_sync method of new_agent as a tool in the caller agent.

    Args:
        caller: The agent instance that will have the new tool registered.
        new_agent: The agent whose run_sync method will be registered as a tool.
    """
    async def new_agent_tool(ctx: RunContext[Any], user_prompt: str) -> str:
        """
        Tool function that wraps the new_agent's run_sync method.
        
        Args:
            ctx: The run context.
            user_prompt: The user prompt to pass to the new_agent.
        
        Returns:
            The result from the new_agent's run_sync method.
        """
        result = new_agent.run_sync(user_prompt)
        return result.data

    # Create a Tool instance using the new_agent's metadata
    tool = Tool(
        function=new_agent_tool,
        name=new_agent.name or "new_agent_tool",
        description=new_agent.system_prompt or "Tool wrapping new_agent's run_sync method."
    )

    # Register the tool with the caller agent
    caller._register_tool(tool)
