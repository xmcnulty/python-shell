from typing import List
import os
from app.commands.command import Command
from app.core.output_handler import OutputHandler

class PWD(Command):
    def execute(self, args: List[str], stdout: OutputHandler):
        stdout.write(os.getcwd())