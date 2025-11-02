import sys


def main():
    while True:
        sys.stdout.write("$ ")
        
        command = input()

        if not command:
            print("please enter a command")
            continue

        if command.split()[0] == "exit":
            args = command.split()

            return int(args[1]) if len(args) > 1 else 0

        if command.split()[0] == "echo":
            print(command[4:].lstrip())
            continue

        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
