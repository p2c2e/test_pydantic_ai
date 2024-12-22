from pydantic_ai import Agent, ModelRetry, UnexpectedModelBehavior

agent = Agent('openai:gpt-4o')


@agent.tool_plain
def calc_volume(size: int) -> int:  # (1)!
    if size == 42:
        return size**3
    else:
        print("Raising Retry")
        raise UnexpectedModelBehavior("WRONG")
#        raise ModelRetry('Please try again.')


try:
    result = agent.run_sync('Please get me the volume of a box with size 6.')
except UnexpectedModelBehavior as e:
    print('An error occurred:', e)
    #> An error occurred: Tool exceeded max retries count of 1
    print('cause:', repr(e.__cause__))
    #> cause: ModelRetry('Please try again.')
    print('messages:', agent.last_run_messages)
    """
    messages:
    [
        ModelRequest(
            parts=[
                UserPromptPart(
                    content='Please get me the volume of a box with size 6.',
                    timestamp=datetime.datetime(...),
                    part_kind='user-prompt',
                )
            ],
            kind='request',
        ),
        ModelResponse(
            parts=[
                ToolCallPart(
                    tool_name='calc_volume',
                    args=ArgsDict(args_dict={'size': 6}),
                    tool_call_id=None,
                    part_kind='tool-call',
                )
            ],
            timestamp=datetime.datetime(...),
            kind='response',
        ),
        ModelRequest(
            parts=[
                RetryPromptPart(
                    content='Please try again.',
                    tool_name='calc_volume',
                    tool_call_id=None,
                    timestamp=datetime.datetime(...),
                    part_kind='retry-prompt',
                )
            ],
            kind='request',
        ),
        ModelResponse(
            parts=[
                ToolCallPart(
                    tool_name='calc_volume',
                    args=ArgsDict(args_dict={'size': 6}),
                    tool_call_id=None,
                    part_kind='tool-call',
                )
            ],
            timestamp=datetime.datetime(...),
            kind='response',
        ),
    ]
    """
else:
    print("="*50)
    print(result.data)
