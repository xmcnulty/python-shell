from typing import List, Optional, Tuple
from app.core.model.parsed_command import ParsedCommand
from app.core.model.output_config import *
import shlex



class CommandLineParser:

    def parse_input(self, input) -> ParsedCommand:
        split_commands = shlex.split(input)

        cmd = split_commands[0] if split_commands else ""

        if len(split_commands) > 1:
            stdout, stderr, args = self._parse_redirects(split_commands[1:])
        else:
            stdout, stderr, args = None, None, []

        result = ParsedCommand(
            command=cmd,
            args=args,
            stdout=stdout,
            stderr=stderr
        )

        return result
    
    def _parse_redirects(self, args: List[str]) -> Tuple[Optional[OutputConfig], Optional[OutputConfig], List[str]]:
        """
        Process arguments for stdout redirects ('>' or '1>').
        Returns a tuple: (output_file, cleaned_args)
        Redirects are removed from the returned args list.
        """
        cleaned_args = []
        stdout = None
        stderr = None
        i = 0

        while i < len(args):
            if args[i] in {">", "1>"}:
                if i + 1 >= len(args):
                    raise Exception(f"stdout redirect missing target file")
                
                stdout = OutputConfig(file_path=args[i + 1], type=OutputType.WRITE)
                i += 2
            elif args[i] == "2>":
                if i + 1 >= len(args):
                    raise Exception("stdout redirect missing target file")
                
                stderr = OutputConfig(file_path=args[i + 1], type=OutputType.WRITE)
                i += 2
            else:
                cleaned_args.append(args[i])
                i += 1

        return stdout, stderr, cleaned_args
