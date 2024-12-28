from __future__ import annotations
from typing import TYPE_CHECKING

import arcade
from arcade import SpriteCircle, SpriteList, Vec2

from eofjam.core.entity import Entity
from eofjam.lib.collider import Collider

if TYPE_CHECKING:
    from eofjam.core.world import World


class Bullet:
    def __init__(self, owner: Entity, position: Vec2, velocity: Vec2 = None, scale: float = 1):
        self.owner = owner
        self.sprite = SpriteCircle(128, arcade.color.BLUE)
        self.position = position
        self.velocity = velocity if velocity else Vec2(0, 0)
        self.scale = scale
        self.dead: bool = False
        self.time_alive: float = 0

        self.max_time: float = 5.0

    @property
    def hitbox(self) -> Collider:
        return Collider(self.position, self.sprite.width / 2)

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
                    # TODO: Add health code here

    def draw(self) -> None:
        self.spritelist.draw()
