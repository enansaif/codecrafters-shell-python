import sys

class Command:
    def execute(self, arge):
        raise NotImplementedError("Execute function has to be implemented")

class EchoCommand(Command):
    def execute(self, args):
        print(" ".join(args))

class ExitCommand(Command):
    def execute(self, args):
        sys.exit()

class TypeCommand(Command):
    def execute(self, args):
        if not args:
            print("no command given")
        elif args[0] in ['echo', 'exit', 'type']:
            print(f"{args[0]} is a shell builtin")
        else:
            print(f"{args[0]}: not found")

class Shell:
    def __init__(self):
        self.commands = {
            'echo' : EchoCommand(),
            'exit' : ExitCommand(),
            'type' : TypeCommand(),
        }

    def execute_command(self, command, args):
        if command in self.commands:
            target = self.commands[command]
            target.execute(args)
        else:
            print(f"{command}: command not found")

def main():
    shell = Shell()
    while True:
        try:
            parts = input("$ ").lower().split()
            if not parts:
                continue
            command, *args = parts
            shell.execute_command(command, args)
        except Exception as e:
            print(f"Error {e}")

if __name__ == "__main__":
    main()
