import arcade
from arcade import Rect, draw_rect_filled, draw_text

from eofjam.constants import HAZARD_MIN_SCALE_COLOR, HAZARD_MAX_SCALE_COLOR, HAZARD_BOTH_COLOR, GRILL_COLOR, CHARGER_COLOR, TEXT_COLOR
from eofjam.game.entity import Entity, Player
from eofjam.lib.collider import RectCollider
from eofjam.lib.utils import smerp


class Hazard:
    def __init__(self, rect: Rect, min_scale: float | None = None, max_scale: float | None = None):
        self.rect = rect
        self.min_scale = min_scale
        self.max_scale = max_scale

    @property
    def hitbox(self) -> RectCollider:
        return RectCollider(self.rect)

    def passable(self, scale: float) -> bool:
        if self.min_scale is not None and scale < self.min_scale:
            return False
        if self.max_scale is not None and scale > self.max_scale:
            return False
        return True

    def interact(self, other: Entity) -> None:
        # This is a stub.
        ...

    def draw(self) -> None:
        if self.min_scale is not None and self.max_scale is not None:
            draw_rect_filled(self.rect, HAZARD_BOTH_COLOR)
            draw_text(f"{self.min_scale}x-{self.max_scale}x", self.rect.left + 5, self.rect.top + 5, TEXT_COLOR, anchor_y = "top", font_size = 24, font_name = "CMUNRM")
        elif self.min_scale is not None:
            draw_rect_filled(self.rect, HAZARD_MIN_SCALE_COLOR)
            draw_text(f"{self.min_scale}x", self.rect.left + 5, self.rect.top + 5, TEXT_COLOR, anchor_y = "top", font_size = 24, font_name = "CMUNRM")
        elif self.max_scale is not None:
            draw_rect_filled(self.rect, HAZARD_MAX_SCALE_COLOR)
            draw_text(f"{self.max_scale}x", self.rect.left + 5, self.rect.top + 5, TEXT_COLOR, anchor_y = "top", font_size = 24, font_name = "CMUNRM")

class Grill(Hazard):
    def __init__(self, rect: Rect):
        # Grills don't care about mix/max size.
        super().__init__(rect)

    def interact(self, other: Entity) -> None:
        clock = arcade.clock.GLOBAL_CLOCK
        if isinstance(other, Player):
            other.scale_energy = smerp(other.scale_energy, 0.0, 10, clock.delta_time)

    def draw(self) -> None:
        draw_rect_filled(self.rect, GRILL_COLOR)

class Charger(Hazard):
    def __init__(self, rect: Rect,charge_to: float = 2.0, charge_speed: float = 10):
        # Chargers don't care about mix/max size.
        super().__init__(rect)
        self.charge_to = charge_to
        self.charge_speed = charge_speed  # ?: Dragon, help, how the f*** does this number work

    def interact(self, other: Entity) -> None:
        clock = arcade.clock.GLOBAL_CLOCK
        if isinstance(other, Player):
            other.scale_energy = smerp(other.scale_energy, max(self.charge_to, other.scale_energy), self.charge_speed, clock.delta_time)

    def draw(self) -> None:
        draw_rect_filled(self.rect, CHARGER_COLOR)
        draw_text(f"{self.charge_to}E", self.rect.left + 5, self.rect.top + 5, TEXT_COLOR, anchor_y = "top", font_size = 24, font_name = "CMUNRM")
