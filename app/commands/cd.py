from typing import Optional
from . import register_command
from pathlib import Path
import os

@register_command("cd")
def cd(args: Optional[str]):
    path = Path.home() if args and args == "~" else args

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