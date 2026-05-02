"""
Definición del mundo de vóxeles y generación de instancias.
Uso de Numba para acelerar la recolección de vóxeles sólidos.
"""

import numpy as np
import numba as nb
from .primitives import create_unit_cube


# --------------- Patrones de prueba ---------------
def create_solid_cube(chunk_size=16):
    """Cubo macizo de color gris."""
    voxels = np.ones((chunk_size, chunk_size, chunk_size), dtype=np.uint8)
    return voxels


def create_stairs(chunk_size=16):
    """Escalera desde (0,0,0) hasta (15,15,15) alternando colores."""
    voxels = np.zeros((chunk_size, chunk_size, chunk_size), dtype=np.uint8)
    for x in range(chunk_size):
        for y in range(chunk_size):
            # altura máxima en función de x,y
            h = min(x, y) + 1
            for z in range(h):
                voxels[x, y, z] = 1  # sólido
    return voxels


def create_pyramid(chunk_size=16):
    """Pirámide centrada con escalones."""
    voxels = np.zeros((chunk_size, chunk_size, chunk_size), dtype=np.uint8)
    cx, cy = chunk_size // 2, chunk_size // 2
    for z in range(chunk_size):
        # Radio del cuadrado en este nivel
        r = chunk_size // 2 - z
        if r < 0:
            break
        for x in range(cx - r, cx + r):
            for y in range(cy - r, cy + r):
                if 0 <= x < chunk_size and 0 <= y < chunk_size:
                    voxels[x, y, z] = 1
    return voxels


def create_checkerboard(chunk_size=16):
    """Tablero 3D alternando colores según paridad (x+y+z)."""
    voxels = np.zeros((chunk_size, chunk_size, chunk_size), dtype=np.uint8)
    for x in range(chunk_size):
        for y in range(chunk_size):
            for z in range(chunk_size):
                if (x + y + z) % 2 == 0:
                    voxels[x, y, z] = 1
    return voxels


# Diccionario de patrones
patterns = {
    "solid": create_solid_cube,
    "stairs": create_stairs,
    "pyramid": create_pyramid,
    "checker": create_checkerboard,
}


# --------------- Numba: generación de buffers de instancias ---------------
@nb.njit(cache=True)
def _collect_solid_voxels(voxels, chunk_size):
    """
    Recorre la grilla de vóxeles y devuelve:
        - positions: array (N,3) centros de cada vóxel sólido
        - colors: array (N,3) colores RGB (0-1)
    """
    # Contar sólidos primero para asignar arrays
    count = 0
    for x in range(chunk_size):
        for y in range(chunk_size):
            for z in range(chunk_size):
                if voxels[x, y, z] != 0:
                    count += 1

    positions = np.empty((count, 3), dtype=np.float32)
    colors = np.empty((count, 3), dtype=np.float32)

    idx = 0
    for x in range(chunk_size):
        for y in range(chunk_size):
            for z in range(chunk_size):
                if voxels[x, y, z] != 0:
                    # Centro del vóxel: (x, y, z) (ya que el cubo unidad tiene lado 1)
                    positions[idx, 0] = x + 0.5
                    positions[idx, 1] = y + 0.5
                    positions[idx, 2] = z + 0.5

                    # Color determinístico basado en tipo (por ahora solo un color gris)
                    # Más adelante se puede mapear voxels[x,y,z] a material
                    if voxels[x, y, z] == 1:
                        # gris claro
                        colors[idx] = (0.7, 0.7, 0.7)
                    else:
                        # otros valores para futuros materiales
                        colors[idx] = (0.7, 0.7, 0.7)
                    idx += 1
    print(count)
    return positions, colors


def generate_voxel_instances(voxels, chunk_size):
    """Interfaz pública que llama a la función acelerada."""
    return _collect_solid_voxels(voxels, chunk_size)