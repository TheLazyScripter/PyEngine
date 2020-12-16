from typing import Union, Tuple, List
import pygame
from Core.Architecture.GameObject.game_object import GameObject
from Core.Architecture.Component import SpriteRenderer, Renderer, TextRenderer, Transform
from Core.Architecture.CONSTANTS import NORMAL_DRAW, DEBUG_DRAW

from Core.Architecture.Component import Renderer


class Camera(GameObject):
    instance = None

    def __init__(self, name: str, size: Union[Tuple[int, int], List[int]], tag: str = "CAMERA") -> None:

        super(Camera, self).__init__(name, tag)
        if not Camera.instance:
            Camera.instance = self
        self.size = size
        self.renderer = None
        self.add_component(Renderer(surface=pygame.Surface(self.size)))
        self.renderer = self.get_component(Renderer)

    def start(self):
        super(Camera, self).start()

    def update(self):
        pass

    def draw(self, obj_list: List[GameObject], mode=NORMAL_DRAW):
        if self.started and self.enabled:
            self.renderer.surface.fill((255, 255, 255))
            cull = self.get_draw_list(obj_list)
            for i in cull:
                i.draw(mode)
                i.render(self.renderer.surface, mode=mode)

    def get_draw_list(self, obj_list: List[GameObject]) -> Union[List[Renderer], List]:
        objs = []
        for obj in obj_list:
            renderer = (obj.get_component(SpriteRenderer) or
                        obj.get_component(Renderer) or
                        obj.get_component(TextRenderer))

            if renderer:
                obj_rect = renderer.rect
                if self.renderer.rect.topleft[0] < obj_rect.bottomright[0] and self.renderer.rect.topleft[1] < obj_rect.bottomright[1]:
                    if self.renderer.rect.bottomright[0] > obj_rect.topleft[0] and self.renderer.rect.bottomright[1] > obj_rect.topleft[1]:
                        if obj != self:
                            objs.append(renderer)
        return objs

    def render(self, surface, mode=NORMAL_DRAW):
        if mode == DEBUG_DRAW:  # Draw Camera Rect
            pygame.draw.rect(self.renderer.surface, (0, 255, 0), self.renderer.rect, 2)

        surface.blit(self.renderer.surface, self.get_component(Transform).position.components())

    @staticmethod
    def main():
        return Camera.instance

    @GameObject._required(GameObject.enabled, GameObject.started)
    def destroy(self, after: int):
        super(Camera, self).destroy(after)
        if Camera.instance == self:
            Camera.instance = None
