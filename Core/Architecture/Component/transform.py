from PyMath import Vector2, radians_to_degrees, look_towards
from .__component import Component
from ..CONSTANTS import COMPONENT_TRANSFORM


class Transform(Component):
    def __init__(self, position, rotation):
        super(Transform, self).__init__(COMPONENT_TRANSFORM)
        self.position = position if isinstance(position, Vector2) else Vector2(position) if position else Vector2.zero()
        self.rotation = rotation if rotation else 0

    def set_pos(self, position):
        self.position = Vector2(position)

    def set_rotation(self, angle):
        assert -360 <= angle <= 360
        self.rotation = angle

    def rotate(self, angle):
        self.rotation = (self.rotation + angle) % 360

    def rotate_towards(self, position, percent=1):
        position = self.position.lerp(position, percent)
        angle = look_towards(self.position, position)
        self.rotation += radians_to_degrees(angle)

    def translate(self, velocity):
        """
        Method to Update the transforms direction vector each frame. Call this when you want the transform to
        begin moving or to slow it down. Vector is applied to the current direction to allow
        for diagonal movement.
        
        Uses - move(Vector2(1.4, 0))
               move(Vector2(0, -2.3))
               move(Vector2(-1.4, 2))

        :param Vector2 velocity:
        :return None:
        """

        self.position += velocity
