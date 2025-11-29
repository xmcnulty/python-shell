from typing import Optional
from app.core.model.output_config import *

class OutputHandler:

    _path = None
    _append = None
    _file = None

    def __init__(self, config: Optional[OutputConfig]) -> None:
        if config:
            self._path = config.file_path
            self._append = config.type.value
            self._file = open(self._path, self._append)

    def write(self, output: str):
        if self._file:
            # Write output exactly as provided. Do not inject additional newlines;
            # callers (builtins or external command wrapper) should include
            # trailing newlines where appropriate.
            self._file.write(output)
            self._file.flush()
        else:
            # When not redirecting to a file, print to stdout as usual.
            print(output, end="")

    def close(self):
        if self._file:
            self._file.close()
            self._file = None
    
    def __del__(self):
        self.close()
