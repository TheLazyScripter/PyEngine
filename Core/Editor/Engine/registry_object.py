from __future__ import annotations
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .registry import Registry


class RegistryObject:
    def __init__(self, priority: int, target: type, *args, **kwargs):
        self.__priority = priority
        self.__target = target


