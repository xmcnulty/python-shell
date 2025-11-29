from app.commands.command import Command
from app.core.history_manager import app_history
from typing import List

class History(Command):
    def execute(self, args: List[str]) -> int:
        try:
            # Implement history command logic here
            # For now, just write a placeholder message
            if args:
                n = int(args[0])
                hist = app_history.get_last(n)
            else:
                hist = app_history.get_last()

            output = ""
            for idx, cmd in hist:
                output += f"    {idx}  {cmd}\n"
            self._stdout.write(output)
            return 0
        except Exception as e:
            self._stderr.write(f"An unexpected error occured:\n{e}\n")
            return -1