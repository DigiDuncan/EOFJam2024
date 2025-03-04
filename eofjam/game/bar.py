from arcade import Sprite, SpriteList, Vec2, Texture, get_window
from resources import load_png


class Bar:
    def __init__(self, position: Vec2, middle: str = None, *, back: str = None, front: str = None):
        self._position = position
        self.back_tex = load_png(back) if back is not None else None
        self.middle_tex = load_png(middle)
        self.middle_tex_crop = Texture.create_empty(f'{self.middle_tex.atlas_name}_cropped', self.middle_tex.size)
        self.front_tex = load_png(front) if front is not None else None

        print(self.middle_tex.atlas_name, self.middle_tex_crop.atlas_name)

        self.atlas = get_window().ctx.default_atlas

        self.atlas.add(self.middle_tex)
        self.atlas.add(self.middle_tex_crop)

        self.spritelist = SpriteList[Sprite](capacity = 3)
        if self.back_tex:
            self.back_sprite = Sprite(self.back_tex)
            self.spritelist.append(self.back_sprite)
        self.middle_sprite = Sprite(self.middle_tex_crop)
        self.spritelist.append(self.middle_sprite)
        if self.front_tex:
            self.front_sprite = Sprite(self.front_tex)
            self.spritelist.append(self.front_sprite)

        self.position = position

        self._percentage = 1.0

    @property
    def position(self) -> Vec2:
        return self._position

    @position.setter
    def position(self, v: Vec2) -> None:
        self._position = v
        self._position -= Vec2(*self.middle_tex.size) / 2
        for s in self.spritelist:
            s.position = self._position

    @property
    def percentage(self) -> float:
        return self._percentage

    @percentage.setter
    def percentage(self, v: float) -> None:
        self._percentage = v

    def pp(self):
        self.atlas.save('asdjkhas.png', draw_borders=True)

    def draw(self) -> None:
        self.middle_region = self.atlas.get_texture_region_info(self.middle_tex.atlas_name)
        self.crop_region = self.atlas.get_texture_region_info(self.middle_tex_crop.atlas_name)

        self.crop_region.y = self.middle_region.y
        self.crop_region.height = self.middle_region.height
        self.crop_region.width = self.percentage * self.middle_region.width
        self.crop_region.x = self.middle_region.x + self.middle_region.width - self.crop_region.width

        ux, uy, uw, uh = self.crop_region.x / self.atlas.width, self.crop_region.y / self.atlas.height, self.crop_region.width / self.atlas.width, self.crop_region.height / self.atlas.height
        self.crop_region.texture_coordinates = (ux, uy, ux + uw, uy, ux, uy + uh, ux + uw, uy + uh)

        slot = self.atlas._texture_uvs.get_existing_or_free_slot(self.middle_tex_crop.atlas_name)
        self.atlas._texture_uvs.set_slot_data(slot, self.crop_region.texture_coordinates)

        self.middle_sprite.width = self.crop_region.width
        self.middle_sprite.right = self.position.x + self.middle_tex.width / 2.0

        self.spritelist.draw()


class HealthBar(Bar):
    def __init__(self, position: Vec2):
        super().__init__(position, "health", front = "bar")

class EnergyBar(Bar):
    def __init__(self, position: Vec2):
        super().__init__(position, "energy", front = "bar")
