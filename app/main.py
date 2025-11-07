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
            return int(parsed_input.context.args[0]) if parsed_input.context.args else 0
        
        executor.execute_parsed_command(parsed_input)
        
        """
        handler = command_registry.get(parsed_input.command)

        if handler:
            handler(parsed_input.args, parsed_input.output)
        else:
            # check if command is an executable in PATH
            exec_path = find_executable(parsed_input.command)

            # if it is, execute it and print output
            if exec_path:
                result = subprocess.run(
                    [parsed_input.command] + parsed_input.args if parsed_input.args else [parsed_input.command],
                    capture_output=True,
                    text=True
                )

                if result.stdout:
                    print(result.stdout, end="")
                if result.stderr:
                    print(result.stderr, end="")
            else:
                print(f"{parsed_input.command}: command not found")
                """


if __name__ == "__main__":
    main()
