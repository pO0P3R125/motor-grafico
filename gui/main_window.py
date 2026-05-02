"""
Ventana principal de la aplicación.

Organiza los paneles acoplables, la barra de menú, la barra de
herramientas y la barra de estado. Centraliza el Viewport como
widget central. Carga la hoja de estilos oscura.

Atributos principales:
    - viewport: instancia del visor 3D
    - tool_panel: panel de herramientas (izquierda)
    - object_library: biblioteca de objetos (derecha)
    - property_panel: panel de propiedades (derecha)
    - undo_redo_manager: gestor de deshacer/rehacer (to do)
"""

import os
from PyQt6.QtWidgets import (
    QMainWindow, QDockWidget, QMenuBar, QMenu, QToolBar,
    QStatusBar, QMessageBox, QFileDialog,
)
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt, QSize

from .viewport import Viewport
from .panels.tool_panel import ToolPanel
from .panels.object_library import ObjectLibrary
from .panels.property_panel import PropertyPanel
# from utils.undo_redo import UndoRedoManager   # se activará más adelante


class MainWindow(QMainWindow):
    """
    Ventana principal con diseño MDI.

    Layout:
        - Central: Viewport
        - Dock izquierdo: ToolPanel
        - Dock derecho: ObjectLibrary (arriba) + PropertyPanel (abajo)
        - Barra de menú superior
        - Barra de estado inferior
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Motor de Maquetas Voxel")
        self.setMinimumSize(1280, 720)

        # ---------- Widget central (visor 3D) ----------
        self.viewport = Viewport()
        self.setCentralWidget(self.viewport)

        # ---------- Paneles laterales ----------
        self.tool_panel = ToolPanel()
        self.object_library = ObjectLibrary()
        self.property_panel = PropertyPanel()

        # Dock izquierdo: herramientas
        self.tool_dock = QDockWidget("Herramientas", self)
        self.tool_dock.setWidget(self.tool_panel)
        self.tool_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.tool_dock)

        # Dock derecho superior: biblioteca de objetos
        self.lib_dock = QDockWidget("Biblioteca", self)
        self.lib_dock.setWidget(self.object_library)
        self.lib_dock.setAllowedAreas(
            Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea
        )
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.lib_dock)

        # Dock derecho inferior: propiedades
        self.props_dock = QDockWidget("Propiedades", self)
        self.props_dock.setWidget(self.property_panel)
        self.props_dock.setAllowedAreas(
            Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea
        )
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.props_dock)

        # ---------- Barras de menú y herramientas ----------
        self._create_menus()
        self._create_toolbar()
        self._create_statusbar()

        # ---------- Gestor de deshacer/rehacer (placeholder) ----------
        # self.undo_redo_manager = UndoRedoManager()
        # Más adelante se conectará a las acciones correspondientes

        # ---------- Estilo oscuro ----------
        self._load_stylesheet()

    # ------------------------------------------------------------------
    def _create_menus(self):
        """Construye la barra de menú con las acciones básicas."""
        menubar = self.menuBar()

        # --- Menú Archivo ---
        file_menu = menubar.addMenu("&Archivo")

        new_action = QAction("&Nuevo proyecto", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self._on_new_project)
        file_menu.addAction(new_action)

        open_action = QAction("&Abrir proyecto...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._on_open_project)
        file_menu.addAction(open_action)

        save_action = QAction("&Guardar proyecto", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self._on_save_project)
        file_menu.addAction(save_action)

        save_as_action = QAction("Guardar proyecto &como...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self._on_save_as_project)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        import_action = QAction("&Importar modelo...", self)
        import_action.setShortcut(QKeySequence("Ctrl+I"))
        import_action.triggered.connect(self._on_import_model)
        file_menu.addAction(import_action)

        export_action = QAction("&Exportar escena...", self)
        export_action.triggered.connect(self._on_export_scene)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("&Salir", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # --- Menú Editar ---
        edit_menu = menubar.addMenu("&Editar")

        self.undo_action = QAction("&Deshacer", self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.setEnabled(False)  # se activará cuando el gestor lo permita
        edit_menu.addAction(self.undo_action)

        self.redo_action = QAction("&Rehacer", self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.setEnabled(False)
        edit_menu.addAction(self.redo_action)

        edit_menu.addSeparator()

        prefs_action = QAction("&Preferencias...", self)
        prefs_action.triggered.connect(self._on_preferences)
        edit_menu.addAction(prefs_action)

        # --- Menú Vista ---
        view_menu = menubar.addMenu("&Vista")

        reset_cam_action = QAction("&Restablecer cámara", self)
        reset_cam_action.setShortcut(QKeySequence("Ctrl+0"))
        reset_cam_action.triggered.connect(self._on_reset_camera)
        view_menu.addAction(reset_cam_action)

        view_menu.addSeparator()
        view_menu.addAction(self.tool_dock.toggleViewAction())
        view_menu.addAction(self.lib_dock.toggleViewAction())
        view_menu.addAction(self.props_dock.toggleViewAction())

        # --- Menú Ayuda ---
        help_menu = menubar.addMenu("Ay&uda")
        about_action = QAction("&Acerca de...", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

    def _create_toolbar(self):
        """Barra de herramientas principal (acciones rápidas)."""
        toolbar = QToolBar("Herramientas principales")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # Acciones placeholder: más adelante se añadirán botones de modo
        # Por ahora ponemos algunas acciones comunes
        # (usamos texto en lugar de iconos)
        import_btn = toolbar.addAction("Importar")
        import_btn.triggered.connect(self._on_import_model)

        toolbar.addSeparator()
        # Espacio para futuros modos: añadir vóxel, eliminar, etc.
        # Se conectarán desde el controlador.

    def _create_statusbar(self):
        """Barra de estado con mensaje inicial."""
        status = QStatusBar()
        status.showMessage("Listo")
        self.setStatusBar(status)

    # ---------- Slots de menú (placeholders) ----------
    def _on_new_project(self):
        QMessageBox.information(self, "Nuevo proyecto",
                                "Funcionalidad no implementada aún.")

    def _on_open_project(self):
        QMessageBox.information(self, "Abrir proyecto",
                                "Funcionalidad no implementada aún.")

    def _on_save_project(self):
        QMessageBox.information(self, "Guardar proyecto",
                                "Funcionalidad no implementada aún.")

    def _on_save_as_project(self):
        QMessageBox.information(self, "Guardar como",
                                "Funcionalidad no implementada aún.")

    def _on_import_model(self):
        """
        Delega la importación al panel de biblioteca.
        En el futuro, el flujo involucrará al motor.
        """
        self.object_library._import_model()

    def _on_export_scene(self):
        QMessageBox.information(self, "Exportar escena",
                                "Funcionalidad no implementada aún.")

    def _on_preferences(self):
        QMessageBox.information(self, "Preferencias",
                                "Funcionalidad no implementada aún.")

    def _on_reset_camera(self):
        QMessageBox.information(self, "Cámara",
                                "Cámara restablecida (placeholder).")

    def _on_about(self):
        QMessageBox.about(
            self,
            "Acerca de",
            "Motor de Maquetas Voxel\n"
            "Proyecto de Graficación\n"
            "Versión 0.1 – en desarrollo"
        )

    # ------------------------------------------------------------------
    def _load_stylesheet(self):
        """Carga la hoja de estilo oscura desde el archivo QSS."""
        # Buscar la ruta relativa al directorio del script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        style_path = os.path.join(current_dir, "styles", "dark_theme.qss")
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        else:
            # Fallback por si el archivo no se encuentra
            print("[MainWindow] No se encontró dark_theme.qss, usando estilo por defecto.")