from abc import ABC, abstractmethod
from typing import List
from app.core.output_handler import OutputHandler
from app.core.model.execution_result import ExecutionResult

class Command(ABC):
    @abstractmethod
    def execute(self, args: List[str]) -> ExecutionResult:
        pass