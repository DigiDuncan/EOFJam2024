from eofjam.core.application import View

class EOFJamView(View):

    def __init__(self) -> None:
        super().__init__()

    def on_draw(self) -> None:
        self.clear()
