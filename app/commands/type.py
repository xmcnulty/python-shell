from typing import Optional, List
from . import command_registry, register_command
from app.utils.path_utils import find_executable

@register_command("type")
def type(args: Optional[List[str]]):
    if args:
        if args[0] in command_registry:
            print(f"{args[0]} is a shell builtin")
        else:
            path = find_executable(args[0])

            if path:
                print(f"{args[0]} is {path}")
            else:
                print(f"{args[0]}: not found")
                
            