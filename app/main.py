import sys
import readline
from app.core.command_line_parser import CommandLineParser
from app.commands.command_factory import CommandFactory
from app.core.execution_handler import ExecutionHandler
from app.core.completion_handler import CompletionHandler
from app.exceptions.command_exceptions import ExitException

def main():
    factory = CommandFactory().create_with_builtins()
    executor = ExecutionHandler(factory=factory)
    parser = CommandLineParser()

    completion_handler = CompletionHandler(builtins=list(factory.commands))

    def completer(text, state):
        options = completion_handler.complete_command(text)

        if len(options) == 1:
            options[0] += " "

        return options[state] if state < len(options) else None
    
    readline.set_completer(completer)

    if "libedit" in (readline.__doc__ or ""):
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

    while True:
        cmdline = input("$ ").strip()

        if not cmdline:
            continue

        parsed_input = parser.parse_input(cmdline)

        if not parsed_input.command:
            return
        
        if parsed_input.command == "exit":
            return int(parsed_input.args[0]) if parsed_input.args else 0

        try:
            executor.execute_parsed_command(parsed_input)
        except ExitException as e:
            return e.exit_code


if __name__ == "__main__":
    main()
