import sys, subprocess
from app.commands import command_registry
from app.utils.path_utils import find_executable
from app.utils.arg_utils import process_args

command_registry["exit"] = None

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        
        cmdline = input().strip()
        if not cmdline:
            continue

        parts = process_args(cmdline)
        cmd = parts[0] if parts else ""
        args = parts[1:] if len(parts) > 1 else None

        if cmd == "exit":
            return int(args[0]) if args and args[0].isnumeric() else 0

        handler = command_registry.get(cmd)

        if handler:
            handler(args)
        else:
            # check if command is an executable in PATH
            exec_path = find_executable(cmd)

            # if it is, execute it and print output
            if exec_path:
                result = subprocess.run(
                    [cmd] + args if args else [cmd],
                    capture_output=True,
                    text=True
                )

                if result.stdout:
                    print(result.stdout, end="")
                if result.stderr:
                    print(result.stderr, end="")
            else:
                print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()
