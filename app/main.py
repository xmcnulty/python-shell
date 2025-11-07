import sys
from app.core.command_line_parser import CommandLineParser
from app.commands.command_factory import CommandFactory
from app.commands.echo import Echo
from app.commands.cd import CD
from app.commands.type import Type
from app.commands.pwd import PWD
from app.core.execution_handler import ExecutionHandler

def main():
    factory = CommandFactory()
    factory.register("echo", Echo)
    factory.register("cd", CD)
    factory.register("type", Type)
    factory.register("pwd", PWD)

    executor = ExecutionHandler(factory=factory)
    parser = CommandLineParser()

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        
        cmdline = input().strip()
        if not cmdline:
            continue

        parsed_input = parser.parse_input(cmdline)

        if not parsed_input.command:
            return
        
        if parsed_input.command == "exit":
            return int(parsed_input.args[0]) if parsed_input.args else 0
        
        executor.execute_parsed_command(parsed_input)


if __name__ == "__main__":
    main()
