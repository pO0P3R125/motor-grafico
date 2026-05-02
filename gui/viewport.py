"""
Viewport – QOpenGLWidget que albergará el renderizado con ModernGL.

Por ahora limpia el fondo con un color gris oscuro y muestra un
mensaje "Viewport – Sin motor". Más adelante se conectará al
contexto OpenGL y al renderizador.
"""


import glm
import moderngl
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt

from engine.core import Engine
from engine.scene import Node, VoxelWorldNode
from engine.camera import Camera
from engine.renderer import Renderer
from engine.voxel_world import patterns


class Viewport(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.engine = None
        self.scene_root = None
        self.voxel_node = None
        self.camera = None
        self.renderer = None
        self.current_pattern = "solid"
        self._initialized = False

    def initializeGL(self):
        # 1) Asegurar que el contexto Qt esté activo
        self.makeCurrent()

        # 2) Crear el contexto ModernGL compartiendo el de Qt
        self.ctx = moderngl.create_context(standalone=False)
        # También se puede usar: self.ctx = moderngl.Context()
        # Si no funciona standalone=False, prueba con moderngl.Context()

        self.engine = Engine()
        self.engine.init(self.ctx)

        # 3) Grafo de escena
        self.scene_root = Node("root")
        self.voxel_node = VoxelWorldNode(chunk_size=16)
        self.scene_root.add_child(self.voxel_node)

        self.camera = Camera(mode="orbit", world_center=glm.vec3(8, 8, 8))
        self.renderer = Renderer(self.engine)

        # 4) Cargar patrón inicial
        self._load_pattern(self.current_pattern)

        print(f"ModernGL context version: {self.ctx.version_code}")
        print(f"Instance count: {self.voxel_node.instance_count}")
        self._initialized = True

    def _load_pattern(self, name):
        voxels = patterns[name]()
        self.voxel_node.load_voxel_data(voxels)
        self.voxel_node.setup_vao(self.engine)

    def paintGL(self):
        if not self._initialized:
            return

        # Asegurar que el contexto Qt sigue activo
        self.makeCurrent()
        self.renderer.render(
            self.scene_root,
            self.camera,
            self.width(),
            self.height(),
        )
        # Forzar ejecución de comandos
        #self.ctx.finish()
        self.voxel_node.vao.render()

        # Seguir pidiendo frames
        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        print(key)
        if key == Qt.Key.Key_1:
            self.current_pattern = "solid"
            self._load_pattern("solid")
        elif key == Qt.Key.Key_2:
            self.current_pattern = "stairs"
            self._load_pattern("stairs")
        elif key == Qt.Key.Key_3:
            self.current_pattern = "pyramid"
            self._load_pattern("pyramid")
        elif key == Qt.Key.Key_4:
            self.current_pattern = "checker"
            self._load_pattern("checker")
        elif key == Qt.Key.Key_C:
            self.camera.toggle_mode()
        else:
            super().keyPressEvent(event)