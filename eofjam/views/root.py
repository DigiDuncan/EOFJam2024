from arcade import Camera2D, Vec2
import arcade

from resources import load_LDtk

from eofjam.constants import BG_COLOR, DEBUG_COLOR, TEXT_COLOR
from eofjam.core.application import View
from eofjam.game.bar import EnergyBar, HealthBar
from eofjam.game.entity import Player
from eofjam.core.world import World
from eofjam.core.store import game


class RootView(View):

    def __init__(self):
        super().__init__()

        self.player = Player("player", Vec2(*self.window.center))
        self.camera = Camera2D()
        self.enemies = []

        self.world = World(self.player, self.camera, load_LDtk('world'))
        self.world.load_world()
        self.world.draw_bounds = False

        # Temp call here
        self.world.load_level('Level_0')

        self.health_bar = HealthBar(self.window.rect.top_right - Vec2(5, 5))
        self.energy_bar = EnergyBar(self.window.rect.top_right - Vec2(5, 30))


        # Temp Debug
        self.test_path = []

    def on_update(self, delta_time: float) -> None:
        self.world.update(delta_time)
        self.health_bar.percentage = (self.player.health / self.player.max_health)
        self.energy_bar.percentage = (self.player.energy / 2)

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
            case arcade.key.LSHIFT:
                self.player.sprinting = True
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
            case arcade.key.B:
                self.world.draw_bounds = not self.world.draw_bounds
            case arcade.key.E:
                self.player.energy = 2.0

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
            case arcade.key.LSHIFT:
                self.player.sprinting = False
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

            if self.test_path:
                s = self.world.navigation.pixel_width 
                hs = s / 2.0
                arcade.draw_line_strip([(n.location[0] * s + hs, n.location[1] * s + hs) for n in self.test_path], arcade.color.AFRICAN_VIOLET, 5)

        self.health_bar.draw()
        self.energy_bar.draw()
        arcade.draw_text(f"{self.player.scale}x", 0, self.window.height, anchor_y = "top",
                         color = DEBUG_COLOR if game.run.unlimited_scale else TEXT_COLOR, multiline = True, width = 400,
                         font_name = "CMU Serif", font_size = 24)
        
       

    def on_mouse_motion(self, x, y, dx, dy):
        px, py, _ = self.camera.unproject((x, y))
        if self.world.bounds.point_in_rect((px, py)):
            self.test_path = self.world.navigation.get_path(self.player.position, (px, py))
            print(self.test_path)

        
