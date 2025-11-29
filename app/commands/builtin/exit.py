from typing import List
from app.commands.command import Command
from app.exceptions.command_exceptions import ExitException

class Exit(Command):
    def execute(self, args: List[str]) -> int:
        raise ExitException(exit_code=int(args[0]) if args else 0)