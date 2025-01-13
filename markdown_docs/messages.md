Skip to content

[ ![logo](../../img/logo-white.svg) ](../.. "PydanticAI")

PydanticAI

pydantic_ai.messages

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
    * pydantic_ai.messages  [ pydantic_ai.messages  ](./) Table of contents 
      * messages 
      * SystemPromptPart 
        * content 
        * part_kind 
      * UserPromptPart 
        * content 
        * timestamp 
        * part_kind 
      * ToolReturnPart 
        * tool_name 
        * content 
        * tool_call_id 
        * timestamp 
        * part_kind 
      * RetryPromptPart 
        * content 
        * tool_name 
        * tool_call_id 
        * timestamp 
        * part_kind 
      * ModelRequestPart 
      * ModelRequest 
        * parts 
        * kind 
      * TextPart 
        * content 
        * part_kind 
      * ArgsJson 
        * args_json 
      * ArgsDict 
        * args_dict 
      * ToolCallPart 
        * tool_name 
        * args 
        * tool_call_id 
        * part_kind 
        * from_raw_args 
        * args_as_dict 
        * args_as_json_str 
      * ModelResponsePart 
      * ModelResponse 
        * parts 
        * timestamp 
        * kind 
      * ModelMessage 
      * ModelMessagesTypeAdapter 
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

  * messages 
  * SystemPromptPart 
    * content 
    * part_kind 
  * UserPromptPart 
    * content 
    * timestamp 
    * part_kind 
  * ToolReturnPart 
    * tool_name 
    * content 
    * tool_call_id 
    * timestamp 
    * part_kind 
  * RetryPromptPart 
    * content 
    * tool_name 
    * tool_call_id 
    * timestamp 
    * part_kind 
  * ModelRequestPart 
  * ModelRequest 
    * parts 
    * kind 
  * TextPart 
    * content 
    * part_kind 
  * ArgsJson 
    * args_json 
  * ArgsDict 
    * args_dict 
  * ToolCallPart 
    * tool_name 
    * args 
    * tool_call_id 
    * part_kind 
    * from_raw_args 
    * args_as_dict 
    * args_as_json_str 
  * ModelResponsePart 
  * ModelResponse 
    * parts 
    * timestamp 
    * kind 
  * ModelMessage 
  * ModelMessagesTypeAdapter 

  1. [ Introduction  ](../..)
  2. [ API Reference  ](../agent/)

# `pydantic_ai.messages`

The structure of `ModelMessage` can be shown as a graph:

###  SystemPromptPart `dataclass`

A system prompt, generally written by the application developer.

This gives the model context and guidance on how to respond.

Source code in `pydantic_ai_slim/pydantic_ai/messages.py`

    
    
    14
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

|

    
    
    @dataclass
    class SystemPromptPart:
        """A system prompt, generally written by the application developer.
    
        This gives the model context and guidance on how to respond.
        """
    
        content: str
        """The content of the prompt."""
    
        part_kind: Literal['system-prompt'] = 'system-prompt'
        """Part type identifier, this is available on all parts as a discriminator."""
      
  
---|---  
  
####  content `instance-attribute`

    
    
    content: [str](https://docs.python.org/3/library/stdtypes.html#str)
    

The content of the prompt.

####  part_kind `class-attribute` `instance-attribute`

    
    
    part_kind: [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "typing.Literal")['system-prompt'] = 'system-prompt'
    

Part type identifier, this is available on all parts as a discriminator.

###  UserPromptPart `dataclass`

A user prompt, generally written by the end user.

Content comes from the `user_prompt` parameter of
[`Agent.run`](../agent/#pydantic_ai.Agent.run),
[`Agent.run_sync`](../agent/#pydantic_ai.Agent.run_sync), and
[`Agent.run_stream`](../agent/#pydantic_ai.Agent.run_stream).

Source code in `pydantic_ai_slim/pydantic_ai/messages.py`

    
    
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

|

    
    
    @dataclass
    class UserPromptPart:
        """A user prompt, generally written by the end user.
    
        Content comes from the `user_prompt` parameter of [`Agent.run`][pydantic_ai.Agent.run],
        [`Agent.run_sync`][pydantic_ai.Agent.run_sync], and [`Agent.run_stream`][pydantic_ai.Agent.run_stream].
        """
    
        content: str
        """The content of the prompt."""
    
        timestamp: datetime = field(default_factory=_now_utc)
        """The timestamp of the prompt."""
    
        part_kind: Literal['user-prompt'] = 'user-prompt'
        """Part type identifier, this is available on all parts as a discriminator."""
      
  
---|---  
  
####  content `instance-attribute`

    
    
    content: [str](https://docs.python.org/3/library/stdtypes.html#str)
    

The content of the prompt.

####  timestamp `class-attribute` `instance-attribute`

    
    
    timestamp: [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime "datetime.datetime") = [field](https://docs.python.org/3/library/dataclasses.html#dataclasses.field "dataclasses.field")(default_factory=now_utc)
    

The timestamp of the prompt.

####  part_kind `class-attribute` `instance-attribute`

    
    
    part_kind: [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "typing.Literal")['user-prompt'] = 'user-prompt'
    

Part type identifier, this is available on all parts as a discriminator.

###  ToolReturnPart `dataclass`

A tool return message, this encodes the result of running a tool.

Source code in `pydantic_ai_slim/pydantic_ai/messages.py`

    
    
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

|

    
    
    @dataclass
    class ToolReturnPart:
        """A tool return message, this encodes the result of running a tool."""
    
        tool_name: str
        """The name of the "tool" was called."""
    
        content: Any
        """The return value."""
    
        tool_call_id: str | None = None
        """Optional tool call identifier, this is used by some models including OpenAI."""
    
        timestamp: datetime = field(default_factory=_now_utc)
        """The timestamp, when the tool returned."""
    
        part_kind: Literal['tool-return'] = 'tool-return'
        """Part type identifier, this is available on all parts as a discriminator."""
    
        def model_response_str(self) -> str:
            if isinstance(self.content, str):
                return self.content
            else:
                return tool_return_ta.dump_json(self.content).decode()
    
        def model_response_object(self) -> dict[str, Any]:
            # gemini supports JSON dict return values, but no other JSON types, hence we wrap anything else in a dict
            if isinstance(self.content, dict):
                return tool_return_ta.dump_python(self.content, mode='json')  # pyright: ignore[reportUnknownMemberType]
            else:
                return {'return_value': tool_return_ta.dump_python(self.content, mode='json')}
      
  
---|---  
  
####  tool_name `instance-attribute`

    
    
    tool_name: [str](https://docs.python.org/3/library/stdtypes.html#str)
    

The name of the "tool" was called.

####  content `instance-attribute`

    
    
    content: [Any](https://docs.python.org/3/library/typing.html#typing.Any "typing.Any")
    

The return value.

####  tool_call_id `class-attribute` `instance-attribute`

    
    
    tool_call_id: [str](https://docs.python.org/3/library/stdtypes.html#str) | None = None
    

Optional tool call identifier, this is used by some models including OpenAI.

####  timestamp `class-attribute` `instance-attribute`

    
    
    timestamp: [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime "datetime.datetime") = [field](https://docs.python.org/3/library/dataclasses.html#dataclasses.field "dataclasses.field")(default_factory=now_utc)
    

The timestamp, when the tool returned.

####  part_kind `class-attribute` `instance-attribute`

    
    
    part_kind: [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "typing.Literal")['tool-return'] = 'tool-return'
    

Part type identifier, this is available on all parts as a discriminator.

###  RetryPromptPart `dataclass`

A message back to a model asking it to try again.

This can be sent for a number of reasons:

  * Pydantic validation of tool arguments failed, here content is derived from a Pydantic [`ValidationError`](https://docs.pydantic.dev/latest/api/pydantic_core/#pydantic_core.ValidationError)
  * a tool raised a [`ModelRetry`](../exceptions/#pydantic_ai.exceptions.ModelRetry) exception
  * no tool was found for the tool name
  * the model returned plain text when a structured response was expected
  * Pydantic validation of a structured response failed, here content is derived from a Pydantic [`ValidationError`](https://docs.pydantic.dev/latest/api/pydantic_core/#pydantic_core.ValidationError)
  * a result validator raised a [`ModelRetry`](../exceptions/#pydantic_ai.exceptions.ModelRetry) exception

Source code in `pydantic_ai_slim/pydantic_ai/messages.py`

    
    
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

|

    
    
    @dataclass
    class RetryPromptPart:
        """A message back to a model asking it to try again.
    
        This can be sent for a number of reasons:
    
        * Pydantic validation of tool arguments failed, here content is derived from a Pydantic
          [`ValidationError`][pydantic_core.ValidationError]
        * a tool raised a [`ModelRetry`][pydantic_ai.exceptions.ModelRetry] exception
        * no tool was found for the tool name
        * the model returned plain text when a structured response was expected
        * Pydantic validation of a structured response failed, here content is derived from a Pydantic
          [`ValidationError`][pydantic_core.ValidationError]
        * a result validator raised a [`ModelRetry`][pydantic_ai.exceptions.ModelRetry] exception
        """
    
        content: list[pydantic_core.ErrorDetails] | str
        """Details of why and how the model should retry.
    
        If the retry was triggered by a [`ValidationError`][pydantic_core.ValidationError], this will be a list of
        error details.
        """
    
        tool_name: str | None = None
        """The name of the tool that was called, if any."""
    
        tool_call_id: str | None = None
        """Optional tool call identifier, this is used by some models including OpenAI."""
    
        timestamp: datetime = field(default_factory=_now_utc)
        """The timestamp, when the retry was triggered."""
    
        part_kind: Literal['retry-prompt'] = 'retry-prompt'
        """Part type identifier, this is available on all parts as a discriminator."""
    
        def model_response(self) -> str:
            if isinstance(self.content, str):
                description = self.content
            else:
                json_errors = error_details_ta.dump_json(self.content, exclude={'__all__': {'ctx'}}, indent=2)
                description = f'{len(self.content)} validation errors: {json_errors.decode()}'
            return f'{description}\n\nFix the errors and try again.'
      
  
---|---  
  
####  content `instance-attribute`

    
    
    content: [list](https://docs.python.org/3/library/stdtypes.html#list)[[ErrorDetails](https://docs.pydantic.dev/latest/api/pydantic_core/#pydantic_core.ErrorDetails "pydantic_core.ErrorDetails")] | [str](https://docs.python.org/3/library/stdtypes.html#str)
    

Details of why and how the model should retry.

If the retry was triggered by a
[`ValidationError`](https://docs.pydantic.dev/latest/api/pydantic_core/#pydantic_core.ValidationError),
this will be a list of error details.

####  tool_name `class-attribute` `instance-attribute`

    
    
    tool_name: [str](https://docs.python.org/3/library/stdtypes.html#str) | None = None
    

The name of the tool that was called, if any.

####  tool_call_id `class-attribute` `instance-attribute`

    
    
    tool_call_id: [str](https://docs.python.org/3/library/stdtypes.html#str) | None = None
    

Optional tool call identifier, this is used by some models including OpenAI.

####  timestamp `class-attribute` `instance-attribute`

    
    
    timestamp: [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime "datetime.datetime") = [field](https://docs.python.org/3/library/dataclasses.html#dataclasses.field "dataclasses.field")(default_factory=now_utc)
    

The timestamp, when the retry was triggered.

####  part_kind `class-attribute` `instance-attribute`

    
    
    part_kind: [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "typing.Literal")['retry-prompt'] = 'retry-prompt'
    

Part type identifier, this is available on all parts as a discriminator.

###  ModelRequestPart `module-attribute`

    
    
    ModelRequestPart = [Annotated](https://docs.python.org/3/library/typing.html#typing.Annotated "typing.Annotated")[
        [Union](https://docs.python.org/3/library/typing.html#typing.Union "typing.Union")[
            SystemPromptPart,
            UserPromptPart,
            ToolReturnPart,
            RetryPromptPart,
        ],
        [Discriminator](https://docs.pydantic.dev/latest/api/types/#pydantic.types.Discriminator "pydantic.Discriminator")("part_kind"),
    ]
    

A message part sent by PydanticAI to a model.

###  ModelRequest `dataclass`

A request generated by PydanticAI and sent to a model, e.g. a message from the
PydanticAI app to the model.

Source code in `pydantic_ai_slim/pydantic_ai/messages.py`

    
    
    135
    136
    137
    138
    139
    140
    141
    142
    143

|

    
    
    @dataclass
    class ModelRequest:
        """A request generated by PydanticAI and sent to a model, e.g. a message from the PydanticAI app to the model."""
    
        parts: list[ModelRequestPart]
        """The parts of the user message."""
    
        kind: Literal['request'] = 'request'
        """Message type identifier, this is available on all parts as a discriminator."""
      
  
---|---  
  
####  parts `instance-attribute`

    
    
    parts: [list](https://docs.python.org/3/library/stdtypes.html#list)[ModelRequestPart]
    

The parts of the user message.

####  kind `class-attribute` `instance-attribute`

    
    
    kind: [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "typing.Literal")['request'] = 'request'
    

Message type identifier, this is available on all parts as a discriminator.

###  TextPart `dataclass`

A plain text response from a model.

Source code in `pydantic_ai_slim/pydantic_ai/messages.py`

    
    
    146
    147
    148
    149
    150
    151
    152
    153
    154

|

    
    
    @dataclass
    class TextPart:
        """A plain text response from a model."""
    
        content: str
        """The text content of the response."""
    
        part_kind: Literal['text'] = 'text'
        """Part type identifier, this is available on all parts as a discriminator."""
      
  
---|---  
  
####  content `instance-attribute`

    
    
    content: [str](https://docs.python.org/3/library/stdtypes.html#str)
    

The text content of the response.

####  part_kind `class-attribute` `instance-attribute`

    
    
    part_kind: [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "typing.Literal")['text'] = 'text'
    

Part type identifier, this is available on all parts as a discriminator.

###  ArgsJson `dataclass`

Tool arguments as a JSON string.

Source code in `pydantic_ai_slim/pydantic_ai/messages.py`

    
    
    157
    158
    159
    160
    161
    162

|

    
    
    @dataclass
    class ArgsJson:
        """Tool arguments as a JSON string."""
    
        args_json: str
        """A JSON string of arguments."""
      
  
---|---  
  
####  args_json `instance-attribute`

    
    
    args_json: [str](https://docs.python.org/3/library/stdtypes.html#str)
    

A JSON string of arguments.

###  ArgsDict `dataclass`

Tool arguments as a Python dictionary.

Source code in `pydantic_ai_slim/pydantic_ai/messages.py`

    
    
    165
    166
    167
    168
    169
    170

|

    
    
    @dataclass
    class ArgsDict:
        """Tool arguments as a Python dictionary."""
    
        args_dict: dict[str, Any]
        """A python dictionary of arguments."""
      
  
---|---  
  
####  args_dict `instance-attribute`

    
    
    args_dict: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any "typing.Any")]
    

A python dictionary of arguments.

###  ToolCallPart `dataclass`

A tool call from a model.

Source code in `pydantic_ai_slim/pydantic_ai/messages.py`

    
    
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

|

    
    
    @dataclass
    class ToolCallPart:
        """A tool call from a model."""
    
        tool_name: str
        """The name of the tool to call."""
    
        args: ArgsJson | ArgsDict
        """The arguments to pass to the tool.
    
        Either as JSON or a Python dictionary depending on how data was returned.
        """
    
        tool_call_id: str | None = None
        """Optional tool call identifier, this is used by some models including OpenAI."""
    
        part_kind: Literal['tool-call'] = 'tool-call'
        """Part type identifier, this is available on all parts as a discriminator."""
    
        @classmethod
        def from_raw_args(cls, tool_name: str, args: str | dict[str, Any], tool_call_id: str | None = None) -> Self:
            """Create a `ToolCallPart` from raw arguments."""
            if isinstance(args, str):
                return cls(tool_name, ArgsJson(args), tool_call_id)
            elif isinstance(args, dict):
                return cls(tool_name, ArgsDict(args), tool_call_id)
            else:
                assert_never(args)
    
        def args_as_dict(self) -> dict[str, Any]:
            """Return the arguments as a Python dictionary.
    
            This is just for convenience with models that require dicts as input.
            """
            if isinstance(self.args, ArgsDict):
                return self.args.args_dict
            args = pydantic_core.from_json(self.args.args_json)
            assert isinstance(args, dict), 'args should be a dict'
            return cast(dict[str, Any], args)
    
        def args_as_json_str(self) -> str:
            """Return the arguments as a JSON string.
    
            This is just for convenience with models that require JSON strings as input.
            """
            if isinstance(self.args, ArgsJson):
                return self.args.args_json
            return pydantic_core.to_json(self.args.args_dict).decode()
    
        def has_content(self) -> bool:
            if isinstance(self.args, ArgsDict):
                return any(self.args.args_dict.values())
            else:
                return bool(self.args.args_json)
      
  
---|---  
  
####  tool_name `instance-attribute`

    
    
    tool_name: [str](https://docs.python.org/3/library/stdtypes.html#str)
    

The name of the tool to call.

####  args `instance-attribute`

    
    
    args: ArgsJson | ArgsDict
    

The arguments to pass to the tool.

Either as JSON or a Python dictionary depending on how data was returned.

####  tool_call_id `class-attribute` `instance-attribute`

    
    
    tool_call_id: [str](https://docs.python.org/3/library/stdtypes.html#str) | None = None
    

Optional tool call identifier, this is used by some models including OpenAI.

####  part_kind `class-attribute` `instance-attribute`

    
    
    part_kind: [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "typing.Literal")['tool-call'] = 'tool-call'
    

Part type identifier, this is available on all parts as a discriminator.

####  from_raw_args `classmethod`

    
    
    from_raw_args(
        tool_name: [str](https://docs.python.org/3/library/stdtypes.html#str),
        args: [str](https://docs.python.org/3/library/stdtypes.html#str) | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any "typing.Any")],
        tool_call_id: [str](https://docs.python.org/3/library/stdtypes.html#str) | None = None,
    ) -> [Self](https://typing-extensions.readthedocs.io/en/latest/index.html#typing_extensions.Self "typing_extensions.Self")
    

Create a `ToolCallPart` from raw arguments.

Source code in `pydantic_ai_slim/pydantic_ai/messages.py`

    
    
    192
    193
    194
    195
    196
    197
    198
    199
    200

|

    
    
    @classmethod
    def from_raw_args(cls, tool_name: str, args: str | dict[str, Any], tool_call_id: str | None = None) -> Self:
        """Create a `ToolCallPart` from raw arguments."""
        if isinstance(args, str):
            return cls(tool_name, ArgsJson(args), tool_call_id)
        elif isinstance(args, dict):
            return cls(tool_name, ArgsDict(args), tool_call_id)
        else:
            assert_never(args)
      
  
---|---  
  
####  args_as_dict

    
    
    args_as_dict() -> [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any "typing.Any")]
    

Return the arguments as a Python dictionary.

This is just for convenience with models that require dicts as input.

Source code in `pydantic_ai_slim/pydantic_ai/messages.py`

    
    
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

    
    
    def args_as_dict(self) -> dict[str, Any]:
        """Return the arguments as a Python dictionary.
    
        This is just for convenience with models that require dicts as input.
        """
        if isinstance(self.args, ArgsDict):
            return self.args.args_dict
        args = pydantic_core.from_json(self.args.args_json)
        assert isinstance(args, dict), 'args should be a dict'
        return cast(dict[str, Any], args)
      
  
---|---  
  
####  args_as_json_str

    
    
    args_as_json_str() -> [str](https://docs.python.org/3/library/stdtypes.html#str)
    

Return the arguments as a JSON string.

This is just for convenience with models that require JSON strings as input.

Source code in `pydantic_ai_slim/pydantic_ai/messages.py`

    
    
    213
    214
    215
    216
    217
    218
    219
    220

|

    
    
    def args_as_json_str(self) -> str:
        """Return the arguments as a JSON string.
    
        This is just for convenience with models that require JSON strings as input.
        """
        if isinstance(self.args, ArgsJson):
            return self.args.args_json
        return pydantic_core.to_json(self.args.args_dict).decode()
      
  
---|---  
  
###  ModelResponsePart `module-attribute`

    
    
    ModelResponsePart = [Annotated](https://docs.python.org/3/library/typing.html#typing.Annotated "typing.Annotated")[
        [Union](https://docs.python.org/3/library/typing.html#typing.Union "typing.Union")[TextPart, ToolCallPart],
        [Discriminator](https://docs.pydantic.dev/latest/api/types/#pydantic.types.Discriminator "pydantic.Discriminator")("part_kind"),
    ]
    

A message part returned by a model.

###  ModelResponse `dataclass`

A response from a model, e.g. a message from the model to the PydanticAI app.

Source code in `pydantic_ai_slim/pydantic_ai/messages.py`

    
    
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

|

    
    
    @dataclass
    class ModelResponse:
        """A response from a model, e.g. a message from the model to the PydanticAI app."""
    
        parts: list[ModelResponsePart]
        """The parts of the model message."""
    
        timestamp: datetime = field(default_factory=_now_utc)
        """The timestamp of the response.
    
        If the model provides a timestamp in the response (as OpenAI does) that will be used.
        """
    
        kind: Literal['response'] = 'response'
        """Message type identifier, this is available on all parts as a discriminator."""
    
        @classmethod
        def from_text(cls, content: str, timestamp: datetime | None = None) -> Self:
            return cls([TextPart(content)], timestamp=timestamp or _now_utc())
    
        @classmethod
        def from_tool_call(cls, tool_call: ToolCallPart) -> Self:
            return cls([tool_call])
      
  
---|---  
  
####  parts `instance-attribute`

    
    
    parts: [list](https://docs.python.org/3/library/stdtypes.html#list)[ModelResponsePart]
    

The parts of the model message.

####  timestamp `class-attribute` `instance-attribute`

    
    
    timestamp: [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime "datetime.datetime") = [field](https://docs.python.org/3/library/dataclasses.html#dataclasses.field "dataclasses.field")(default_factory=now_utc)
    

The timestamp of the response.

If the model provides a timestamp in the response (as OpenAI does) that will
be used.

####  kind `class-attribute` `instance-attribute`

    
    
    kind: [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "typing.Literal")['response'] = 'response'
    

Message type identifier, this is available on all parts as a discriminator.

###  ModelMessage `module-attribute`

    
    
    ModelMessage = [Union](https://docs.python.org/3/library/typing.html#typing.Union "typing.Union")[ModelRequest, ModelResponse]
    

Any message send to or returned by a model.

###  ModelMessagesTypeAdapter `module-attribute`

    
    
    ModelMessagesTypeAdapter = [TypeAdapter](https://docs.pydantic.dev/latest/api/type_adapter/#pydantic.type_adapter.TypeAdapter "pydantic.TypeAdapter")(
        [list](https://docs.python.org/3/library/stdtypes.html#list)[[Annotated](https://docs.python.org/3/library/typing.html#typing.Annotated "typing.Annotated")[ModelMessage, [Discriminator](https://docs.pydantic.dev/latest/api/types/#pydantic.types.Discriminator "pydantic.Discriminator")("kind")]],
        config=[ConfigDict](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict "pydantic.ConfigDict")(defer_build=True),
    )
    

Pydantic
[`TypeAdapter`](https://docs.pydantic.dev/latest/api/type_adapter/#pydantic.type_adapter.TypeAdapter)
for (de)serializing messages.

© Pydantic Services Inc. 2024 to present

