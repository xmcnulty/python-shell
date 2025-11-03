from typing import Optional
import os

def find_executable(cmd: str) -> Optional[str]:
    for path_dir in os.getenv("PATH", "").split(os.pathsep):
        candidate = os.path.join(path_dir, cmd)

        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    
    return None