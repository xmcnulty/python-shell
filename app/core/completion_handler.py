from typing import List

class CompletionHandler:
    def __init__(self, builtins: List[str]) -> None:
        self._builtins = builtins

    def complete_command(self, prefix: str) -> List[str]:
        return [cmd for cmd in self._builtins if cmd.startswith(prefix)]