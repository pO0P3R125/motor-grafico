"""
Panel de herramientas (izquierda).

Contendrá botones para activar modos de edición (añadir vóxel,
eliminar, seleccionar, mover, etc.) y opciones de pincel/color.
Por ahora es un contenedor vacío con un layout vertical, listo
para extender en futuros sprints.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ToolPanel(QWidget):
    """
    Panel lateral de herramientas.

    Funcionalidad prevista:
        - Botones de modo: Añadir vóxel, Eliminar, Seleccionar,
          Mover, Rotar.
        - Selector de tipo de pincel (cubo, esfera, tamaño).
        - Paleta de colores / material.

    Señales que podría emitir (a implementar):
        tool_changed(str)       # cambio de herramienta activa
        brush_size_changed(int)
        color_changed(QColor)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Herramientas")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        placeholder = QLabel("Panel de herramientas\n(próximamente)")
        placeholder.setWordWrap(True)
        layout.addWidget(placeholder)
        layout.addStretch()