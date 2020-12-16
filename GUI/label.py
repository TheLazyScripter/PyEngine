from __future__ import annotations
from Core.Architecture import GameObject, TextRenderer
import pygame.font as f


class Label(GameObject):
    def __init__(self, name, text="", font: f.Font = f.get_default_font(), size=16, 
                 background_image=None, background_color=(255, 255, 255)):
        
        super().__init__(name, "label")
        self.text = text
        self.font = font if isinstance(font, f.Font) else f.SysFont(font, size)
        self.size = size
        self.background_image = background_image  # <- Todo: Make this work
        self.add_component(TextRenderer(self.font, self.size, background_color))
        self.text_renderer = self.get_component(TextRenderer)
        self.text_renderer.draw(color=(0, 255, 0), text=self.text, antialias=True)

    def set_text(self, text):
        self.text = text

    def update(self):
        super().update()
        self.text_renderer.draw(color=(0, 255, 0), text=self.text, antialias=True)
