from ..GameObject import GameObject


class ObjectManager:
    """
    Root ObjectManager class used to store and update
    non-physics GameObjects. Objects are updated once per
    frame by the Application.

    Singleton class used to allow for only one instance
    of ObjectManager. All subsequent initialization's will return
    the first instance.
    """

    _instance = None

    class Singleton:

        @staticmethod
        def save():
            for game_object in GameObject.game_objects():
                game_object.save()

        @staticmethod
        def load():
            for game_object in GameObject.game_objects():
                game_object.load()

        @staticmethod
        def add_object(game_object):
            if not ObjectManager().has_object(game_object):
                GameObject.game_objects()[game_object.id] = game_object

        @staticmethod
        def get_objects():
            return GameObject.game_objects().values()

        @staticmethod
        def has_object(game_object):
            return game_object.id in GameObject.game_objects()

        @staticmethod
        def fixed_update():
            for game_object in GameObject.game_objects().values():
                game_object.fixed_update()

        @staticmethod
        def update():
            """
            Called each frame by the Application used to
            update each child object. Should not be used
            by outside systems.

            :return: None
            """

            for game_object in list(GameObject.game_objects().values()):
                game_object.update()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = cls.Singleton()
        return cls._instance
    
    def __getattr__(self, item):
        return getattr(self._instance, item)
