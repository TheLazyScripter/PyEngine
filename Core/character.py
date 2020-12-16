import pygame

from PyMath import Vector2, radians_to_degrees, look_towards
from Core.Architecture import Transform, SpriteRenderer, RigidBody2D
from Core.Architecture import EventSystem
from Core.Architecture import GameObject


class Character(GameObject):

    def __init__(self, name, tag, speed, sprite):
        super(Character, self).__init__(name, tag)
        self.speed = speed
        self.add_component(RigidBody2D())
        self.add_component(SpriteRenderer(sprite))

        self.look_direction = None
        self.direction = Vector2.zero()
        self.target_character = None

        self.transform: Transform = self.get_component(Transform)
        self.sprite_renderer: SpriteRenderer = self.get_component(SpriteRenderer)

    def start(self):
        super(Character, self).start()
        self.transform = self.get_component(Transform)
        self.sprite_renderer = self.get_component(SpriteRenderer)

    def target(self, character):
        self.target_character = character

    def look_at(self, position):
        self.look_direction = position
        
    def follow_target(self):
        self.move_towards(self.target_character)

    def move_towards(self, target: GameObject):
        if isinstance(target, Vector2):
            target_dir = self.transform.position - target
        elif isinstance(target, GameObject):
            target_dir = self.transform.position - target.get_component(Transform).position
        else:
            raise Exception("Vector or Character obj expected")

        # new_vector = Vector2(*(1 if i > 1 else -1 for i in -target_dir))
        new_vector = (-target_dir.normalized())  # Less Rigid movement at the cost of speed
        self.transform.set_pos(self.transform.position + (new_vector * self.speed))

    def check_events(self):
        if EventSystem().get_key_downs((pygame.K_w, pygame.K_UP)):
            self.direction += Vector2.up() * self.speed
        elif EventSystem().get_key_downs((pygame.K_s, pygame.K_DOWN)):
            self.direction += Vector2.down() * self.speed
        elif EventSystem().get_key_downs((pygame.K_a, pygame.K_LEFT)):
            self.direction += Vector2.left() * self.speed
        elif EventSystem().get_key_downs((pygame.K_d, pygame.K_RIGHT)):
            self.direction += Vector2.right() * self.speed

        if EventSystem().get_key_ups((pygame.K_w, pygame.K_UP)):
            self.direction -= Vector2.up() * self.speed
        elif EventSystem().get_key_ups((pygame.K_s, pygame.K_DOWN)):
            self.direction -= Vector2.down() * self.speed
        elif EventSystem().get_key_ups((pygame.K_a, pygame.K_LEFT)):
            self.direction -= Vector2.left() * self.speed
        elif EventSystem().get_key_ups((pygame.K_d, pygame.K_RIGHT)):
            self.direction -= Vector2.right() * self.speed

    def update(self):
        if self.enabled and self.started:
            super(Character, self).update()
            self.check_events()
            if self.target_character:
                self.look_direction = self.target_character.transform.position
                self.move_towards(self.target_character.transform.position)
            else:
                self.look_direction = Vector2(*pygame.mouse.get_pos())
            self.transform.rotation = radians_to_degrees(look_towards(self.transform.position, self.look_direction))
            self.sprite_renderer.rotate(self.transform.rotation)

    def fixed_update(self):
        if self.enabled and self.started:
            super(Character, self).fixed_update()
            self.get_component(RigidBody2D).set_velocity(self.direction)
