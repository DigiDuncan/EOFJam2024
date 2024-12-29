import arcade
from arcade import Rect, Vec2, draw_rect_filled, draw_text

from eofjam.game.entity import Entity
from eofjam.lib.collider import RectCollider


class Hazard:
    def __init__(self, rect: Rect, min_scale: float | None = None, max_scale: float | None = None):
        self.rect = rect
        self.min_scale = min_scale
        self.max_scale = max_scale

    @property
    def hitbox(self) -> RectCollider:
        return RectCollider(self.rect)

    def collide(self, other: Entity) -> Vec2:
        if (self.min_scale is not None and other.scale < self.min_scale) or (self.max_scale is not None and other.scale > self.max_scale):
            # return other.hitbox.collide(self.hitbox, other.position)
            # TODO: Circles and rectangles can't collide right now! A!
            ...
        return other.position

    def draw(self) -> None:
        if self.min_scale is not None and self.max_scale is not None:
            draw_rect_filled(self.rect, arcade.color.BROWN.replace(a = 64))
            draw_text(f"{self.min_scale}x-{self.max_scale}x", self.rect.left + 5, self.rect.top + 5, arcade.color.BLACK, anchor_y = "top", font_size = 24)
        elif self.min_scale is not None:
            draw_rect_filled(self.rect, arcade.color.MAGENTA.replace(a = 64))
            draw_text(f"{self.min_scale}x", self.rect.left + 5, self.rect.top + 5, arcade.color.BLACK, anchor_y = "top", font_size = 24)
        elif self.max_scale is not None:
            draw_rect_filled(self.rect, arcade.color.YELLOW.replace(a = 64))
            draw_text(f"{self.max_scale}x", self.rect.left + 5, self.rect.top + 5, arcade.color.BLACK, anchor_y = "top", font_size = 24)
