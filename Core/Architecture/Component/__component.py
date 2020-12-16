from __future__ import annotations
from typing import Optional


class Component(object):
    """
    Base Component class used for all other components. Should not be used manually on user end.
    """

    components = {}

    def __init__(self, comp_type: str) -> None:
        """
        :ivar str comp_type: Named Type
        :ivar GameObject game_object: Parent GameObject
        :ivar bool __is_enabled: Whether object should be updated
        """

        self.__type = comp_type
        self.__game_object = None
        self.__is_enabled = False
        self.__register()


    @property
    def enabled(self) -> bool:
        """
        Should Component be updated
        """

        return self.__is_enabled

    @property
    def type(self) -> str:
        return self.__type

    @property
    def game_object(self) -> Optional[GameObject]:
        return self.__game_object

    def set_parent(self, game_object: GameObject) -> None:
        """
        Attach this Component to a GameObject, should not be called directly
        """

        if self.__game_object:
            self.__game_object.remove_component(self)
        self.__is_enabled = True
        self.__game_object = game_object

    def disable(self) -> None:
        """
        Disable this Component
        """

        self.__is_enabled = False

    def enable(self) -> None:
        """
        Enable this Component
        """

        self.__is_enabled = True

    def toggle(self) -> None:
        """
        Toggle whether Component is enabled
        """

        self.__is_enabled = not self.__is_enabled

    def awake(self) -> None:
        """
        Called once when Component is created
        """

        pass

    def start(self) -> None:
        """
        Called once when after all Component's have been awoken
        """

        pass

    def update(self) -> None:
        """
        Called once per frame
        """

        pass

    def fixed_update(self) -> None:
        """
        Called every set amount of time, use this for
        more precise calculations
        """

        pass

    def __register(self):
        Component.components[self.type] = type(self)
