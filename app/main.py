import sys
import os

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
    def __init__(self, commands):
        self.commands = commands
    
    def search_dirs(self, command):
        paths = os.environ.get("PATH")
        directories = paths.split(':')
        for directory in directories:
            file_path = os.path.join(directory, command)
            if os.path.isfile(file_path):
                print(f"{command} is {file_path}")
                return True
        return False
        
    def execute(self, args):
        if not args:
            print("no command given")
        elif args[0] in self.commands:
            print(f"{args[0]} is a shell builtin")
        else:
            if not self.search_dirs(command=args[0]):
                print(f"{args[0]}: not found")

class Shell:
    def __init__(self):
        self.commands = {}
        self.commands['type'] = TypeCommand(self.commands)
        self.commands['echo'] = EchoCommand()
        self.commands['exit'] = ExitCommand()

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
