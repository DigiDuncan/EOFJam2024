import arcade.clock
from eofjam.core.application import View
from eofjam.lib.collider import CircleCollider, InverseCircleCollider, collide, Collider

import arcade

GRAVITY = 981
BIAS = 0.05
SLOP = 2
DRAG = 0.0005

class Body:

    def __init__(self, shape: Collider, mass: float, velocity: arcade.Vec2):
        self.shape = shape
        self.mass = mass
        self.inv = 0.0 if mass == 0.0 else 1.0 / mass
        self.velocity = velocity

    def __hash__(self):
        return hash(id(self))
    
    def __eq__(self, value):
        return id(self) == id(value)
    
class Collision:

    def __init__(self, a: Body, b: Body):
        self.a = a
        self.b = b

        self.impulse: float = 0
        self.normal: arcade.Vec2 = arcade.Vec2()

        self.persistent = False

    def compute_impulse(self):
        n, d = collide(self.a.shape, self.b.shape)
        effective_mass = 0.0 if (self.a.inv + self.b.inv) == 0.0 else 1.0 / (self.a.inv + self.b.inv)
        self.normal = n
        return effective_mass * (n.dot(self.b.velocity - self.a.velocity) - BIAS * (d - SLOP) / arcade.clock.GLOBAL_CLOCK.delta_time)

    def apply_impulse(self, impulse: arcade.Vec2):
        self.a.velocity = self.a.velocity + self.a.inv * impulse
        self.b.velocity = self.b.velocity - self.b.inv * impulse

class CollisionView(View):

    def __init__(self) -> None:
        super().__init__()
        self.bounds = Body(InverseCircleCollider(arcade.Vec2(self.center_x, self.center_y), self.height / 2.0 - 20), 0.0, arcade.Vec2())
        self.bodies = [
            self.bounds,
            Body(CircleCollider(arcade.Vec2(self.center_x - 100, self.center_y), 30), 30.0, arcade.Vec2(300, 0)),
            Body(CircleCollider(arcade.Vec2(self.center_x + 100, self.center_y), 30), 30.0, arcade.Vec2(-300, 0))
        ]
        self.collisions: dict[tuple[Body, Body], Collision] = {}

        self.iterations = 10

        self.grabbed = None
        self.g_mass = 0.0

    def on_draw(self) -> None:
        self.clear()
        for body in self.bodies:
            body.shape.draw()

    def collision(self, a: Body, b: Body):
        n, d = collide(a.shape, b.shape)

        if 0 < d:
            if (a, b) in self.collisions:
                self.collisions.pop((a, b))
            elif (b, a) in self.collisions:
                self.collisions.pop((b, a))
            return
        
        if (a, b) in self.collisions:
            collision = self.collisions[(a, b)]
            collision.persistent = True
        elif (b, a) in self.collisions:
            collision = self.collisions[(b, a)]
            collision.persistent = True
        else:
            collision = Collision(a, b)
            self.collisions[(a, b)] = collision

        old_impulse = collision.impulse
        delta = collision.compute_impulse()
        collision.impulse += delta
        collision.impulse = max(0, collision.impulse)
        delta = collision.impulse - old_impulse
        collision.apply_impulse(delta * n)

    def on_update(self, delta_time):
        g = arcade.Vec2(0.0, -GRAVITY * delta_time)
        for body in self.bodies:
            if body.inv <= 0.0:
                continue
            body.velocity = body.velocity + g
            body.velocity = body.velocity - body.velocity * body.velocity.length() * DRAG * delta_time

        # warm starts
        for collision in self.collisions.values():
            collision.apply_impulse(collision.impulse * collision.normal)

        for i in range(self.iterations):
            for idx, body in enumerate(self.bodies):
                for other in self.bodies[idx:]:
                    if body == other:
                        continue
                    self.collision(body, other)
        
        if self.grabbed is not None:
            self.grabbed.velocity = arcade.Vec2()
        
        for body in self.bodies:
            body.shape.position = body.shape.position + body.velocity * delta_time

    def on_key_press(self, symbol, modifiers):
        self.bodies.append(Body(CircleCollider(arcade.Vec2(self.center_x, self.center_y), 30), 30, arcade.Vec2.from_heading(1.62, 300.0)))

    def on_mouse_press(self, x, y, button, modifiers):
        if self.grabbed is not None:
            return
        
        p = arcade.Vec2(x, y)
        for obj in self.bodies[1:]:
            if obj.shape.contains(p):
                self.grabbed = obj
                self.g_mass = obj.mass
                obj.mass = 0.0
                obj.inv = 0.0
    
    def on_mouse_release(self, x, y, button, modifiers):
        if self.grabbed is not None:
            self.grabbed.mass = self.g_mass
            self.grabbed.inv = 0.0 if self.g_mass == 0.0 else 1.0 / self.g_mass
            self.grabbed = None

    def on_mouse_drag(self, x, y, dx, dy, _buttons, _modifiers):
        if self.grabbed is None:
            return
        self.grabbed.shape.position = arcade.Vec2(x, y)
        self.grabbed.velocity = arcade.Vec2(dx, dy) / self.window.delta_time