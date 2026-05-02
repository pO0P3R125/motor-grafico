"""
Geometrías básicas compartidas.

Proporciona los datos del cubo unidad (1×1×1) centrado en el origen.
La función devuelve (vértices, normales, índices) como arrays numpy.
"""

import numpy as np
import moderngl


def create_unit_cube():
    """Devuelve (packed_vertices, indices) con intercalado (x,y,z, nx,ny,nz)."""
    h = 0.5
    faces = [
        # Frontal (z+)
        ((-h, -h,  h), (-h,  h,  h), ( h,  h,  h), ( h, -h,  h)),
        # Trasera (z-)
        ((-h, -h, -h), ( h, -h, -h), ( h,  h, -h), (-h,  h, -h)),
        # Superior (y+)
        ((-h,  h, -h), (-h,  h,  h), ( h,  h,  h), ( h,  h, -h)),
        # Inferior (y-)
        ((-h, -h, -h), ( h, -h, -h), ( h, -h,  h), (-h, -h,  h)),
        # Derecha (x+)
        (( h, -h, -h), ( h,  h, -h), ( h,  h,  h), ( h, -h,  h)),
        # Izquierda (x-)
        ((-h, -h, -h), (-h, -h,  h), (-h,  h,  h), (-h,  h, -h)),
    ]
    #normals_list = [
    #    (0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)
    #]

    vertex_list = []
    index_list = []
    v_offset = 0

    for face_idx, (v0, v1, v2, v3) in enumerate(faces):
        #n = normals_list[face_idx]
        for v in (v0, v1, v2, v3):
            vertex_list.extend(v)
            #vertex_list.extend(n)
        index_list.extend([v_offset, v_offset+1, v_offset+2,
                           v_offset, v_offset+2, v_offset+3])
        v_offset += 4

    vertices = np.array(vertex_list, dtype=np.float32)
    indices = np.array(index_list, dtype=np.uint32)
    return vertices, indices