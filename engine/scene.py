"""
Grafo de escena jerárquico.

Node base con transformaciones locales y lista de hijos.
VoxelWorldNode maneja la malla de instancias y su renderizado.
"""

import glm
import numpy as np
import moderngl
from .voxel_world import generate_voxel_instances


class Node:
    def __init__(self, name=""):
        self.name = name
        self.parent: Node = None
        self.children: list[Node] = []
        self.local_position = glm.vec3(0)
        self.local_rotation = glm.quat()
        self.local_scale = glm.vec3(1)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)
        child.parent = None

    def get_world_matrix(self):
        translate = glm.translate(glm.mat4(1), self.local_position)
        rotate = glm.mat4_cast(self.local_rotation)
        scale = glm.scale(glm.mat4(1), self.local_scale)
        local_mat = translate * rotate * scale
        if self.parent:
            return self.parent.get_world_matrix() * local_mat
        return local_mat

    def update(self, delta_time):
        for child in self.children:
            child.update(delta_time)

    def render(self, view_matrix, projection_matrix, program):
        for child in self.children:
            child.render(view_matrix, projection_matrix, program)


class VoxelWorldNode(Node):
    def __init__(self, chunk_size=16, name="VoxelWorld"):
        super().__init__(name)
        self.chunk_size = chunk_size
        self.voxel_data: np.ndarray = None
        self.instance_count = 0
        self.vao: moderngl.VertexArray = None
        self._positions = None
        self._colors = None

    def load_voxel_data(self, voxel_array: np.ndarray):
        self.voxel_data = voxel_array
        self._rebuild_mesh()

    def _rebuild_mesh(self):
        if self.voxel_data is None:
            return
        self._positions, self._colors = generate_voxel_instances(
            self.voxel_data, self.chunk_size
        )
        self.instance_count = len(self._positions)

    def setup_vao(self, engine):
        if self._positions is None:
            return
        self.instance_pos_vbo = engine.ctx.buffer(self._positions)
        self.instance_color_vbo = engine.ctx.buffer(self._colors)

        self.vao = engine.ctx.vertex_array(
            engine.program,
            [
                (engine.cube_vbo, '3f', 'aPos'),
                #(engine.cube_vbo, '3f 3f', 'aPos', 'aNormal'),
                (self.instance_pos_vbo, '3f /v', 'instancePos'),
                (self.instance_color_vbo, '3f /v', 'instanceColor'),
            ],
            index_buffer=engine.cube_ibo,
        )

    def render(self, view_matrix, projection_matrix, program):
        if self.instance_count == 0 or self.vao is None:
            return
        model = self.get_world_matrix()
        program['view'].write(view_matrix)
        program['projection'].write(projection_matrix)
        self.vao.render(instances=self.instance_count)