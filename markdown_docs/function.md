Skip to content

[ ![logo](../../../img/logo-white.svg) ](../../.. "PydanticAI")

PydanticAI

pydantic_ai.models.function

Type to start searching

[ pydantic/pydantic-ai

  * v0.0.14
  * 4.2k
  * 255

](https://github.com/pydantic/pydantic-ai "Go to repository")

[ ![logo](../../../img/logo-white.svg) ](../../.. "PydanticAI") PydanticAI

[ pydantic/pydantic-ai

  * v0.0.14
  * 4.2k
  * 255

](https://github.com/pydantic/pydantic-ai "Go to repository")

  * [ Introduction  ](../../..)
  * [ Installation  ](../../../install/)
  * [ Getting Help  ](../../../help/)
  * [ Contributing  ](../../../contributing/)
  * Documentation  Documentation 
    * [ Agents  ](../../../agents/)
    * [ Models  ](../../../models/)
    * [ Dependencies  ](../../../dependencies/)
    * [ Function Tools  ](../../../tools/)
    * [ Results  ](../../../results/)
    * [ Messages and chat history  ](../../../message-history/)
    * [ Testing and Evals  ](../../../testing-evals/)
    * [ Debugging and Monitoring  ](../../../logfire/)
  * [ Examples  ](../../../examples/)

Examples

    * [ Pydantic Model  ](../../../examples/pydantic-model/)
    * [ Weather agent  ](../../../examples/weather-agent/)
    * [ Bank support  ](../../../examples/bank-support/)
    * [ SQL Generation  ](../../../examples/sql-gen/)
    * [ RAG  ](../../../examples/rag/)
    * [ Stream markdown  ](../../../examples/stream-markdown/)
    * [ Stream whales  ](../../../examples/stream-whales/)
    * [ Chat App with FastAPI  ](../../../examples/chat-app/)
  * API Reference  API Reference 
    * [ pydantic_ai.Agent  ](../../agent/)
    * [ pydantic_ai.tools  ](../../tools/)
    * [ pydantic_ai.result  ](../../result/)
    * [ pydantic_ai.messages  ](../../messages/)
    * [ pydantic_ai.exceptions  ](../../exceptions/)
    * [ pydantic_ai.settings  ](../../settings/)
    * [ pydantic_ai.models  ](../base/)
    * [ pydantic_ai.models.openai  ](../openai/)
    * [ pydantic_ai.models.anthropic  ](../anthropic/)
    * [ pydantic_ai.models.gemini  ](../gemini/)
    * [ pydantic_ai.models.vertexai  ](../vertexai/)
    * [ pydantic_ai.models.groq  ](../groq/)
    * [ pydantic_ai.models.mistral  ](../mistral/)
    * [ pydantic_ai.models.ollama  ](../ollama/)
    * [ pydantic_ai.models.test  ](../test/)
    * pydantic_ai.models.function  [ pydantic_ai.models.function  ](./) Table of contents 
      * function 
      * FunctionModel 
        * __init__ 
      * AgentInfo 
        * function_tools 
        * allow_text_result 
        * result_tools 
        * model_settings 
      * DeltaToolCall 
        * name 
        * json_args 
      * DeltaToolCalls 
      * FunctionDef 
      * StreamFunctionDef 
      * FunctionAgentModel 
      * FunctionStreamTextResponse 
      * FunctionStreamStructuredResponse 

Table of contents

  * function 
  * FunctionModel 
    * __init__ 
  * AgentInfo 
    * function_tools 
    * allow_text_result 
    * result_tools 
    * model_settings 
  * DeltaToolCall 
    * name 
    * json_args 
  * DeltaToolCalls 
  * FunctionDef 
  * StreamFunctionDef 
  * FunctionAgentModel 
  * FunctionStreamTextResponse 
  * FunctionStreamStructuredResponse 

  1. [ Introduction  ](../../..)
  2. [ API Reference  ](../../agent/)

# `pydantic_ai.models.function`

A model controlled by a local function.

`FunctionModel` is similar to [`TestModel`](../test/), but allows greater
control over the model's behavior.

Its primary use case is for more advanced unit testing than is possible with
`TestModel`.

Here's a minimal example:

function_model_usage.py

    
    
    from pydantic_ai import Agent
    from pydantic_ai.messages import ModelMessage, ModelResponse
    from pydantic_ai.models.function import FunctionModel, AgentInfo
    
    my_agent = Agent('openai:gpt-4o')
    
    
    async def model_function(
        messages: list[ModelMessage], info: AgentInfo
    ) -> ModelResponse:
        print(messages)
        """
        [
            ModelRequest(
                parts=[
                    UserPromptPart(
                        content='Testing my agent...',
                        timestamp=datetime.datetime(...),
                        part_kind='user-prompt',
                    )
                ],
                kind='request',
            )
        ]
        """
        print(info)
        """
        AgentInfo(
            function_tools=[], allow_text_result=True, result_tools=[], model_settings=None
        )
        """
        return ModelResponse.from_text('hello world')
    
    
    async def test_my_agent():
        """Unit test for my_agent, to be run by pytest."""
        with my_agent.override(model=FunctionModel(model_function)):
            result = await my_agent.run('Testing my agent...')
            assert result.data == 'hello world'
    

See [Unit testing with `FunctionModel`](../../../testing-evals/#unit-testing-
with-functionmodel) for detailed documentation.

###  FunctionModel `dataclass`

Bases: `[Model](../base/#pydantic_ai.models.Model "pydantic_ai.models.Model")`

A model controlled by a local function.

Apart from `__init__`, all methods are private or match those of the base
class.

Source code in `pydantic_ai_slim/pydantic_ai/models/function.py`

    
    
    32
    33
    34
    35
    36
    37
    38
    39
    40
    41
    42
    43
    44
    45
    46
    47
    48
    49
    50
    51
    52
    53
    54
    55
    56
    57
    58
    59
    60
    61
    62
    63
    64
    65
    66
    67
    68
    69
    70
    71
    72
    73
    74
    75
    76
    77
    78
    79
    80
    81
    82

|

    
    
    @dataclass(init=False)
    class FunctionModel(Model):
        """A model controlled by a local function.
    
        Apart from `__init__`, all methods are private or match those of the base class.
        """
    
        function: FunctionDef | None = None
        stream_function: StreamFunctionDef | None = None
    
        @overload
        def __init__(self, function: FunctionDef) -> None: ...
    
        @overload
        def __init__(self, *, stream_function: StreamFunctionDef) -> None: ...
    
        @overload
        def __init__(self, function: FunctionDef, *, stream_function: StreamFunctionDef) -> None: ...
    
        def __init__(self, function: FunctionDef | None = None, *, stream_function: StreamFunctionDef | None = None):
            """Initialize a `FunctionModel`.
    
            Either `function` or `stream_function` must be provided, providing both is allowed.
    
            Args:
                function: The function to call for non-streamed requests.
                stream_function: The function to call for streamed requests.
            """
            if function is None and stream_function is None:
                raise TypeError('Either `function` or `stream_function` must be provided')
            self.function = function
            self.stream_function = stream_function
    
        async def agent_model(
            self,
            *,
            function_tools: list[ToolDefinition],
            allow_text_result: bool,
            result_tools: list[ToolDefinition],
        ) -> AgentModel:
            return FunctionAgentModel(
                self.function, self.stream_function, AgentInfo(function_tools, allow_text_result, result_tools, None)
            )
    
        def name(self) -> str:
            labels: list[str] = []
            if self.function is not None:
                labels.append(self.function.__name__)
            if self.stream_function is not None:
                labels.append(f'stream-{self.stream_function.__name__}')
            return f'function:{",".join(labels)}'
      
  
---|---  
  
####  __init__

    
    
    __init__(function: FunctionDef) -> None
    
    
    
    __init__(*, stream_function: StreamFunctionDef) -> None
    
    
    
    __init__(
        function: FunctionDef,
        *,
        stream_function: StreamFunctionDef
    ) -> None
    
    
    
    __init__(
        function: FunctionDef | None = None,
        *,
        stream_function: StreamFunctionDef | None = None
    )
    

Initialize a `FunctionModel`.

Either `function` or `stream_function` must be provided, providing both is
allowed.

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`function` |  `FunctionDef | None` |  The function to call for non-streamed requests. |  `None`  
`stream_function` |  `StreamFunctionDef | None` |  The function to call for streamed requests. |  `None`  
  
Source code in `pydantic_ai_slim/pydantic_ai/models/function.py`

    
    
    51
    52
    53
    54
    55
    56
    57
    58
    59
    60
    61
    62
    63

|

    
    
    def __init__(self, function: FunctionDef | None = None, *, stream_function: StreamFunctionDef | None = None):
        """Initialize a `FunctionModel`.
    
        Either `function` or `stream_function` must be provided, providing both is allowed.
    
        Args:
            function: The function to call for non-streamed requests.
            stream_function: The function to call for streamed requests.
        """
        if function is None and stream_function is None:
            raise TypeError('Either `function` or `stream_function` must be provided')
        self.function = function
        self.stream_function = stream_function
      
  
---|---  
  
###  AgentInfo `dataclass`

Information about an agent.

This is passed as the second to functions used within `FunctionModel`.

Source code in `pydantic_ai_slim/pydantic_ai/models/function.py`

    
    
     85
     86
     87
     88
     89
     90
     91
     92
     93
     94
     95
     96
     97
     98
     99
    100
    101
    102
    103

|

    
    
    @dataclass(frozen=True)
    class AgentInfo:
        """Information about an agent.
    
        This is passed as the second to functions used within [`FunctionModel`][pydantic_ai.models.function.FunctionModel].
        """
    
        function_tools: list[ToolDefinition]
        """The function tools available on this agent.
    
        These are the tools registered via the [`tool`][pydantic_ai.Agent.tool] and
        [`tool_plain`][pydantic_ai.Agent.tool_plain] decorators.
        """
        allow_text_result: bool
        """Whether a plain text result is allowed."""
        result_tools: list[ToolDefinition]
        """The tools that can called as the final result of the run."""
        model_settings: ModelSettings | None
        """The model settings passed to the run call."""
      
  
---|---  
  
####  function_tools `instance-attribute`

    
    
    function_tools: [list](https://docs.python.org/3/library/stdtypes.html#list)[[ToolDefinition](../../tools/#pydantic_ai.tools.ToolDefinition "pydantic_ai.tools.ToolDefinition")]
    

The function tools available on this agent.

These are the tools registered via the
[`tool`](../../agent/#pydantic_ai.Agent.tool) and
[`tool_plain`](../../agent/#pydantic_ai.Agent.tool_plain) decorators.

####  allow_text_result `instance-attribute`

    
    
    allow_text_result: [bool](https://docs.python.org/3/library/functions.html#bool)
    

Whether a plain text result is allowed.

####  result_tools `instance-attribute`

    
    
    result_tools: [list](https://docs.python.org/3/library/stdtypes.html#list)[[ToolDefinition](../../tools/#pydantic_ai.tools.ToolDefinition "pydantic_ai.tools.ToolDefinition")]
    

The tools that can called as the final result of the run.

####  model_settings `instance-attribute`

    
    
    model_settings: [ModelSettings](../../settings/#pydantic_ai.settings.ModelSettings "pydantic_ai.settings.ModelSettings") | None
    

The model settings passed to the run call.

###  DeltaToolCall `dataclass`

Incremental change to a tool call.

Used to describe a chunk when streaming structured responses.

Source code in `pydantic_ai_slim/pydantic_ai/models/function.py`

    
    
    106
    107
    108
    109
    110
    111
    112
    113
    114
    115
    116

|

    
    
    @dataclass
    class DeltaToolCall:
        """Incremental change to a tool call.
    
        Used to describe a chunk when streaming structured responses.
        """
    
        name: str | None = None
        """Incremental change to the name of the tool."""
        json_args: str | None = None
        """Incremental change to the arguments as JSON"""
      
  
---|---  
  
####  name `class-attribute` `instance-attribute`

    
    
    name: [str](https://docs.python.org/3/library/stdtypes.html#str) | None = None
    

Incremental change to the name of the tool.

####  json_args `class-attribute` `instance-attribute`

    
    
    json_args: [str](https://docs.python.org/3/library/stdtypes.html#str) | None = None
    

Incremental change to the arguments as JSON

###  DeltaToolCalls `module-attribute`

    
    
    DeltaToolCalls: [TypeAlias](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypeAlias "typing_extensions.TypeAlias") = [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[int](https://docs.python.org/3/library/functions.html#int), DeltaToolCall]
    

A mapping of tool call IDs to incremental changes.

###  FunctionDef `module-attribute`

    
    
    FunctionDef: [TypeAlias](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypeAlias "typing_extensions.TypeAlias") = [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[
        [[list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")], AgentInfo],
        [Union](https://docs.python.org/3/library/typing.html#typing.Union "typing.Union")[[ModelResponse](../../messages/#pydantic_ai.messages.ModelResponse "pydantic_ai.messages.ModelResponse"), [Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "collections.abc.Awaitable")[[ModelResponse](../../messages/#pydantic_ai.messages.ModelResponse "pydantic_ai.messages.ModelResponse")]],
    ]
    

A function used to generate a non-streamed response.

###  StreamFunctionDef `module-attribute`

    
    
    StreamFunctionDef: [TypeAlias](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypeAlias "typing_extensions.TypeAlias") = [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[
        [[list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")], AgentInfo],
        [AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator "collections.abc.AsyncIterator")[[Union](https://docs.python.org/3/library/typing.html#typing.Union "typing.Union")[[str](https://docs.python.org/3/library/stdtypes.html#str), DeltaToolCalls]],
    ]
    

A function used to generate a streamed response.

While this is defined as having return type of `AsyncIterator[Union[str,
DeltaToolCalls]]`, it should really be considered as
`Union[AsyncIterator[str], AsyncIterator[DeltaToolCalls]`,

E.g. you need to yield all text or all `DeltaToolCalls`, not mix them.

###  FunctionAgentModel `dataclass`

Bases: `[AgentModel](../base/#pydantic_ai.models.AgentModel
"pydantic_ai.models.AgentModel")`

Implementation of `AgentModel` for FunctionModel.

Source code in `pydantic_ai_slim/pydantic_ai/models/function.py`

    
    
    135
    136
    137
    138
    139
    140
    141
    142
    143
    144
    145
    146
    147
    148
    149
    150
    151
    152
    153
    154
    155
    156
    157
    158
    159
    160
    161
    162
    163
    164
    165
    166
    167
    168
    169
    170
    171
    172
    173
    174
    175
    176

|

    
    
    @dataclass
    class FunctionAgentModel(AgentModel):
        """Implementation of `AgentModel` for [FunctionModel][pydantic_ai.models.function.FunctionModel]."""
    
        function: FunctionDef | None
        stream_function: StreamFunctionDef | None
        agent_info: AgentInfo
    
        async def request(
            self, messages: list[ModelMessage], model_settings: ModelSettings | None
        ) -> tuple[ModelResponse, result.Usage]:
            agent_info = replace(self.agent_info, model_settings=model_settings)
    
            assert self.function is not None, 'FunctionModel must receive a `function` to support non-streamed requests'
            if inspect.iscoroutinefunction(self.function):
                response = await self.function(messages, agent_info)
            else:
                response_ = await _utils.run_in_executor(self.function, messages, agent_info)
                assert isinstance(response_, ModelResponse), response_
                response = response_
            # TODO is `messages` right here? Should it just be new messages?
            return response, _estimate_usage(chain(messages, [response]))
    
        @asynccontextmanager
        async def request_stream(
            self, messages: list[ModelMessage], model_settings: ModelSettings | None
        ) -> AsyncIterator[EitherStreamedResponse]:
            assert (
                self.stream_function is not None
            ), 'FunctionModel must receive a `stream_function` to support streamed requests'
            response_stream = self.stream_function(messages, self.agent_info)
            try:
                first = await response_stream.__anext__()
            except StopAsyncIteration as e:
                raise ValueError('Stream function must return at least one item') from e
    
            if isinstance(first, str):
                text_stream = cast(AsyncIterator[str], response_stream)
                yield FunctionStreamTextResponse(first, text_stream)
            else:
                structured_stream = cast(AsyncIterator[DeltaToolCalls], response_stream)
                yield FunctionStreamStructuredResponse(first, structured_stream)
      
  
---|---  
  
###  FunctionStreamTextResponse `dataclass`

Bases: `[StreamTextResponse](../base/#pydantic_ai.models.StreamTextResponse
"pydantic_ai.models.StreamTextResponse")`

Implementation of `StreamTextResponse` for FunctionModel.

Source code in `pydantic_ai_slim/pydantic_ai/models/function.py`

    
    
    179
    180
    181
    182
    183
    184
    185
    186
    187
    188
    189
    190
    191
    192
    193
    194
    195
    196
    197
    198
    199
    200
    201
    202
    203

|

    
    
    @dataclass
    class FunctionStreamTextResponse(StreamTextResponse):
        """Implementation of `StreamTextResponse` for [FunctionModel][pydantic_ai.models.function.FunctionModel]."""
    
        _next: str | None
        _iter: AsyncIterator[str]
        _timestamp: datetime = field(default_factory=_utils.now_utc, init=False)
        _buffer: list[str] = field(default_factory=list, init=False)
    
        async def __anext__(self) -> None:
            if self._next is not None:
                self._buffer.append(self._next)
                self._next = None
            else:
                self._buffer.append(await self._iter.__anext__())
    
        def get(self, *, final: bool = False) -> Iterable[str]:
            yield from self._buffer
            self._buffer.clear()
    
        def usage(self) -> result.Usage:
            return result.Usage()
    
        def timestamp(self) -> datetime:
            return self._timestamp
      
  
---|---  
  
###  FunctionStreamStructuredResponse `dataclass`

Bases:
`[StreamStructuredResponse](../base/#pydantic_ai.models.StreamStructuredResponse
"pydantic_ai.models.StreamStructuredResponse")`

Implementation of `StreamStructuredResponse` for FunctionModel.

Source code in `pydantic_ai_slim/pydantic_ai/models/function.py`

    
    
    206
    207
    208
    209
    210
    211
    212
    213
    214
    215
    216
    217
    218
    219
    220
    221
    222
    223
    224
    225
    226
    227
    228
    229
    230
    231
    232
    233
    234
    235
    236
    237
    238
    239
    240
    241

|

    
    
    @dataclass
    class FunctionStreamStructuredResponse(StreamStructuredResponse):
        """Implementation of `StreamStructuredResponse` for [FunctionModel][pydantic_ai.models.function.FunctionModel]."""
    
        _next: DeltaToolCalls | None
        _iter: AsyncIterator[DeltaToolCalls]
        _delta_tool_calls: dict[int, DeltaToolCall] = field(default_factory=dict)
        _timestamp: datetime = field(default_factory=_utils.now_utc)
    
        async def __anext__(self) -> None:
            if self._next is not None:
                tool_call = self._next
                self._next = None
            else:
                tool_call = await self._iter.__anext__()
    
            for key, new in tool_call.items():
                if current := self._delta_tool_calls.get(key):
                    current.name = _utils.add_optional(current.name, new.name)
                    current.json_args = _utils.add_optional(current.json_args, new.json_args)
                else:
                    self._delta_tool_calls[key] = new
    
        def get(self, *, final: bool = False) -> ModelResponse:
            calls: list[ModelResponsePart] = []
            for c in self._delta_tool_calls.values():
                if c.name is not None and c.json_args is not None:
                    calls.append(ToolCallPart.from_raw_args(c.name, c.json_args))
    
            return ModelResponse(calls, timestamp=self._timestamp)
    
        def usage(self) -> result.Usage:
            return _estimate_usage([self.get()])
    
        def timestamp(self) -> datetime:
            return self._timestamp
      
  
---|---  
  
© Pydantic Services Inc. 2024 to present

