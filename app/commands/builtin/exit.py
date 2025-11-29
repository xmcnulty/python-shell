from typing import List
from app.commands.command import Command
from app.core.history_manager import app_history
from app.exceptions.command_exceptions import ExitException

class Exit(Command):
    def execute(self, args: List[str]) -> int:

        app_history.write_on_exit()
        raise ExitException(exit_code=int(args[0]) if args else 0)