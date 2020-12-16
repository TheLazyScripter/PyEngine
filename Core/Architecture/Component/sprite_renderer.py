from typing import Union
from .renderer import *
from ..CONSTANTS import COMPONENT_SPRITE_RENDERER


class SpriteRenderer(Renderer):
    """
    SpriteRenderer Component used to store 2D image
    information and draw it to the window.
    """

    def __init__(self, sprite_location: str) -> None:
        """
        Create a new SpriteRenderer Component from a
        image file

        :ivar sprite_location str: Image File including path
        :ivar __original_sprite Surface: Surface loaded from image file
        :ivar rect Rect: Rect
        """
        self.sprite_location = sprite_location
        self.__original_sprite = pygame.image.load(self.sprite_location).convert()
        self.__original_sprite.set_colorkey((255, 255, 255, 255))
        self.image = self.__original_sprite
        super(SpriteRenderer, self).__init__(COMPONENT_SPRITE_RENDERER, pygame.Surface(self.image.get_size()))
        self.surface.convert()
        self.surface.set_colorkey((255, 255, 255, 255))

    def rotate(self, angle: Union[int, float]) -> None:
        """
        Rotate the original sprite Surface and update the current
        to ensure as little image info is lost.
        """

        self.image = pygame.transform.rotate(self.__original_sprite, angle)

    def draw(self, mode=NORMAL_DRAW):

        self.surface.fill((255, 255, 255))
        self.surface.blit(self.image, self.center_on_surface(self.surface, self.image))
        if mode == DEBUG_DRAW:
            pygame.draw.rect(self.surface, (255, 0, 0), self.surface.get_rect(), 2)
            pygame.draw.circle(self.surface, (255, 0, 0), self.surface.get_rect().center, 3)
