from typing import List, Set
import os
import stat
import time
from pathlib import Path
from app.utils.path_utils import get_path_executables

class CompletionHandler:
    def __init__(self, builtins: List[str]) -> None:
        self._builtins = builtins
        self._executable_cache: Set[str] = set()
        self._last_path_check: float = 0
        self._cache_timeout: float = 5.0  # Cache executables for 5 seconds
        self._update_executable_cache()

    def complete_command(self, prefix: str) -> List[str]:
        # First check builtins
        matches = [cmd for cmd in self._builtins if cmd.startswith(prefix)]
        
        # If no builtin matches or prefix is empty, check PATH executables
        if not matches or not prefix:
            self._update_executable_cache()
            matches.extend([cmd for cmd in self._executable_cache if cmd.startswith(prefix)])
        
        return sorted(matches)

    def _update_executable_cache(self) -> None:
        """
        Update the cache of executable files from PATH if the cache has expired.
        """
        current_time = time.time()
        if current_time - self._last_path_check < self._cache_timeout:
            return

        self._executable_cache.clear()

        self._executable_cache = get_path_executables()

        self._last_path_check = current_time