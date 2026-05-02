"""
Panel de biblioteca de objetos (derecha).

Muestra una lista de modelos OBJ (u otros formatos) disponibles
para insertar en la maqueta, cada uno con una miniatura.
Incluye un botón "Importar…" para añadir nuevos modelos al catálogo
y permite seleccionar un elemento para colocarlo en la escena.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget,
    QListWidgetItem, QLabel, QFileDialog, QMessageBox,
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
import os


class ObjectLibrary(QWidget):
    """
    Biblioteca de modelos 3D.

    Señales futuras:
        model_selected(file_path: str)   # cuando se selecciona un modelo de la lista
        model_added(file_path: str)      # cuando se importa un nuevo modelo

    Por ahora la lista se llena con algunos ejemplos y se usa un
    icono placeholder para las miniaturas.
    """

    model_selected = pyqtSignal(str)   # emisión preparada para el futuro

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Biblioteca de objetos")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Título interno
        title = QLabel("Modelos disponibles")
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)

        # Lista de modelos con miniaturas
        self.list_widget = QListWidget()
        self.list_widget.setIconSize(QPixmap(48, 48).size())
        self.list_widget.setSelectionMode(
            QListWidget.SelectionMode.SingleSelection
        )
        # Conexión temporal para depuración (se activará más adelante)
        self.list_widget.itemSelectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self.list_widget)

        # Botón de importar
        self.import_btn = QPushButton("Importar…")
        self.import_btn.clicked.connect(self._import_model)
        layout.addWidget(self.import_btn)

        # Cargar algunos ejemplos placeholder
        self._populate_placeholders()

    def _populate_placeholders(self):
        """Inserta ejemplos gráficos mientras no tengamos modelos reales."""
        # Icono genérico (cuadrado gris)
        pixmap = QPixmap(48, 48)
        pixmap.fill(Qt.GlobalColor.darkGray)
        icon = QIcon(pixmap)

        samples = [
            "silla_moderna.obj",
            "mesa_centro.glb",
            "lampara_pie.obj",
            "estanteria.obj",
        ]
        for name in samples:
            item = QListWidgetItem(icon, name)
            item.setData(Qt.ItemDataRole.UserRole, name)  # ruta ficticia
            self.list_widget.addItem(item)

        # Seleccionar el primer elemento por defecto
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def _import_model(self):
        """
        Abre un diálogo para seleccionar un archivo 3D (OBJ/GLB/glTF).
        En el futuro copiará el modelo a la carpeta de assets y
        generará su miniatura. Por ahora solo muestra una notificación.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Importar modelo",
            "",
            "Modelos 3D (*.obj *.glb *.gltf *.fbx);;Todos los archivos (*.*)",
        )
        if not file_path:
            return

        # Placeholder: notificar al usuario que el motor aún no está conectado
        QMessageBox.information(
            self,
            "Importar modelo",
            f"Modelo seleccionado:\n{file_path}\n\n"
            "La funcionalidad de importación se integrará en la siguiente fase.",
        )
        # En el futuro se emitirá model_added(file_path) y se añadirá a la lista.

    def _on_selection_changed(self):
        """
        Emite la señal model_selected con la ruta del modelo cuando
        el motor esté listo. Por ahora simplemente se registra.
        """
        selected = self.list_widget.currentItem()
        if selected:
            # En el futuro se leerá la ruta real almacenada en UserRole
            # self.model_selected.emit(selected.data(Qt.ItemDataRole.UserRole))
            print(f"[ObjectLibrary] Seleccionado: {selected.text()}")