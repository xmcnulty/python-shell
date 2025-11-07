from typing import List
from app.commands.command import Command
from app.core.model.execution_result import ExecutionResult
from app.commands.external_cmd import ExternalCmd

class Type(Command):
    def execute(self, args: List[str]) -> ExecutionResult:
        if args:
            if args[0] in {"echo", "cd", "pwd", "type", "exit"}:
                return ExecutionResult(stdout=f"{args[0]} is a shell builtin")
            else:
                path = ExternalCmd.find_executable(args[0])

                if path:
                    return ExecutionResult(stdout=f"{args[0]} is {path}")
                else:
                    return ExecutionResult(code=-1, stderr=f"{args[0]}: not found")
                
        return ExecutionResult()
                
            