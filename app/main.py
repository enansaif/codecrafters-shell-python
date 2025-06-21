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
    def __init__(self, builtins):
        self.builtins = builtins
    
    def _find_path(self, command):
        paths = os.environ.get("PATH")
        directories = paths.split(':')
        for directory in directories:
            file_path = os.path.join(directory, command)
            if os.path.isfile(file_path):
                return file_path
        return None
        
    def execute(self, args):
        if not args:
            print("no command given")
            return
        command = args[0]
        if command in self.builtins:
            print(f"{command} is a shell builtin")
        else:
            command_path = self._find_path(command)
            if command_path:
                print(f"{command} is {command_path}")
            else:
                print(f"{command}: not found")

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
