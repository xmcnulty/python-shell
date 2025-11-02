import sys
from typing import Optional

def echo(args: Optional[str]):
    if args:
        print(args.lstrip())

def type_cmd(args: Optional[str]):
    if args:
        if args in commands.keys():
            print(f"{args} is a shell builtin")
        else:
            print(f"{args}: not found")

commands = {
    "exit" : None, 
    "echo" : echo, 
    "type" : type_cmd
}

def main():
    while True:
        sys.stdout.write("$ ")
        
        command = input()
        
        if not command:
            print("please enter a command")
            continue

        elements = command.split(maxsplit=1)
        cmd = elements[0]
        args = elements[1] if len(elements) == 2 else None

        if cmd == "exit":
            return int(args) if args and args.isnumeric() else 0

        if cmd in commands.keys():
            commands[cmd](args)
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
