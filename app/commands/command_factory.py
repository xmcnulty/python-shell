from app.commands.command import Command
from app.commands.external_cmd import ExternalCmd

class CommandFactory:
    def __init__(self) -> None:
        self._registry = {}

    def register(self, name: str, command_cls: Command.__class__):
        self._registry[name] = command_cls

    def create(self, name: str) -> Command:
        command_cls = self._registry.get(name)

        if command_cls:
            return command_cls()
        else:
            return ExternalCmd(cmd=name)