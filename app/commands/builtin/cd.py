from typing import List
from pathlib import Path
import os
from app.commands.command import Command

class CD(Command):
    def execute(self, args: List[str]) -> int:
        path = None

        if args:
            path = Path.home() if args[0] == "~" else args[0]

        if path:
            try:
                os.chdir(path)
                return 0
            except FileNotFoundError:
                self._stderr.write(f"cd: {path}: No such file or directory\n")
                return -1
            except NotADirectoryError:
                self._stderr.write(f"cd: {path}: No such file or directory\n")
                return -1
            except PermissionError:
                self._stderr.write(f"cd: {path}: Permission denied\n")
                return -1
        else:
            self._stderr.write(f"cd: {path}: No such file or directory\n")
            return -1