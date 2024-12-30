import random
from arcade import XYWH, Camera2D, Vec2
import arcade

from eofjam.constants import BG_COLOR, DEBUG_COLOR, TEXT_COLOR
from eofjam.core.application import View
from eofjam.game.entity import BulletSpawner, Enemy, Player
from eofjam.core.world import World
from eofjam.core.store import game
from eofjam.game.hazard import Charger, Grill, Hazard


class RootView(View):

    def __init__(self):
        super().__init__()

        self.player = Player(Vec2(*self.window.center))
        self.camera = Camera2D()
        self.enemies = []

        self.world = World(self.player, self.camera, self.enemies)

        for _ in range(50):
            p = (self.world.bounds).uv_to_position((random.random(), random.random()))
            e = Enemy(p)
            self.enemies.append(e)

        r = XYWH(self.window.center_x, 2000, 800, 400)
        self.world.hazards.append(Hazard(r, max_scale = 1.0))

        gr = XYWH(self.window.center_x + 2000, 2000, 800, 400)
        self.world.hazards.append(Grill(gr))

        cr = XYWH(self.window.center_x + 4000, 2000, 800, 400)
        self.world.hazards.append(Charger(cr))

        spawner = BulletSpawner(self.world.bullets, Vec2(self.window.center_x + 3000, 2000), speed = 90)
        self.enemies.append(spawner)

        self.world.enemies = self.enemies
        self.world.refresh_enemies()
        self.world.scale = 1
        self.world.draw_bounds = True

    def on_update(self, delta_time: float) -> None:
        self.world.update(delta_time)

    def on_key_press(self, symbol, modifiers) -> None:  # noqa: ANN001
        match symbol:
            case arcade.key.NUM_ADD:
                self.player.scaling_up = True
            case arcade.key.NUM_SUBTRACT:
                self.player.scaling_down = True
            case arcade.key.W:
                self.player.up = True
            case arcade.key.A:
                self.player.left = True
            case arcade.key.S:
                self.player.down = True
            case arcade.key.D:
                self.player.right = True
            case arcade.key.NUM_8:
                self.player.fire_up = True
            case arcade.key.NUM_5:
                self.player.fire_down = True
            case arcade.key.NUM_4:
                self.player.fire_left = True
            case arcade.key.NUM_6:
                self.player.fire_right = True
            case arcade.key.NUM_1:
                self.world.scale = 1
            case arcade.key.NUM_MULTIPLY:
                game.run.unlimited_scale = not game.run.unlimited_scale
            case arcade.key.NUM_DIVIDE:
                self.world.draw_bounds = not self.world.draw_bounds
            case arcade.key.NUM_DECIMAL:
                self.player.scale_energy = 2.0

    def on_key_release(self, symbol, modifiers) -> None:  # noqa: ANN001
        match symbol:
            case arcade.key.NUM_ADD:
                self.player.scaling_up = False
            case arcade.key.NUM_SUBTRACT:
                self.player.scaling_down = False
            case arcade.key.W:
                self.player.up = False
            case arcade.key.A:
                self.player.left = False
            case arcade.key.S:
                self.player.down = False
            case arcade.key.D:
                self.player.right = False
            case arcade.key.NUM_8:
                self.player.fire_up = False
            case arcade.key.NUM_5:
                self.player.fire_down = False
            case arcade.key.NUM_4:
                self.player.fire_left = False
            case arcade.key.NUM_6:
                self.player.fire_right = False

    def on_draw(self) -> None:
        self.clear(BG_COLOR)
        with self.camera.activate():
            self.world.draw()
        arcade.draw_text(f"{self.player.scale}x\nEnergy: {self.player.scale_energy:.3f}", 0, self.window.height, anchor_y = "top",
                         color = DEBUG_COLOR if game.run.unlimited_scale else TEXT_COLOR, multiline = True, width = 400,
                         font_name = "CMUNRM", font_size = 24)
