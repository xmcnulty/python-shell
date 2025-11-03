from typing import Optional
from . import command_registry, register_command
from app.utils.path_utils import find_executable

@register_command("type")
def type(args: Optional[str]):
    if args:
        if args in command_registry:
            print(f"{args} is a shell builtin")
        else:
            path = find_executable(args)

            if path:
                print(f"{args} is {path}")
            else:
                print(f"{args}: not found")
                
            