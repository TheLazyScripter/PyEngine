from __future__ import annotations
from typing import TYPE_CHECKING
from PyMath import queue

if TYPE_CHECKING:
    from .registry_object import RegistryObject


class Registry(queue.Queue):

    def __init__(self):
        super().__init__(unique=True)

    def __setitem__(self, key: str, value: queue.T) -> None:
        pass

    def __getitem__(self, item: queue.T):
        pass
