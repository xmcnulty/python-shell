import sys


def main():
    while True:
        sys.stdout.write("$ ")
        
        command = input().split()

        if not command:
            print("please enter a command")
            continue

        if command[0] == "exit":
            return int(command[1]) if len(command) > 1 else 0

        print(f"{command[0]}: command not found")


if __name__ == "__main__":
    main()
