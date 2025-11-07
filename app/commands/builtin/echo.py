from typing import List
from app.commands.command import Command
from app.core.model.execution_result import ExecutionResult

class Echo(Command):
    def execute(self, args: List[str]) -> ExecutionResult:
        try:
            return ExecutionResult(stdout=' '.join(args))
        except Exception as e:
            return ExecutionResult(code=-5, stderr=f"an unexpeced error occured:\n{e}")