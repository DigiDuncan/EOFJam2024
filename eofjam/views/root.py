import random
from arcade import Camera2D, SpriteList
import arcade
from eofjam.core.application import View
from eofjam.core.entity import Enemy, Player
from eofjam.core.world import World


class RootView(View):

    def __init__(self):
        super().__init__()

        self.player = Player(self.window.center)
        self.camera = Camera2D()
        self.world = World(self.player, self.camera)

        self.enemy_spritelist = SpriteList()
        self.enemies = []
        for i in range(10):
            p = (self.window.rect * 2).uv_to_position((random.random(), random.random()))
            e = Enemy(p)
            self.enemies.append(e)
            self.enemy_spritelist.append(e.sprite)

    def on_update(self, delta_time: float) -> None:
        self.player.update(delta_time)
        self.world.update()

    def on_key_press(self, symbol, modifiers) -> None:
        match symbol:
            case arcade.key.NUM_ADD:
                self.player.scale += 0.025
            case arcade.key.NUM_SUBTRACT:
                self.player.scale -= 0.025
            case arcade.key.W:
                self.player.up = True
            case arcade.key.A:
                self.player.left = True
            case arcade.key.S:
                self.player.down = True
            case arcade.key.D:
                self.player.right = True

    def on_key_release(self, symbol, modifiers) -> None:
        match symbol:
            case arcade.key.W:
                self.player.up = False
            case arcade.key.A:
                self.player.left = False
            case arcade.key.S:
                self.player.down = False
            case arcade.key.D:
                self.player.right = False

    def on_draw(self) -> None:
        self.clear()
        with self.camera.activate():
            self.enemy_spritelist.draw()
            self.player.draw()
        arcade.draw_text(f"{self.player.scale}x", 0, self.window.height, anchor_y = "top")
