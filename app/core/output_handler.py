from typing import Optional

class OutputHandler:

    def __init__(self, path: Optional[str], append: bool) -> None:
        self._path = path
        self._append = append
        self._file = None

        if path:
            mode = "a" if append else "w"
            self._file = open(path, mode, encoding='utf-8')


    @property
    def path(self) -> Optional[str]:
        return self._path
    
    @property
    def append(self) -> bool:
        return self._append

    def write(self, output: str):
        if self._file:
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
