from __future__ import annotations
from typing import TYPE_CHECKING, Union
from PyMath import queue
from time import time

if TYPE_CHECKING:
    from .registry_object import RegistryObject


class Registry(queue.Queue):

    def __init__(self, num_layers=5):
        super().__init__(unique=True)
        for i in range(num_layers):
            self.push(queue.Queue())

    def add_object(self, obj: RegistryObject):
        try:
            self[obj.priority-1] = obj
        except IndexError:
            print(obj.priority, self)

    def process(self):
        for layer in self:
            print(layer)
            if len(layer) > 0:
                for obj in layer:
                    obj.process()

    @staticmethod
    def do_after(obj, fn, delay):
        start = time()
        while time() - start < delay:
            yield
        print("Here")
        fn()

    def do_once(self, obj, fn):
        fn()

    def do_forever(self, obj, fn):
        self.add_object(obj)
        fn()

    def __iter__(self):
        self.__pos = 0
        return self

    def __next__(self):
        self.__pos += 1
        if self.__pos < len(self._collection):
            return self._collection[self.__pos-1]
        raise StopIteration

    def __setitem__(self, key: Union[str, int], value: queue.T) -> None:
        self._collection[key].push(value)

    def __getitem__(self, item: queue.T):
        return self._collection[item]
