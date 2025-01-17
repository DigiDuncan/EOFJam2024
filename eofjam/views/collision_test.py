from eofjam.core.application import View
from eofjam.lib.collider import RectCollider, CircleCollider, InverseRectCollider, Collider

import arcade

class CollisionView(View):

    def __init__(self) -> None:
        super().__init__()
        self.rect_collider = RectCollider(arcade.LBWH(300, 200, 100, 300))
        self.circle_collider = CircleCollider(arcade.Vec2(800, 300), 200)
        self.inverse_collider = InverseRectCollider(self.window.rect.scale(0.8))

        self.mouse: Collider = None
        self.mouse_size = 400
        self.mouse_t = 1

    def _make_mouse(self, pos, size):
        self.mouse = None
        match self.mouse_t:
            case 1:
                self.mouse = RectCollider(arcade.XYWH(pos[0], pos[1], size, size))
            case 2:
                self.mouse = CircleCollider(arcade.Vec2(*pos), size)
            case 3:
                self.mouse = InverseRectCollider(arcade.XYWH(pos[0], pos[1], size, size))

    def on_draw(self) -> None:
        self.clear()
        self.rect_collider.draw()
        self.circle_collider.draw()
        self.inverse_collider.draw()

        if self.mouse is None:
            return
        
        self.mouse.draw()

        if self.rect_collider.overlaps(self.mouse):
            arcade.draw_text('collides!', self.rect_collider.position.x, self.rect_collider.position.y, arcade.color.WHITE, anchor_x='center')

        
        if self.circle_collider.overlaps(self.mouse):
            arcade.draw_text('collides!', self.circle_collider.position.x, self.circle_collider.position.y, arcade.color.WHITE, anchor_x='center')

        
        if self.inverse_collider.overlaps(self.mouse):
            arcade.draw_text('collides!', self.inverse_collider.position.x, self.inverse_collider.position.y, arcade.color.WHITE, anchor_x='center')

    def on_key_press(self, symbol, modifiers):
        match symbol:
            case arcade.key.KEY_1:
                self.mouse_t = 1
                self.mouse = None
            case arcade.key.KEY_2:
                self.mouse_t = 2
                self.mouse = None
            case arcade.key.KEY_3:
                self.mouse_t = 3
                self.mouse = None

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.mouse_size = max(1, min(1000, self.mouse_size + scroll_y * 10))
        self._make_mouse((x, y), self.mouse_size)

    def on_mouse_motion(self, x, y, dx, dy):
        self._make_mouse((x, y), self.mouse_size)