"""
Renderizador: recorre la escena y dibuja utilizando el engine.
"""

class Renderer:
    def __init__(self, engine):
        self.engine = engine

    def render(self, scene_root, camera, viewport_width, viewport_height):
        ctx = self.engine.ctx
        # Usar el framebuffer de pantalla por defecto
        ctx.screen.use()
        # Limpiar con gris oscuro (si todo va bien se verá ese color)
        ctx.clear(0.1, 0.1, 0.1)

        if scene_root is None:
            return

        view = camera.get_view_matrix()
        proj = camera.projection_matrix(viewport_width, viewport_height)

        # Debug: imprimir matrices (quitar después)
        # print("View:", view)
        # print("Proj:", proj)

        scene_root.render(view, proj, self.engine.program)