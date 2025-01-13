Skip to content

[ ![logo](../../../img/logo-white.svg) ](../../.. "PydanticAI")

PydanticAI

pydantic_ai.models.ollama

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
    * pydantic_ai.models.ollama  [ pydantic_ai.models.ollama  ](./) Table of contents 
      * Setup 
      * Example local usage 
      * Example using a remote server 
        * ollama 
        * CommonOllamaModelNames 
        * OllamaModelName 
        * OllamaModel 
          * __init__ 
    * [ pydantic_ai.models.test  ](../test/)
    * [ pydantic_ai.models.function  ](../function/)

Table of contents

  * Setup 
  * Example local usage 
  * Example using a remote server 
    * ollama 
    * CommonOllamaModelNames 
    * OllamaModelName 
    * OllamaModel 
      * __init__ 

  1. [ Introduction  ](../../..)
  2. [ API Reference  ](../../agent/)

# `pydantic_ai.models.ollama`

## Setup

For details on how to set up authentication with this model, see [model
configuration for Ollama](../../../models/#ollama).

## Example local usage

With `ollama` installed, you can run the server with the model you want to
use:

terminal-run-ollama

    
    
    ollama run llama3.2
    

(this will pull the `llama3.2` model if you don't already have it downloaded)

Then run your code, here's a minimal example:

ollama_example.py

    
    
    from pydantic import BaseModel
    
    from pydantic_ai import Agent
    
    
    class CityLocation(BaseModel):
        city: str
        country: str
    
    
    agent = Agent('ollama:llama3.2', result_type=CityLocation)
    
    result = agent.run_sync('Where were the olympics held in 2012?')
    print(result.data)
    #> city='London' country='United Kingdom'
    print(result.usage())
    """
    Usage(requests=1, request_tokens=57, response_tokens=8, total_tokens=65, details=None)
    """
    

## Example using a remote server

ollama_example_with_remote_server.py

    
    
    from pydantic import BaseModel
    
    from pydantic_ai import Agent
    from pydantic_ai.models.ollama import OllamaModel
    
    ollama_model = OllamaModel(
        model_name='qwen2.5-coder:7b',  
        base_url='http://192.168.1.74:11434/v1',  
    )
    
    
    class CityLocation(BaseModel):
        city: str
        country: str
    
    
    agent = Agent(model=ollama_model, result_type=CityLocation)
    
    result = agent.run_sync('Where were the olympics held in 2012?')
    print(result.data)
    #> city='London' country='United Kingdom'
    print(result.usage())
    """
    Usage(requests=1, request_tokens=57, response_tokens=8, total_tokens=65, details=None)
    """
    

  1.   2. 

See `OllamaModel` for more information

###  CommonOllamaModelNames `module-attribute`

    
    
    CommonOllamaModelNames = [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "typing.Literal")[
        "codellama",
        "gemma",
        "gemma2",
        "llama3",
        "llama3.1",
        "llama3.2",
        "llama3.2-vision",
        "llama3.3",
        "mistral",
        "mistral-nemo",
        "mixtral",
        "phi3",
        "qwq",
        "qwen",
        "qwen2",
        "qwen2.5",
        "starcoder2",
    ]
    

This contains just the most common ollama models.

For a full list see [ollama.com/library](https://ollama.com/library).

###  OllamaModelName `module-attribute`

    
    
    OllamaModelName = [Union](https://docs.python.org/3/library/typing.html#typing.Union "typing.Union")[CommonOllamaModelNames, [str](https://docs.python.org/3/library/stdtypes.html#str)]
    

Possible ollama models.

Since Ollama supports hundreds of models, we explicitly list the most models
but allow any name in the type hints.

###  OllamaModel `dataclass`

Bases: `[Model](../base/#pydantic_ai.models.Model "pydantic_ai.models.Model")`

A model that implements Ollama using the OpenAI API.

Internally, this uses the [OpenAI Python
client](https://github.com/openai/openai-python) to interact with the Ollama
server.

Apart from `__init__`, all methods are private or match those of the base
class.

Source code in `pydantic_ai_slim/pydantic_ai/models/ollama.py`

    
    
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

|

    
    
    @dataclass(init=False)
    class OllamaModel(Model):
        """A model that implements Ollama using the OpenAI API.
    
        Internally, this uses the [OpenAI Python client](https://github.com/openai/openai-python) to interact with the Ollama server.
    
        Apart from `__init__`, all methods are private or match those of the base class.
        """
    
        model_name: OllamaModelName
        openai_model: OpenAIModel
    
        def __init__(
            self,
            model_name: OllamaModelName,
            *,
            base_url: str | None = 'http://localhost:11434/v1/',
            openai_client: AsyncOpenAI | None = None,
            http_client: AsyncHTTPClient | None = None,
        ):
            """Initialize an Ollama model.
    
            Ollama has built-in compatability for the OpenAI chat completions API ([source](https://ollama.com/blog/openai-compatibility)), so we reuse the
            [`OpenAIModel`][pydantic_ai.models.openai.OpenAIModel] here.
    
            Args:
                model_name: The name of the Ollama model to use. List of models available [here](https://ollama.com/library)
                    You must first download the model (`ollama pull <MODEL-NAME>`) in order to use the model
                base_url: The base url for the ollama requests. The default value is the ollama default
                openai_client: An existing
                    [`AsyncOpenAI`](https://github.com/openai/openai-python?tab=readme-ov-file#async-usage)
                    client to use, if provided, `base_url` and `http_client` must be `None`.
                http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
            """
            self.model_name = model_name
            if openai_client is not None:
                assert base_url is None, 'Cannot provide both `openai_client` and `base_url`'
                assert http_client is None, 'Cannot provide both `openai_client` and `http_client`'
                self.openai_model = OpenAIModel(model_name=model_name, openai_client=openai_client)
            else:
                # API key is not required for ollama but a value is required to create the client
                http_client_ = http_client or cached_async_http_client()
                oai_client = AsyncOpenAI(base_url=base_url, api_key='ollama', http_client=http_client_)
                self.openai_model = OpenAIModel(model_name=model_name, openai_client=oai_client)
    
        async def agent_model(
            self,
            *,
            function_tools: list[ToolDefinition],
            allow_text_result: bool,
            result_tools: list[ToolDefinition],
        ) -> AgentModel:
            return await self.openai_model.agent_model(
                function_tools=function_tools,
                allow_text_result=allow_text_result,
                result_tools=result_tools,
            )
    
        def name(self) -> str:
            return f'ollama:{self.model_name}'
      
  
---|---  
  
####  __init__

    
    
    __init__(
        model_name: OllamaModelName,
        *,
        base_url: [str](https://docs.python.org/3/library/stdtypes.html#str) | None = "http://localhost:11434/v1/",
        openai_client: AsyncOpenAI | None = None,
        http_client: AsyncClient | None = None
    )
    

Initialize an Ollama model.

Ollama has built-in compatability for the OpenAI chat completions API
([source](https://ollama.com/blog/openai-compatibility)), so we reuse the
[`OpenAIModel`](../openai/#pydantic_ai.models.openai.OpenAIModel) here.

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`model_name` |  `OllamaModelName` |  The name of the Ollama model to use. List of models available [here](https://ollama.com/library) You must first download the model (`ollama pull <MODEL-NAME>`) in order to use the model |  _required_  
`base_url` |  `[str](https://docs.python.org/3/library/stdtypes.html#str) | None` |  The base url for the ollama requests. The default value is the ollama default |  `'http://localhost:11434/v1/'`  
`openai_client` |  `AsyncOpenAI | None` |  An existing [`AsyncOpenAI`](https://github.com/openai/openai-python?tab=readme-ov-file#async-usage) client to use, if provided, `base_url` and `http_client` must be `None`. |  `None`  
`http_client` |  `AsyncClient | None` |  An existing `httpx.AsyncClient` to use for making HTTP requests. |  `None`  
  
Source code in `pydantic_ai_slim/pydantic_ai/models/ollama.py`

    
    
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

|

    
    
    def __init__(
        self,
        model_name: OllamaModelName,
        *,
        base_url: str | None = 'http://localhost:11434/v1/',
        openai_client: AsyncOpenAI | None = None,
        http_client: AsyncHTTPClient | None = None,
    ):
        """Initialize an Ollama model.
    
        Ollama has built-in compatability for the OpenAI chat completions API ([source](https://ollama.com/blog/openai-compatibility)), so we reuse the
        [`OpenAIModel`][pydantic_ai.models.openai.OpenAIModel] here.
    
        Args:
            model_name: The name of the Ollama model to use. List of models available [here](https://ollama.com/library)
                You must first download the model (`ollama pull <MODEL-NAME>`) in order to use the model
            base_url: The base url for the ollama requests. The default value is the ollama default
            openai_client: An existing
                [`AsyncOpenAI`](https://github.com/openai/openai-python?tab=readme-ov-file#async-usage)
                client to use, if provided, `base_url` and `http_client` must be `None`.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        """
        self.model_name = model_name
        if openai_client is not None:
            assert base_url is None, 'Cannot provide both `openai_client` and `base_url`'
            assert http_client is None, 'Cannot provide both `openai_client` and `http_client`'
            self.openai_model = OpenAIModel(model_name=model_name, openai_client=openai_client)
        else:
            # API key is not required for ollama but a value is required to create the client
            http_client_ = http_client or cached_async_http_client()
            oai_client = AsyncOpenAI(base_url=base_url, api_key='ollama', http_client=http_client_)
            self.openai_model = OpenAIModel(model_name=model_name, openai_client=oai_client)
      
  
---|---  
  
© Pydantic Services Inc. 2024 to present

