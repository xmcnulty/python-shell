from app.core.command_line_parser import ParsedCommand
from app.commands.command_factory import CommandFactory
from app.core.output_handler import OutputHandler

class ExecutionHandler:

    def __init__(self, factory: CommandFactory) -> None:
        self._factory = factory

    def execute_parsed_command(self, cmd: ParsedCommand):
        """
        TODO: Based on Parsed command, create an output handler to handle stdout.
        then check if command is a builtin, otherwise execute using subprocess.
        """
        command_obj = self._factory.create(name=cmd.command)

        std_out = OutputHandler(config=cmd.stdout)
        std_err = OutputHandler(config=cmd.stderr)

        result = command_obj.execute(args=cmd.args)

        if result.stdout:
            std_out.write(result.stdout)

        if result.stderr:
            std_err.write(result.stderr)