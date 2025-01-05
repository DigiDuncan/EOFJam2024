import arcade
import arcade.clock
from arcade import Rect, Sprite, draw_rect_filled, draw_rect_outline, draw_text
from arcade.future.background import Background

from eofjam.constants import HAZARD_MIN_SCALE_COLOR, HAZARD_MAX_SCALE_COLOR, HAZARD_BOTH_COLOR, CHARGER_COLOR, PICKUP_BOTH_COLOR, PICKUP_ENERGY_COLOR, PICKUP_HEALTH_COLOR, PICKUP_NONE_COLOR, TEXT_COLOR, HEALER_COLOR
from eofjam.game.entity import Entity, Player
from eofjam.lib.collider import RectCollider
from eofjam.lib.utils import smerp
from resources import get_png_path, load_png_sheet


class Hazard:
    def __init__(self, rect: Rect, min_scale: float | None = None, max_scale: float | None = None):
        self.rect = rect
        self.min_scale = min_scale
        self.max_scale = max_scale

        self.enabled = True

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
        if not self.enabled:
            return
        if self.min_scale is not None and self.max_scale is not None:
            draw_rect_filled(self.rect, HAZARD_BOTH_COLOR)
            draw_text(f"{self.min_scale}x-{self.max_scale}x", self.rect.left + 5, self.rect.top + 5, TEXT_COLOR, anchor_y = "top", font_size = 24, font_name = "CMU Serif")
        elif self.min_scale is not None:
            draw_rect_filled(self.rect, HAZARD_MIN_SCALE_COLOR)
            draw_text(f"{self.min_scale}x", self.rect.left + 5, self.rect.top + 5, TEXT_COLOR, anchor_y = "top", font_size = 24, font_name = "CMU Serif")
        elif self.max_scale is not None:
            draw_rect_filled(self.rect, HAZARD_MAX_SCALE_COLOR)
            draw_text(f"{self.max_scale}x", self.rect.left + 5, self.rect.top + 5, TEXT_COLOR, anchor_y = "top", font_size = 24, font_name = "CMU Serif")


# For the below hazards, their "speeds" are it's half-life in 1/x seconds.


class Grill(Hazard):
    def __init__(self, rect: Rect, speed: float = 10):
        # Grills don't care about mix/max size.
        super().__init__(rect)
        self.speed = speed
        self.background = Background.from_file(get_png_path("grill"), self.rect.bottom_left, self.rect.size)

    def interact(self, other: Entity) -> None:
        if not self.enabled:
            return
        clock = arcade.clock.GLOBAL_CLOCK
        if isinstance(other, Player):
            other.energy = smerp(other.energy, 0.0, self.speed, clock.delta_time)

    def draw(self) -> None:
        if not self.enabled:
            return
        self.background.texture.offset = (arcade.clock.GLOBAL_CLOCK.time * -100, 0)
        self.background.draw()

class Charger(Hazard):
    def __init__(self, rect: Rect,charge_to: float = 2.0, speed: float = 10):
        # Chargers don't care about mix/max size.
        super().__init__(rect)
        self.charge_to = charge_to
        self.speed = speed

    def interact(self, other: Entity) -> None:
        if not self.enabled:
            return
        clock = arcade.clock.GLOBAL_CLOCK
        if isinstance(other, Player):
            other.energy = smerp(other.energy, max(self.charge_to, other.energy), self.speed, clock.delta_time)

    def draw(self) -> None:
        if not self.enabled:
            return
        draw_rect_filled(self.rect, CHARGER_COLOR)
        draw_text(f"{self.charge_to}E", self.rect.left + 5, self.rect.top + 5, TEXT_COLOR, anchor_y = "top", font_size = 24, font_name = "CMU Serif")

class Laser(Hazard):
    def __init__(self, rect: Rect, speed: float = 10):
        # Lasers don't care about mix/max size.
        super().__init__(rect)
        self.speed = speed
        self.background = Background.from_file(get_png_path("laser"), self.rect.bottom_left, self.rect.size)

    def interact(self, other: Entity) -> None:
        if not self.enabled:
            return
        clock = arcade.clock.GLOBAL_CLOCK
        last_health = other.health
        other.health = smerp(other.health, 0.0, self.speed, clock.delta_time)
        if int(last_health / 10) != int(other.health / 10):
            other.last_damage_time = arcade.clock.GLOBAL_CLOCK.time

    def draw(self) -> None:
        if not self.enabled:
            return
        self.background.texture.offset = (arcade.clock.GLOBAL_CLOCK.time * -100, 0)
        self.background.draw()

class Healer(Hazard):
    def __init__(self, rect: Rect, charge_to: float, speed: float = 10):
        # Healers don't care about mix/max size.
        super().__init__(rect)
        self.charge_to = charge_to
        self.speed = speed

    def interact(self, other: Entity) -> None:
        if not self.enabled:
            return
        clock = arcade.clock.GLOBAL_CLOCK
        other.health = min(smerp(other.health, self.charge_to, self.speed, clock.delta_time), other.max_health)

    def draw(self) -> None:
        if not self.enabled:
            return
        draw_rect_filled(self.rect, HEALER_COLOR)
        draw_text(f"{self.charge_to}H", self.rect.left + 5, self.rect.top + 5, TEXT_COLOR, anchor_y = "top", font_size = 24, font_name = "CMU Serif")

class Pickup(Hazard):
    def __init__(self, rect: Rect, *, health: float = 0, energy: float = 0):
        # Pickups don't care about mix/max size.
        super().__init__(rect)

        self.health = health
        self.energy = energy

    def interact(self, other: Entity) -> None:
        if not self.enabled:
            return
        if isinstance(other, Player):
            other.health = min(other.max_health, other.health + self.health)
            other.energy = min(2, other.energy + self.energy)
            self.enabled = False

    def draw(self) -> None:
        if not self.enabled:
            return
        color = PICKUP_NONE_COLOR
        if self.health and self.energy:
            color = PICKUP_BOTH_COLOR
        elif self.health:
            color = PICKUP_HEALTH_COLOR
        elif self.energy:
            color = PICKUP_ENERGY_COLOR
        draw_rect_filled(self.rect, color)
        draw_rect_outline(self.rect, color.replace(a = 255), 3)
        draw_text(f"+{self.health}H\n+{self.energy}E", self.rect.left + 5, self.rect.top + 5, TEXT_COLOR, anchor_y = "top", font_size = 24, font_name = "CMU Serif", multiline = True, width = 128)

class Door(Hazard):
    def __init__(self, rect: Rect):
        # Pickups don't care about mix/max size.
        super().__init__(rect)
        self.open = False

        tex = load_png_sheet("textures").get_texture(1536, 0, 64, 64)
        self.sprite = Sprite(tex)
        self.sprite.position = self.rect.bottom_left

    def passable(self, scale: float) -> bool:
        return scale <= 1.0 and self.open

    def draw(self) -> None:
        return arcade.draw_sprite(self.sprite)

class Button(Hazard):
    def __init__(self, rect: Rect, target: Door):
        # Pickups don't care about mix/max size.
        super().__init__(rect)
        self.target = target

        tex = load_png_sheet("textures").get_texture(1536, 0, 64, 64)
        self.sprite = Sprite(tex)
        self.sprite.position = self.rect.bottom_left

        self.last_pushed = None

    def interact(self, other: Entity) -> None:
        time = arcade.clock.GLOBAL_CLOCK.time
        if self.last_pushed is None or self.last_pushed + 1 < time:
            self.target.open = not self.target.open
            self.last_pushed = time

    def passable(self, scale: float) -> bool:
        return scale <= 1.0 and self.open

    def draw(self) -> None:
        return arcade.draw_sprite(self.sprite)
