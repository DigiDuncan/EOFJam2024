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
        self.enemies = []

        self.world = World(self.player, self.camera, self.enemies)

        for _ in range(25):
            p = (self.world.bounds).uv_to_position((random.random(), random.random()))
            e = Enemy(p)
            self.enemies.append(e)

        self.world.enemies = self.enemies
        self.world.refresh_enemies()
        self.world.scale = 1

    def on_update(self, delta_time: float) -> None:
        self.world.update(delta_time)

    def on_key_press(self, symbol, modifiers) -> None:
        match symbol:
            case arcade.key.NUM_ADD:
                self.world.scale += 0.025
            case arcade.key.NUM_SUBTRACT:
                self.world.scale -= 0.025
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
            self.world.draw()
        arcade.draw_text(f"{self.player.scale}x", 0, self.window.height, anchor_y = "top")
