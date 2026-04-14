# engine/graphics/shader.py
from unicodedata import name

from OpenGL.GL import *

class Shader:
    def __init__(self, vertex_path, fragment_path):
        with open(vertex_path, 'r') as f:
            vertex_src = f.read()
        with open(fragment_path, 'r') as f:
            fragment_src = f.read()

        self.program = glCreateProgram()

        vertex = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex, vertex_src)
        glCompileShader(vertex)

        fragment = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment, fragment_src)
        glCompileShader(fragment)

        glAttachShader(self.program, vertex)
        glAttachShader(self.program, fragment)
        glLinkProgram(self.program)

        glDeleteShader(vertex)
        glDeleteShader(fragment)

    def use(self):
        glUseProgram(self.program)
        
    def set_mat4(self, name, matrix):
        from OpenGL.GL import glGetUniformLocation, glUniformMatrix4fv
        location = glGetUniformLocation(self.program, name)
        glUniformMatrix4fv(location, 1, False, matrix)