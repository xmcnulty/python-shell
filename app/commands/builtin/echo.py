from typing import List
from app.commands.command import Command

class Echo(Command):
    def execute(self, args: List[str]) -> int:
        try:
            # echo should print a trailing newline like POSIX echo
            out = ' '.join(args) + "\n"
            self._stdout.write(out)
            return 0
        except Exception as e:
            self._stderr.write(f"an unexpected error occured:\n{e}\n")
            return -1