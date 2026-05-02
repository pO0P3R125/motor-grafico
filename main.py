"""
Punto de entrada de la aplicación.

Inicializa QApplication y crea la ventana principal.
"""

import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Voxel Maquette")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()