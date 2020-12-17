from __future__ import annotations
from PyMath import Vector2
import pygame

# Todo: Think about how editor/window objects should be represented and updated
# Todo: Possibly a message system that utilizes some sort of callback/registry system


class Pane(object):
    """Root pane/Widget object for managing and updating GUI elements in the editor

    Pane's should house a context manager of some sort for handling user input therefore
    they need to know whether they have. Context manager should also contain menus for
    right click and hover information. Pane's should be subclassed for specific needs
    and problems. Pane's should be resizeable on request, snap to window/pane edges, be
    draggable, closeable,  and have the ability (if pygame allows. I don't think it does)
    to float freestanding from the current editor window. Pane's should only be drawn when they change
    their individual elements change. Perhaps Pane's should be able to exist
    stacked within themselves or maybe I need another object for this purpose."""

    def __init__(self, size: Vector2):
        self.surface = pygame.Surface(size.components())
        self.parent = None