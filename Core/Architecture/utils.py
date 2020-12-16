from PyMath import Vector2
from .GameObject import GameObject
from .Component import Transform

def instantiate(game_object, position=None, rotation=0,
                transform=None, parent=None, keep_world_position=True,
                **kwargs):
    """
    Initialize a GameObject and add it to the ObjectManager for future use

    If object is already instantiated raise exception. Prioritize passed
    transform if any, otherwise, create a new Transform with position and rotation if set
    and apply it to the GameObject. We prioritize named position and rotation over passed
    transform's values.

    If parent GameObject is passed and game_object doesn't already have a parent,
    we add the game_object to parent and parent to game_object.

    keep_world_position is used to determine the actual location of the object.
    If False, position is set relative to the parent object not the world.


    :param GameObject game_object: GameObject to initialize and add
    :param Vector2 position: Position to be applied to our transform
    :param float rotation: Rotation in degrees to apply to our transform
    :param Transform transform: Optional transform
    :param GameObject parent: Parent GameObject
    :param bool keep_world_position: Whether local position should be overridden by parent GameObject
    :return: None
    :raises: InstantiationError
    """

    if not isinstance(game_object, GameObject):
        raise TypeError(
            "game_object {} expected, found {}".format(type(GameObject("TypeDef", "")), type(game_object)))

    if GameObject.find_object_by_id(game_object.id):
        game_object.id = GameObject.generate_unique_id()

    pos = position if isinstance(position, Vector2) else kwargs.get("position", Vector2(0, 0))
    rot = rotation or kwargs.get("rotation")
    transform = transform or kwargs.get("transform") or Transform(pos, rot)

    GameObject.game_objects()[game_object.id] = game_object
    if parent:
        if not keep_world_position:
            pos += parent.get_component(Transform).position

        parent.add_child(game_object)

    transform.set_pos(pos if pos > 0 else transform.position)
    transform.set_rotation(rot if rot else transform.rotation)
    game_object.add_component(transform)

    game_object.start()
