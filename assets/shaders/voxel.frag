#version 330 core

in vec3 fragColor;
out vec4 FragColor;

void main()
{
    // Futuro: iluminación (Phong, PBR) se integrará aquí
    FragColor = vec4(fragColor, 1.0);
}