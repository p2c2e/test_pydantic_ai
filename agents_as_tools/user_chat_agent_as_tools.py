import datetime
from typing import Optional

from dotenv import load_dotenv
from pydantic_ai import Agent

from agent_utils import register_agent_as_tool
from filesurfer_agent import create_filesurfer_agent, FileSurferState
from websurfer_agent import create_websurfer_agent, BrowserState

load_dotenv()

user_proxy = Agent(
    'openai:gpt-4o-mini',
    deps_type=Optional[str], # type: ignore
    result_type=str,  # type: ignore
    system_prompt=(
        f"You are an helpful AI assistant who has extensive general knowledge. Today is {datetime.date.today()}"
    ),
)

from pydantic_ai.messages import ModelRequest, ModelResponse

# Create the web_surfer agent
web_surfer = create_websurfer_agent()

# Register the web_surfer agent as a tool in the user_proxy agent
if web_surfer is not None:
    def deps_fn():
        return BrowserState()
    register_agent_as_tool(user_proxy, web_surfer, deps_fn)
else:
    raise ValueError("Failed to create web_surfer agent")


file_surfer =  create_filesurfer_agent()
if file_surfer is not None:
    def deps_fn():
        return FileSurferState(current_dir="/tmp")
    register_agent_as_tool(user_proxy, file_surfer, deps_fn)

history: list[ModelRequest | ModelResponse] | None = []
while True:
    query = input("Begin> ")
    if query.lower().strip() == 'quit':
        break
    else:
        result = user_proxy.run_sync(query, message_history=history)
        # print(result)

        history += result.new_messages()
        history = history[-3:]
        print(result.data)
