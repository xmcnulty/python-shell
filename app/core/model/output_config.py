from dataclasses import dataclass
from typing import Optional
from enum import Enum

class OutputType(Enum):
    APPEND = "a"
    WRITE = "w"
    NONE = ""

@dataclass(frozen=True)
class OutputConfig:
    """
    Stores configuration for redirecting output. 
    Contains path to output file and whether output should be appended to file.
    If filepath is empty, output to stdout or stderr.
    """
    file_path: str
    type: OutputType
