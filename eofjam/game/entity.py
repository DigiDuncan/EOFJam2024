from __future__ import annotations
import math
from typing import TYPE_CHECKING
import arcade
from arcade import Sprite, SpriteCircle, Vec2
import arcade.clock

from eofjam.lib.types import BASICALLY_ZERO
from eofjam.lib.utils import clamp

if TYPE_CHECKING:
    from eofjam.game.bullet import BulletList

from eofjam.constants import ENEMY_COLOR, PLAYER_COLOR, SPAWNER_COLOR
from eofjam.lib.collider import CircleCollider

TAU_THREE_SIXTYTHS = math.tau / 360

class Entity:
    def __init__(self, position: Vec2, sprite: Sprite, rotation: float = 0.0, scale: float = 1.0):
        self._position: Vec2 = position
        self._rotation: float = rotation
        self.sprite: Sprite = sprite
        self.flash_sprite = SpriteCircle(self.sprite.width / 2, arcade.color.WHITE)
        self._scale: float = scale
        self.velocity: Vec2 = Vec2()

        self.position = position
        self.rotation = rotation
        self.scale = scale

        self.max_health: int = 100

        self.health: int = 100
        self.strength: float = 1
        self.defense: float = 1
        self._speed: float = 400
        self.sprinting = False
        self.bullet_speed: float = 500
        self.last_damage_time = None

        self.immobile = False

    @property
    def hitbox(self) -> CircleCollider:
        return CircleCollider(self.position, self.sprite.width / 2)

    @property
    def position(self) -> Vec2:
        return self._position

    @position.setter
    def position(self, v: Vec2) -> None:
        self.sprite.position = v
        self.flash_sprite.position = v
        self._position = v

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, v: float) -> None:
        self.sprite.rotation = v
        self._rotation = v

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, v: float) -> None:
        self.sprite.scale = round(v / 4, 3)
        self.flash_sprite.scale = round(v / 4, 3)
        self._scale = round(v, 3)

    @property
    def speed(self) -> float:
        return self._speed / math.sqrt(self.scale) * (1.5 if self.sprinting else 1.0)

    @speed.setter
    def speed(self, v: float) -> None:
        self._speed = v

    def update(self, delta_time: float) -> None:
        if self.last_damage_time is not None:
            t = (arcade.clock.GLOBAL_CLOCK.time - self.last_damage_time) * 4
            a = int(clamp(0, arcade.math.lerp(255, 0, t), 255))
            self.flash_sprite.alpha = a
        else:
            self.flash_sprite.alpha = 0

class Enemy(Entity):
    def __init__(self, position: Vec2, rotation: float = 0.0, scale: float = 1.0):
        sprite = SpriteCircle(512, ENEMY_COLOR)
        super().__init__(position, sprite, rotation, scale)

        self.max_health = 5
        self.health = 5

class Player(Entity):
    def __init__(self, position: Vec2, rotation: float = 0.0, scale: float = 1.0):
        sprite = SpriteCircle(128, PLAYER_COLOR)
        super().__init__(position, sprite, rotation, scale)

        self.up = False
        self.down = False
        self.left = False
        self.right = False

        self.fire_up = False
        self.fire_down = False
        self.fire_left = False
        self.fire_right = False

        self.scaling_up = False
        self.scaling_down = False

        self.energy = 2.0
        self.scale_speed = 1.0

        self.fire_rate = 0.25

        self.speed = 600

    @property
    def speed(self) -> float:
        return self._speed / math.sqrt(self.scale) * (1.5 if self.sprinting and self.energy > BASICALLY_ZERO else 1.0)

    @speed.setter
    def speed(self, v: float) -> None:
        self._speed = v

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, v: float) -> None:
        self.sprite.scale = v
        self.flash_sprite.scale = v
        self._scale = v

    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        direction = Vec2(self.right - self.left, self.up - self.down).normalize()
        self.velocity = direction * self.speed
        if self.sprinting:
            self.energy -= (delta_time / 2.5)

class BulletSpawner(Entity):
    def __init__(self, bullet_list: BulletList, position: Vec2, rotation: float = 0.0, scale: float = 1, speed: float = 0.0, fire_rate: float = 0.25):
        sprite = SpriteCircle(256, SPAWNER_COLOR)
        super().__init__(position, sprite, rotation, scale)

        self.bullet_list = bullet_list
        self.speed = speed
        self.immobile = True
        self.fire_rate = fire_rate
        self.active = True

        self.bullet_timer = 0.0

    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        self.bullet_timer += delta_time
        if self.active:
            self.rotation += self.speed * delta_time
            if self.bullet_timer >= self.fire_rate:
                self.bullet_list.spawn(self, self.position, Vec2.from_heading(self.rotation * TAU_THREE_SIXTYTHS, self.bullet_speed), self.scale)
                self.bullet_timer = 0.0
