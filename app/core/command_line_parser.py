from typing import List, Optional, Tuple
from app.core.model.parsed_command import ParsedCommand
from app.core.model.output_config import *
import shlex



class CommandLineParser:

    def parse_input(self, input) -> List[ParsedCommand]:
        parsed_commands = []
        split_commands = self._split_by_pipe(shlex.split(input))

        for cmd in split_commands:
            # TODO: Exception and error handling
            command = cmd[0] if cmd else ""

            if len(cmd) > 1:
                stdout, stderr, args = self._parse_redirects(cmd[1:])
            else:
                stdout, stderr, args = None, None, []

            parsed_cmd = ParsedCommand(command=command, args=args, stdout=stdout, stderr=stderr)

            parsed_commands.append(parsed_cmd)

        return parsed_commands
    
    def _split_by_pipe(self, words: List[str]) -> List[List[str]]:
        token = "|"
        result = []
        current = []

        for word in words:
            if word == token:
                if current:
                    result.append(current)
                    current = []
            else:
                current.append(word)
            
        if current:
            result.append(current)

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
            elif args[i] in {">>", "1>>"}:
                if i + 1 >= len(args):
                    raise Exception(f"stdout redirect missing target file")
                
                stdout = OutputConfig(file_path=args[i + 1], type=OutputType.APPEND)
                i += 2
            elif args[i] == "2>>":
                if i + 1 >= len(args):
                    raise Exception("stdout redirect missing target file")
                
                stderr = OutputConfig(file_path=args[i + 1], type=OutputType.APPEND)
                i += 2
            else:
                cleaned_args.append(args[i])
                i += 1

        return stdout, stderr, cleaned_args
