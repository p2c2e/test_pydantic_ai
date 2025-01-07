from typing import Union, Optional, Any, Callable, Tuple

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext, ModelRetry

from input_sources import InputSource, TerminalInputSource

import rag_agent

load_dotenv(verbose=True)

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



async def create_form_agent(
    form_model: type[BaseModel], 
    topic: str,
    input_source: InputSource,
    validator: Callable[[BaseModel], None] = None
) -> Tuple[Agent[None, Union[BaseModel, str]], Callable]:
    """Create an agent for handling form filling based on a Pydantic model.
    
    Args:
        form_model: The Pydantic model class defining the form structure
        topic: The topic of the form
        input_source: Source for getting user input
        
    Returns:
        A tuple of (configured Agent instance, validator function)
    """
    agent = Agent(
        'openai:gpt-4o-mini',
        deps_type=str,  # type: ignore
        result_type=Union[form_model, str],  # type: ignore
        system_prompt=(
            f"You are an AI Form filling expert."
            f"Start the conversation by greeting the user and mentioning you are trying gather information about {topic}"
            f"Earliest possible chance, mention the names of a few fields you want from the User"
            f"then Extract the {form_model.__name__} fields from user input. "
            "If you are not able to complete the form with all data, ask for the missing data. "
            "You can skip Optional items in the data. "
            "Do not bother 'reconfirming' with details. If you have sufficient information, just complete the exercise."
        ),
        result_retries=15,
    )

    async def validate_result(ctx: RunContext[Any], agent_result: Union[form_model, str]) -> form_model:
        if isinstance(agent_result, form_model):
            if validator:
                validator(agent_result)
            return agent_result
        else:
            print(f"\nAgent: {agent_result}")
            user_input = await input_source.get_input("You: ")
            raise ModelRetry(user_input)

    agent.result_validator(validate_result)
    return agent, validate_result





async def run_form_dialog(input_source: InputSource = None):
    """Run an interactive form filling dialog with the user."""
    if input_source is None:
        input_source = TerminalInputSource()

    class FormDetails(BaseModel):
        name: str
        age: int
        city: Optional[str] = None

    def my_validator(form_data: FormDetails) -> None:
        """Default validation rules for form data"""
        if hasattr(form_data, 'age') and form_data.age < 18:
            raise ValueError("Age must be at least 18")
        if hasattr(form_data, 'city') and form_data.city and form_data.city.lower() == "pisa":
            raise ModelRetry("Pisa folks are not allowed. Pick a different city")

    agent, _ = await create_form_agent(
        FormDetails, 
        "User Demographics", 
        input_source,
        validator=my_validator
    )
    history = []
    
    initial_prompt = await input_source.get_input("You: ")
    if initial_prompt.lower().strip() == 'quit':
        return
        
    try:
        result = await agent.run(initial_prompt, message_history=history)
        print(f"\nForm completed successfully:\n{result.data}")
        return result.data
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    import asyncio
    
    # Example of using terminal input
    asyncio.run(run_form_dialog())
    
    # Example of using callback input
    # async def example_with_callback():
    #     def web_callback(prompt: str) -> str:
    #         # This could be replaced with actual web form handling
    #         return "John Doe, 25, New York"
    #     
    #     from input_sources import CallbackInputSource
    #     callback_source = CallbackInputSource(web_callback)
    #     await run_form_dialog(callback_source)
    # 
    # asyncio.run(example_with_callback())
