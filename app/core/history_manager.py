from typing import List, Tuple
from collections import namedtuple
import threading

DEFAULT_MAX_SIZE = 100

HistoryLineItem = namedtuple("HistoryLineItem", ["index", "command"])

class HistoryManager:

    def __init__(self, max_size: int = DEFAULT_MAX_SIZE):
        self.max_size = max_size
        self.history: List[HistoryLineItem] = []
        self.lock = threading.RLock()
        self._last_appended_index = 0

    def add(self, command: str) -> None:
        with self.lock:
            if len(self.history) >= self.max_size:
                self.history.pop(0)
            self.history.append(HistoryLineItem(len(self.history) + 1, command))

    def get_last(self, n: int = -1) -> List[HistoryLineItem]:
        with self.lock:
            if n not in range(0, len(self.history) + 1):
                return list(self.history)
            else:
                return list(self.history[-n:])
            
    def read_from_file(self, filepath: str) -> None:
        with self.lock:
            try:
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        self.add(line.strip())
            except FileNotFoundError:
                pass  # If the file doesn't exist, we start with an empty history

    def write_to_file(self, filepath: str) -> None:
        with self.lock:
            try:
                with open(filepath, 'w') as f:
                    for item in self.history:
                        f.write(f"{item.command}\n")
            except Exception:
                pass  # Ignore any exceptions during writing

    def append_to_file(self, filepath: str) -> None:
        with self.lock:
            try:
                with open(filepath, 'a') as f:
                    for item in self.history[self._last_appended_index:]:
                        f.write(f"{item.command}\n")
                    self._last_appended_index = len(self.history)
            except Exception:
                pass  # Ignore any exceptions during appending
        
app_history = HistoryManager()