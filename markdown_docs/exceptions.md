Skip to content

[ ![logo](../../img/logo-white.svg) ](../.. "PydanticAI")

PydanticAI

pydantic_ai.exceptions

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
    * pydantic_ai.exceptions  [ pydantic_ai.exceptions  ](./) Table of contents 
      * exceptions 
      * ModelRetry 
        * message 
      * UserError 
        * message 
      * AgentRunError 
        * message 
      * UsageLimitExceeded 
      * UnexpectedModelBehavior 
        * message 
        * body 
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

  * exceptions 
  * ModelRetry 
    * message 
  * UserError 
    * message 
  * AgentRunError 
    * message 
  * UsageLimitExceeded 
  * UnexpectedModelBehavior 
    * message 
    * body 

  1. [ Introduction  ](../..)
  2. [ API Reference  ](../agent/)

# `pydantic_ai.exceptions`

###  ModelRetry

Bases:
`[Exception](https://docs.python.org/3/library/exceptions.html#Exception)`

Exception raised when a tool function should be retried.

The agent will return the message to the model and ask it to try calling the
function/tool again.

Source code in `pydantic_ai_slim/pydantic_ai/exceptions.py`

    
    
     8
     9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19

|

    
    
    class ModelRetry(Exception):
        """Exception raised when a tool function should be retried.
    
        The agent will return the message to the model and ask it to try calling the function/tool again.
        """
    
        message: str
        """The message to return to the model."""
    
        def __init__(self, message: str):
            self.message = message
            super().__init__(message)
      
  
---|---  
  
####  message `instance-attribute`

    
    
    message: [str](https://docs.python.org/3/library/stdtypes.html#str) = message
    

The message to return to the model.

###  UserError

Bases:
`[RuntimeError](https://docs.python.org/3/library/exceptions.html#RuntimeError)`

Error caused by a usage mistake by the application developer — You!

Source code in `pydantic_ai_slim/pydantic_ai/exceptions.py`

    
    
    22
    23
    24
    25
    26
    27
    28
    29
    30

|

    
    
    class UserError(RuntimeError):
        """Error caused by a usage mistake by the application developer — You!"""
    
        message: str
        """Description of the mistake."""
    
        def __init__(self, message: str):
            self.message = message
            super().__init__(message)
      
  
---|---  
  
####  message `instance-attribute`

    
    
    message: [str](https://docs.python.org/3/library/stdtypes.html#str) = message
    

Description of the mistake.

###  AgentRunError

Bases:
`[RuntimeError](https://docs.python.org/3/library/exceptions.html#RuntimeError)`

Base class for errors occurring during an agent run.

Source code in `pydantic_ai_slim/pydantic_ai/exceptions.py`

    
    
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

|

    
    
    class AgentRunError(RuntimeError):
        """Base class for errors occurring during an agent run."""
    
        message: str
        """The error message."""
    
        def __init__(self, message: str):
            self.message = message
            super().__init__(message)
    
        def __str__(self) -> str:
            return self.message
      
  
---|---  
  
####  message `instance-attribute`

    
    
    message: [str](https://docs.python.org/3/library/stdtypes.html#str) = message
    

The error message.

###  UsageLimitExceeded

Bases: `AgentRunError`

Error raised when a Model's usage exceeds the specified limits.

Source code in `pydantic_ai_slim/pydantic_ai/exceptions.py`

    
    
    47
    48

|

    
    
    class UsageLimitExceeded(AgentRunError):
        """Error raised when a Model's usage exceeds the specified limits."""
      
  
---|---  
  
###  UnexpectedModelBehavior

Bases: `AgentRunError`

Error caused by unexpected Model behavior, e.g. an unexpected response code.

Source code in `pydantic_ai_slim/pydantic_ai/exceptions.py`

    
    
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

|

    
    
    class UnexpectedModelBehavior(AgentRunError):
        """Error caused by unexpected Model behavior, e.g. an unexpected response code."""
    
        message: str
        """Description of the unexpected behavior."""
        body: str | None
        """The body of the response, if available."""
    
        def __init__(self, message: str, body: str | None = None):
            self.message = message
            if body is None:
                self.body: str | None = None
            else:
                try:
                    self.body = json.dumps(json.loads(body), indent=2)
                except ValueError:
                    self.body = body
            super().__init__(message)
    
        def __str__(self) -> str:
            if self.body:
                return f'{self.message}, body:\n{self.body}'
            else:
                return self.message
      
  
---|---  
  
####  message `instance-attribute`

    
    
    message: [str](https://docs.python.org/3/library/stdtypes.html#str) = message
    

Description of the unexpected behavior.

####  body `instance-attribute`

    
    
    body: [str](https://docs.python.org/3/library/stdtypes.html#str) | None = [dumps](https://docs.python.org/3/library/json.html#json.dumps "json.dumps")([loads](https://docs.python.org/3/library/json.html#json.loads "json.loads")(body), indent=2)
    

The body of the response, if available.

© Pydantic Services Inc. 2024 to present

