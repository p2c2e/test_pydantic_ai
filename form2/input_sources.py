from abc import ABC, abstractmethod
from typing import Callable

class InputSource(ABC):
    @abstractmethod
    async def get_input(self, prompt: str) -> str:
        """Get input from the source"""
        pass

class TerminalInputSource(InputSource):
    async def get_input(self, prompt: str) -> str:
        return input(prompt)

class CallbackInputSource(InputSource):
    def __init__(self, callback: Callable[[str], str]):
        self.callback = callback
        
    async def get_input(self, prompt: str) -> str:
        return self.callback(prompt)
