import time
from threading import Thread

from pygame.constants import QUIT
from pygame.time import Clock

from .event_system import EventSystem
from .object_manager import ObjectManager


# TODO: Have main loop return to Application after starting threads. Think App should handle closing rather
# TODO: than 'GameEngine'


class GameEngine:
    def __init__(self, fps, window):
        self.__fps = fps
        self.clock = Clock()

        self.__thread_update = Thread(target=self.object_update)
        self.__thread_render = Thread(target=self.render)
        self.__thread_fixed_update = Thread(target=self.object_fixed_update)

        self.window = window

        self.running = False

    def initialize(self):
        self.window.start()

    def update(self):
        last_time = time.time()
        while self.running:
            if EventSystem().get_events(QUIT):
                self.stop()
            if time.time() - last_time > 1.0:
                last_time = time.time()
                EventSystem().flush()
            EventSystem().update()
            self.clock.tick(self.__fps)

    def render(self):
        while self.running:
            self.window.draw(ObjectManager().get_objects())
            self.clock.tick(self.window.fps)

    def object_update(self):
        while self.running:
            ObjectManager().update()
            self.clock.tick(self.__fps)
                
    def object_fixed_update(self):
        while self.running:
            ObjectManager().fixed_update()
            time.sleep(.002)

    def start(self):
        self.running = True
        self.__thread_update.start()
        self.__thread_render.start()
        self.__thread_fixed_update.start()
        self.update()

    def stop(self):
        self.running = False
