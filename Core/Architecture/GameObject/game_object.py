from __future__ import annotations

import threading
from time import sleep
from typing import TYPE_CHECKING, Optional, Iterable, List, Union, Type

from ..CONSTANTS import *

if TYPE_CHECKING:  # Dirty Hack to make 'Component' type available
    # noinspection PyProtectedMember
    from ..Component import Component, TYPE_COMP


class GameObject(object):
    """
    Root object class for all objects in Core. GameObject
    is meant to be overridden by external subclasses. Use instantiate
    to add GameObject instance to the ObjectManager.
    """

    __game_objects = {}

    def _required(*required):
        def wrapper(fn):
            def inner(self, *args, **kwargs):
                if all([i.fget(self)] for i in required):
                    return fn(self, *args, **kwargs)
            return inner
        return wrapper

    def __init__(self, name: str, tag: Optional[str] = None, obj_id: Optional[int] = None,
                 children: Optional[Iterable[GameObject]] = None,
                 components: Optional[Iterable[Component]] = None,
                 enabled: bool = True):
        """
        :ivar iterable children:
        :ivar Transform transform: Objects Transform Component
        :ivar GameObject game_object: Objects parent GameObject
        """

        self.__name = name
        self.__tag = tag
        self.__id = obj_id if obj_id and obj_id not in GameObject.__game_objects else GameObject.generate_unique_id()
        self.__children = children if children else []
        self.__components: List[Component] = components if components else []
        self.parent = None
        self.__is_enabled = enabled
        self.__started = False
        self.awake()

    @property
    def name(self):
        return self.__name

    @property
    def tag(self):
        return self.__tag

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, gid):
        self.__id = gid

    @property
    def enabled(self):
        return self.__is_enabled

    @property
    def started(self):
        return self.__started

    def enable(self):
        self.__is_enabled = True

    def disable(self):
        self.__is_enabled = False

    def toggle_enable(self):
        self.__is_enabled = not self.__is_enabled

    def add_child(self, game_object: GameObject) -> None:
        """
        Add a child GameObject to this object and
        set the parent of the added GameObject to this GameObject.

        Method checks that the GameObject is not already a child.
        """

        if not self.get_child_with_name(game_object.name):
            self.__children.append(GameObject.find_object_by_id(game_object.id))
            game_object.set_parent(self)

    def remove_child(self, game_object: GameObject) -> None:
        """
        Remove the passed GameObject from our child list. First
        checks that GameObject exists.
        """
        if self.get_child_with_name(game_object.name):
            self.__children.remove(game_object)

    def set_parent(self, game_object: GameObject) -> None:
        """
        Set this GameObject's parent to the passed GameObject. If a parent
        already exists, first remove this GameObject from the parent.
        Add's this GameObject to the new parent's child list
        """

        if self.parent != game_object:
            if self.parent:  # We already have a parent
                self.parent.remove_child(self)  # Remove ourselves from the parent

            self.parent = GameObject.find_object_by_id(game_object.id)
            self.parent.add_child(self)

    def get_child_with_name(self, name: str) -> Optional[GameObject]:
        """
        Return the first instance of a GameObject whose name
        matches the passed str.
        """

        for obj in self.__children:
            if obj.name == name:
                return obj
        return None

    def get_child_with_tag(self, tag: str) -> Optional[GameObject]:
        for obj in self.__children:
            if obj.tag == tag:
                return obj
        return None

    def get_all_children_with_tag(self, tag: str) -> Optional[List[GameObject]]:
        matches = []
        for obj in self.__children:
            if obj.tag == tag:
                matches.append(obj)
        return matches if len(matches) > 0 else None

    def add_component(self, component: Component) -> None:
        """Add a new Component to this GameObject if Component doesn't already exist"""
        if not self.get_component(type(component)):
            self.__components.append(component)
            component.set_parent(self)

    def remove_component(self, component: Component) -> None:
        """Remove a Component from this GameObject"""
        self.__components.remove(component)
        component.set_parent(None)

    def remove_component_of_type(self, comp_type: Type[Component]) -> None:
        """Remove a Component by type from this GameObject"""

        self.remove_component(self.get_component(comp_type))

    def get_component(self, component_type: Type[Component]) -> Optional[TYPE_COMP]:
        """Get a reference to a Component attached to this GameObject, whose type matches

        :returns Component: The 'Component' attached to the 'GameObject' whose type matches"""

        for component in self.__components:
            if isinstance(component, component_type):
                return component
        return None

    def get_component_in_children(self, component_type: type) -> Optional[TYPE_COMP]:
        for child in self.__children:
            m = child.get_component_in_children(component_type)
            if m:
                return m
        return None

    def get_component_in_parent(self, comp_type: type) -> Optional[TYPE_COMP]:
        if self.parent:
            for child in self.parent.children:
                m = child.get_component(comp_type)
                if m:
                    return m
        return None
    
    def send_message(self, method_name: str, *args, **kwargs) -> None:
        for component in self.__components:
            try:
                getattr(component, method_name)(args, kwargs)
            except KeyError:
                pass

    def broadcast_message(self, method_name: str, *args, **kwargs) -> None:
        """Calls the method named method_name on every 'Component' in this 'GameObject' or any of its children"""
        for obj in self.__children:
            obj.broadcast_message(method_name, *args, **kwargs)
        self.send_message(method_name, *args, **kwargs)

    @_required(enabled)
    def awake(self):
        """
        Method to wake up this GameObject and all child Component
        that is called once before start.

        This is called automatically by the Application and should
        not be called externally. Awake and Start are separated
        to allow for control over load order.

        Overload to adjust load order of custom objects.
        """

        for component in self.__components:
            component.set_parent(self)
            component.awake()

    @_required(enabled)
    def start(self):
        """
        Method to start this GameObject and all child Component.
        This is called automatically by the Application and
        should not be called externally.

        This is called once before the first update.

        Overload to adjust load order of custom objects.
        """
        self.__started = True
        for component in self.__components:
            component.start()

    @_required(enabled, started)
    def update(self):
        """
        Method to update this GameObject and all child Component.
        This is called automatically by the Application and
        should not be called externally.

        This is called once per frame after start.

        Overload's allowed.
        """

        for component in self.__components:
            component.update()

    @_required(enabled, started)
    def fixed_update(self):
        """
        Method to update this GameObject and all child Component.
        This is called automatically by the Application and
        should not be called externally. Use fixed_update
        rather than update for more precise calculations.

        This is called once per game loop after start.

        Overload's allowed.
        """
        if self.__is_enabled and self.__started:
            for component in self.__components:
                component.fixed_update()

    @_required(enabled, started)
    def destroy(self, after: int = 0) -> None:
        """Destroy a GameObject after a certain amount of time"""

        def _destroy_object() -> None:
            sleep(after)
            del GameObject.__game_objects[self.id]

        if after:
            threading.Thread(target=_destroy_object).start()
        else:
            del GameObject.__game_objects[self.id]

    @staticmethod
    def game_objects():
        return GameObject.__game_objects

    @staticmethod
    def generate_unique_id(start: int = None) -> int:
        """Generate a unique id used to differentiate GameObjects"""

        obj_id = start or len(GameObject.game_objects())
        while obj_id in GameObject.game_objects():
            obj_id += 1
        return obj_id

    @staticmethod
    def find_object_by_id(obj_id: int) -> Optional[GameObject]:
        """Find a GameObject by unique ID"""

        return GameObject.__game_objects.get(obj_id, None)

    @staticmethod
    def find_object_by_name(name: str) -> Optional[GameObject]:
        """Find the first GameObject whose name matches. Faster than find_all."""

        for obj in GameObject.__game_objects.values():
            if obj.name == name:
                return obj
        return None

    @staticmethod
    def find_object_by_tag(tag: str) -> Optional[GameObject]:
        """Find the first GameObject whose tag matches. Faster than find_all."""

        for obj in GameObject.__game_objects.values():
            if obj.tag == tag:
                return obj
        return None

    @staticmethod
    def find_all_objects_by_name(name: str) -> Union[GameObject, list]:
        """Find all objects whose name matches. Slower than find."""

        found = []
        for obj in GameObject.__game_objects.values():
            if obj.name == name:
                found.append(obj)
        return found

    @staticmethod
    def find_all_objects_by_tag(tag: str) -> Union[GameObject, list]:
        """Find all objects whose tag matches. Slower than find."""

        found = []
        for obj in GameObject.__game_objects.values():
            if obj.tag == tag:
                found.append(obj)
        return found

    @staticmethod
    def find_object_matching_any(to_match: {str: Iterable}) -> Optional[GameObject]:
        """Find all objects that match any key/item pair"""

        for obj in GameObject.__game_objects.values():
            for k, v in to_match.items():
                if isinstance(v, (tuple, set, list)):
                    for value in v:
                        if not hasattr(obj, value):
                            return obj
                else:
                    if not hasattr(obj, v):
                        return obj
        return None

    @staticmethod
    def find_object_matching_all(to_match: dict) -> Optional[GameObject]:
        """Find first object that matches every key/item pair"""

        for obj in GameObject.__game_objects.values():
            match = True
            for k, v in to_match.items():
                if isinstance(v, (tuple, set, list)):
                    for value in v:
                        if not hasattr(obj, value):
                            match = False
                else:
                    if not hasattr(obj, v):
                        match = False
            if match:
                return obj
        return None

    @staticmethod
    def find_all_objects_matching_any(to_match: dict) -> Optional[Iterable[GameObject]]:
        """Find all objects that match any key/item pair"""

        matches = []
        for obj in GameObject.__game_objects.values():
            for k, v in to_match.items():
                if isinstance(v, (tuple, set, list)):
                    for value in v:
                        if hasattr(obj, value):
                            matches.append(obj)
                else:
                    if hasattr(obj, v):
                        matches.append(obj)
        return matches

    @staticmethod
    def find_all_objects_matching_all(to_match: dict) -> Optional[Iterable[GameObject]]:
        """Find all objects that match every key/item pair"""

        matches = []
        for obj in GameObject.__game_objects.values():
            match = True
            for k, v in to_match.items():
                if isinstance(v, (tuple, list, set)):
                    for value in v:
                        if not hasattr(obj, value):
                            match = False
                else:
                    if not hasattr(obj, v):
                        match = False
            if match:
                matches.append(obj)
        return matches

    @staticmethod
    def find_renderable_objects() -> Optional[Iterable[GameObject]]:
        """Find all objects that have Renderer components"""

        key = {"type": [COMPONENT_TEXT_RENDERER, COMPONENT_SPRITE_RENDERER, COMPONENT_RENDERER]}
        return GameObject.find_all_objects_matching_any(key)
