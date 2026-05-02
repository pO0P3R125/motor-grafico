#version 330 core

layout (location = 0) in vec3 aPos;          // vértice del cubo unidad
//layout (location = 1) in vec3 aNormal;       // normal del cubo
layout (location = 2) in vec3 instancePos;   // posición del vóxel
layout (location = 3) in vec3 instanceColor; // color del vóxel

uniform mat4 view;
uniform mat4 projection;

out vec3 fragColor;

void main()
{
    // traslación del cubo al centro del vóxel (coordenadas del mundo)
    vec3 worldPos = aPos + instancePos;
    gl_Position = projection * view * vec4(worldPos, 1.0);
    fragColor = instanceColor;
}