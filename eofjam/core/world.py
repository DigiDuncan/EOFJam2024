from arcade import Camera2D
from .entity import Player

class World:
    def __init__(self, player: Player, camera: Camera2D):
        self.player: Player = player
        self.camera: Camera2D = camera

    def update(self) -> None:
        self.camera.zoom = 1 / (self.player.scale * 4)
