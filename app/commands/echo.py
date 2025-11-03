from typing import Optional
from . import register_command

@register_command("echo")
def echo(args: Optional[str]):
    if args:
        print(args.lstrip())