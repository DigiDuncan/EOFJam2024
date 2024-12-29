from __future__ import annotations
from typing import Protocol

from arcade import Rect, Vec2, draw_rect_outline
import arcade

class Collider(Protocol):
    def overlaps(self, other: Collider) -> bool:
        ...

    def collide(self, other: Collider, new_point: Vec2) -> Vec2:
        ...

    def draw(self) -> None:
        ...

class RectCollider:
    def __init__(self, rect: Rect):
        self.rect = rect

    def overlaps(self, other: RectCollider) -> bool:
        return self.rect.overlaps(other.rect)

    def collide(self, other: RectCollider, new_point: Vec2) -> Vec2:
        moved_hitbox = self.rect.at_position(new_point)
        if other.rect.overlaps(moved_hitbox):
            # Try just moving the X
            moved_x_hitbox = self.rect.align_x(new_point.x)
            if other.rect.overlaps(moved_x_hitbox):
                # Try just moving the Y?
                moved_y_hitbox = self.rect.align_y(new_point.y)
                if other.rect.overlaps(moved_y_hitbox):
                    # Give up
                    return self.center
                return moved_y_hitbox.center
            return moved_x_hitbox.center
        return new_point

    def draw(self) -> None:
        draw_rect_outline(self, arcade.color.RED)

class CircleCollider:
    def __init__(self, position: Vec2, radius: float):
        self.position = position
        self.radius = radius

    def overlaps(self, other: CircleCollider) -> bool:
        return (self.position - other.position).length() - (other.radius + self.radius) <= 0.0

    def collide(self, other: CircleCollider, new_point: Vec2) -> Vec2:
        diff = new_point - other.position
        length = diff.length()
        seperation = length - (other.radius + self.radius)

        if seperation > 0.0:
            return new_point
        direction = diff / length
        offset = max(seperation, self.radius + other.radius)

        return other.position + direction * offset

    def draw(self) -> None:
        arcade.draw_circle_outline(*self.position, radius = self.radius, color = arcade.color.RED)
