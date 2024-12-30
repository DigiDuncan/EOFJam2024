from arcade import Sprite, SpriteList, Vec2
from resources import load_png


class Bar:
    def __init__(self, position: Vec2, middle: str = None, *, back: str = None, front: str = None):
        self._position = position
        self.back_tex = load_png(back) if back is not None else None
        self.middle_tex = load_png(middle)
        self.front_tex = load_png(front) if front is not None else None

        self.spritelist = SpriteList[Sprite](capacity = 3)
        if self.back_tex:
            self.back_sprite = Sprite(self.back_tex)
            self.spritelist.append(self.back_sprite)
        self.middle_sprite = Sprite(self.middle_tex)
        self.spritelist.append(self.middle_sprite)
        if self.front_tex:
            self.front_sprite = Sprite(self.front_tex)
            self.spritelist.append(self.front_sprite)

        self._percentage = 1.0

    @property
    def position(self) -> Vec2:
        return self._position

    @position.setter
    def position(self, v: Vec2) -> None:
        self._position = v
        for s in self.spritelist:
            s.position = v

    @property
    def percentage(self) -> float:
        return self._percentage

    @percentage.setter
    def percentage(self, v: float) -> None:
        self._percentage = v

    def draw(self) -> None:
        self.spritelist.draw()


class HealthBar(Bar):
    def __init__(self, position: Vec2):
        super().__init__(position, "health", front = "bar")

class EnergyBar(Bar):
    def __init__(self, position: Vec2):
        super().__init__(position, "energy", front = "bar")
