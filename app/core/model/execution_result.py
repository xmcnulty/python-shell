from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ExecutionResult:
    code: int = 0
    stdout: Optional[str] = None
    stderr: Optional[str] = None