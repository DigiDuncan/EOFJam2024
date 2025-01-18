from __future__ import annotations
from typing import Protocol
from enum import Enum, auto

from arcade import Rect, Vec2, draw_rect_outline, draw_circle_outline
from arcade.color import RED, GREEN
import arcade


class ColliderShape(Enum):
    CIRCLE = auto()
    CIRCLE_INVERTED = auto()
    RECT = auto()
    RECT_INVERTED = auto()
    POLYGON = auto() # Not Implimented
    POLYGON_INVERTED = auto() # Not Implimented

class Collider(Protocol):
    position: Vec2
    shape: ColliderShape

    def contains(self, point: Vec2) -> bool:
        ...

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
        self.shape = ColliderShape.CIRCLE

    def contains(self, point: Vec2):
        return (self.position - point).length_squared() <= self.radius**2

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
        
class InverseCircleCollider(Collider):
    
    def __init__(self, position: Vec2, radius: float):
        self.position = position
        self.radius = radius
        self.shape = ColliderShape.CIRCLE_INVERTED

    def contains(self, point: Vec2):
        return (self.position - point).length_squared() >= self.radius**2
    
    def draw(self):
        draw_circle_outline(self.position.x, self.position.y, self.radius, GREEN)

    # TODO

class RectCollider(Collider):

    def __init__(self, rect: Rect):
        self.rect: Rect = rect

    def contains(self, point):
        return self.rect.point_in_rect(point)

    @property
    def position(self):
        return self.rect.center

    @position.setter
    def position(self, position: Vec2):
        self.rect = self.rect.align_center(position)

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
    
    @position.setter
    def position(self, position: Vec2):
        self.rect = self.rect.align_center(position)

    def contains(self, point):
        return not self.rect.point_in_rect(point)

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

# collision functions return the collision normal and the intersection depth
# norm is experienced by a (b -> a)
# The depth is eqivalent for both

def collide_circles(a: CircleCollider, b: CircleCollider) -> tuple[Vec2, float]:
    diff = a.position - b.position
    norm = diff.normalize()
    return norm, diff.length() - a.radius - b.radius

def collide_circle_inverse(a: CircleCollider, b: InverseCircleCollider) -> tuple[Vec2, float]:
    diff = b.position - a.position
    norm = diff.normalize()
    return norm, b.radius - diff.length() - a.radius

def collide_circle_rect(a: CircleCollider, b: RectCollider) -> tuple[Vec2, float]:
    pass

def collide_circle_rect_inverse(a: CircleCollider, b: RectCollider) -> tuple[Vec2, float]:
    pass

def collide_circles_inverted(a: InverseCircleCollider, b: CircleCollider) -> tuple[Vec2, float]:
    # There is no way for these to not intersect lmao
    diff = b.position - a.position
    norm = diff.normalize()
    return -norm, -abs(diff.length() - a.radius - b.radius)

def collide_circle_inverse_rect(a: InverseCircleCollider, b: RectCollider) -> tuple[Vec2, float]:
    pass

def collide_circle_rect_inverted(a: InverseCircleCollider, b: InverseRectCollider) -> tuple[Vec2, float]:
    pass

def collide_rects(a: RectCollider, b: RectCollider) -> tuple[Vec2, float]:
    tb = b.rect.bottom - a.rect.top
    bt = b.rect.top - a.rect.bottom
    lr = b.rect.right - a.rect.left
    rl = b.rect.left - a.rect.right

    edge = max(tb, bt, lr, rl)

    if edge == tb: # top collision
        return Vec2(0.0, 1.0), tb
    elif edge == bt: # bottom collision
        return Vec2(0.0, -1.0), bt
    elif edge == lr: # left collision
        return Vec2(1.0, 0.0), lr
    elif edge == rl: # right collision
        return Vec2(-1.0, 0.0), rl

def collide_rect_inverse(a: RectCollider, b: InverseRectCollider) -> tuple[Vec2, float]:
    pass

def collide_rects_inverted(a: InverseRectCollider, b: InverseRectCollider) -> tuple[Vec2, float]:
    pass


def collide(a: Collider, b: Collider) -> tuple[Vec2, float]:
    # I see why maybe this isn't the best way to do this -.-
    match (a.shape, b.shape):
        case (ColliderShape.CIRCLE, ColliderShape.CIRCLE):
            return collide_circles(a, b)
        case (ColliderShape.CIRCLE, ColliderShape.CIRCLE_INVERTED):
            return collide_circle_inverse(a, b)
        case (ColliderShape.CIRCLE, ColliderShape.RECT):
            return collide_circle_rect(a, b)
        case (ColliderShape.CIRCLE, ColliderShape.RECT_INVERTED):
            return collide_circle_rect_inverse(a, b)
        case (ColliderShape.CIRCLE_INVERTED, ColliderShape.CIRCLE):
            n, d = collide_circle_inverse(b, a)
            return -n, d
        case (ColliderShape.CIRCLE_INVERTED, ColliderShape.CIRCLE_INVERTED):
            return collide_circles_inverted(a, b)
        case (ColliderShape.CIRCLE_INVERTED, ColliderShape.RECT):
            return collide_circle_inverse_rect(a, b)
        case (ColliderShape.CIRCLE_INVERTED, ColliderShape.RECT_INVERTED):
            return collide_circle_rect_inverted(a, b)
        case (ColliderShape.RECT, ColliderShape.CIRCLE):
            n, d = collide_circle_rect(b, a)
            return -n, d
        case (ColliderShape.RECT, ColliderShape.CIRCLE_INVERTED):
            n, d = collide_circle_inverse_rect(b, a)
            return -n, d
        case (ColliderShape.RECT, ColliderShape.RECT):
            return collide_rects(a, b)
        case (ColliderShape.RECT, ColliderShape.RECT_INVERTED):
            return collide_rect_inverse(a, b)
        case (ColliderShape.RECT_INVERTED, ColliderShape.CIRCLE):
            n, d = collide_circle_inverse_rect(b, a)
            return -n, d
        case (ColliderShape.RECT_INVERTED, ColliderShape.CIRCLE_INVERTED):
            n, d = collide_circle_rect_inverted(b, a)
            return -n, d
        case (ColliderShape.RECT_INVERTED, ColliderShape.RECT):
            n, d = collide_rect_inverse(b, a)
            return -n, d
        case (ColliderShape.RECT_INVERTED, ColliderShape.RECT_INVERTED):
            return collide_rects_inverted(a, b)
        case _:
            raise ValueError(f'{a} or {b} are of unknown/unimplemented shapes')
