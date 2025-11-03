from typing import Optional, List
from . import register_command
from pathlib import Path
import os

@register_command("cd")
def cd(args: Optional[List[str]]):
    path = None

    if args:
        path = Path.home() if args[0] == "~" else args[0]

    if path:
        try:
            os.chdir(path)
        except FileNotFoundError:
            print(f"cd: {path}: No such file or directory")
        except NotADirectoryError:
            print("Not a directory")
        except PermissionError:
            print("Permission denied")
    else:
        print(f"cd: {path}: No such file or directory")