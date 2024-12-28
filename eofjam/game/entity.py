import arcade
from arcade import Sprite, SpriteCircle, Vec2

from eofjam.lib.collider import Collider

class Entity:
    def __init__(self, position: Vec2, sprite: Sprite, rotation: float = 0.0, scale: float = 1.0):
        self._position: Vec2 = position
        self._rotation: float = rotation
        self.sprite: Sprite = sprite
        self._scale: float = scale

        self.position = position
        self.rotation = rotation
        self.scale = scale

        self.health: int = 1
        self.strength: float = 1
        self.defense: float = 1
        self.speed: float = 400
        self.bullet_speed: float = 500

    @property
    def hitbox(self) -> Collider:
        return Collider(self.position, self.sprite.width / 2)

    @property
    def position(self) -> Vec2:
        return self._position

    @position.setter
    def position(self, v: Vec2) -> None:
        self.sprite.position = v
        self._position = v

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, v: float) -> None:
        self.sprite.rotation = v
        self._rotation = v

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, v: float) -> None:
        self.sprite.scale = round(v / 4, 3)
        self._scale = round(v, 3)

    def draw(self) -> None:
        arcade.draw_sprite(self.sprite)

class Enemy(Entity):
    def __init__(self, position: Vec2, rotation: float = 0.0, scale: float = 1.0):
        sprite = SpriteCircle(512, arcade.color.CHARM_PINK)
        super().__init__(position, sprite, rotation, scale)

class Player(Entity):
    def __init__(self, position: Vec2, rotation: float = 0.0, scale: float = 1.0):
        sprite = SpriteCircle(128, arcade.color.CHARM_GREEN)
        super().__init__(position, sprite, rotation, scale)

        self.up = False
        self.down = False
        self.left = False
        self.right = False

        self.fire_up = False
        self.fire_down = False
        self.fire_left = False
        self.fire_right = False

        self.scaling_up = False
        self.scaling_down = False

        self.scale_energy = 2.0
        self.scale_speed = 1.0

        self.fire_rate = 0.25

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, v: float) -> None:
        self.sprite.scale = v
        self._scale = v

    def update(self, delta_time: float) -> None:
        if self.up:
            self.position = self.position + Vec2(0, self.speed * delta_time)
        if self.down:
            self.position = self.position + Vec2(0, -self.speed * delta_time)
        if self.left:
            self.position = self.position + Vec2(-self.speed * delta_time, 0)
        if self.right:
            self.position = self.position + Vec2(self.speed * delta_time, 0)
