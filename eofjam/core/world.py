from __future__ import annotations

import math
from typing import Any
import arcade
from arcade import Camera2D, Rect, SpriteList, Vec2, get_window
from arcade.camera.grips import constrain_xy

from resources import LDtk, load_png_sheet
from pathlib import Path

from eofjam.game.bullet import BulletList
from eofjam.game.hazard import Button, Door, Exit, Grill, Hazard, Laser
from eofjam.lib.types import BASICALLY_ZERO
from eofjam.lib.utils import clamp, smerp
from eofjam.game.entity import BulletSpawner, Enemy, Entity, Player
from eofjam.core.store import game
from eofjam.lib.collider import Collider, InverseRectCollider, RectCollider

WORLD_SCALE_MIN = (math.log2(0.1) + 2) / 2
WORLD_SCALE_MAX = (math.log2(10) + 2) / 2

class TileSet:

    def __init__(self, data: LDtk.TilesetDefintion, atlas: arcade.texture_atlas.TextureAtlasBase = None):
        self.atlas = atlas or get_window().ctx.default_atlas
        self.data = data
        self.tiles: list[arcade.Texture] = []
        self.tile_data: dict[int, str] = {custom.tile_id: custom.data for custom in data.custom_data}

        # Assumed img is in `resources/images`
        set_name = Path(data.rel_path).stem
        self.sheet = load_png_sheet(set_name)

        for row in range(data.c_height):
            for col in range(data.c_width):
                x = data.padding + col * (data.tile_grid_size + data.spacing)
                y = data.padding + row * (data.tile_grid_size + data.spacing)
                tex = self.sheet.get_texture(x, y, data.tile_grid_size, data.tile_grid_size)
                self.tiles.append(tex)
                self.atlas.add(tex)

    @property
    def tile_size(self) -> int:
        return self.data.tile_grid_size

    def __getitem__(self, idx: int):
        return self.tiles[idx]

    def get_data(self, idx: int) -> str:
        return self.tile_data[idx]


class World:
    def __init__(self, player: Player, camera: Camera2D, data: LDtk.LDtkRoot):
        self.world_data: LDtk.LDtkRoot = data
        self.levels: dict[str, LDtk.Level] = {}
        self.tilesets: dict[str, TileSet] = {}
        self.player: Player = player
        self.camera: Camera2D = camera
        self.bounds: Rect = get_window().rect * 8

        self.terrain: list[Collider] = [InverseRectCollider(self.bounds)]
        self.tiles: SpriteList = None
        self.enemies: list[Enemy] = []
        self.hazards: list[Hazard] = []

        self.entity_spritelist = SpriteList()
        self.bullets: BulletList = BulletList(self)

        self._scale = 1
        self.target_scale = 1

        self.bullet_timer = 0.0

        self.draw_bounds = False

        self.current_level = None

    def get_entity_from_id(self, iid: str) -> Any:  # noqa: ANN401
        for e in self.entities + self.hazards:
            if hasattr(e, "uuid"):
                if e.uuid == iid:
                    return e
        return None

    def load_world(self) -> None:
        self.levels = {level.identifier: level for level in self.world_data.levels}
        for tileset in self.world_data.defs.tilesets:
            self.tilesets[tileset.uid] = TileSet(tileset)

        self.tiles = SpriteList(False, capacity=2048)

    def load_level(self, level_name: str) -> None:
        # Check if the level name even exists
        if level_name not in self.levels:
            print('Failed to load level, ignoring command!')
            return

        # Get the LDtk level data
        level = self.levels[level_name]
        # Extract the layers by name for easy access later.
        # If a level doesn't use a layer it won't show up so maybe do some checks
        layers = {layer.identifier: layer for layer in level.layer_instances}

        # Get the px bounds and add the inverse collider
        self.bounds = arcade.LBWH(0, 0, level.px_width*4, level.px_height*4)
        self.terrain = [InverseRectCollider(self.bounds)]

        # Reset hazards and enemies
        self.hazards = []
        self.enemies = []

        # Get every wall entity. Has a little check to make sure its only walls
        for wall in layers['Walls'].entity_instances:
            if wall.identifier != 'Wall':
                print(f'Entity {wall.identifier} on wrong layer!')
                continue
            self.terrain.append(RectCollider(arcade.LBWH(wall.px_x*4, (level.px_height - wall.px_y - wall.height)*4, wall.width*4, wall.height*4)))

        # Pass 1
        for entity in layers['Static'].entity_instances:
            fields = {}
            for f in entity.field_instances:
                fields[f.identifer] = f.value

            # Common stats
            pos = Vec2(entity.px_x, level.px_height - entity.px_y) * 4
            rect = arcade.LBWH(entity.px_x*4, (level.px_height - entity.px_y - entity.height)*4, entity.width*4, entity.height*4)
            scale = entity.width / 64

            match entity.identifier:
                case "Spawnpoint":
                    self.player.position = pos
                case "Exit":
                    self.hazards.append(Exit(pos, fields["level_name"]))
                case "Grill":
                    self.hazards.append(Grill(rect))
                case "Laser":
                    self.hazards.append(Laser(rect))
                case "Door":
                    print(entity.iid)
                    self.hazards.append(Door(rect, entity.iid))
                case "BulletSpawner":
                    self.enemies.append(BulletSpawner(self.bullets, pos, 0, scale, fields["speed"], fields["fire_rate"]))

        # Pass 2
        # We have to do this pass seperately because we need entities from Pass 1 to be referenced
        for entity in layers['Static'].entity_instances:
            fields = {}
            for f in entity.field_instances:
                fields[f.identifer] = f.value

            # Common stats
            pos = Vec2(entity.px_x, level.px_height - entity.px_y) * 4
            rect = arcade.LBWH(entity.px_x*4, (level.px_height - entity.px_y - entity.height)*4, entity.width*4, entity.height*4)
            scale = entity.width / 64

            match entity.identifier:
                case "Button":
                    target = fields["Target"].entity_iid
                    self.hazards.append(Button(rect, self.get_entity_from_id(target)))

        for entity in layers['Dynamic'].entity_instances:
            match entity.identifier:
            # Get every enemy
                case "Enemy":
                    self.enemies.append(Enemy(Vec2(entity.px_x, level.px_height - entity.px_y) * 4, 0, entity.width / 64))

        # Clear the tiles sprites and add new ones.
        # A layer can only use one tileset so we grab it then the LDtk tile_id gives us the texture.
        self.tiles.clear()
        tile_set = self.tilesets[layers['Tiles'].tileset_def_uid]
        tile_size = tile_set.tile_size * 4
        for tile in layers['Tiles'].grid_tiles:
            self.tiles.append(arcade.Sprite(tile_set[tile.tile_id], 4, tile.pos_x*4 + tile_size / 2, (level.px_height - tile.pos_y)*4 - tile_size / 2))

        # Update the entity spritelists
        self.refresh_sprites()
        self.scale = 1
        self.current_level = level_name

    @property
    def entities(self) -> list[Entity]:
        return [self.player, *self.enemies]

    def refresh_sprites(self) -> None:
        self.entity_spritelist.clear()
        for e in self.entities:
            self.entity_spritelist.append(e.sprite)
            self.entity_spritelist.append(e.flash_sprite)

    @property
    def scale(self) -> float:
        return self.target_scale

    @scale.setter
    def scale(self, v: float) -> None:
        if game.run.unlimited_scale:
            self.target_scale = round(clamp(WORLD_SCALE_MIN, v, WORLD_SCALE_MAX), 3)
        else:
            self.target_scale = round(clamp(0, v, 2), 3)

    def handle_scale(self) -> None:
        s = round(math.exp2(2 * self._scale - 2), 5)
        self.player.scale = s
        self.camera.zoom = 1 / clamp(1, s * 4, 16)

    def update(self, delta_time: float) -> None:
        # Handle player scaling
        if self.player.scaling_up and self.player.scaling_down:
            pass
        elif not game.run.unlimited_scale and self.scale >= 2 and self.player.scaling_up:
            # We have to do this here to avoid losing energy for no reason
            pass
        elif not game.run.unlimited_scale and self.scale <= 0 and self.player.scaling_down:
            # We have to do this here to avoid losing energy for no reason
            pass
        elif self.player.scaling_up:
            ds = self.player.scale_speed * delta_time
            if ds > self.player.energy:
                ds = self.player.energy
            self.scale += ds
            self.player.energy -= ds
        elif self.player.scaling_down:
            ds = self.player.scale_speed * delta_time
            if ds > self.player.energy:
                ds = self.player.energy
            self.scale -= ds
            self.player.energy -= ds

        # Handle world scaling
        self._scale = smerp(self._scale, self.target_scale, 10, delta_time)
        self.handle_scale()

        # Bullets
        self.bullet_timer += delta_time
        if self.bullet_timer >= self.player.fire_rate * self.player.scale and (self.player.fire_up or self.player.fire_down or self.player.fire_left or self.player.fire_right):
            v = Vec2(0, 0)
            if self.player.fire_up:
                v += Vec2(0, 1)
            if self.player.fire_down:
                v += Vec2(0, -1)
            if self.player.fire_left:
                v += Vec2(-1, 0)
            if self.player.fire_right:
                v += Vec2(1, 0)

            v = v.normalize() * self.player.bullet_speed
            if v.length != 0:
                self.bullets.spawn(self.player, self.player.position, v, self.player.scale)
                self.bullet_timer = 0.0

        # update loops
        for e in self.entities:
            e.update(delta_time)
        self.bullets.update(delta_time)

        # Update positions
        for entity in self.entities:
            entity.position += entity.velocity * delta_time

        # Collision checks?
        # For ease of logic lets do this in a few steps (reduces loop count too)

        entities = self.entities

        for entity in entities:
            collider = entity.hitbox

            # entity - player collisions
            for other in entities:
                other_c = other.hitbox
                if other == entity or not collider.overlaps(other_c):
                    continue

                overlap, normal = collider.collide(other_c)
                # These mass calculations are rough, but hey, it's a game jam.
                e_mass = max(1.0, 4 * entity.scale) ** 2 if not entity.immobile else math.inf
                o_mass = max(1.0, 4 * other.scale) ** 2 if not other.immobile else math.inf
                entity.position += abs(overlap) * normal / e_mass
                other.position += -abs(overlap) * normal / o_mass

            # entity - terrain collisions
            for terrain in self.terrain:
                if not collider.overlaps(terrain):
                    continue

                overlap, normal = collider.collide(terrain)
                entity.position += abs(overlap) * normal

            # entity - hazard collisions
            for hazard in self.hazards:
                hazard_c = hazard.hitbox
                if collider.overlaps(hazard_c):
                    if not hazard.passable(entity.scale):
                        overlap, normal = collider.collide(hazard_c)
                        entity.position += abs(overlap) * normal
                    hazard.interact(entity)

        # Health
        rem = []
        for e in self.enemies:
            if e.health <= BASICALLY_ZERO:
                rem.append(e)
        for e in rem:
            self.enemies.remove(e)

        self.refresh_sprites()

        # Camera
        self.camera.position = self.player.position
        self.camera.position = constrain_xy(self.camera.view_data, self.bounds)

        # Handle warping
        if self.player.wants_to_leave:
            self.load_level(self.player.wants_to_leave)
            self.player.wants_to_leave = None

        # Handle dying
        if self.player.health <= 0.0:
            self.load_level(self.current_level)
            self.player.health = self.player.max_health
            self.player.energy = 2.0
            self.player.scale = 1.0

    def draw(self) -> None:
        self.tiles.draw(pixelated = True)
        for h in self.hazards:
            h.draw()
        self.entity_spritelist.draw()
        self.bullets.draw()
        if self.draw_bounds:
            for collider in self.terrain:
                collider.draw()
            for hazard in self.hazards:
                arcade.draw_rect_outline(hazard.rect, arcade.color.GREEN, 4)
            # arcade.draw_rect_outline(self.bounds, DEBUG_COLOR, border_width = max(1, int(self.scale * 4)))
