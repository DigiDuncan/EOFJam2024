from __future__ import annotations
from typing import TYPE_CHECKING

import arcade
from arcade import SpriteCircle, SpriteList, Vec2
import arcade.clock

from eofjam.constants import BULLET_NONE_COLOR, BULLET_HEALTH_COLOR, BULLET_ENERGY_COLOR, BULLET_BOTH_COLOR
from eofjam.game.entity import Player
from eofjam.lib.collider import CircleCollider

if TYPE_CHECKING:
    from eofjam.game.entity import Entity
    from eofjam.core.world import World


class Bullet:
    def __init__(self, owner: Entity, position: Vec2, velocity: Vec2 = None, scale: float = 1,
                 health_loss: float = 1.0, energy_loss: float = 0.0):
        self.owner = owner

        if health_loss and energy_loss:
            color = BULLET_BOTH_COLOR
        elif health_loss:
            color = BULLET_HEALTH_COLOR
        elif energy_loss:
            color = BULLET_ENERGY_COLOR
        else:
            color = BULLET_NONE_COLOR

        self.sprite = SpriteCircle(128, color)

        self.position = position
        self.velocity = velocity if velocity else Vec2(0, 0)
        self.scale = scale
        self.dead: bool = False
        self.time_alive: float = 0

        self.max_time: float = 5.0

        self.health_loss = health_loss
        self.energy_loss = energy_loss

    @property
    def hitbox(self) -> CircleCollider:
        return CircleCollider(self.position, self.sprite.width / 2)

    @property
    def position(self) -> Vec2:
        return self._position

    @position.setter
    def position(self, v: Vec2) -> None:
        self.sprite.position = v
        self._position = v

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, v: float) -> None:
        self.sprite.scale = round(v / 4, 3)
        self._scale = round(v, 3)

    def draw(self) -> None:
        arcade.draw_sprite(self.sprite)

    def update(self, delta_time: float) -> None:
        self.position += self.velocity * delta_time
        self.time_alive += delta_time
        if self.time_alive >= self.max_time:
            self.dead = True

class BulletList:
    def __init__(self, world: World):
        self.bullets: list[Bullet] = []
        self.world = world

        self.spritelist = SpriteList()

    def spawn(self, owner: Entity, position: Vec2, velocity: Vec2 = None, scale: float = 1) -> None:
        b = Bullet(owner, position, velocity, scale)
        self.bullets.append(b)
        self.spritelist.append(b.sprite)

    def update(self, delta_time: float) -> None:
        for b in self.bullets:
            b.update(delta_time)
            if b.position not in self.world.bounds:
                b.dead = True
        self.check_collisions()
        rem = [b for b in self.bullets if b.dead]
        for b in rem:
            self.bullets.remove(b)
            self.spritelist.remove(b.sprite)

    def check_collisions(self) -> None:
        for e in [self.world.player, *self.world.enemies]:
            for b in self.bullets:
                if b.hitbox.overlaps(e.hitbox) and e != b.owner:
                    b.dead = True
                    e.health -= b.health_loss
                    e.last_damage_time = arcade.clock.GLOBAL_CLOCK.time
                    if isinstance(e, Player):
                        e.scale_energy -= b.energy_loss

    def draw(self) -> None:
        self.spritelist.draw()
