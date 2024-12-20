from eofjam.core.application import View


class RootView(View):

    def __init__(self):
        super().__init__()

    def on_draw(self) -> None:
        self.clear()
