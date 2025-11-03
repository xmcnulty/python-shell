from typing import Optional, List
from . import register_command

@register_command("echo")
def echo(args: Optional[List[str]]):
    if args:
        print(' '.join(args))