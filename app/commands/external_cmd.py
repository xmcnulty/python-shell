from typing import List
from app.commands.command import Command
from app.core.model.execution_result import ExecutionResult
from typing import Optional
import os
import subprocess

class ExternalCmd(Command):
    def __init__(self, cmd: str) -> None:
         self.cmd = cmd
         super().__init__()

    @staticmethod
    def find_executable(cmd: str) -> Optional[str]:
        for path_dir in os.getenv("PATH", "").split(os.pathsep):
            candidate = os.path.join(path_dir, cmd)

            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return candidate
        
        return None

    def execute(self, args: List[str]) -> ExecutionResult:
            # check if command is an executable in PATH
            exec_path = self.find_executable(self.cmd)

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