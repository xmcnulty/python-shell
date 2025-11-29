from app.core.command_line_parser import ParsedCommand
from app.commands.command_factory import CommandFactory
from app.core.output_handler import OutputHandler, OutputType
from typing import List
import os, sys

class ExecutionHandler:

    def __init__(self, factory: CommandFactory) -> None:
        self._factory = factory

    def execute_parsed_command(self, commands: List[ParsedCommand]):
        """
        Execute a pipeline of ParsedCommand objects using POSIX pipes and forks.
        Supports redirects: if a ParsedCommand has stdout/stderr OutputConfig, it will
        open the file and dup2 that fd to stdout/stderr for that command.
        Builtin commands (registered in factory) are executed in the child process by
        instantiating via the factory and calling execute(...).
        External commands are executed with os.execvp(argv[0], argv).

        Returns when all child processes have exited (parent waits for them).
        """
        if not commands:
            return 0

        # Special-case: single builtin command should run in the parent process so
        # that side-effects (like `cd`) persist in the shell. If there's exactly
        # one command and it is a registered builtin, execute it here and return.
        if len(commands) == 1:
            single = commands[0]
            factory = self._factory
            if single.command in factory.registered_commands:
                # Create OutputHandler instances (they will open files if redirects are set)
                stdout_handler = OutputHandler(config=single.stdout)
                stderr_handler = OutputHandler(config=single.stderr)

                builtin_obj = factory.create(name=single.command, stdout=stdout_handler, stderr=stderr_handler)
                try:
                    exit_code = builtin_obj.execute(args=single.args)
                except SystemExit as se:
                    # Map SystemExit to exit code
                    exit_code = se.code if isinstance(se.code, int) else 1
                finally:
                    try:
                        stdout_handler.close()
                    except Exception:
                        pass
                    try:
                        stderr_handler.close()
                    except Exception:
                        pass

                return exit_code if isinstance(exit_code, int) else 0

        num_cmds = len(commands)
        pipes = []  # list of (read_fd, write_fd)
        for _ in range(max(0, num_cmds - 1)):
            pipes.append(os.pipe())  # (r, w)

        pids = []

        for i, cmd in enumerate(commands):
            # Determine stdin_fd and stdout_fd for this command
            # default: inherit from parent (i.e., current stdin/stdout)
            stdin_fd = None
            stdout_fd = None
            stderr_fd = None

            # if not the first command, stdin comes from previous pipe read end
            if i > 0:
                prev_r, prev_w = pipes[i - 1]
                stdin_fd = prev_r

            # if not the last command, stdout goes to current pipe write end
            if i < num_cmds - 1:
                cur_r, cur_w = pipes[i]
                stdout_fd = cur_w

            # handle stdout redirect to file (overrides pipe for this command)
            if cmd.stdout:
                mode = 'w' if cmd.stdout.type == OutputType.WRITE else 'a'
                # open file and get fd
                f = open(cmd.stdout.file_path, mode)
                stdout_fd = f.fileno()

            # handle stderr redirect to file
            if cmd.stderr:
                mode = 'w' if cmd.stderr.type == OutputType.WRITE else 'a'
                f_err = open(cmd.stderr.file_path, mode)
                stderr_fd = f_err.fileno()

            pid = os.fork()
            if pid == 0:
                # Child process
                # If stdin_fd set -> dup to 0
                if stdin_fd is not None:
                    os.dup2(stdin_fd, 0)

                # If stdout_fd set -> dup to 1
                if stdout_fd is not None:
                    os.dup2(stdout_fd, 1)

                # If stderr_fd set -> dup to 2
                if stderr_fd is not None:
                    os.dup2(stderr_fd, 2)

                # Close all pipe fds in child (they are duplicated where needed)
                for (r, w) in pipes:
                    try:
                        os.close(r)
                    except OSError:
                        pass
                    try:
                        os.close(w)
                    except OSError:
                        pass

                # Now run builtin or external
                factory = self._factory
                if cmd.command in factory.registered_commands:
                    # Builtin: create using factory. Pass OutputHandler(None) so the builtin
                    # writes to stdout/stderr (already duped)
                    stdout_handler = OutputHandler(config=None)
                    stderr_handler = OutputHandler(config=None)
                    builtin_obj = factory.create(name=cmd.command, stdout=stdout_handler, stderr=stderr_handler)
                    # Call execute; builtins may call print() or self._stdout.write()
                    try:
                        exit_code = builtin_obj.execute(args=cmd.args)
                    except SystemExit as se:
                        # exit exception mapping if any
                        os._exit(se.code if isinstance(se.code, int) else 1)
                    except BaseException:
                        os._exit(1)
                    os._exit(exit_code if isinstance(exit_code, int) else 0)
                else:
                    # External: execvp
                    argv = [cmd.command] + (cmd.args or [])
                    try:
                        os.execvp(cmd.command, argv)
                    except FileNotFoundError:
                        # write error to stderr then exit
                        sys.stderr.write(f"{cmd.command}: command not found\n")
                        os._exit(127)
                    except Exception as e:
                        sys.stderr.write(str(e) + "\n")
                        os._exit(1)
            else:
                # Parent process
                pids.append(pid)
                # parent must close fds it doesn't need:
                # close the write-end of the previous pipe (we only keep it in children)
                if i > 0:
                    prev_r, prev_w = pipes[i - 1]
                    try:
                        os.close(prev_r)
                    except OSError:
                        pass
                    try:
                        os.close(prev_w)
                    except OSError:
                        pass
                # For the last command, parent still needs to close all pipe fds eventually

        # Close any remaining pipe fds in parent
        for (r, w) in pipes:
            for fd in (r, w):
                try:
                    os.close(fd)
                except OSError:
                    pass

        # Wait for children to finish
        status_codes = []
        for pid in pids:
            try:
                _, status = os.waitpid(pid, 0)
                # get exit code
                if os.WIFEXITED(status):
                    status_codes.append(os.WEXITSTATUS(status))
                elif os.WIFSIGNALED(status):
                    # Translate signal to non-zero exit code (128 + signum typical)
                    status_codes.append(128 + os.WTERMSIG(status))
                else:
                    status_codes.append(1)
            except ChildProcessError:
                # already waited
                pass

        # return the last command status (or 0)
        return status_codes[-1] if status_codes else 0