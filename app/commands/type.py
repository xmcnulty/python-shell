from typing import Optional
from . import command_registry, register_command

@register_command("type")
def type(args: Optional[str]):
    if args:
        if args in command_registry:
            print(f"{args} is a shell builtin")
        else:
            print(f"{args}: not found")