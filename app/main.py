import sys
import os
import subprocess
import shlex

def find_command_path(command):
    paths = os.environ.get("PATH")
    directories = paths.split(':')
    for directory in directories:
        file_path = os.path.join(directory, command)
        if os.path.isfile(file_path):
            return file_path
    return None

class Command:
    def execute(self, args):
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
        
    def execute(self, args):
        if not args:
            print("no input given")
            return
        command = args[0]
        if command in self.builtins:
            print(f"{command} is a shell builtin")
        else:
            command_path = find_command_path(command)
            if command_path:
                print(f"{command} is {command_path}")
            else:
                print(f"{command}: not found")

class PwdCommand(Command):
    def execute(self, args):
        print(os.getcwd())

class CdCommand(Command):
    def execute(self, args):
        if not args:
            print("no input given")
            return
        directory = args[0]
        if directory == '~':
            os.chdir(os.environ['HOME'])
        elif not os.path.isdir(directory):
            print(f"cd: {directory}: No such file or directory")
        else:
            os.chdir(directory)
            
class Shell:
    def __init__(self):
        self.commands = {}
        self.commands['type'] = TypeCommand(self.commands)
        self.commands['echo'] = EchoCommand()
        self.commands['exit'] = ExitCommand()
        self.commands['pwd'] = PwdCommand()
        self.commands['cd'] = CdCommand()

    def execute_command(self, command, args):
        if command in self.commands:
            target = self.commands[command]
            target.execute(args)
        else:
            command_path = find_command_path(command)
            if command_path:
                subprocess.run([command] + args)
            else:
                print(f"{command}: command not found")

def main():
    shell = Shell()
    while True:
        try:
            parts = input("$ ")
            if not parts:
                continue
            command, *args = shlex.split(parts)
            shell.execute_command(command, args)
        except Exception as e:
            print(f"Error {e}")

if __name__ == "__main__":
    main()
