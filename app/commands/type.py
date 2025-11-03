from typing import Optional
from . import command_registry, register_command
import os

@register_command("type")
def type(args: Optional[str]):
    if args:
        if args in command_registry:
            print(f"{args} is a shell builtin")
        else:
            for path_dir in os.getenv("PATH", "").split(os.pathsep):
                candidate = os.path.join(path_dir, args)

                if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                    print(f"{args} is {candidate}")
                    return
                
            print(f"{args}: not found")