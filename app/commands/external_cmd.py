from typing import List
from app.commands.command import Command
from app.core.model.execution_result import ExecutionResult
from app.utils.path_utils import find_executable_path
import subprocess

class ExternalCmd(Command):
    def __init__(self, cmd: str) -> None:
         self.cmd = cmd
         super().__init__()

    def execute(self, args: List[str]) -> ExecutionResult:
            # check if command is an executable in PATH
            exec_path = find_executable_path(self.cmd)

            # if it is, execute it and print output
            if exec_path:
                result = subprocess.run(
                    [self.cmd] + args if args else [self.cmd],
                    capture_output=True,
                    text=True
                )
        
                stdout_text = result.stdout.rstrip("\n") if result.stdout else ""
                stderr_text = result.stderr.rstrip("\n") if result.stderr else ""

                return ExecutionResult(
                     code=result.returncode,
                     stdout=stdout_text,
                     stderr=stderr_text
                )
            else:
                 return ExecutionResult(code=-1, stderr=f"{self.cmd}: command not found")