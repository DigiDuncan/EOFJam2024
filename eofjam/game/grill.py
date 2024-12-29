import arcade
from arcade import Rect, draw_rect_filled
import arcade.clock

from eofjam.game.entity import Entity, Player
from eofjam.lib.collider import RectCollider
from eofjam.lib.utils import smerp


class Grill:
    def __init__(self, rect: Rect):
        self.rect = rect

    @property
    def hitbox(self) -> RectCollider:
        return RectCollider(self.rect)

    def collide(self, other: Entity) -> None:
        clock = arcade.clock.GLOBAL_CLOCK
        if other.hitbox.overlaps(self.hitbox):
            if isinstance(other, Player):
                other.scale_energy = smerp(other.scale_energy, 0.0, 10, clock.delta_time)

    def draw(self) -> None:
        draw_rect_filled(self.rect, arcade.color.ELECTRIC_CYAN)
