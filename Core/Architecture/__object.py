from __future__ import annotations
from typing import Optional, List, TypeVar, Type, Union

T = TypeVar("T", Type['Component'], Type['GO'])


class Object(object):
    """Root Object for EVERYTHING"""
    __OBJECTS: List[Object] = []

    def __init__(self, name: str):
        self.__name = name
        self.__instance_id: int = len(Object.__OBJECTS)
        Object.__OBJECTS.append(self)

    @property
    def name(self):
        return self.__name

    @property
    def instance_id(self):
        return self.__instance_id

    def __str__(self):
        return f'<{self.__class__.__name__}> {self.__name}'

    def __repr__(self):
        return None

    @staticmethod
    def find_object_of_type(object_type: Type[T]) -> Optional[T]:
        """Return the first instance of an Object of type Type"""

        if object_type is not Object:
            for obj in Object.__OBJECTS:
                if isinstance(obj, object_type):
                    return obj

    @staticmethod
    def find_objects_of_type(object_type: Type[T]) -> Union[List, List[T]]:
        """Return a list of Objects of type Type"""

        if object_type is not Object:
            return [obj for obj in Object.__OBJECTS if isinstance(obj, object_type)]
