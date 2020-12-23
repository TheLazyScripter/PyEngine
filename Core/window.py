from __future__ import annotations
import pygame
from Core.Architecture import Camera
from Core.Architecture.CONSTANTS import NORMAL_DRAW


# TODO: Unwind Camera from Window. Currently fucked

class Window:
    _instance = None

    class Singleton:
        def __init__(self, size, title, fps=60, background_color=(255, 255, 255), full_screen=False, mode=NORMAL_DRAW):
            self.width, self.height = self.size = size
            self.title = title
            self.fps = fps
            self.background_color = background_color
            self.__mode = mode
            self.__redraw = True
            self.__fs = full_screen
            self.__window = None
            self.__is_active = False
            self.camera = None
    
        def start(self):
            if not self.__window:
                self.__window = pygame.display.set_mode(self.size, 0, 32)
                pygame.display.set_caption(self.title)
                self.camera = Camera.main()
    
        def add_camera(self, camera: Camera):
            self.camera = camera
    
        def update(self):
            self.__is_active = pygame.display.get_active()
    
        def draw(self, objects):
            if self.camera:
                self.__window.fill((255, 255, 0))
                self.camera.draw(objects, self.__mode)
                self.camera.render(self.__window, self.__mode)
    
            pygame.display.update()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            try:
                cls._instance = Window.Singleton(*args, **kwargs)
            except Exception as e:
                print(e)
        return cls._instance

    def __getattr__(self, item):
        if not self._instance:
            raise RuntimeError("Must Create the Window First")
        return getattr(self._instance, item)
