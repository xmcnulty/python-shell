from typing import List, Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class CommandContext:
    args: List[str]
    stdout: Optional[str] # if None, print to terminal
    append_stdout: bool = False