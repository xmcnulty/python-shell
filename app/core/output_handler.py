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
            if self._append == "a":
                self._file.seek(0, 2)  # Move to end of file
                if self._file.tell() > 0:
                    self._file.write("\n")
                    
            self._file.write(output)
            self._file.flush()
        else:
            print(output)

    def close(self):
        if self._file:
            self._file.close()
            self._file = None
    
    def __del__(self):
        self.close()
