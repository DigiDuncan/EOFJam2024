from template.core.application import Window
from template.views.root import RootView

def main() -> None:
    win = Window()
    root = RootView()

    win.show_view(root)
    win.run()
