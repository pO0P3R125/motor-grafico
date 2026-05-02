"""
Motor central: crea el contexto ModernGL, carga shaders y proporciona
la geometría del cubo unidad (compartida por todos los chunks).
"""

import moderngl
from .primitives import create_unit_cube

class Engine:
    def __init__(self):
        self.ctx: moderngl.Context = None
        self.program: moderngl.Program = None
        self.cube_vbo: moderngl.Buffer = None
        self.cube_ibo: moderngl.Buffer = None

    def init(self, ctx: moderngl.Context):
        self.ctx = ctx
        self.ctx.enable(moderngl.DEPTH_TEST)

        with open("assets/shaders/voxel.vert", "r") as f:
            vs = f.read()
        with open("assets/shaders/voxel.frag", "r") as f:
            fs = f.read()
        self.program = self.ctx.program(vertex_shader=vs, fragment_shader=fs)

        vertices, indices = create_unit_cube()
        self.cube_vbo = self.ctx.buffer(vertices)
        self.cube_ibo = self.ctx.buffer(indices)

        # VAO base solo con atributos del cubo (sin instancias aún)
        self.cube_vao = self.ctx.vertex_array(
            self.program,
            [(self.cube_vbo, '3f', 'aPos')],
            #[(self.cube_vbo, '3f 3f', 'aPos', 'aNormal')],
            self.cube_ibo,
        )

    def destroy(self):
        if self.ctx:
            self.ctx.release()