from eofjam.core.application import Window
from eofjam.views.root import RootView

from resources import load_font

def main() -> None:
    win = Window()
    root = RootView()

    for font in ["CMUNBX", "CMUNRM", "CMUNTI"]:
        load_font(font)

    win.show_view(root)
    win.run()
