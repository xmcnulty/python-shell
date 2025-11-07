from typing import List, Optional, Tuple
from dataclasses import dataclass
from app.core.command_context import CommandContext
from app.core.error import InvalidRedirectError
import shlex

@dataclass(frozen=True)
class ParsedCommand:
    command: str
    context: CommandContext

class CommandLineParser:

    def parse_input(self, input) -> ParsedCommand:
        split_commands = shlex.split(input)

        cmd = split_commands[0] if split_commands else ""

        if len(split_commands) > 1:
            output, args = self._parse_redirects(split_commands[1:])
        else:
            output, args = None, []

        result = ParsedCommand(
            command=cmd,
            context=CommandContext(args=args, stdout=output)
        )

        return result
    
    def _parse_redirects(self, args: List[str]) -> Tuple[Optional[str], List[str]]:
        """
        Process arguments for stdout redirects ('>' or '1>').
        Returns a tuple: (output_file, cleaned_args)
        Redirects are removed from the returned args list.
        """
        cleaned_args = []
        output = None
        i = 0

        while i < len(args):
            if args[i] in {">", "1>"}:
                if i + 1 >= len(args):
                    raise InvalidRedirectError(f"Redirect missing target file")
                
                output = args[i + 1]
                i += 2
            else:
                cleaned_args.append(args[i])
                i += 1

        return output, cleaned_args
