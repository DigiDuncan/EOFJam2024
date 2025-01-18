from __future__ import annotations

from arcade import Vec2

from eofjam.lib.collider import Collider

class Object:

    def __init__(self, uuid: str, position: Vec2, collider: Collider):
        self.uuid: str = uuid
        self.collider: Collider = collider
        self.position = position

    def __hash__(self):
        return hash(self.uuid)
    
    def __eq__(self, value: Object):
        return self.uuid == value.uuid
    
    @property
    def position(self):
        return self.collider.position
    
    @position.setter
    def position(self, position: Vec2):
        self.collider.position = position
    
    def update(self):
        pass

    def enter(self):
        pass

    def interact(self):
        pass

    def exit(self):
        pass

    def draw(self):
        self.collider.draw


class Entity(Object):
    
    def __init__(self, uuid, position, collider, sprite, scale):
        Object.__init__(self, uuid, position, collider)
        self.sprite = sprite
        self.velocity: Vec2 = Vec2()