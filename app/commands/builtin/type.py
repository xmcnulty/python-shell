from typing import List
from app.commands.command import Command
from app.core.model.execution_result import ExecutionResult
from app.commands.external_cmd import ExternalCmd
from app.commands.command_factory import CommandFactory
import shutil

class Type(Command):
    def execute(self, args: List[str]) -> ExecutionResult:
        if not args:
            return ExecutionResult()
            
        command_name = args[0]
        factory = CommandFactory.get_instance()
        
        if factory and command_name in factory.registered_commands:
            return ExecutionResult(stdout=f"{command_name} is a shell builtin")
        
        # Check if it's an external command
        path = shutil.which(command_name)
        if path:
            return ExecutionResult(stdout=f"{command_name} is {path}")
        
        return ExecutionResult(code=-1, stderr=f"{command_name}: not found")