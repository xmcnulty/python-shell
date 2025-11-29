from abc import ABC, abstractmethod
from typing import List
from app.core.output_handler import OutputHandler

class Command(ABC):
    def __init__(self, stdout: OutputHandler, stderr: OutputHandler) -> None:
        self._stdout = stdout
        self._stderr = stderr
        
        super().__init__()

    @abstractmethod
    def execute(self, args: List[str]) -> int:
        pass