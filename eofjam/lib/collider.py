from __future__ import annotations

from arcade import Vec2
import arcade

class Collider:

    def __init__(self, position: Vec2, radius: float):
        self.position = position
        self.radius = radius

    def overlaps(self, other: Collider) -> bool:
        return (self.position - other.position).length() - (other.radius + self.radius) <= 0.0

    def collide(self, other: Collider, new_point: Vec2) -> Vec2:
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
