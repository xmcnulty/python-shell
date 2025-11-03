command_registry = {}

def register_command(name):
    def decorator(func):
        command_registry[name] = func
        return func
    return decorator

from . import echo, type, pwd, cd