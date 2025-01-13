Skip to content

[ ![logo](../../../img/logo-white.svg) ](../../.. "PydanticAI")

PydanticAI

pydantic_ai.models.test

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
    * pydantic_ai.models.test  [ pydantic_ai.models.test  ](./) Table of contents 
      * test 
      * TestModel 
        * call_tools 
        * custom_result_text 
        * custom_result_args 
        * seed 
        * agent_model_function_tools 
        * agent_model_allow_text_result 
        * agent_model_result_tools 
      * TestAgentModel 
      * TestStreamTextResponse 
      * TestStreamStructuredResponse 
    * [ pydantic_ai.models.function  ](../function/)

Table of contents

  * test 
  * TestModel 
    * call_tools 
    * custom_result_text 
    * custom_result_args 
    * seed 
    * agent_model_function_tools 
    * agent_model_allow_text_result 
    * agent_model_result_tools 
  * TestAgentModel 
  * TestStreamTextResponse 
  * TestStreamStructuredResponse 

  1. [ Introduction  ](../../..)
  2. [ API Reference  ](../../agent/)

# `pydantic_ai.models.test`

Utility model for quickly testing apps built with PydanticAI.

Here's a minimal example:

test_model_usage.py

    
    
    from pydantic_ai import Agent
    from pydantic_ai.models.test import TestModel
    
    my_agent = Agent('openai:gpt-4o', system_prompt='...')
    
    
    async def test_my_agent():
        """Unit test for my_agent, to be run by pytest."""
        m = TestModel()
        with my_agent.override(model=m):
            result = await my_agent.run('Testing my agent...')
            assert result.data == 'success (no tool calls)'
        assert m.agent_model_function_tools == []
    

See [Unit testing with `TestModel`](../../../testing-evals/#unit-testing-with-
testmodel) for detailed documentation.

###  TestModel `dataclass`

Bases: `[Model](../base/#pydantic_ai.models.Model "pydantic_ai.models.Model")`

A model specifically for testing purposes.

This will (by default) call all tools in the agent, then return a tool
response if possible, otherwise a plain response.

How useful this model is will vary significantly.

Apart from `__init__` derived by the `dataclass` decorator, all methods are
private or match those of the base class.

Source code in `pydantic_ai_slim/pydantic_ai/models/test.py`

    
    
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
     83
     84
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
    104
    105
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
    117

|

    
    
    @dataclass
    class TestModel(Model):
        """A model specifically for testing purposes.
    
        This will (by default) call all tools in the agent, then return a tool response if possible,
        otherwise a plain response.
    
        How useful this model is will vary significantly.
    
        Apart from `__init__` derived by the `dataclass` decorator, all methods are private or match those
        of the base class.
        """
    
        # NOTE: Avoid test discovery by pytest.
        __test__ = False
    
        call_tools: list[str] | Literal['all'] = 'all'
        """List of tools to call. If `'all'`, all tools will be called."""
        custom_result_text: str | None = None
        """If set, this text is return as the final result."""
        custom_result_args: Any | None = None
        """If set, these args will be passed to the result tool."""
        seed: int = 0
        """Seed for generating random data."""
        agent_model_function_tools: list[ToolDefinition] | None = field(default=None, init=False)
        """Definition of function tools passed to the model.
    
        This is set when the model is called, so will reflect the function tools from the last step of the last run.
        """
        agent_model_allow_text_result: bool | None = field(default=None, init=False)
        """Whether plain text responses from the model are allowed.
    
        This is set when the model is called, so will reflect the value from the last step of the last run.
        """
        agent_model_result_tools: list[ToolDefinition] | None = field(default=None, init=False)
        """Definition of result tools passed to the model.
    
        This is set when the model is called, so will reflect the result tools from the last step of the last run.
        """
    
        async def agent_model(
            self,
            *,
            function_tools: list[ToolDefinition],
            allow_text_result: bool,
            result_tools: list[ToolDefinition],
        ) -> AgentModel:
            self.agent_model_function_tools = function_tools
            self.agent_model_allow_text_result = allow_text_result
            self.agent_model_result_tools = result_tools
    
            if self.call_tools == 'all':
                tool_calls = [(r.name, r) for r in function_tools]
            else:
                function_tools_lookup = {t.name: t for t in function_tools}
                tools_to_call = (function_tools_lookup[name] for name in self.call_tools)
                tool_calls = [(r.name, r) for r in tools_to_call]
    
            if self.custom_result_text is not None:
                assert allow_text_result, 'Plain response not allowed, but `custom_result_text` is set.'
                assert self.custom_result_args is None, 'Cannot set both `custom_result_text` and `custom_result_args`.'
                result: _utils.Either[str | None, Any | None] = _utils.Either(left=self.custom_result_text)
            elif self.custom_result_args is not None:
                assert result_tools is not None, 'No result tools provided, but `custom_result_args` is set.'
                result_tool = result_tools[0]
    
                if k := result_tool.outer_typed_dict_key:
                    result = _utils.Either(right={k: self.custom_result_args})
                else:
                    result = _utils.Either(right=self.custom_result_args)
            elif allow_text_result:
                result = _utils.Either(left=None)
            elif result_tools:
                result = _utils.Either(right=None)
            else:
                result = _utils.Either(left=None)
    
            return TestAgentModel(tool_calls, result, result_tools, self.seed)
    
        def name(self) -> str:
            return 'test-model'
      
  
---|---  
  
####  call_tools `class-attribute` `instance-attribute`

    
    
    call_tools: [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "typing.Literal")['all'] = 'all'
    

List of tools to call. If `'all'`, all tools will be called.

####  custom_result_text `class-attribute` `instance-attribute`

    
    
    custom_result_text: [str](https://docs.python.org/3/library/stdtypes.html#str) | None = None
    

If set, this text is return as the final result.

####  custom_result_args `class-attribute` `instance-attribute`

    
    
    custom_result_args: [Any](https://docs.python.org/3/library/typing.html#typing.Any "typing.Any") | None = None
    

If set, these args will be passed to the result tool.

####  seed `class-attribute` `instance-attribute`

    
    
    seed: [int](https://docs.python.org/3/library/functions.html#int) = 0
    

Seed for generating random data.

####  agent_model_function_tools `class-attribute` `instance-attribute`

    
    
    agent_model_function_tools: [list](https://docs.python.org/3/library/stdtypes.html#list)[[ToolDefinition](../../tools/#pydantic_ai.tools.ToolDefinition "pydantic_ai.tools.ToolDefinition")] | None = (
        [field](https://docs.python.org/3/library/dataclasses.html#dataclasses.field "dataclasses.field")(default=None, init=False)
    )
    

Definition of function tools passed to the model.

This is set when the model is called, so will reflect the function tools from
the last step of the last run.

####  agent_model_allow_text_result `class-attribute` `instance-attribute`

    
    
    agent_model_allow_text_result: [bool](https://docs.python.org/3/library/functions.html#bool) | None = [field](https://docs.python.org/3/library/dataclasses.html#dataclasses.field "dataclasses.field")(
        default=None, init=False
    )
    

Whether plain text responses from the model are allowed.

This is set when the model is called, so will reflect the value from the last
step of the last run.

####  agent_model_result_tools `class-attribute` `instance-attribute`

    
    
    agent_model_result_tools: [list](https://docs.python.org/3/library/stdtypes.html#list)[[ToolDefinition](../../tools/#pydantic_ai.tools.ToolDefinition "pydantic_ai.tools.ToolDefinition")] | None = (
        [field](https://docs.python.org/3/library/dataclasses.html#dataclasses.field "dataclasses.field")(default=None, init=False)
    )
    

Definition of result tools passed to the model.

This is set when the model is called, so will reflect the result tools from
the last step of the last run.

###  TestAgentModel `dataclass`

Bases: `[AgentModel](../base/#pydantic_ai.models.AgentModel
"pydantic_ai.models.AgentModel")`

Implementation of `AgentModel` for testing purposes.

Source code in `pydantic_ai_slim/pydantic_ai/models/test.py`

    
    
    120
    121
    122
    123
    124
    125
    126
    127
    128
    129
    130
    131
    132
    133
    134
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
    177
    178
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
    204
    205
    206
    207
    208
    209
    210
    211

|

    
    
    @dataclass
    class TestAgentModel(AgentModel):
        """Implementation of `AgentModel` for testing purposes."""
    
        # NOTE: Avoid test discovery by pytest.
        __test__ = False
    
        tool_calls: list[tuple[str, ToolDefinition]]
        # left means the text is plain text; right means it's a function call
        result: _utils.Either[str | None, Any | None]
        result_tools: list[ToolDefinition]
        seed: int
    
        async def request(
            self, messages: list[ModelMessage], model_settings: ModelSettings | None
        ) -> tuple[ModelResponse, Usage]:
            model_response = self._request(messages, model_settings)
            usage = _estimate_usage([*messages, model_response])
            return model_response, usage
    
        @asynccontextmanager
        async def request_stream(
            self, messages: list[ModelMessage], model_settings: ModelSettings | None
        ) -> AsyncIterator[EitherStreamedResponse]:
            msg = self._request(messages, model_settings)
            usage = _estimate_usage(messages)
    
            # TODO: Rework this once we make StreamTextResponse more general
            texts: list[str] = []
            tool_calls: list[ToolCallPart] = []
            for item in msg.parts:
                if isinstance(item, TextPart):
                    texts.append(item.content)
                elif isinstance(item, ToolCallPart):
                    tool_calls.append(item)
                else:
                    assert_never(item)
    
            if texts:
                yield TestStreamTextResponse('\n\n'.join(texts), usage)
            else:
                yield TestStreamStructuredResponse(msg, usage)
    
        def gen_tool_args(self, tool_def: ToolDefinition) -> Any:
            return _JsonSchemaTestData(tool_def.parameters_json_schema, self.seed).generate()
    
        def _request(self, messages: list[ModelMessage], model_settings: ModelSettings | None) -> ModelResponse:
            # if there are tools, the first thing we want to do is call all of them
            if self.tool_calls and not any(isinstance(m, ModelResponse) for m in messages):
                return ModelResponse(
                    parts=[ToolCallPart.from_raw_args(name, self.gen_tool_args(args)) for name, args in self.tool_calls]
                )
    
            if messages:
                last_message = messages[-1]
                assert isinstance(last_message, ModelRequest), 'Expected last message to be a `ModelRequest`.'
    
                # check if there are any retry prompts, if so retry them
                new_retry_names = {p.tool_name for p in last_message.parts if isinstance(p, RetryPromptPart)}
                if new_retry_names:
                    return ModelResponse(
                        parts=[
                            ToolCallPart.from_raw_args(name, self.gen_tool_args(args))
                            for name, args in self.tool_calls
                            if name in new_retry_names
                        ]
                    )
    
            if response_text := self.result.left:
                if response_text.value is None:
                    # build up details of tool responses
                    output: dict[str, Any] = {}
                    for message in messages:
                        if isinstance(message, ModelRequest):
                            for part in message.parts:
                                if isinstance(part, ToolReturnPart):
                                    output[part.tool_name] = part.content
                    if output:
                        return ModelResponse.from_text(pydantic_core.to_json(output).decode())
                    else:
                        return ModelResponse.from_text('success (no tool calls)')
                else:
                    return ModelResponse.from_text(response_text.value)
            else:
                assert self.result_tools, 'No result tools provided'
                custom_result_args = self.result.right
                result_tool = self.result_tools[self.seed % len(self.result_tools)]
                if custom_result_args is not None:
                    return ModelResponse(parts=[ToolCallPart.from_raw_args(result_tool.name, custom_result_args)])
                else:
                    response_args = self.gen_tool_args(result_tool)
                    return ModelResponse(parts=[ToolCallPart.from_raw_args(result_tool.name, response_args)])
      
  
---|---  
  
###  TestStreamTextResponse `dataclass`

Bases: `[StreamTextResponse](../base/#pydantic_ai.models.StreamTextResponse
"pydantic_ai.models.StreamTextResponse")`

A text response that streams test data.

Source code in `pydantic_ai_slim/pydantic_ai/models/test.py`

    
    
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
    242
    243
    244
    245
    246
    247

|

    
    
    @dataclass
    class TestStreamTextResponse(StreamTextResponse):
        """A text response that streams test data."""
    
        _text: str
        _usage: Usage
        _iter: Iterator[str] = field(init=False)
        _timestamp: datetime = field(default_factory=_utils.now_utc)
        _buffer: list[str] = field(default_factory=list, init=False)
    
        def __post_init__(self):
            *words, last_word = self._text.split(' ')
            words = [f'{word} ' for word in words]
            words.append(last_word)
            if len(words) == 1 and len(self._text) > 2:
                mid = len(self._text) // 2
                words = [self._text[:mid], self._text[mid:]]
            self._iter = iter(words)
    
        async def __anext__(self) -> None:
            next_str = _utils.sync_anext(self._iter)
            response_tokens = _estimate_string_usage(next_str)
            self._usage += Usage(response_tokens=response_tokens, total_tokens=response_tokens)
            self._buffer.append(next_str)
    
        def get(self, *, final: bool = False) -> Iterable[str]:
            yield from self._buffer
            self._buffer.clear()
    
        def usage(self) -> Usage:
            return self._usage
    
        def timestamp(self) -> datetime:
            return self._timestamp
      
  
---|---  
  
###  TestStreamStructuredResponse `dataclass`

Bases:
`[StreamStructuredResponse](../base/#pydantic_ai.models.StreamStructuredResponse
"pydantic_ai.models.StreamStructuredResponse")`

A structured response that streams test data.

Source code in `pydantic_ai_slim/pydantic_ai/models/test.py`

    
    
    250
    251
    252
    253
    254
    255
    256
    257
    258
    259
    260
    261
    262
    263
    264
    265
    266
    267
    268
    269

|

    
    
    @dataclass
    class TestStreamStructuredResponse(StreamStructuredResponse):
        """A structured response that streams test data."""
    
        _structured_response: ModelResponse
        _usage: Usage
        _iter: Iterator[None] = field(default_factory=lambda: iter([None]))
        _timestamp: datetime = field(default_factory=_utils.now_utc, init=False)
    
        async def __anext__(self) -> None:
            return _utils.sync_anext(self._iter)
    
        def get(self, *, final: bool = False) -> ModelResponse:
            return self._structured_response
    
        def usage(self) -> Usage:
            return self._usage
    
        def timestamp(self) -> datetime:
            return self._timestamp
      
  
---|---  
  
© Pydantic Services Inc. 2024 to present
