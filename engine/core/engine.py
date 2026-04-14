# engine/core/engine.py
from engine.core.window import Window

class Engine:
    def __init__(self):
        self.window = Window()

    def run(self):
        while not self.window.should_close():
            self.window.update()