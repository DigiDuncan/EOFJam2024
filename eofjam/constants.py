from arcade import color
from arcade.types import Color

OFF_WHITE = Color.from_gray(int(255*0.9))
OFF_BLACK = Color.from_gray(int(255*0.1))

BG_COLOR = OFF_BLACK
BORDER_COLOR = OFF_BLACK
TEXT_COLOR = OFF_BLACK

DEBUG_COLOR = color.MAGENTA

PLAYER_COLOR = color.CHARM_GREEN
ENEMY_COLOR = color.CHARM_PINK

BULLET_NONE_COLOR = color.WHITE
BULLET_HEALTH_COLOR = color.BLUE
BULLET_ENERGY_COLOR = color.GREEN
BULLET_BOTH_COLOR = color.RED

HAZARD_NONE_COLOR = color.WHITE
HAZARD_MIN_SCALE_COLOR = color.YELLOW.replace(a = 64)
HAZARD_MAX_SCALE_COLOR = color.MAGENTA.replace(a = 64)
HAZARD_BOTH_COLOR = color.CYAN.replace(a = 64)

# These will be sprites one day...?
CHARGER_COLOR = color.CG_BLUE
SPAWNER_COLOR = color.SLATE_GRAY
HEALER_COLOR = color.CG_RED

PICKUP_HEALTH_COLOR = color.CG_RED.replace(a = 128)
PICKUP_ENERGY_COLOR = color.CG_BLUE.replace(a = 128)
PICKUP_BOTH_COLOR = color.ROYAL_PURPLE.replace(a = 128)
PICKUP_NONE_COLOR = color.WHITE.replace(a = 128)
