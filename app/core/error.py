class CommandLineError(Exception):
    pass

class InvalidRedirectError(CommandLineError):
    # TODO: Some custom implementation
    pass

class InvalidCommandError(CommandLineError):
    def __init__(self, cmd_entered: str) -> None:
        super().__init__(f"{cmd_entered}: command not found")