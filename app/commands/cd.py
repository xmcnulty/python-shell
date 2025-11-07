from typing import List
from pathlib import Path
import os
from app.commands.command import Command
from app.core.output_handler import OutputHandler

class CD(Command):
    def execute(self, args: List[str], stdout: OutputHandler):
        path = None

        if args:
            path = Path.home() if args[0] == "~" else args[0]

        if path:
            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {path}: No such file or directory")
            except NotADirectoryError:
                print("Not a directory")
            except PermissionError:
                print("Permission denied")
        else:
            stdout.write(f"cd: {path}: No such file or directory")