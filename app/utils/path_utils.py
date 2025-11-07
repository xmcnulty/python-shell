from typing import Optional
import os

def find_executable_path(cmd: str) -> Optional[str]:
    for path_dir in os.getenv("PATH", "").split(os.pathsep):
        candidate = os.path.join(path_dir, cmd)

        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate

    return None

def get_path_executables() -> set[str]:
    executables = set()
    for path_dir in os.getenv("PATH", "").split(os.pathsep):
        if not path_dir:
            continue

        try:
            for entry in os.scandir(path_dir):
                if entry.is_file() and os.access(entry.path, os.X_OK):
                    executables.add(entry.name)
        except (FileNotFoundError, PermissionError):
            continue

    return executables