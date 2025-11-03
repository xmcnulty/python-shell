import sys, subprocess
from .commands import command_registry
from .utils.path_utils import find_executable

command_registry["exit"] = None

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        
        cmdline = input().strip()
        if not cmdline:
            continue

        parts = cmdline.split(maxsplit=1)
        cmd = parts[0]
        args = parts[1] if len(parts) == 2 else None

        if cmd == "exit":
            return int(args) if args and args.isnumeric() else 0

        handler = command_registry.get(cmd)

        if handler:
            handler(args)
        else:
            # check if command is an executable in PATH
            exec_path = find_executable(cmd)

            # if it is, execute it and print output
            if exec_path:
                result = subprocess.run(
                    [exec_path] + args.split() if args else [exec_path],
                    capture_output=True,
                    text=True
                )

                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            else:
                print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()
