Skip to content

[ ![logo](../../img/logo-white.svg) ](../.. "PydanticAI")

PydanticAI

pydantic_ai.result

Type to start searching

[ pydantic/pydantic-ai

  * v0.0.14
  * 4.2k
  * 255

](https://github.com/pydantic/pydantic-ai "Go to repository")

[ ![logo](../../img/logo-white.svg) ](../.. "PydanticAI") PydanticAI

[ pydantic/pydantic-ai

  * v0.0.14
  * 4.2k
  * 255

](https://github.com/pydantic/pydantic-ai "Go to repository")

  * [ Introduction  ](../..)
  * [ Installation  ](../../install/)
  * [ Getting Help  ](../../help/)
  * [ Contributing  ](../../contributing/)
  * Documentation  Documentation 
    * [ Agents  ](../../agents/)
    * [ Models  ](../../models/)
    * [ Dependencies  ](../../dependencies/)
    * [ Function Tools  ](../../tools/)
    * [ Results  ](../../results/)
    * [ Messages and chat history  ](../../message-history/)
    * [ Testing and Evals  ](../../testing-evals/)
    * [ Debugging and Monitoring  ](../../logfire/)
  * [ Examples  ](../../examples/)

Examples

    * [ Pydantic Model  ](../../examples/pydantic-model/)
    * [ Weather agent  ](../../examples/weather-agent/)
    * [ Bank support  ](../../examples/bank-support/)
    * [ SQL Generation  ](../../examples/sql-gen/)
    * [ RAG  ](../../examples/rag/)
    * [ Stream markdown  ](../../examples/stream-markdown/)
    * [ Stream whales  ](../../examples/stream-whales/)
    * [ Chat App with FastAPI  ](../../examples/chat-app/)
  * API Reference  API Reference 
    * [ pydantic_ai.Agent  ](../agent/)
    * [ pydantic_ai.tools  ](../tools/)
    * pydantic_ai.result  [ pydantic_ai.result  ](./) Table of contents 
      * result 
      * ResultData 
      * ResultValidatorFunc 
      * Usage 
        * requests 
        * request_tokens 
        * response_tokens 
        * total_tokens 
        * details 
        * __add__ 
      * RunResult 
        * all_messages 
        * all_messages_json 
        * new_messages 
        * new_messages_json 
        * data 
        * usage 
      * StreamedRunResult 
        * all_messages 
        * all_messages_json 
        * new_messages 
        * new_messages_json 
        * usage_so_far 
        * is_complete 
        * stream 
        * stream_text 
        * stream_structured 
        * get_data 
        * is_structured 
        * usage 
        * timestamp 
        * validate_structured_result 
    * [ pydantic_ai.messages  ](../messages/)
    * [ pydantic_ai.exceptions  ](../exceptions/)
    * [ pydantic_ai.settings  ](../settings/)
    * [ pydantic_ai.models  ](../models/base/)
    * [ pydantic_ai.models.openai  ](../models/openai/)
    * [ pydantic_ai.models.anthropic  ](../models/anthropic/)
    * [ pydantic_ai.models.gemini  ](../models/gemini/)
    * [ pydantic_ai.models.vertexai  ](../models/vertexai/)
    * [ pydantic_ai.models.groq  ](../models/groq/)
    * [ pydantic_ai.models.mistral  ](../models/mistral/)
    * [ pydantic_ai.models.ollama  ](../models/ollama/)
    * [ pydantic_ai.models.test  ](../models/test/)
    * [ pydantic_ai.models.function  ](../models/function/)

Table of contents

  * result 
  * ResultData 
  * ResultValidatorFunc 
  * Usage 
    * requests 
    * request_tokens 
    * response_tokens 
    * total_tokens 
    * details 
    * __add__ 
  * RunResult 
    * all_messages 
    * all_messages_json 
    * new_messages 
    * new_messages_json 
    * data 
    * usage 
  * StreamedRunResult 
    * all_messages 
    * all_messages_json 
    * new_messages 
    * new_messages_json 
    * usage_so_far 
    * is_complete 
    * stream 
    * stream_text 
    * stream_structured 
    * get_data 
    * is_structured 
    * usage 
    * timestamp 
    * validate_structured_result 

  1. [ Introduction  ](../..)
  2. [ API Reference  ](../agent/)

# `pydantic_ai.result`

###  ResultData `module-attribute`

    
    
    ResultData = TypeVar('ResultData', default=[str](https://docs.python.org/3/library/stdtypes.html#str))
    

Type variable for the result data of a run.

###  ResultValidatorFunc `module-attribute`

    
    
    ResultValidatorFunc = [Union](https://docs.python.org/3/library/typing.html#typing.Union "typing.Union")[
        [Callable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "collections.abc.Callable")[
            [[RunContext](../tools/#pydantic_ai.tools.RunContext "pydantic_ai.tools.RunContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")], ResultData], ResultData
        ],
        [Callable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "collections.abc.Callable")[
            [[RunContext](../tools/#pydantic_ai.tools.RunContext "pydantic_ai.tools.RunContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")], ResultData],
            [Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "collections.abc.Awaitable")[ResultData],
        ],
        [Callable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "collections.abc.Callable")[[ResultData], ResultData],
        [Callable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "collections.abc.Callable")[[ResultData], [Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "collections.abc.Awaitable")[ResultData]],
    ]
    

A function that always takes `ResultData` and returns `ResultData` and:

  * may or may not take [`RunContext`](../tools/#pydantic_ai.tools.RunContext) as a first argument
  * may or may not be async

Usage `ResultValidatorFunc[AgentDeps, ResultData]`.

###  Usage `dataclass`

LLM usage associated with a request or run.

Responsibility for calculating usage is on the model; PydanticAI simply sums
the usage information across requests.

You'll need to look up the documentation of the model you're using to convert
usage to monetary costs.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
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

|

    
    
    @dataclass
    class Usage:
        """LLM usage associated with a request or run.
    
        Responsibility for calculating usage is on the model; PydanticAI simply sums the usage information across requests.
    
        You'll need to look up the documentation of the model you're using to convert usage to monetary costs.
        """
    
        requests: int = 0
        """Number of requests made to the LLM API."""
        request_tokens: int | None = None
        """Tokens used in processing requests."""
        response_tokens: int | None = None
        """Tokens used in generating responses."""
        total_tokens: int | None = None
        """Total tokens used in the whole run, should generally be equal to `request_tokens + response_tokens`."""
        details: dict[str, int] | None = None
        """Any extra details returned by the model."""
    
        def __add__(self, other: Usage) -> Usage:
            """Add two Usages together.
    
            This is provided so it's trivial to sum usage information from multiple requests and runs.
            """
            counts: dict[str, int] = {}
            for f in 'requests', 'request_tokens', 'response_tokens', 'total_tokens':
                self_value = getattr(self, f)
                other_value = getattr(other, f)
                if self_value is not None or other_value is not None:
                    counts[f] = (self_value or 0) + (other_value or 0)
    
            details = self.details.copy() if self.details is not None else None
            if other.details is not None:
                details = details or {}
                for key, value in other.details.items():
                    details[key] = details.get(key, 0) + value
    
            return Usage(**counts, details=details or None)
      
  
---|---  
  
####  requests `class-attribute` `instance-attribute`

    
    
    requests: [int](https://docs.python.org/3/library/functions.html#int) = 0
    

Number of requests made to the LLM API.

####  request_tokens `class-attribute` `instance-attribute`

    
    
    request_tokens: [int](https://docs.python.org/3/library/functions.html#int) | None = None
    

Tokens used in processing requests.

####  response_tokens `class-attribute` `instance-attribute`

    
    
    response_tokens: [int](https://docs.python.org/3/library/functions.html#int) | None = None
    

Tokens used in generating responses.

####  total_tokens `class-attribute` `instance-attribute`

    
    
    total_tokens: [int](https://docs.python.org/3/library/functions.html#int) | None = None
    

Total tokens used in the whole run, should generally be equal to
`request_tokens + response_tokens`.

####  details `class-attribute` `instance-attribute`

    
    
    details: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [int](https://docs.python.org/3/library/functions.html#int)] | None = None
    

Any extra details returned by the model.

####  __add__

    
    
    __add__(other: Usage) -> Usage
    

Add two Usages together.

This is provided so it's trivial to sum usage information from multiple
requests and runs.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
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

|

    
    
    def __add__(self, other: Usage) -> Usage:
        """Add two Usages together.
    
        This is provided so it's trivial to sum usage information from multiple requests and runs.
        """
        counts: dict[str, int] = {}
        for f in 'requests', 'request_tokens', 'response_tokens', 'total_tokens':
            self_value = getattr(self, f)
            other_value = getattr(other, f)
            if self_value is not None or other_value is not None:
                counts[f] = (self_value or 0) + (other_value or 0)
    
        details = self.details.copy() if self.details is not None else None
        if other.details is not None:
            details = details or {}
            for key, value in other.details.items():
                details[key] = details.get(key, 0) + value
    
        return Usage(**counts, details=details or None)
      
  
---|---  
  
###  RunResult `dataclass`

Bases: `_BaseRunResult[ResultData]`

Result of a non-streamed run.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
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

|

    
    
    @dataclass
    class RunResult(_BaseRunResult[ResultData]):
        """Result of a non-streamed run."""
    
        data: ResultData
        """Data from the final response in the run."""
        _usage: Usage
    
        def usage(self) -> Usage:
            """Return the usage of the whole run."""
            return self._usage
      
  
---|---  
  
####  all_messages

    
    
    all_messages() -> [list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")]
    

Return the history of _messages.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
     97
     98
     99
    100

|

    
    
    def all_messages(self) -> list[_messages.ModelMessage]:
        """Return the history of _messages."""
        # this is a method to be consistent with the other methods
        return self._all_messages
      
  
---|---  
  
####  all_messages_json

    
    
    all_messages_json() -> [bytes](https://docs.python.org/3/library/stdtypes.html#bytes)
    

Return all messages from `all_messages` as JSON bytes.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
    102
    103
    104

|

    
    
    def all_messages_json(self) -> bytes:
        """Return all messages from [`all_messages`][pydantic_ai.result._BaseRunResult.all_messages] as JSON bytes."""
        return _messages.ModelMessagesTypeAdapter.dump_json(self.all_messages())
      
  
---|---  
  
####  new_messages

    
    
    new_messages() -> [list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")]
    

Return new messages associated with this run.

System prompts and any messages from older runs are excluded.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
    106
    107
    108
    109
    110
    111

|

    
    
    def new_messages(self) -> list[_messages.ModelMessage]:
        """Return new messages associated with this run.
    
        System prompts and any messages from older runs are excluded.
        """
        return self.all_messages()[self._new_message_index :]
      
  
---|---  
  
####  new_messages_json

    
    
    new_messages_json() -> [bytes](https://docs.python.org/3/library/stdtypes.html#bytes)
    

Return new messages from `new_messages` as JSON bytes.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
    113
    114
    115

|

    
    
    def new_messages_json(self) -> bytes:
        """Return new messages from [`new_messages`][pydantic_ai.result._BaseRunResult.new_messages] as JSON bytes."""
        return _messages.ModelMessagesTypeAdapter.dump_json(self.new_messages())
      
  
---|---  
  
####  data `instance-attribute`

    
    
    data: ResultData
    

Data from the final response in the run.

####  usage

    
    
    usage() -> Usage
    

Return the usage of the whole run.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
    130
    131
    132

|

    
    
    def usage(self) -> Usage:
        """Return the usage of the whole run."""
        return self._usage
      
  
---|---  
  
###  StreamedRunResult `dataclass`

Bases: `_BaseRunResult[ResultData]`,
`[Generic](https://docs.python.org/3/library/typing.html#typing.Generic
"typing.Generic")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps
"pydantic_ai.tools.AgentDeps"), ResultData]`

Result of a streamed run that returns structured data via a tool call.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
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
    242
    243
    244
    245
    246
    247
    248
    249
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
    270
    271
    272
    273
    274
    275
    276
    277
    278
    279
    280
    281
    282
    283
    284
    285
    286
    287
    288
    289
    290
    291
    292
    293
    294
    295
    296
    297
    298
    299
    300
    301
    302
    303
    304
    305
    306
    307
    308
    309
    310
    311
    312
    313
    314
    315
    316
    317
    318
    319
    320
    321
    322
    323
    324
    325
    326
    327
    328
    329
    330
    331
    332
    333
    334
    335
    336
    337
    338
    339
    340
    341
    342
    343
    344
    345
    346

|

    
    
    @dataclass
    class StreamedRunResult(_BaseRunResult[ResultData], Generic[AgentDeps, ResultData]):
        """Result of a streamed run that returns structured data via a tool call."""
    
        usage_so_far: Usage
        """Usage of the run up until the last request."""
        _usage_limits: UsageLimits | None
        _stream_response: models.EitherStreamedResponse
        _result_schema: _result.ResultSchema[ResultData] | None
        _run_ctx: RunContext[AgentDeps]
        _result_validators: list[_result.ResultValidator[AgentDeps, ResultData]]
        _result_tool_name: str | None
        _on_complete: Callable[[], Awaitable[None]]
        is_complete: bool = field(default=False, init=False)
        """Whether the stream has all been received.
    
        This is set to `True` when one of
        [`stream`][pydantic_ai.result.StreamedRunResult.stream],
        [`stream_text`][pydantic_ai.result.StreamedRunResult.stream_text],
        [`stream_structured`][pydantic_ai.result.StreamedRunResult.stream_structured] or
        [`get_data`][pydantic_ai.result.StreamedRunResult.get_data] completes.
        """
    
        async def stream(self, *, debounce_by: float | None = 0.1) -> AsyncIterator[ResultData]:
            """Stream the response as an async iterable.
    
            The pydantic validator for structured data will be called in
            [partial mode](https://docs.pydantic.dev/dev/concepts/experimental/#partial-validation)
            on each iteration.
    
            Args:
                debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
                    Debouncing is particularly important for long structured responses to reduce the overhead of
                    performing validation as each token is received.
    
            Returns:
                An async iterable of the response data.
            """
            if isinstance(self._stream_response, models.StreamTextResponse):
                async for text in self.stream_text(debounce_by=debounce_by):
                    yield cast(ResultData, text)
            else:
                async for structured_message, is_last in self.stream_structured(debounce_by=debounce_by):
                    yield await self.validate_structured_result(structured_message, allow_partial=not is_last)
    
        async def stream_text(self, *, delta: bool = False, debounce_by: float | None = 0.1) -> AsyncIterator[str]:
            """Stream the text result as an async iterable.
    
            !!! note
                This method will fail if the response is structured,
                e.g. if [`is_structured`][pydantic_ai.result.StreamedRunResult.is_structured] returns `True`.
    
            !!! note
                Result validators will NOT be called on the text result if `delta=True`.
    
            Args:
                delta: if `True`, yield each chunk of text as it is received, if `False` (default), yield the full text
                    up to the current point.
                debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
                    Debouncing is particularly important for long structured responses to reduce the overhead of
                    performing validation as each token is received.
            """
            usage_checking_stream = _get_usage_checking_stream_response(
                self._stream_response, self._usage_limits, self.usage
            )
    
            with _logfire.span('response stream text') as lf_span:
                if isinstance(self._stream_response, models.StreamStructuredResponse):
                    raise exceptions.UserError('stream_text() can only be used with text responses')
                if delta:
                    async with _utils.group_by_temporal(usage_checking_stream, debounce_by) as group_iter:
                        async for _ in group_iter:
                            yield ''.join(self._stream_response.get())
                    final_delta = ''.join(self._stream_response.get(final=True))
                    if final_delta:
                        yield final_delta
                else:
                    # a quick benchmark shows it's faster to build up a string with concat when we're
                    # yielding at each step
                    chunks: list[str] = []
                    combined = ''
                    async with _utils.group_by_temporal(usage_checking_stream, debounce_by) as group_iter:
                        async for _ in group_iter:
                            new = False
                            for chunk in self._stream_response.get():
                                chunks.append(chunk)
                                new = True
                            if new:
                                combined = await self._validate_text_result(''.join(chunks))
                                yield combined
    
                    new = False
                    for chunk in self._stream_response.get(final=True):
                        chunks.append(chunk)
                        new = True
                    if new:
                        combined = await self._validate_text_result(''.join(chunks))
                        yield combined
                    lf_span.set_attribute('combined_text', combined)
                    await self._marked_completed(_messages.ModelResponse.from_text(combined))
    
        async def stream_structured(
            self, *, debounce_by: float | None = 0.1
        ) -> AsyncIterator[tuple[_messages.ModelResponse, bool]]:
            """Stream the response as an async iterable of Structured LLM Messages.
    
            !!! note
                This method will fail if the response is text,
                e.g. if [`is_structured`][pydantic_ai.result.StreamedRunResult.is_structured] returns `False`.
    
            Args:
                debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
                    Debouncing is particularly important for long structured responses to reduce the overhead of
                    performing validation as each token is received.
    
            Returns:
                An async iterable of the structured response message and whether that is the last message.
            """
            usage_checking_stream = _get_usage_checking_stream_response(
                self._stream_response, self._usage_limits, self.usage
            )
    
            with _logfire.span('response stream structured') as lf_span:
                if isinstance(self._stream_response, models.StreamTextResponse):
                    raise exceptions.UserError('stream_structured() can only be used with structured responses')
                else:
                    # we should already have a message at this point, yield that first if it has any content
                    msg = self._stream_response.get()
                    for item in msg.parts:
                        if isinstance(item, _messages.ToolCallPart) and item.has_content():
                            yield msg, False
                            break
                    async with _utils.group_by_temporal(usage_checking_stream, debounce_by) as group_iter:
                        async for _ in group_iter:
                            msg = self._stream_response.get()
                            for item in msg.parts:
                                if isinstance(item, _messages.ToolCallPart) and item.has_content():
                                    yield msg, False
                                    break
                    msg = self._stream_response.get(final=True)
                    yield msg, True
                    lf_span.set_attribute('structured_response', msg)
                    await self._marked_completed(msg)
    
        async def get_data(self) -> ResultData:
            """Stream the whole response, validate and return it."""
            usage_checking_stream = _get_usage_checking_stream_response(
                self._stream_response, self._usage_limits, self.usage
            )
    
            async for _ in usage_checking_stream:
                pass
    
            if isinstance(self._stream_response, models.StreamTextResponse):
                text = ''.join(self._stream_response.get(final=True))
                text = await self._validate_text_result(text)
                await self._marked_completed(_messages.ModelResponse.from_text(text))
                return cast(ResultData, text)
            else:
                message = self._stream_response.get(final=True)
                await self._marked_completed(message)
                return await self.validate_structured_result(message)
    
        @property
        def is_structured(self) -> bool:
            """Return whether the stream response contains structured data (as opposed to text)."""
            return isinstance(self._stream_response, models.StreamStructuredResponse)
    
        def usage(self) -> Usage:
            """Return the usage of the whole run.
    
            !!! note
                This won't return the full usage until the stream is finished.
            """
            return self.usage_so_far + self._stream_response.usage()
    
        def timestamp(self) -> datetime:
            """Get the timestamp of the response."""
            return self._stream_response.timestamp()
    
        async def validate_structured_result(
            self, message: _messages.ModelResponse, *, allow_partial: bool = False
        ) -> ResultData:
            """Validate a structured result message."""
            assert self._result_schema is not None, 'Expected _result_schema to not be None'
            assert self._result_tool_name is not None, 'Expected _result_tool_name to not be None'
            match = self._result_schema.find_named_tool(message.parts, self._result_tool_name)
            if match is None:
                raise exceptions.UnexpectedModelBehavior(
                    f'Invalid message, unable to find tool: {self._result_schema.tool_names()}'
                )
    
            call, result_tool = match
            result_data = result_tool.validate(call, allow_partial=allow_partial, wrap_validation_errors=False)
    
            for validator in self._result_validators:
                result_data = await validator.validate(result_data, call, self._run_ctx)
            return result_data
    
        async def _validate_text_result(self, text: str) -> str:
            for validator in self._result_validators:
                text = await validator.validate(  # pyright: ignore[reportAssignmentType]
                    text,  # pyright: ignore[reportArgumentType]
                    None,
                    self._run_ctx,
                )
            return text
    
        async def _marked_completed(self, message: _messages.ModelResponse) -> None:
            self.is_complete = True
            self._all_messages.append(message)
            await self._on_complete()
      
  
---|---  
  
####  all_messages

    
    
    all_messages() -> [list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")]
    

Return the history of _messages.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
     97
     98
     99
    100

|

    
    
    def all_messages(self) -> list[_messages.ModelMessage]:
        """Return the history of _messages."""
        # this is a method to be consistent with the other methods
        return self._all_messages
      
  
---|---  
  
####  all_messages_json

    
    
    all_messages_json() -> [bytes](https://docs.python.org/3/library/stdtypes.html#bytes)
    

Return all messages from `all_messages` as JSON bytes.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
    102
    103
    104

|

    
    
    def all_messages_json(self) -> bytes:
        """Return all messages from [`all_messages`][pydantic_ai.result._BaseRunResult.all_messages] as JSON bytes."""
        return _messages.ModelMessagesTypeAdapter.dump_json(self.all_messages())
      
  
---|---  
  
####  new_messages

    
    
    new_messages() -> [list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")]
    

Return new messages associated with this run.

System prompts and any messages from older runs are excluded.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
    106
    107
    108
    109
    110
    111

|

    
    
    def new_messages(self) -> list[_messages.ModelMessage]:
        """Return new messages associated with this run.
    
        System prompts and any messages from older runs are excluded.
        """
        return self.all_messages()[self._new_message_index :]
      
  
---|---  
  
####  new_messages_json

    
    
    new_messages_json() -> [bytes](https://docs.python.org/3/library/stdtypes.html#bytes)
    

Return new messages from `new_messages` as JSON bytes.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
    113
    114
    115

|

    
    
    def new_messages_json(self) -> bytes:
        """Return new messages from [`new_messages`][pydantic_ai.result._BaseRunResult.new_messages] as JSON bytes."""
        return _messages.ModelMessagesTypeAdapter.dump_json(self.new_messages())
      
  
---|---  
  
####  usage_so_far `instance-attribute`

    
    
    usage_so_far: Usage
    

Usage of the run up until the last request.

####  is_complete `class-attribute` `instance-attribute`

    
    
    is_complete: [bool](https://docs.python.org/3/library/functions.html#bool) = [field](https://docs.python.org/3/library/dataclasses.html#dataclasses.field "dataclasses.field")(default=False, init=False)
    

Whether the stream has all been received.

This is set to `True` when one of `stream`, `stream_text`, `stream_structured`
or `get_data` completes.

####  stream `async`

    
    
    stream(
        *, debounce_by: [float](https://docs.python.org/3/library/functions.html#float) | None = 0.1
    ) -> [AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator "collections.abc.AsyncIterator")[ResultData]
    

Stream the response as an async iterable.

The pydantic validator for structured data will be called in [partial
mode](https://docs.pydantic.dev/dev/concepts/experimental/#partial-validation)
on each iteration.

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`debounce_by` |  `[float](https://docs.python.org/3/library/functions.html#float) | None` |  by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing. Debouncing is particularly important for long structured responses to reduce the overhead of performing validation as each token is received. |  `0.1`  
  
Returns:

Type | Description  
---|---  
`[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator "collections.abc.AsyncIterator")[ResultData]` |  An async iterable of the response data.  
  
Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
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

|

    
    
    async def stream(self, *, debounce_by: float | None = 0.1) -> AsyncIterator[ResultData]:
        """Stream the response as an async iterable.
    
        The pydantic validator for structured data will be called in
        [partial mode](https://docs.pydantic.dev/dev/concepts/experimental/#partial-validation)
        on each iteration.
    
        Args:
            debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
                Debouncing is particularly important for long structured responses to reduce the overhead of
                performing validation as each token is received.
    
        Returns:
            An async iterable of the response data.
        """
        if isinstance(self._stream_response, models.StreamTextResponse):
            async for text in self.stream_text(debounce_by=debounce_by):
                yield cast(ResultData, text)
        else:
            async for structured_message, is_last in self.stream_structured(debounce_by=debounce_by):
                yield await self.validate_structured_result(structured_message, allow_partial=not is_last)
      
  
---|---  
  
####  stream_text `async`

    
    
    stream_text(
        *, delta: [bool](https://docs.python.org/3/library/functions.html#bool) = False, debounce_by: [float](https://docs.python.org/3/library/functions.html#float) | None = 0.1
    ) -> [AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator "collections.abc.AsyncIterator")[[str](https://docs.python.org/3/library/stdtypes.html#str)]
    

Stream the text result as an async iterable.

Note

This method will fail if the response is structured, e.g. if `is_structured`
returns `True`.

Note

Result validators will NOT be called on the text result if `delta=True`.

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`delta` |  `[bool](https://docs.python.org/3/library/functions.html#bool)` |  if `True`, yield each chunk of text as it is received, if `False` (default), yield the full text up to the current point. |  `False`  
`debounce_by` |  `[float](https://docs.python.org/3/library/functions.html#float) | None` |  by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing. Debouncing is particularly important for long structured responses to reduce the overhead of performing validation as each token is received. |  `0.1`  
  
Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
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

|

    
    
    async def stream_text(self, *, delta: bool = False, debounce_by: float | None = 0.1) -> AsyncIterator[str]:
        """Stream the text result as an async iterable.
    
        !!! note
            This method will fail if the response is structured,
            e.g. if [`is_structured`][pydantic_ai.result.StreamedRunResult.is_structured] returns `True`.
    
        !!! note
            Result validators will NOT be called on the text result if `delta=True`.
    
        Args:
            delta: if `True`, yield each chunk of text as it is received, if `False` (default), yield the full text
                up to the current point.
            debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
                Debouncing is particularly important for long structured responses to reduce the overhead of
                performing validation as each token is received.
        """
        usage_checking_stream = _get_usage_checking_stream_response(
            self._stream_response, self._usage_limits, self.usage
        )
    
        with _logfire.span('response stream text') as lf_span:
            if isinstance(self._stream_response, models.StreamStructuredResponse):
                raise exceptions.UserError('stream_text() can only be used with text responses')
            if delta:
                async with _utils.group_by_temporal(usage_checking_stream, debounce_by) as group_iter:
                    async for _ in group_iter:
                        yield ''.join(self._stream_response.get())
                final_delta = ''.join(self._stream_response.get(final=True))
                if final_delta:
                    yield final_delta
            else:
                # a quick benchmark shows it's faster to build up a string with concat when we're
                # yielding at each step
                chunks: list[str] = []
                combined = ''
                async with _utils.group_by_temporal(usage_checking_stream, debounce_by) as group_iter:
                    async for _ in group_iter:
                        new = False
                        for chunk in self._stream_response.get():
                            chunks.append(chunk)
                            new = True
                        if new:
                            combined = await self._validate_text_result(''.join(chunks))
                            yield combined
    
                new = False
                for chunk in self._stream_response.get(final=True):
                    chunks.append(chunk)
                    new = True
                if new:
                    combined = await self._validate_text_result(''.join(chunks))
                    yield combined
                lf_span.set_attribute('combined_text', combined)
                await self._marked_completed(_messages.ModelResponse.from_text(combined))
      
  
---|---  
  
####  stream_structured `async`

    
    
    stream_structured(
        *, debounce_by: [float](https://docs.python.org/3/library/functions.html#float) | None = 0.1
    ) -> [AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator "collections.abc.AsyncIterator")[[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[ModelResponse](../messages/#pydantic_ai.messages.ModelResponse "pydantic_ai.messages.ModelResponse"), [bool](https://docs.python.org/3/library/functions.html#bool)]]
    

Stream the response as an async iterable of Structured LLM Messages.

Note

This method will fail if the response is text, e.g. if `is_structured` returns
`False`.

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`debounce_by` |  `[float](https://docs.python.org/3/library/functions.html#float) | None` |  by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing. Debouncing is particularly important for long structured responses to reduce the overhead of performing validation as each token is received. |  `0.1`  
  
Returns:

Type | Description  
---|---  
`[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator "collections.abc.AsyncIterator")[[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[ModelResponse](../messages/#pydantic_ai.messages.ModelResponse "pydantic_ai.messages.ModelResponse"), [bool](https://docs.python.org/3/library/functions.html#bool)]]` |  An async iterable of the structured response message and whether that is the last message.  
  
Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
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
    248
    249
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
    270
    271
    272
    273
    274
    275
    276
    277

|

    
    
    async def stream_structured(
        self, *, debounce_by: float | None = 0.1
    ) -> AsyncIterator[tuple[_messages.ModelResponse, bool]]:
        """Stream the response as an async iterable of Structured LLM Messages.
    
        !!! note
            This method will fail if the response is text,
            e.g. if [`is_structured`][pydantic_ai.result.StreamedRunResult.is_structured] returns `False`.
    
        Args:
            debounce_by: by how much (if at all) to debounce/group the response chunks by. `None` means no debouncing.
                Debouncing is particularly important for long structured responses to reduce the overhead of
                performing validation as each token is received.
    
        Returns:
            An async iterable of the structured response message and whether that is the last message.
        """
        usage_checking_stream = _get_usage_checking_stream_response(
            self._stream_response, self._usage_limits, self.usage
        )
    
        with _logfire.span('response stream structured') as lf_span:
            if isinstance(self._stream_response, models.StreamTextResponse):
                raise exceptions.UserError('stream_structured() can only be used with structured responses')
            else:
                # we should already have a message at this point, yield that first if it has any content
                msg = self._stream_response.get()
                for item in msg.parts:
                    if isinstance(item, _messages.ToolCallPart) and item.has_content():
                        yield msg, False
                        break
                async with _utils.group_by_temporal(usage_checking_stream, debounce_by) as group_iter:
                    async for _ in group_iter:
                        msg = self._stream_response.get()
                        for item in msg.parts:
                            if isinstance(item, _messages.ToolCallPart) and item.has_content():
                                yield msg, False
                                break
                msg = self._stream_response.get(final=True)
                yield msg, True
                lf_span.set_attribute('structured_response', msg)
                await self._marked_completed(msg)
      
  
---|---  
  
####  get_data `async`

    
    
    get_data() -> ResultData
    

Stream the whole response, validate and return it.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
    279
    280
    281
    282
    283
    284
    285
    286
    287
    288
    289
    290
    291
    292
    293
    294
    295
    296

|

    
    
    async def get_data(self) -> ResultData:
        """Stream the whole response, validate and return it."""
        usage_checking_stream = _get_usage_checking_stream_response(
            self._stream_response, self._usage_limits, self.usage
        )
    
        async for _ in usage_checking_stream:
            pass
    
        if isinstance(self._stream_response, models.StreamTextResponse):
            text = ''.join(self._stream_response.get(final=True))
            text = await self._validate_text_result(text)
            await self._marked_completed(_messages.ModelResponse.from_text(text))
            return cast(ResultData, text)
        else:
            message = self._stream_response.get(final=True)
            await self._marked_completed(message)
            return await self.validate_structured_result(message)
      
  
---|---  
  
####  is_structured `property`

    
    
    is_structured: [bool](https://docs.python.org/3/library/functions.html#bool)
    

Return whether the stream response contains structured data (as opposed to
text).

####  usage

    
    
    usage() -> Usage
    

Return the usage of the whole run.

Note

This won't return the full usage until the stream is finished.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
    303
    304
    305
    306
    307
    308
    309

|

    
    
    def usage(self) -> Usage:
        """Return the usage of the whole run.
    
        !!! note
            This won't return the full usage until the stream is finished.
        """
        return self.usage_so_far + self._stream_response.usage()
      
  
---|---  
  
####  timestamp

    
    
    timestamp() -> [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime "datetime.datetime")
    

Get the timestamp of the response.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
    311
    312
    313

|

    
    
    def timestamp(self) -> datetime:
        """Get the timestamp of the response."""
        return self._stream_response.timestamp()
      
  
---|---  
  
####  validate_structured_result `async`

    
    
    validate_structured_result(
        message: [ModelResponse](../messages/#pydantic_ai.messages.ModelResponse "pydantic_ai.messages.ModelResponse"), *, allow_partial: [bool](https://docs.python.org/3/library/functions.html#bool) = False
    ) -> ResultData
    

Validate a structured result message.

Source code in `pydantic_ai_slim/pydantic_ai/result.py`

    
    
    315
    316
    317
    318
    319
    320
    321
    322
    323
    324
    325
    326
    327
    328
    329
    330
    331
    332

|

    
    
    async def validate_structured_result(
        self, message: _messages.ModelResponse, *, allow_partial: bool = False
    ) -> ResultData:
        """Validate a structured result message."""
        assert self._result_schema is not None, 'Expected _result_schema to not be None'
        assert self._result_tool_name is not None, 'Expected _result_tool_name to not be None'
        match = self._result_schema.find_named_tool(message.parts, self._result_tool_name)
        if match is None:
            raise exceptions.UnexpectedModelBehavior(
                f'Invalid message, unable to find tool: {self._result_schema.tool_names()}'
            )
    
        call, result_tool = match
        result_data = result_tool.validate(call, allow_partial=allow_partial, wrap_validation_errors=False)
    
        for validator in self._result_validators:
            result_data = await validator.validate(result_data, call, self._run_ctx)
        return result_data
      
  
---|---  
  
© Pydantic Services Inc. 2024 to present

