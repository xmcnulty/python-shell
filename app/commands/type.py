from typing import List
from app.commands.command import Command
from app.core.output_handler import OutputHandler
from app.commands.external_cmd import ExternalCmd

class Type(Command):
    def execute(self, args: List[str], stdout: OutputHandler):
        if args:
            if args[0] in {"echo", "cd", "pwd", "type", "exit"}:
                stdout.write(f"{args[0]} is a shell builtin")
            else:
                path = ExternalCmd.find_executable(args[0])

                if path:
                    stdout.write(f"{args[0]} is {path}")
                else:
                    stdout.write(f"{args[0]}: not found")
                
            