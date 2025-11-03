from . import register_command
import os

@register_command("pwd")
def pwd(args):
    print(os.getcwd())