Skip to content

[ ![logo](../../../img/logo-white.svg) ](../../.. "PydanticAI")

PydanticAI

pydantic_ai.models

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
    * pydantic_ai.models  [ pydantic_ai.models  ](./) Table of contents 
      * models 
      * KnownModelName 
      * Model 
        * agent_model 
      * AgentModel 
        * request 
        * request_stream 
      * StreamTextResponse 
        * __aiter__ 
        * __anext__ 
        * get 
        * usage 
        * timestamp 
      * StreamStructuredResponse 
        * __aiter__ 
        * __anext__ 
        * get 
        * usage 
        * timestamp 
      * ALLOW_MODEL_REQUESTS 
      * check_allow_model_requests 
      * override_allow_model_requests 
    * [ pydantic_ai.models.openai  ](../openai/)
    * [ pydantic_ai.models.anthropic  ](../anthropic/)
    * [ pydantic_ai.models.gemini  ](../gemini/)
    * [ pydantic_ai.models.vertexai  ](../vertexai/)
    * [ pydantic_ai.models.groq  ](../groq/)
    * [ pydantic_ai.models.mistral  ](../mistral/)
    * [ pydantic_ai.models.ollama  ](../ollama/)
    * [ pydantic_ai.models.test  ](../test/)
    * [ pydantic_ai.models.function  ](../function/)

Table of contents

  * models 
  * KnownModelName 
  * Model 
    * agent_model 
  * AgentModel 
    * request 
    * request_stream 
  * StreamTextResponse 
    * __aiter__ 
    * __anext__ 
    * get 
    * usage 
    * timestamp 
  * StreamStructuredResponse 
    * __aiter__ 
    * __anext__ 
    * get 
    * usage 
    * timestamp 
  * ALLOW_MODEL_REQUESTS 
  * check_allow_model_requests 
  * override_allow_model_requests 

  1. [ Introduction  ](../../..)
  2. [ API Reference  ](../../agent/)

# `pydantic_ai.models`

Logic related to making requests to an LLM.

The aim here is to make a common interface for different LLMs, so that the
rest of the code can be agnostic to the specific LLM being used.

###  KnownModelName `module-attribute`

    
    
    KnownModelName = [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "typing.Literal")[
        "openai:gpt-4o",
        "openai:gpt-4o-mini",
        "openai:gpt-4-turbo",
        "openai:gpt-4",
        "openai:o1-preview",
        "openai:o1-mini",
        "openai:o1",
        "openai:gpt-3.5-turbo",
        "groq:llama-3.3-70b-versatile",
        "groq:llama-3.1-70b-versatile",
        "groq:llama3-groq-70b-8192-tool-use-preview",
        "groq:llama3-groq-8b-8192-tool-use-preview",
        "groq:llama-3.1-70b-specdec",
        "groq:llama-3.1-8b-instant",
        "groq:llama-3.2-1b-preview",
        "groq:llama-3.2-3b-preview",
        "groq:llama-3.2-11b-vision-preview",
        "groq:llama-3.2-90b-vision-preview",
        "groq:llama3-70b-8192",
        "groq:llama3-8b-8192",
        "groq:mixtral-8x7b-32768",
        "groq:gemma2-9b-it",
        "groq:gemma-7b-it",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.0-flash-exp",
        "vertexai:gemini-1.5-flash",
        "vertexai:gemini-1.5-pro",
        "mistral:mistral-small-latest",
        "mistral:mistral-large-latest",
        "mistral:codestral-latest",
        "mistral:mistral-moderation-latest",
        "ollama:codellama",
        "ollama:gemma",
        "ollama:gemma2",
        "ollama:llama3",
        "ollama:llama3.1",
        "ollama:llama3.2",
        "ollama:llama3.2-vision",
        "ollama:llama3.3",
        "ollama:mistral",
        "ollama:mistral-nemo",
        "ollama:mixtral",
        "ollama:phi3",
        "ollama:qwq",
        "ollama:qwen",
        "ollama:qwen2",
        "ollama:qwen2.5",
        "ollama:starcoder2",
        "claude-3-5-haiku-latest",
        "claude-3-5-sonnet-latest",
        "claude-3-opus-latest",
        "test",
    ]
    

Known model names that can be used with the `model` parameter of
[`Agent`](../../agent/#pydantic_ai.Agent).

`KnownModelName` is provided as a concise way to specify a model.

###  Model

Bases: `[ABC](https://docs.python.org/3/library/abc.html#abc.ABC "abc.ABC")`

Abstract class for a model.

Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
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

    
    
    class Model(ABC):
        """Abstract class for a model."""
    
        @abstractmethod
        async def agent_model(
            self,
            *,
            function_tools: list[ToolDefinition],
            allow_text_result: bool,
            result_tools: list[ToolDefinition],
        ) -> AgentModel:
            """Create an agent model, this is called for each step of an agent run.
    
            This is async in case slow/async config checks need to be performed that can't be done in `__init__`.
    
            Args:
                function_tools: The tools available to the agent.
                allow_text_result: Whether a plain text final response/result is permitted.
                result_tools: Tool definitions for the final result tool(s), if any.
    
            Returns:
                An agent model.
            """
            raise NotImplementedError()
    
        @abstractmethod
        def name(self) -> str:
            raise NotImplementedError()
      
  
---|---  
  
####  agent_model `abstractmethod` `async`

    
    
    agent_model(
        *,
        function_tools: [list](https://docs.python.org/3/library/stdtypes.html#list)[[ToolDefinition](../../tools/#pydantic_ai.tools.ToolDefinition "pydantic_ai.tools.ToolDefinition")],
        allow_text_result: [bool](https://docs.python.org/3/library/functions.html#bool),
        result_tools: [list](https://docs.python.org/3/library/stdtypes.html#list)[[ToolDefinition](../../tools/#pydantic_ai.tools.ToolDefinition "pydantic_ai.tools.ToolDefinition")]
    ) -> AgentModel
    

Create an agent model, this is called for each step of an agent run.

This is async in case slow/async config checks need to be performed that can't
be done in `__init__`.

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`function_tools` |  `[list](https://docs.python.org/3/library/stdtypes.html#list)[[ToolDefinition](../../tools/#pydantic_ai.tools.ToolDefinition "pydantic_ai.tools.ToolDefinition")]` |  The tools available to the agent. |  _required_  
`allow_text_result` |  `[bool](https://docs.python.org/3/library/functions.html#bool)` |  Whether a plain text final response/result is permitted. |  _required_  
`result_tools` |  `[list](https://docs.python.org/3/library/stdtypes.html#list)[[ToolDefinition](../../tools/#pydantic_ai.tools.ToolDefinition "pydantic_ai.tools.ToolDefinition")]` |  Tool definitions for the final result tool(s), if any. |  _required_  
  
Returns:

Type | Description  
---|---  
`AgentModel` |  An agent model.  
  
Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
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

|

    
    
    @abstractmethod
    async def agent_model(
        self,
        *,
        function_tools: list[ToolDefinition],
        allow_text_result: bool,
        result_tools: list[ToolDefinition],
    ) -> AgentModel:
        """Create an agent model, this is called for each step of an agent run.
    
        This is async in case slow/async config checks need to be performed that can't be done in `__init__`.
    
        Args:
            function_tools: The tools available to the agent.
            allow_text_result: Whether a plain text final response/result is permitted.
            result_tools: Tool definitions for the final result tool(s), if any.
    
        Returns:
            An agent model.
        """
        raise NotImplementedError()
      
  
---|---  
  
###  AgentModel

Bases: `[ABC](https://docs.python.org/3/library/abc.html#abc.ABC "abc.ABC")`

Model configured for each step of an Agent run.

Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
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

|

    
    
    class AgentModel(ABC):
        """Model configured for each step of an Agent run."""
    
        @abstractmethod
        async def request(
            self, messages: list[ModelMessage], model_settings: ModelSettings | None
        ) -> tuple[ModelResponse, Usage]:
            """Make a request to the model."""
            raise NotImplementedError()
    
        @asynccontextmanager
        async def request_stream(
            self, messages: list[ModelMessage], model_settings: ModelSettings | None
        ) -> AsyncIterator[EitherStreamedResponse]:
            """Make a request to the model and return a streaming response."""
            raise NotImplementedError(f'Streamed requests not supported by this {self.__class__.__name__}')
            # yield is required to make this a generator for type checking
            # noinspection PyUnreachableCode
            yield  # pragma: no cover
      
  
---|---  
  
####  request `abstractmethod` `async`

    
    
    request(
        messages: [list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")],
        model_settings: [ModelSettings](../../settings/#pydantic_ai.settings.ModelSettings "pydantic_ai.settings.ModelSettings") | None,
    ) -> [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[ModelResponse](../../messages/#pydantic_ai.messages.ModelResponse "pydantic_ai.messages.ModelResponse"), [Usage](../../result/#pydantic_ai.result.Usage "pydantic_ai.result.Usage")]
    

Make a request to the model.

Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
    123
    124
    125
    126
    127
    128

|

    
    
    @abstractmethod
    async def request(
        self, messages: list[ModelMessage], model_settings: ModelSettings | None
    ) -> tuple[ModelResponse, Usage]:
        """Make a request to the model."""
        raise NotImplementedError()
      
  
---|---  
  
####  request_stream `async`

    
    
    request_stream(
        messages: [list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")],
        model_settings: [ModelSettings](../../settings/#pydantic_ai.settings.ModelSettings "pydantic_ai.settings.ModelSettings") | None,
    ) -> [AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator "collections.abc.AsyncIterator")[EitherStreamedResponse]
    

Make a request to the model and return a streaming response.

Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
    130
    131
    132
    133
    134
    135
    136
    137
    138

|

    
    
    @asynccontextmanager
    async def request_stream(
        self, messages: list[ModelMessage], model_settings: ModelSettings | None
    ) -> AsyncIterator[EitherStreamedResponse]:
        """Make a request to the model and return a streaming response."""
        raise NotImplementedError(f'Streamed requests not supported by this {self.__class__.__name__}')
        # yield is required to make this a generator for type checking
        # noinspection PyUnreachableCode
        yield  # pragma: no cover
      
  
---|---  
  
###  StreamTextResponse

Bases: `[ABC](https://docs.python.org/3/library/abc.html#abc.ABC "abc.ABC")`

Streamed response from an LLM when returning text.

Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
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

|

    
    
    class StreamTextResponse(ABC):
        """Streamed response from an LLM when returning text."""
    
        def __aiter__(self) -> AsyncIterator[None]:
            """Stream the response as an async iterable, building up the text as it goes.
    
            This is an async iterator that yields `None` to avoid doing the work of validating the input and
            extracting the text field when it will often be thrown away.
            """
            return self
    
        @abstractmethod
        async def __anext__(self) -> None:
            """Process the next chunk of the response, see above for why this returns `None`."""
            raise NotImplementedError()
    
        @abstractmethod
        def get(self, *, final: bool = False) -> Iterable[str]:
            """Returns an iterable of text since the last call to `get()` — e.g. the text delta.
    
            Args:
                final: If True, this is the final call, after iteration is complete, the response should be fully validated
                    and all text extracted.
            """
            raise NotImplementedError()
    
        @abstractmethod
        def usage(self) -> Usage:
            """Return the usage of the request.
    
            NOTE: this won't return the full usage until the stream is finished.
            """
            raise NotImplementedError()
    
        @abstractmethod
        def timestamp(self) -> datetime:
            """Get the timestamp of the response."""
            raise NotImplementedError()
      
  
---|---  
  
####  __aiter__

    
    
    __aiter__() -> [AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator "collections.abc.AsyncIterator")[None]
    

Stream the response as an async iterable, building up the text as it goes.

This is an async iterator that yields `None` to avoid doing the work of
validating the input and extracting the text field when it will often be
thrown away.

Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
    144
    145
    146
    147
    148
    149
    150

|

    
    
    def __aiter__(self) -> AsyncIterator[None]:
        """Stream the response as an async iterable, building up the text as it goes.
    
        This is an async iterator that yields `None` to avoid doing the work of validating the input and
        extracting the text field when it will often be thrown away.
        """
        return self
      
  
---|---  
  
####  __anext__ `abstractmethod` `async`

    
    
    __anext__() -> None
    

Process the next chunk of the response, see above for why this returns `None`.

Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
    152
    153
    154
    155

|

    
    
    @abstractmethod
    async def __anext__(self) -> None:
        """Process the next chunk of the response, see above for why this returns `None`."""
        raise NotImplementedError()
      
  
---|---  
  
####  get `abstractmethod`

    
    
    get(*, final: [bool](https://docs.python.org/3/library/functions.html#bool) = False) -> [Iterable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable "collections.abc.Iterable")[[str](https://docs.python.org/3/library/stdtypes.html#str)]
    

Returns an iterable of text since the last call to `get()` — e.g. the text
delta.

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`final` |  `[bool](https://docs.python.org/3/library/functions.html#bool)` |  If True, this is the final call, after iteration is complete, the response should be fully validated and all text extracted. |  `False`  
  
Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
    157
    158
    159
    160
    161
    162
    163
    164
    165

|

    
    
    @abstractmethod
    def get(self, *, final: bool = False) -> Iterable[str]:
        """Returns an iterable of text since the last call to `get()` — e.g. the text delta.
    
        Args:
            final: If True, this is the final call, after iteration is complete, the response should be fully validated
                and all text extracted.
        """
        raise NotImplementedError()
      
  
---|---  
  
####  usage `abstractmethod`

    
    
    usage() -> [Usage](../../result/#pydantic_ai.result.Usage "pydantic_ai.result.Usage")
    

Return the usage of the request.

NOTE: this won't return the full usage until the stream is finished.

Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
    167
    168
    169
    170
    171
    172
    173

|

    
    
    @abstractmethod
    def usage(self) -> Usage:
        """Return the usage of the request.
    
        NOTE: this won't return the full usage until the stream is finished.
        """
        raise NotImplementedError()
      
  
---|---  
  
####  timestamp `abstractmethod`

    
    
    timestamp() -> [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime "datetime.datetime")
    

Get the timestamp of the response.

Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
    175
    176
    177
    178

|

    
    
    @abstractmethod
    def timestamp(self) -> datetime:
        """Get the timestamp of the response."""
        raise NotImplementedError()
      
  
---|---  
  
###  StreamStructuredResponse

Bases: `[ABC](https://docs.python.org/3/library/abc.html#abc.ABC "abc.ABC")`

Streamed response from an LLM when calling a tool.

Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
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

|

    
    
    class StreamStructuredResponse(ABC):
        """Streamed response from an LLM when calling a tool."""
    
        def __aiter__(self) -> AsyncIterator[None]:
            """Stream the response as an async iterable, building up the tool call as it goes.
    
            This is an async iterator that yields `None` to avoid doing the work of building the final tool call when
            it will often be thrown away.
            """
            return self
    
        @abstractmethod
        async def __anext__(self) -> None:
            """Process the next chunk of the response, see above for why this returns `None`."""
            raise NotImplementedError()
    
        @abstractmethod
        def get(self, *, final: bool = False) -> ModelResponse:
            """Get the `ModelResponse` at this point.
    
            The `ModelResponse` may or may not be complete, depending on whether the stream is finished.
    
            Args:
                final: If True, this is the final call, after iteration is complete, the response should be fully validated.
            """
            raise NotImplementedError()
    
        @abstractmethod
        def usage(self) -> Usage:
            """Get the usage of the request.
    
            NOTE: this won't return the full usage until the stream is finished.
            """
            raise NotImplementedError()
    
        @abstractmethod
        def timestamp(self) -> datetime:
            """Get the timestamp of the response."""
            raise NotImplementedError()
      
  
---|---  
  
####  __aiter__

    
    
    __aiter__() -> [AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator "collections.abc.AsyncIterator")[None]
    

Stream the response as an async iterable, building up the tool call as it
goes.

This is an async iterator that yields `None` to avoid doing the work of
building the final tool call when it will often be thrown away.

Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
    184
    185
    186
    187
    188
    189
    190

|

    
    
    def __aiter__(self) -> AsyncIterator[None]:
        """Stream the response as an async iterable, building up the tool call as it goes.
    
        This is an async iterator that yields `None` to avoid doing the work of building the final tool call when
        it will often be thrown away.
        """
        return self
      
  
---|---  
  
####  __anext__ `abstractmethod` `async`

    
    
    __anext__() -> None
    

Process the next chunk of the response, see above for why this returns `None`.

Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
    192
    193
    194
    195

|

    
    
    @abstractmethod
    async def __anext__(self) -> None:
        """Process the next chunk of the response, see above for why this returns `None`."""
        raise NotImplementedError()
      
  
---|---  
  
####  get `abstractmethod`

    
    
    get(*, final: [bool](https://docs.python.org/3/library/functions.html#bool) = False) -> [ModelResponse](../../messages/#pydantic_ai.messages.ModelResponse "pydantic_ai.messages.ModelResponse")
    

Get the `ModelResponse` at this point.

The `ModelResponse` may or may not be complete, depending on whether the
stream is finished.

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`final` |  `[bool](https://docs.python.org/3/library/functions.html#bool)` |  If True, this is the final call, after iteration is complete, the response should be fully validated. |  `False`  
  
Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
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

|

    
    
    @abstractmethod
    def get(self, *, final: bool = False) -> ModelResponse:
        """Get the `ModelResponse` at this point.
    
        The `ModelResponse` may or may not be complete, depending on whether the stream is finished.
    
        Args:
            final: If True, this is the final call, after iteration is complete, the response should be fully validated.
        """
        raise NotImplementedError()
      
  
---|---  
  
####  usage `abstractmethod`

    
    
    usage() -> [Usage](../../result/#pydantic_ai.result.Usage "pydantic_ai.result.Usage")
    

Get the usage of the request.

NOTE: this won't return the full usage until the stream is finished.

Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
    208
    209
    210
    211
    212
    213
    214

|

    
    
    @abstractmethod
    def usage(self) -> Usage:
        """Get the usage of the request.
    
        NOTE: this won't return the full usage until the stream is finished.
        """
        raise NotImplementedError()
      
  
---|---  
  
####  timestamp `abstractmethod`

    
    
    timestamp() -> [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime "datetime.datetime")
    

Get the timestamp of the response.

Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
    216
    217
    218
    219

|

    
    
    @abstractmethod
    def timestamp(self) -> datetime:
        """Get the timestamp of the response."""
        raise NotImplementedError()
      
  
---|---  
  
###  ALLOW_MODEL_REQUESTS `module-attribute`

    
    
    ALLOW_MODEL_REQUESTS = True
    

Whether to allow requests to models.

This global setting allows you to disable request to most models, e.g. to make
sure you don't accidentally make costly requests to a model during tests.

The testing models [`TestModel`](../test/#pydantic_ai.models.test.TestModel)
and [`FunctionModel`](../function/#pydantic_ai.models.function.FunctionModel)
are no affected by this setting.

###  check_allow_model_requests

    
    
    check_allow_model_requests() -> None
    

Check if model requests are allowed.

If you're defining your own models that have costs or latency associated with
their use, you should call this in `Model.agent_model`.

Raises:

Type | Description  
---|---  
`[RuntimeError](https://docs.python.org/3/library/exceptions.html#RuntimeError)` |  If model requests are not allowed.  
  
Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
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

|

    
    
    def check_allow_model_requests() -> None:
        """Check if model requests are allowed.
    
        If you're defining your own models that have costs or latency associated with their use, you should call this in
        [`Model.agent_model`][pydantic_ai.models.Model.agent_model].
    
        Raises:
            RuntimeError: If model requests are not allowed.
        """
        if not ALLOW_MODEL_REQUESTS:
            raise RuntimeError('Model requests are not allowed, since ALLOW_MODEL_REQUESTS is False')
      
  
---|---  
  
###  override_allow_model_requests

    
    
    override_allow_model_requests(
        allow_model_requests: [bool](https://docs.python.org/3/library/functions.html#bool),
    ) -> [Iterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator "collections.abc.Iterator")[None]
    

Context manager to temporarily override `ALLOW_MODEL_REQUESTS`.

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`allow_model_requests` |  `[bool](https://docs.python.org/3/library/functions.html#bool)` |  Whether to allow model requests within the context. |  _required_  
  
Source code in `pydantic_ai_slim/pydantic_ai/models/__init__.py`

    
    
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

|

    
    
    @contextmanager
    def override_allow_model_requests(allow_model_requests: bool) -> Iterator[None]:
        """Context manager to temporarily override [`ALLOW_MODEL_REQUESTS`][pydantic_ai.models.ALLOW_MODEL_REQUESTS].
    
        Args:
            allow_model_requests: Whether to allow model requests within the context.
        """
        global ALLOW_MODEL_REQUESTS
        old_value = ALLOW_MODEL_REQUESTS
        ALLOW_MODEL_REQUESTS = allow_model_requests  # pyright: ignore[reportConstantRedefinition]
        try:
            yield
        finally:
            ALLOW_MODEL_REQUESTS = old_value  # pyright: ignore[reportConstantRedefinition]
      
  
---|---  
  
© Pydantic Services Inc. 2024 to present

