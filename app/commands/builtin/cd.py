from typing import List
from pathlib import Path
import os
from app.commands.command import Command
from app.core.model.execution_result import ExecutionResult

class CD(Command):
    def execute(self, args: List[str]) -> ExecutionResult:
        path = None

        if args:
            path = Path.home() if args[0] == "~" else args[0]

        if path:
            try:
                os.chdir(path)
                return ExecutionResult()
            except FileNotFoundError:
                return ExecutionResult(code=-1, stderr=f"cd: {path}: No such file or directory")
            except NotADirectoryError:
                return ExecutionResult(code=-1, stderr=f"cd: {path}: No such file or directory")
            except PermissionError:
                return ExecutionResult(code=-1, stderr=f"cd: {path}: Permission denied")
        else:
            return ExecutionResult(code=-1, stderr=f"cd: {path}: No such file or directory")