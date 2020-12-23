from __future__ import annotations
import pygame
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .callback import _


class EventSystem(object):
    """
    System to house and issue pygame events.
    All call's to this object will return the
    first instance.

    Singleton class used to allow for only one instance
    of EventSystem. All subsequent initialization's will return
    the first instance.

    All other systems dependent on pygame events
    should get the events from here.

    """

    _instance = None
    
    class Singleton:

        def __init__(self):
            """
            :ivar list -> pygame.event events: List of pygame events
            :ivar list -> pygame.event key_ups: List of pygame KEYUP events
            :ivar list -> pygame.event key_downs: List of pygame KEYDOWN events
            """

            self.events = []
            self.key_ups = []
            self.key_downs = []

            self._registered_events: List[Event] = []

        def register_event(self, event: Event):
            self._registered_events.append(event)

        @staticmethod
        def check_event(event_list, events):
            found = False
            for event in events:
                for i in range(len(event_list)):
                    if event_list[i].type == event:
                        found = True
                        event_list.pop(i)
            return found

        @staticmethod
        def check_key(event_list, event_keys):
            found = False
            for key in event_keys:
                for event in event_list:
                    if event.key == key:
                        found = True
                        event_list.remove(event)
            return found

        def check_registered_events(self):
            for i in self.events:
                for j in self._registered_events:
                    if i.type == j.type:
                        j.event.execute()
    
        def get_events(self, events):
            if not isinstance(events, (tuple, set, list)):
                events = [events]
            return self.check_event(self.events, events)
    
        def get_key_downs(self, event_keys):
            if not isinstance(event_keys, (tuple, set, list)):
                event_keys = [event_keys]
            return self.check_key(self.key_downs, event_keys)
    
        def get_key_ups(self, event_keys):
            if not isinstance(event_keys, (tuple, set, list)):
                event_keys = [event_keys]
            return self.check_key(self.key_ups, event_keys)
    
        def update(self):
            """
            Refresh the active event list regardless of whether
            the event was handled. Separates KEYUP and KEYDOWN events
            from all others.
    
            :return: None
            """
    
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.key_downs.append(event)
                elif event.type == pygame.KEYUP:
                    self.key_ups.append(event)
                elif event.type == pygame.MOUSEMOTION:
                    MouseMotion().send()
                else:
                    self.events.append(event)
    
        def flush(self):
            self.events = []
            self.key_ups = []
            self.key_downs = []
            
    def __new__(cls):
        if not cls._instance:
            cls._instance = cls.Singleton()
        return cls._instance
    
    def __getattr__(self, item):
        return getattr(self._instance, item)


class Event:
    """Custum Event for EventSystem to manage and execute callbacks.

    Builds upon the pygame.event.Event type and extends to allow for
    callback to be injected into the event and executed by the EventSystem
    later.
    """

    def __init__(self, event_code: int):
        self.type = pygame.USEREVENT + event_code
        self._callback = None

    def register_callback(self, callback: type):
        self._callback = callback
        
    def send(self):

        pygame.event.post(pygame.event.Event(self.type, {"event": self}))

    def execute(self):
        if not self._callback:
            raise RuntimeError("Must register_callback for this event first")
        self._callback()


class OnCollisionEvent(Event):
    def __init__(self):
        super().__init__(1)


class MouseMotion(Event):
    def __init__(self):
        super().__init__(1)
        EventSystem().register_event(self)
        self.register_callback(MouseMotion.print_mouse)

    @staticmethod
    def print_mouse():
        print(pygame.mouse.get_pos())