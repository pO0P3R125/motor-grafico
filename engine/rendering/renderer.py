# engine/rendering/renderer.py

from OpenGL.GL import *
from engine.rendering.shader import Shader
from engine.rendering.mesh import Mesh
import numpy as np
import math
import glfw

class Renderer:
    def __init__(self):
        self.shader = Shader(
            "assets/shaders/vertex.glsl",
            "assets/shaders/fragment.glsl"
        )
        self.mesh = Mesh()

    def render(self):
        # Limpiar pantalla
        glClear(GL_COLOR_BUFFER_BIT)

        # Tiempo
        t = glfw.get_time()
        angle = t

        # Matriz identidad
        model = np.identity(4, dtype=np.float32)

        # Rotación
        cos = math.cos(angle)
        sin = math.sin(angle)

        model[0][0] = cos
        model[0][1] = -sin
        model[1][0] = sin
        model[1][1] = cos

        # 🔥 ESTO TE FALTABA
        self.shader.use()
        self.shader.set_mat4("model", model)
        self.mesh.draw()