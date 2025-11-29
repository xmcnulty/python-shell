from typing import List, Tuple
from collections import namedtuple
import threading

DEFAULT_MAX_SIZE = 100

HistoryLineItem = namedtuple("HistoryLineItem", ["index", "command"])

class HistoryManager:

    def __init__(self, max_size: int = DEFAULT_MAX_SIZE):
        self.max_size = max_size
        self.history: List[HistoryLineItem] = []
        self.lock = threading.Lock()

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
        
app_history = HistoryManager()