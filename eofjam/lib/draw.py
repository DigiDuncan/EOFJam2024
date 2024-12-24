from arcade import draw_line, Vec2
from arcade.types import Color

def draw_cross(origin: Vec2, size: float, color: Color, thickness: float = 1.0) -> None:
    draw_line(
            origin.x - size, origin.y - size,
            origin.x + size, origin.y + size,
            color,
            thickness
        )
    draw_line(
        origin.x + size, origin.y - size,
        origin.x - size, origin.y + size,
        color,
        thickness
    )
