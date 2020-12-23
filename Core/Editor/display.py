import pygame
from PyMath import Vector2


class Display(object):
    def __init__(self, size: Vector2, title: str, flags=None):
        self.__size = size
        self.__title = title
        self.__surface = pygame.display.set_mode(self.__size.components, flags=flags)
        
    def blit(self, surface):
        self.__surface.blit(surface, (0,0))
        
    def on_resize(self, new_size):
        pass
        
window = Display(Vector2(100, 100), "Resize Test", pygame.RESIZABLE)
m = pygame.Surface((150, 100))
m.fill((255,0,0))
while True:
    pygame.event.pump()
    print("Still Updating")
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
        if e.type == pygame.VIDEORESIZE:
            window.blit(m)
    pygame.display.update()