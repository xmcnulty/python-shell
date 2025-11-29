from app.commands.command import Command
from app.core.history_manager import app_history, HistoryLineItem
from typing import List, Optional

class History(Command):
    def execute(self, args: List[str]) -> int:
        try:
            output: Optional[str] = None
            if args:
                match args[0]:
                    case "-r":
                        app_history.read_from_file(args[1])
                    case "-w":
                        app_history.write_to_file(args[1])
                    case "-a":
                        app_history.append_to_file(args[1])
                    case str() as s if s.isdigit():
                        output = self._format_output(app_history.get_last(int(s)))
                    case _:
                        output = self._format_output(app_history.get_last())
            else:
                output = self._format_output(app_history.get_last())

            if output:
                self._stdout.write(output)

            return 0
        except Exception as e:
            self._stderr.write(f"An unexpected error occured:\n{e}\n")
            return -1
    
    def _format_output(self, history_items: List[HistoryLineItem]) -> str:
        output = ""
        for item in history_items:
            output += f"    {item.index}  {item.command}\n"
        return output