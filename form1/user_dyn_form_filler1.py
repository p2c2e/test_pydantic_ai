from typing import Union, Optional, Any

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



def create_form_agent(form_model: type[BaseModel], topic: str) -> Agent[None, Union[BaseModel, str]]:
    """Create an agent for handling form filling based on a Pydantic model.
    
    Args:
        form_model: The Pydantic model class defining the form structure
        
    Returns:
        An configured Agent instance for form filling
    """
    return Agent(
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
        result_retries=15, # Number of attempts to get the form details ... Can we keep this dynamic?
    )



def run_form_dialog():
    """Run an interactive form filling dialog with the user."""

    #1 : Create a Form Model
    class FormDetails(BaseModel):
        name: str
        age: int
        city: Optional[str] = None

    #2 : Create an Agent for the Model
    agent = create_form_agent(FormDetails, "User Demographics")


    #3 Write any validation logic...
    @agent.result_validator
    async def validate_result(ctx: RunContext[Any], agent_result: Union[FormDetails, str]) -> FormDetails:
        print("validate_result called ....")
        if isinstance(agent_result, FormDetails):

            # We can do more complicated validation on what is mandatory, optional, valid values etc.
            if agent_result.age < 18:
                raise ValueError("Age must be at least 18") # Abruptly ends..

            if agent_result.city and agent_result.city.lower() == "pisa":
                raise ModelRetry("Pisa folks are not allowed. Pick a different city") # Chance to recover

            return agent_result
        else:
            # If we get a string, it means the agent needs more information
            print(f"\nAgent: {agent_result}")
            user_input = input("You: ")
            raise ModelRetry(user_input)

    print("Welcome to the form filling assistant! (Type 'quit' to exit)")
    history = []
    
    initial_prompt = input("You: ")
    if initial_prompt.lower().strip() == 'quit':
        return
        
    try:
        result = agent.run_sync(initial_prompt, message_history=history)
        print(f"\nForm completed successfully:\n{result.data}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    run_form_dialog()