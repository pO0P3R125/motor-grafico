# engine/core/engine.py
from engine.core.window import Window
from engine.rendering.renderer import Renderer

class Engine:
    def __init__(self):
        self.window = Window()
        self.renderer = Renderer()

    def run(self):
        while not self.window.should_close():
            self.renderer.render()
            self.window.update()