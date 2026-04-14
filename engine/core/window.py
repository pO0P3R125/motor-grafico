# engine/core/window.py
import glfw

class Window:
    def __init__(self, width=800, height=600, title="Mini Engine"):
        if not glfw.init():
            raise Exception("GLFW no pudo iniciar")

        self.window = glfw.create_window(width, height, title, None, None)
        glfw.make_context_current(self.window)

    def should_close(self):
        return glfw.window_should_close(self.window)

    def update(self):
        glfw.swap_buffers(self.window)
        glfw.poll_events()