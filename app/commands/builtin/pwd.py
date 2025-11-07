from typing import List
import os
from app.commands.command import Command
from app.core.model.execution_result import ExecutionResult

class PWD(Command):
    def execute(self, args: List[str]) -> ExecutionResult:
        try:
            return ExecutionResult(stdout=os.getcwd())
        except Exception as e:
            return ExecutionResult(code=-5, stderr=f"An unexpected error occured:\n{e}")