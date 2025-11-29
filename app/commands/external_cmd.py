from typing import List
from app.commands.command import Command
from app.utils.path_utils import find_executable_path
from app.core.output_handler import OutputHandler
import subprocess

class ExternalCmd(Command):
    def __init__(self, cmd: str, stdout: OutputHandler, stderr: OutputHandler) -> None:
         self.cmd = cmd
         super().__init__(stdout, stderr)

    def execute(self, args: List[str]) -> int:
            # check if command is an executable in PATH
            exec_path = find_executable_path(self.cmd)

            # if it is, execute it and print output
            if exec_path:
                result = subprocess.run(
                    [self.cmd] + args if args else [self.cmd],
                    capture_output=True,
                    text=True
                )
                # Preserve stdout/stderr exactly as produced by the subprocess
                stdout_text = result.stdout if result.stdout else ""
                stderr_text = result.stderr if result.stderr else ""

                self._stdout.write(stdout_text)
                self._stderr.write(stderr_text)

                return result.returncode if result.returncode != 0 else 0
            else:
                 self._stderr.write(f"{self.cmd}: command not found\n")
                 return -1