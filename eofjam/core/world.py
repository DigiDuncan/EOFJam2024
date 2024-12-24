from arcade import Camera2D, Rect, SpriteList, get_window
import arcade
from arcade.camera.grips import constrain_xy

from eofjam.lib.utils import clamp
from .entity import Enemy, Player


class World:
    def __init__(self, player: Player, camera: Camera2D, enemies: list[Enemy] = None):
        self.player: Player = player
        self.camera: Camera2D = camera
        self.enemies: list[Enemy] = [] if enemies is None else enemies
        self.bounds: Rect = get_window().rect * 4

        self.enemy_spritelist = SpriteList()
        for e in enemies:
            self.enemy_spritelist.append(e.sprite)

        self._scale = 1

        self.draw_bounds = False

    def refresh_enemies(self) -> None:
        self.enemy_spritelist.clear()
        for e in self.enemies:
            self.enemy_spritelist.append(e.sprite)

    @property
    def scale(self) -> float:
        return round(self._scale / 4, 3)

    @scale.setter
    def scale(self, v: float) -> None:
        self._scale = clamp(0.125, round(v * 4, 3), 8)
        self.handle_scale()

    def handle_scale(self) -> None:
        self.player.scale = self.scale
        self.camera.zoom = 1 / clamp(1, self._scale, 16)

    def update(self, delta_time: float) -> None:
        self.player.update(delta_time)
        for enemy in self.enemies:
            self.player.position = self.player.hitbox.collide(enemy.hitbox, self.player.position)

        self.camera.position = self.player.position
        self.camera.position = constrain_xy(self.camera.view_data, self.bounds)

    def draw(self) -> None:
        self.enemy_spritelist.draw()
        self.player.draw()
        if self.draw_bounds:
            arcade.draw_rect_outline(self.world.bounds, arcade.color.BLUE)
