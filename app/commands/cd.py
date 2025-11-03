from typing import Optional
from . import register_command
import os

@register_command("cd")
def cd(args: Optional[str]):
    if args:
        try:
            os.chdir(args)
        except FileNotFoundError:
            print(f"cd: {args}: No such file or directory")
        except NotADirectoryError:
            print("Not a directory")
        except PermissionError:
            print("Permission denied")
    else:
        print(f"cd: {args}: No such file or directory")