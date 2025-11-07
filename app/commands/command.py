from abc import ABC, abstractmethod
from typing import List
from app.core.output_handler import OutputHandler

class Command(ABC):
    @abstractmethod
    def execute(self, args: List[str], stdout: OutputHandler):
        pass