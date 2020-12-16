from .__component import Component
from ..CONSTANTS import COMPONENT_SCRIPT


class Script(Component):
    def __init__(self):
        super().__init__(f"{self.__class__.__name__}")
