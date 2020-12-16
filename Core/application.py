from Core.Architecture import *
from Core.Architecture.CONSTANTS import NORMAL_DRAW
from .window import Window

# TODO: Fix how singleton objects are referenced and figure out how to save them accordingly


class Application(object):
    """
    Main Application interface
    """

    def __init__(self, app_name=None, app_size=None, fps=60, mode=NORMAL_DRAW):
        self.window = Window() if Window() else (Window(app_size, app_name, fps, mode) if app_size and app_name else None)
        self.object_manager = ObjectManager([])
        self.engine = GameEngine(fps, Window())
        self.running = False

    def initialize(self):
        self.running = False
        self.engine.initialize()

    def save(self):
        pass

    def load(self):
        # TODO: Make it so there can only be one Camera.
        # TODO: Fix singleton save and load issues by removing them and passing them around correctly
        Camera.instance = Window.camera
        ObjectManager.instance = self.object_manager
        self.object_manager.load()
        Window().load()
        self.engine = GameEngine(self.fps)
        self.initialize()

    def execute(self, on_exit=None):
        if not self.running:
            self.running = True
            self.engine.start()
            if on_exit:
                on_exit()
