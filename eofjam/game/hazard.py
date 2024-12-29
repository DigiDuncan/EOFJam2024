import arcade
from arcade import Rect, draw_rect_filled, draw_text

from eofjam.lib.collider import RectCollider


class Hazard:
    def __init__(self, rect: Rect, min_scale: float | None = None, max_scale: float | None = None):
        self.rect = rect
        self.min_scale = min_scale
        self.max_scale = max_scale

    @property
    def hitbox(self) -> RectCollider:
        return RectCollider(self.rect)

    def draw(self) -> None:
        if self.min_scale is not None and self.max_scale is not None:
            draw_rect_filled(self.rect, arcade.color.BROWN.replace(a = 64))
            draw_text(f"{self.min_scale}x-{self.max_scale}x", self.rect.left + 5, self.rect.top + 5, arcade.color.BLACK, anchor_y = "top")
        elif self.min_scale is not None:
            draw_rect_filled(self.rect, arcade.color.MAGENTA.replace(a = 64))
            draw_text(f"{self.min_scale}x", self.rect.left + 5, self.rect.top + 5, arcade.color.BLACK, anchor_y = "top")
        elif self.max_scale is not None:
            draw_rect_filled(self.rect, arcade.color.YELLOW.replace(a = 64))
            draw_text(f"{self.max_scale}x", self.rect.left + 5, self.rect.top + 5, arcade.color.BLACK, anchor_y = "top")
