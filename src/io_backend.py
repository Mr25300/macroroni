from typing import Callable
from abc import ABC, abstractmethod
from enum import Enum, auto

IOCallback = Callable[[str, bool], None]

class IOBackend(ABC):
    @abstractmethod
    def press(self, out_id: str) -> None:
        pass

    @abstractmethod
    def release(self, out_id: str) -> None:
        pass

    @abstractmethod
    def listen(self, callback: IOCallback) -> None:
        pass
