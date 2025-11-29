from typing import List
import os
from app.commands.command import Command

class PWD(Command):
    def execute(self, args: List[str]) -> int:
        try:
            # pwd should print trailing newline
            self._stdout.write(os.getcwd() + "\n")
            return 0
        except Exception as e:
            self._stderr.write(f"An unexpected error occured:\n{e}\n")
            return -1