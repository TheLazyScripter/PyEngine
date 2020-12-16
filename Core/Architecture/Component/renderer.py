import pygame
from .__component import Component
from .transform import Transform
from ..CONSTANTS import COMPONENT_RENDERER, DEBUG_DRAW, NORMAL_DRAW
from PyMath import Color
from typing import Tuple


class Renderer(Component):
    """
    Base Renderer Component for all current and future
    renderer's. Used to determine how to draw Pygame Surfaces
    and store values associated with them
    """

    def __init__(self, comp_type: str = COMPONENT_RENDERER, surface: pygame.Surface = None, color=Color.black) -> None:
        """
        Create a new Renderer Component to draw surfaces to other surfaces
        or the Pygame Display.

        :ivar surface Surface: Surface Object
        :ivar needs_drawn bool: Whether Surface needs redrawn
        :ivar rect Rect: Rect associated with the Surface and parent Transform
        """

        super(Renderer, self).__init__(comp_type)
        self.__size = None
        self.surface = surface
        self.rect = None
        self.color = color
        self.surface = self.surface if self.surface else pygame.Surface((64, 64))
        self.rect = self.surface.get_rect()

    def update(self) -> None:
        """
        Check whether last drawn Surface is the same as our current Surface
        and draw dependent on a change. Update our Rect comp.
        """

        self.rect = self.surface.get_rect()
        
    def draw(self, mode=NORMAL_DRAW):
        """Draw contents of the Surface"""

        # fill the surface and draw rect if in debug mode
        self.surface.fill(self.color.rgba)
        if mode == DEBUG_DRAW:
            pygame.draw.rect(self.surface, Color.red.rgba, self.rect, 2)
            pygame.draw.circle(self.surface, Color.red.rgba, self.rect.center, 3)

    def render(self, window: pygame.Surface, mode: int = NORMAL_DRAW) -> None:
        """Draw the Surface to the window at our position"""

        self.draw(mode=mode)
        window.blit(self.surface, self.center_on_game_object(self.game_object, self.surface))

    def set_color(self, color: Color):
        self.color = color

    @staticmethod
    def center_on_surface(surface_1: pygame.Surface, surface_2: pygame.Surface) -> Tuple[int, int]:
        """Return the actual center of surface_2 based on surface_1"""

        actual_x = surface_1.get_rect().centerx - (surface_2.get_width() / 2)
        actual_y = surface_1.get_rect().centery - (surface_2.get_height() / 2)
        return actual_x, actual_y

    @staticmethod
    def center_on_game_object(game_object, surface: pygame.Surface) -> Tuple[int, int]:
        """Return the actual center of surface based on game_object.transform"""
        transform = game_object.get_component(Transform)
        x = transform.position.x - surface.get_rect().width / 2
        y = transform.position.y - surface.get_rect().height / 2
        return x, y
