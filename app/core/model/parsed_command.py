from dataclasses import dataclass
from app.core.model.output_config import OutputConfig
from typing import List, Optional

@dataclass(frozen=True)
class ParsedCommand:
    command: str
    args: List[str]
    stdout: Optional[OutputConfig]
    stderr: Optional[OutputConfig]