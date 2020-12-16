from __future__ import annotations

import pygame

from PyMath import Vector2
from .__component import Component
from .transform import Transform
from ..CONSTANTS import COMPONENT_PHYSICS_RIGID_BODY2D, COMPONENT_PHYSICS_BOX_COLLIDER2D, COMPONENT_TRANSFORM


class RigidBody2D(Component):
    """
    RigidBody Component for 2D vectors.
    """

    def __init__(self, mass=1, is_kinematic=False):
        super(RigidBody2D, self).__init__(COMPONENT_PHYSICS_RIGID_BODY2D)
        self.is_kinematic = is_kinematic
        self.mass = mass
        self.velocity = Vector2.zero()
        self.acceleration = Vector2.zero()
        self.force = Vector2.zero()

    def apply_force(self, other_rb: RigidBody2D) -> None:
        self.force = (other_rb.velocity * other_rb.mass) - (self.velocity * self.mass).normalized()

    def set_velocity(self, velocity: Vector2) -> None:
        self.velocity = velocity

    def set_acceleration(self, acceleration: Vector2) -> None:
        self.acceleration = acceleration

    def fixed_update(self):
        transform = self.game_object.get_component(Transform)
        self.velocity += self.acceleration
        self.velocity += self.force
        transform.translate(self.velocity + self.force)
        self.force = Vector2.zero()


class BoxCollider2D(Component):
    # Todo: Figure Out How This Should Work!
    def __init__(self, size, is_trigger=False):
        super(BoxCollider2D, self).__init__(COMPONENT_PHYSICS_BOX_COLLIDER2D)
        self.__size = size
        self.__rect = None
        self.__is_trigger = is_trigger
