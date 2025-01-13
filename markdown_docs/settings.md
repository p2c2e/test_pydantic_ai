Skip to content

[ ![logo](../../img/logo-white.svg) ](../.. "PydanticAI")

PydanticAI

pydantic_ai.settings

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
    * [ pydantic_ai.result  ](../result/)
    * [ pydantic_ai.messages  ](../messages/)
    * [ pydantic_ai.exceptions  ](../exceptions/)
    * pydantic_ai.settings  [ pydantic_ai.settings  ](./) Table of contents 
      * settings 
      * ModelSettings 
        * max_tokens 
        * temperature 
        * top_p 
        * timeout 
      * UsageLimits 
        * request_limit 
        * request_tokens_limit 
        * response_tokens_limit 
        * total_tokens_limit 
        * has_token_limits 
        * check_before_request 
        * check_tokens 
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

  * settings 
  * ModelSettings 
    * max_tokens 
    * temperature 
    * top_p 
    * timeout 
  * UsageLimits 
    * request_limit 
    * request_tokens_limit 
    * response_tokens_limit 
    * total_tokens_limit 
    * has_token_limits 
    * check_before_request 
    * check_tokens 

  1. [ Introduction  ](../..)
  2. [ API Reference  ](../agent/)

# `pydantic_ai.settings`

###  ModelSettings

Bases: `[TypedDict](https://typing-
extensions.readthedocs.io/en/latest/index.html#typing_extensions.TypedDict
"typing_extensions.TypedDict")`

Settings to configure an LLM.

Here we include only settings which apply to multiple models / model
providers.

Source code in `pydantic_ai_slim/pydantic_ai/settings.py`

    
    
    15
    16
    17
    18
    19
    20
    21
    22
    23
    24
    25
    26
    27
    28
    29
    30
    31
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

|

    
    
    class ModelSettings(TypedDict, total=False):
        """Settings to configure an LLM.
    
        Here we include only settings which apply to multiple models / model providers.
        """
    
        max_tokens: int
        """The maximum number of tokens to generate before stopping.
    
        Supported by:
        * Gemini
        * Anthropic
        * OpenAI
        * Groq
        """
    
        temperature: float
        """Amount of randomness injected into the response.
    
        Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to a model's
        maximum `temperature` for creative and generative tasks.
    
        Note that even with `temperature` of `0.0`, the results will not be fully deterministic.
    
        Supported by:
        * Gemini
        * Anthropic
        * OpenAI
        * Groq
        """
    
        top_p: float
        """An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass.
    
        So 0.1 means only the tokens comprising the top 10% probability mass are considered.
    
        You should either alter `temperature` or `top_p`, but not both.
    
        Supported by:
        * Gemini
        * Anthropic
        * OpenAI
        * Groq
        """
    
        timeout: float | Timeout
        """Override the client-level default timeout for a request, in seconds.
    
        Supported by:
        * Gemini
        * Anthropic
        * OpenAI
        * Groq
        """
      
  
---|---  
  
####  max_tokens `instance-attribute`

    
    
    max_tokens: [int](https://docs.python.org/3/library/functions.html#int)
    

The maximum number of tokens to generate before stopping.

Supported by: * Gemini * Anthropic * OpenAI * Groq

####  temperature `instance-attribute`

    
    
    temperature: [float](https://docs.python.org/3/library/functions.html#float)
    

Amount of randomness injected into the response.

Use `temperature` closer to `0.0` for analytical / multiple choice, and closer
to a model's maximum `temperature` for creative and generative tasks.

Note that even with `temperature` of `0.0`, the results will not be fully
deterministic.

Supported by: * Gemini * Anthropic * OpenAI * Groq

####  top_p `instance-attribute`

    
    
    top_p: [float](https://docs.python.org/3/library/functions.html#float)
    

An alternative to sampling with temperature, called nucleus sampling, where
the model considers the results of the tokens with top_p probability mass.

So 0.1 means only the tokens comprising the top 10% probability mass are
considered.

You should either alter `temperature` or `top_p`, but not both.

Supported by: * Gemini * Anthropic * OpenAI * Groq

####  timeout `instance-attribute`

    
    
    timeout: [float](https://docs.python.org/3/library/functions.html#float) | Timeout
    

Override the client-level default timeout for a request, in seconds.

Supported by: * Gemini * Anthropic * OpenAI * Groq

###  UsageLimits `dataclass`

Limits on model usage.

The request count is tracked by pydantic_ai, and the request limit is checked
before each request to the model. Token counts are provided in responses from
the model, and the token limits are checked after each response.

Each of the limits can be set to `None` to disable that limit.

Source code in `pydantic_ai_slim/pydantic_ai/settings.py`

    
    
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
    118
    119
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

|

    
    
    @dataclass
    class UsageLimits:
        """Limits on model usage.
    
        The request count is tracked by pydantic_ai, and the request limit is checked before each request to the model.
        Token counts are provided in responses from the model, and the token limits are checked after each response.
    
        Each of the limits can be set to `None` to disable that limit.
        """
    
        request_limit: int | None = 50
        """The maximum number of requests allowed to the model."""
        request_tokens_limit: int | None = None
        """The maximum number of tokens allowed in requests to the model."""
        response_tokens_limit: int | None = None
        """The maximum number of tokens allowed in responses from the model."""
        total_tokens_limit: int | None = None
        """The maximum number of tokens allowed in requests and responses combined."""
    
        def has_token_limits(self) -> bool:
            """Returns `True` if this instance places any limits on token counts.
    
            If this returns `False`, the `check_tokens` method will never raise an error.
    
            This is useful because if we have token limits, we need to check them after receiving each streamed message.
            If there are no limits, we can skip that processing in the streaming response iterator.
            """
            return any(
                limit is not None
                for limit in (self.request_tokens_limit, self.response_tokens_limit, self.total_tokens_limit)
            )
    
        def check_before_request(self, usage: Usage) -> None:
            """Raises a `UsageLimitExceeded` exception if the next request would exceed the request_limit."""
            request_limit = self.request_limit
            if request_limit is not None and usage.requests >= request_limit:
                raise UsageLimitExceeded(f'The next request would exceed the request_limit of {request_limit}')
    
        def check_tokens(self, usage: Usage) -> None:
            """Raises a `UsageLimitExceeded` exception if the usage exceeds any of the token limits."""
            request_tokens = usage.request_tokens or 0
            if self.request_tokens_limit is not None and request_tokens > self.request_tokens_limit:
                raise UsageLimitExceeded(
                    f'Exceeded the request_tokens_limit of {self.request_tokens_limit} ({request_tokens=})'
                )
    
            response_tokens = usage.response_tokens or 0
            if self.response_tokens_limit is not None and response_tokens > self.response_tokens_limit:
                raise UsageLimitExceeded(
                    f'Exceeded the response_tokens_limit of {self.response_tokens_limit} ({response_tokens=})'
                )
    
            total_tokens = request_tokens + response_tokens
            if self.total_tokens_limit is not None and total_tokens > self.total_tokens_limit:
                raise UsageLimitExceeded(f'Exceeded the total_tokens_limit of {self.total_tokens_limit} ({total_tokens=})')
      
  
---|---  
  
####  request_limit `class-attribute` `instance-attribute`

    
    
    request_limit: [int](https://docs.python.org/3/library/functions.html#int) | None = 50
    

The maximum number of requests allowed to the model.

####  request_tokens_limit `class-attribute` `instance-attribute`

    
    
    request_tokens_limit: [int](https://docs.python.org/3/library/functions.html#int) | None = None
    

The maximum number of tokens allowed in requests to the model.

####  response_tokens_limit `class-attribute` `instance-attribute`

    
    
    response_tokens_limit: [int](https://docs.python.org/3/library/functions.html#int) | None = None
    

The maximum number of tokens allowed in responses from the model.

####  total_tokens_limit `class-attribute` `instance-attribute`

    
    
    total_tokens_limit: [int](https://docs.python.org/3/library/functions.html#int) | None = None
    

The maximum number of tokens allowed in requests and responses combined.

####  has_token_limits

    
    
    has_token_limits() -> [bool](https://docs.python.org/3/library/functions.html#bool)
    

Returns `True` if this instance places any limits on token counts.

If this returns `False`, the `check_tokens` method will never raise an error.

This is useful because if we have token limits, we need to check them after
receiving each streamed message. If there are no limits, we can skip that
processing in the streaming response iterator.

Source code in `pydantic_ai_slim/pydantic_ai/settings.py`

    
    
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

    
    
    def has_token_limits(self) -> bool:
        """Returns `True` if this instance places any limits on token counts.
    
        If this returns `False`, the `check_tokens` method will never raise an error.
    
        This is useful because if we have token limits, we need to check them after receiving each streamed message.
        If there are no limits, we can skip that processing in the streaming response iterator.
        """
        return any(
            limit is not None
            for limit in (self.request_tokens_limit, self.response_tokens_limit, self.total_tokens_limit)
        )
      
  
---|---  
  
####  check_before_request

    
    
    check_before_request(usage: [Usage](../result/#pydantic_ai.result.Usage "pydantic_ai.result.Usage")) -> None
    

Raises a `UsageLimitExceeded` exception if the next request would exceed the
request_limit.

Source code in `pydantic_ai_slim/pydantic_ai/settings.py`

    
    
    115
    116
    117
    118
    119

|

    
    
    def check_before_request(self, usage: Usage) -> None:
        """Raises a `UsageLimitExceeded` exception if the next request would exceed the request_limit."""
        request_limit = self.request_limit
        if request_limit is not None and usage.requests >= request_limit:
            raise UsageLimitExceeded(f'The next request would exceed the request_limit of {request_limit}')
      
  
---|---  
  
####  check_tokens

    
    
    check_tokens(usage: [Usage](../result/#pydantic_ai.result.Usage "pydantic_ai.result.Usage")) -> None
    

Raises a `UsageLimitExceeded` exception if the usage exceeds any of the token
limits.

Source code in `pydantic_ai_slim/pydantic_ai/settings.py`

    
    
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

|

    
    
    def check_tokens(self, usage: Usage) -> None:
        """Raises a `UsageLimitExceeded` exception if the usage exceeds any of the token limits."""
        request_tokens = usage.request_tokens or 0
        if self.request_tokens_limit is not None and request_tokens > self.request_tokens_limit:
            raise UsageLimitExceeded(
                f'Exceeded the request_tokens_limit of {self.request_tokens_limit} ({request_tokens=})'
            )
    
        response_tokens = usage.response_tokens or 0
        if self.response_tokens_limit is not None and response_tokens > self.response_tokens_limit:
            raise UsageLimitExceeded(
                f'Exceeded the response_tokens_limit of {self.response_tokens_limit} ({response_tokens=})'
            )
    
        total_tokens = request_tokens + response_tokens
        if self.total_tokens_limit is not None and total_tokens > self.total_tokens_limit:
            raise UsageLimitExceeded(f'Exceeded the total_tokens_limit of {self.total_tokens_limit} ({total_tokens=})')
      
  
---|---  
  
© Pydantic Services Inc. 2024 to present

