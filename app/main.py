import sys
from .commands import command_registry

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
            print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()
