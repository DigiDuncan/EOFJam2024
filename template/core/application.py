from arcade import View as ArcadeView, Window as ArcadeWindow
# Update these classes if you want custom functionality in your Windows and Views.

__all__ = (
    'Window',
    'View',
    'ArcadeWindow',
    'ArcadeView'
)

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
WINDOW_TITLE = 'template'

class Window(ArcadeWindow):

    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)


class View(ArcadeView):

    def __init__(self, window: Window | None = None) -> None:
        super().__init__(window)
