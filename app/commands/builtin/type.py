from typing import List
from app.commands.command import Command
from app.commands.external_cmd import ExternalCmd
from app.commands.command_factory import CommandFactory
import shutil

class Type(Command):
    def execute(self, args: List[str]) -> int:
        if not args:
            return 0
            
        command_name = args[0]
        factory = CommandFactory.get_instance()
        
        if factory and command_name in factory.registered_commands:
            self._stdout.write(f"{command_name} is a shell builtin\n")
            return 0
        
        # Check if it's an external command
        path = shutil.which(command_name)
        if path:
            self._stdout.write(f"{command_name} is {path}\n")
            return 0
        
        self._stderr.write(f"{command_name}: not found\n")
        return -1