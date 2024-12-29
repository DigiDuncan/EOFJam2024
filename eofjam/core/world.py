import math
import arcade
from arcade import Camera2D, Rect, SpriteList, Vec2, get_window
from arcade.camera.grips import constrain_xy

from eofjam.game.bullet import BulletList
from eofjam.game.grill import Grill
from eofjam.game.hazard import Hazard
from eofjam.lib.utils import clamp, smerp
from eofjam.game.entity import Enemy, Entity, Player
from eofjam.core.store import game


class World:
    def __init__(self, player: Player, camera: Camera2D, enemies: list[Enemy] = None,
                 hazards: list[Hazard] = None, grills: list[Grill] = None):
        self.player: Player = player
        self.camera: Camera2D = camera
        self.enemies: list[Enemy] = [] if enemies is None else enemies
        self.hazards: list[Hazard] = [] if hazards is None else hazards
        self.grills: list[Grill] = [] if grills is None else grills

        self.bounds: Rect = get_window().rect * 4

        self.enemy_spritelist = SpriteList()
        for e in enemies:
            self.enemy_spritelist.append(e.sprite)
        self.bullets: BulletList = BulletList(self)

        self._scale = 1
        self.target_scale = 1

        self.bullet_timer = 0.0

        self.draw_bounds = False

    @property
    def entities(self) -> list[Entity]:
        return [self.player, *self.enemies]

    def refresh_enemies(self) -> None:
        self.enemy_spritelist.clear()
        for e in self.enemies:
            self.enemy_spritelist.append(e.sprite)

    @property
    def scale(self) -> float:
        return self.target_scale

    @scale.setter
    def scale(self, v: float) -> None:
        if game.run.unlimited_scale:
            self.target_scale = round(v, 3)
        else:
            self.target_scale = round(clamp(0, v, 2), 3)

    def handle_scale(self) -> None:
        s = round(math.exp2(2 * self._scale - 2), 5)
        self.player.scale = s
        self.camera.zoom = 1 / clamp(1, s * 4, 16)

    def update(self, delta_time: float) -> None:
        # Handle player scaling
        if self.player.scaling_up and self.player.scaling_down:
            pass
        elif not game.run.unlimited_scale and self.scale >= 2 and self.player.scaling_up:
            # We have to do this here to avoid losing energy for no reason
            pass
        elif not game.run.unlimited_scale and self.scale <= 0 and self.player.scaling_down:
            # We have to do this here to avoid losing energy for no reason
            pass
        elif self.player.scaling_up:
            ds = self.player.scale_speed * delta_time
            if ds > self.player.scale_energy:
                ds = self.player.scale_energy
            self.scale += ds
            self.player.scale_energy -= ds
        elif self.player.scaling_down:
            ds = self.player.scale_speed * delta_time
            if ds > self.player.scale_energy:
                ds = self.player.scale_energy
            self.scale -= ds
            self.player.scale_energy -= ds

        # Handle world scaling
        self._scale = smerp(self._scale, self.target_scale, 10, delta_time)
        self.handle_scale()

        # Bullets
        self.bullet_timer += delta_time
        if self.bullet_timer >= self.player.fire_rate * self.player.scale and (self.player.fire_up or self.player.fire_down or self.player.fire_left or self.player.fire_right):
            v = Vec2(0, 0)
            if self.player.fire_up:
                v += Vec2(0, 1)
            if self.player.fire_down:
                v += Vec2(0, -1)
            if self.player.fire_left:
                v += Vec2(-1, 0)
            if self.player.fire_right:
                v += Vec2(1, 0)

            v = v.normalize() * self.player.bullet_speed
            if v.length != 0:
                self.bullets.spawn(self.player, self.player.position, v, self.player.scale)
                self.bullet_timer = 0.0

        # Collision checks?
        for enemy in self.enemies:
            self.player.position = self.player.hitbox.collide(enemy.hitbox, self.player.position)
        for hazard in self.hazards:
            for entity in self.entities:
                entity.position = hazard.collide(entity)
        for grill in self.grills:
            grill.collide(self.player)

        # Update loops
        self.player.update(delta_time)
        self.bullets.update(delta_time)

        # Camera
        self.camera.position = self.player.position
        self.camera.position = constrain_xy(self.camera.view_data, self.bounds)

    def draw(self) -> None:
        for h in self.hazards:
            h.draw()
        for g in self.grills:
            g.draw()
        self.enemy_spritelist.draw()
        self.player.draw()
        self.bullets.draw()
        if self.draw_bounds:
            arcade.draw_rect_outline(self.bounds, arcade.color.BLUE, border_width = max(1, int(self.player.scale * 4)))
