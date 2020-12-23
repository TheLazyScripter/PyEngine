from PyMath import queue
from typing import Union, Tuple, Mapping, Optional
import pygame


class _System(queue.Queue):
    """Needs some reference to an event system to listen into and
    Callback needs a condition to check against."""

    class _Callback:
        def __init__(self, target: type, *args: Optional[Tuple[any]], **kwargs: Optional[Mapping[any]]):
            self._target = target
            self._args = args
            self._kwargs = kwargs

        def __call__(self) -> Optional[queue.T]:
            return self._target(*self._args, **self._kwargs)

    def __init__(self):
        super().__init__()

    def create_callback(self, target: type, *args: Optional[Tuple[any]], **kwargs: Optional[Mapping[any]]):
        return self._Callback(target, *args, **kwargs)

    def register_callback(self, callback: _Callback, event: pygame.USEREVENT):
        pass

    def __setitem__(self, key: Union[str, int], value: queue.T) -> None:
        self._collection.append(value)

    def __getitem__(self, item: queue.T) -> queue.T:
        return self._collection[item]
