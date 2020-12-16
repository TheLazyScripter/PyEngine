from .renderer import Renderer, NORMAL_DRAW, Color
from ..CONSTANTS import COMPONENT_TEXT_RENDERER


class TextRenderer(Renderer):
    def __init__(self, font, size, bg_color=Color.white):
        self.font = font
        self.size = size
        self.background_color = bg_color
        self.image = None
        super().__init__(COMPONENT_TEXT_RENDERER, color=bg_color)

    def draw(self, mode=NORMAL_DRAW, **kwargs):
        super().draw(mode)
        color = kwargs.get("text_color", (0, 0, 0))
        text = kwargs.get("text", "Text")
        antialias = kwargs.get("antialias", False)
        self.image = self.font.render(text, antialias, color)
        # TODO: Auto fit text or resize surface to fit text
        self.surface.blit(self.image, self.center_on_surface(self.surface, self.image))
