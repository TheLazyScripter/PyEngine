from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .registry import Registry


class RegistryObject:
    def __init__(self, priority: int, target: type, wrapper: type, delay=None, *args, **kwargs):
        self.__priority = priority
        self.process = lambda: wrapper(self, lambda: target(*args, **kwargs), delay=delay)

    @property
    def priority(self):
        return self.__priority
