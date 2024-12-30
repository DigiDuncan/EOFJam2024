import math
import arcade
from arcade import Camera2D, Rect, SpriteList, Vec2, get_window
from arcade.camera.grips import constrain_xy

from eofjam.constants import DEBUG_COLOR
from eofjam.game.bullet import BulletList
from eofjam.game.hazard import Hazard
from eofjam.lib.utils import clamp, smerp
from eofjam.game.entity import Enemy, Entity, Player
from eofjam.core.store import game
from eofjam.lib.collider import Collider, InverseRectCollider


class World:
    def __init__(self, player: Player, camera: Camera2D, enemies: list[Enemy] = None,
                 hazards: list[Hazard] = None):
        self.player: Player = player
        self.camera: Camera2D = camera
        self.bounds: Rect = get_window().rect * 8

        self.terrain: list[Collider] = [InverseRectCollider(self.bounds)]
        self.enemies: list[Enemy] = [] if enemies is None else enemies
        self.hazards: list[Hazard] = [] if hazards is None else hazards

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

        # update loops
        for e in self.entities:
            e.update(delta_time)
        self.bullets.update(delta_time)

        # Update positions
        for entity in self.entities:
            entity.position += entity.velocity * delta_time

        # Collision checks?
        # For ease of logic lets do this in a few steps (reduces loop count too)

        entities = self.entities

        for entity in entities:
            collider = entity.hitbox

            # entity - player collisions
            for other in entities:
                other_c = other.hitbox
                if other == entity or not collider.overlaps(other_c):
                    continue

                overlap, normal = collider.collide(other_c)
                # These mass calculations are rough, but hey, it's a game jam.
                e_mass = max(1.0, 4 * entity.scale) ** 2 if not entity.immobile else math.inf
                o_mass = max(1.0, 4 * other.scale) ** 2 if not other.immobile else math.inf
                entity.position += abs(overlap) * normal / e_mass
                other.position += -abs(overlap) * normal / o_mass

            # entity - terrain collisions
            for terrain in self.terrain:
                if not collider.overlaps(terrain):
                    continue

                overlap, normal = collider.collide(terrain)
                entity.position += abs(overlap) * normal

            # entity - hazard collisions
            for hazard in self.hazards:
                hazard_c = hazard.hitbox
                if collider.overlaps(hazard_c):
                    if not hazard.passable(entity.scale):
                        overlap, normal = collider.collide(hazard_c)
                        entity.position += abs(overlap) * normal
                    hazard.interact(entity)

        # Health
        rem = []
        for e in self.enemies:
            if e.health <= 0:
                rem.append(e)
        for e in rem:
            self.enemies.remove(e)

        self.refresh_enemies()

        # Camera
        self.camera.position = self.player.position
        self.camera.position = constrain_xy(self.camera.view_data, self.bounds)

    def draw(self) -> None:
        for h in self.hazards:
            h.draw()
        self.enemy_spritelist.draw()
        self.player.draw()
        self.bullets.draw()
        if self.draw_bounds:
            arcade.draw_rect_outline(self.bounds, DEBUG_COLOR, border_width = max(1, int(self.player.scale * 4)))
