"""
Cámara con modos estático y órbita.

Sistema de coordenadas del mundo:
    X derecha, Y adelante/atrás, Z arriba.
OpenGL usa Y arriba por defecto, pero nosotros pasaremos la matriz de vista
con up = (0,0,1) para respetar nuestra convención.
"""
import glm
import numpy as np
import time

class Camera:
    def __init__(self, mode="orbit", world_center=glm.vec3(8, 8, 8)):
        self.mode = mode
        self.world_center = world_center
        self.orbit_radius = 25.0
        self.orbit_speed = 0.3   # rad/s
        self._start_time = time.time()
        self.static_position = glm.vec3(20, 20, 25)

    @property
    def up(self):
        return glm.vec3(0.0, 0.0, 1.0)   # Z arriba

    def get_view_matrix(self):
        if self.mode == "orbit":
            elapsed = time.time() - self._start_time
            angle = elapsed * self.orbit_speed
            x = self.world_center.x + self.orbit_radius * np.cos(angle)
            y = self.world_center.y + self.orbit_radius * np.sin(angle)
            z = self.world_center.z + 15.0
            eye = glm.vec3(x, y, z)
            return glm.lookAt(eye, self.world_center, self.up)
        else:
            return glm.lookAt(self.static_position, self.world_center, self.up)

    def projection_matrix(self, width, height):
        return glm.perspective(glm.radians(45.0), width / height, 0.1, 100.0)

    def toggle_mode(self):
        self.mode = "static" if self.mode == "orbit" else "orbit"
        self._start_time = time.time()