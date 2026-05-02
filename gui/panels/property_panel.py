"""
Panel de propiedades (derecha, inferior a la biblioteca).

Muestra las propiedades del objeto seleccionado (vóxel u OBJ):
posición, rotación, escala, color/material.
Permite la edición en tiempo real de estos valores.

Estructura:
    - Campos numéricos para X, Y, Z de posición, rotación, escala.
    - Selector de color / material.
    - Layout en forma de formulario con QFormLayout.
"""

from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QDoubleSpinBox, QPushButton,
    QGroupBox, QVBoxLayout, QColorDialog, QLabel,
)
from PyQt6.QtGui import QIcon, QPixmap, QColor
from PyQt6.QtCore import pyqtSignal


class PropertyPanel(QWidget):
    """
    Panel de edición de propiedades del elemento activo.

    Señales previstas (a conectar con la escena):
        property_changed(property_name: str, value)

    Por ahora los campos son editables pero no afectan a la escena.
    """

    property_changed = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Propiedades")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # --- Grupo: Transformación ---
        transform_group = QGroupBox("Transformación")
        form = QFormLayout(transform_group)

        # Posición
        self.pos_x = self._create_double_spinbox(-9999, 9999, 0.0)
        self.pos_y = self._create_double_spinbox(-9999, 9999, 0.0)
        self.pos_z = self._create_double_spinbox(-9999, 9999, 0.0)
        form.addRow("Pos X:", self.pos_x)
        form.addRow("Pos Y:", self.pos_y)
        form.addRow("Pos Z:", self.pos_z)

        # Rotación (en grados)
        self.rot_x = self._create_double_spinbox(-360, 360, 0.0)
        self.rot_y = self._create_double_spinbox(-360, 360, 0.0)
        self.rot_z = self._create_double_spinbox(-360, 360, 0.0)
        form.addRow("Rot X:", self.rot_x)
        form.addRow("Rot Y:", self.rot_y)
        form.addRow("Rot Z:", self.rot_z)

        # Escala (mínimo 0.01 para evitar degeneraciones)
        self.scale_x = self._create_double_spinbox(0.01, 100, 1.0)
        self.scale_y = self._create_double_spinbox(0.01, 100, 1.0)
        self.scale_z = self._create_double_spinbox(0.01, 100, 1.0)
        form.addRow("Esc X:", self.scale_x)
        form.addRow("Esc Y:", self.scale_y)
        form.addRow("Esc Z:", self.scale_z)

        main_layout.addWidget(transform_group)

        # --- Grupo: Color / Material ---
        material_group = QGroupBox("Color / Material")
        mat_layout = QVBoxLayout(material_group)

        self.color_button = QPushButton()
        self.color_button.setFixedSize(48, 48)
        self._current_color = QColor(200, 200, 200)  # gris claro
        self._update_color_button()
        self.color_button.clicked.connect(self._choose_color)
        mat_layout.addWidget(self.color_button)

        self.material_label = QLabel("Material: ninguno")
        self.material_label.setWordWrap(True)
        mat_layout.addWidget(self.material_label)

        main_layout.addWidget(material_group)
        main_layout.addStretch()

    def _create_double_spinbox(self, min_val, max_val, default):
        spin = QDoubleSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        spin.setDecimals(3)
        spin.setSingleStep(0.1)
        # En el futuro se conectará a property_changed
        return spin

    def _choose_color(self):
        """Abre el selector de color Qt y actualiza el botón."""
        color = QColorDialog.getColor(self._current_color, self, "Seleccionar color")
        if color.isValid():
            self._current_color = color
            self._update_color_button()
            # Futuro: emitir señal con el nuevo color

    def _update_color_button(self):
        """Pinta el botón con el color actual."""
        pixmap = QPixmap(48, 48)
        pixmap.fill(self._current_color)
        self.color_button.setIcon(QIcon(pixmap))
        self.color_button.setIconSize(pixmap.size())

    # Métodos públicos para recibir propiedades del objeto seleccionado
    def set_object_properties(self, position, rotation, scale, color: QColor):
        """
        Actualiza los campos con los datos del objeto activo.
        (Se conectará más adelante desde la controladora)
        """
        self.pos_x.setValue(position[0])
        self.pos_y.setValue(position[1])
        self.pos_z.setValue(position[2])
        self.rot_x.setValue(rotation[0])
        self.rot_y.setValue(rotation[1])
        self.rot_z.setValue(rotation[2])
        self.scale_x.setValue(scale[0])
        self.scale_y.setValue(scale[1])
        self.scale_z.setValue(scale[2])
        self._current_color = color
        self._update_color_button()