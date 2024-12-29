from __future__ import annotations
from typing import Protocol

from arcade import Rect, Vec2, draw_rect_outline, draw_circle_outline
from arcade.color import RED, GREEN
import arcade


class Collider(Protocol):
    position: Vec2

    def overlaps(self, other: Collider) -> bool:
        ...

    def collide(self, other: Collider) -> tuple[float, Vec2]:
        ...

    def distance(self, point: Vec2) -> float:
        ...

    def direction(self, point: Vec2) -> float:
        ...

    def draw(self) -> None:
        ...

class CircleCollider(Collider):

    def __init__(self, position: Vec2, radius: float):
        self.position = position
        self.radius = radius

    def overlaps(self, other: Collider) -> bool:
        return other.distance(self.position) - self.radius <= 0.0

    def collide(self, other: Collider) -> tuple[float, Vec2]:
        direction = other.direction(self.position)
        overlap = other.distance(self.position) - self.radius
        
        return overlap, direction

    def distance(self, point: Vec2) -> float:
        return (point - self.position).length() - self.radius

    def direction(self, point: Vec2) -> float:
        return (point - self.position).normalize()

    def draw(self):
        draw_circle_outline(self.position.x, self.position.y, self.radius, RED)


class RectCollider(Collider):

    def __init__(self, rect: Rect):
        self.rect: Rect = rect

    @property
    def position(self):
        return self.rect.center

    def overlaps(self, other: Collider):
        diff = (self.position - other.position).length()
        return self.distance(other.position) + other.distance(self.position) - diff <= 0.0
    
    def collide(self, other: Collider) -> tuple[float, Vec2]:
        normal = other.direction(self.position)
        diff = (self.position - other.position).length()
        return self.distance(other.position) + other.direction(self.position) - diff, normal


    def distance(self, point):
        x, y, w, h = self.rect.xywh
        diff = Vec2(point.x - x, point.y - y)

        dx = abs(diff.x) - w / 2.0
        dy = abs(diff.y) - h / 2.0

        return (max(dx, 0.0)**2 + max(dy, 0.0)**2)**0.5 + min(max(dx, dy), 0.0)

    def direction(self, point):
        x, y, w, h = self.rect.xywh
        diff = Vec2(point.x - x, point.y - y)

        ux = 2.0 * diff.x / w
        uy = 2.0 * diff.y / h

        if uy >= abs(ux):
            # Collides upward
            return Vec2(0.0, 1.0)
        elif uy <= -abs(ux):
            # Collides downward
            return Vec2(0.0, -1.0)
        elif ux >= abs(uy):
            # Collides rightward
            return Vec2(1.0, 0.0)
        elif ux <= -abs(uy):
            # Collides leftward
            return Vec2(-1.0, 0.0)
        else:
            return Vec2(0.0, 0.0)
    
    def draw(self):
        draw_rect_outline(self.rect, arcade.color.RED)


class InverseRectCollider(Collider):

    def __init__(self, rect: Rect):
        self.rect: Rect = rect

    @property
    def position(self):
        return self.rect.center

    def overlaps(self, other: Collider):
        diff = (self.position - other.position).length()
        return self.distance(other.position) + other.distance(self.position) - diff <= 0.0
    
    def collide(self, other: Collider) -> tuple[float, Vec2]:
        normal = other.direction(self.position)
        diff = (self.position - other.position).length()
        return self.distance(other.position) + other.direction(self.position) - diff, normal

    def distance(self, point):
        x, y, w, h = self.rect.xywh
        diff = Vec2(point.x - x, point.y - y)

        dx = abs(diff.x) - w / 2.0
        dy = abs(diff.y) - h / 2.0

        return -((max(dx, 0.0)**2 + max(dy, 0.0)**2)**0.5 + min(max(dx, dy), 0.0))

    def direction(self, point):
        x, y, w, h = self.rect.xywh
        diff = Vec2(point.x - x, point.y - y)

        ux = 2.0 * diff.x / w
        uy = 2.0 * diff.y / h

        if uy >= abs(ux):
            # Collides upward
            return Vec2(0.0, -1.0)
        elif uy <= -abs(ux):
            # Collides downward
            return Vec2(0.0, 1.0)
        elif ux >= abs(uy):
            # Collides rightward
            return Vec2(-1.0, 0.0)
        elif ux <= -abs(uy):
            # Collides leftward
            return Vec2(1.0, 0.0)
        else:
            return Vec2(0.0, 0.0)
    
    def draw(self):
        draw_rect_outline(self.rect, GREEN)