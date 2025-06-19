import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        command_split = command.split()
        if command_split[0] == 'exit':
            break
        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
