"""
Gestor de deshacer / rehacer basado en el patrón Command.

Por el momento sólo se define la clase con los métodos
necesarios. En el futuro se integrarán comandos concretos
(add_voxel, delete_voxel, move_object, etc.).
"""

from typing import List


class UndoRedoManager:
    """
    Administra una pila de comandos ejecutados para permitir
    las operaciones de deshacer y rehacer.

    Uso previsto:
        mgr = UndoRedoManager()
        mgr.execute(comando)    # ejecuta y guarda el comando
        mgr.undo()              # deshace la última acción
        mgr.redo()              # rehace la última acción deshecha
    """

    def __init__(self):
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []

    def execute(self, command: "Command"):
        """Ejecuta un comando y lo coloca en la pila de deshacer."""
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()  # al ejecutar un nuevo comando se pierde la historia de rehacer

    def undo(self) -> bool:
        """Deshace el último comando, si es posible. Retorna True si tuvo éxito."""
        if not self._undo_stack:
            return False
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)
        return True

    def redo(self) -> bool:
        """Rehace el último comando deshecho. Retorna True si tuvo éxito."""
        if not self._redo_stack:
            return False
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)
        return True

    def clear(self):
        """Limpia todo el historial."""
        self._undo_stack.clear()
        self._redo_stack.clear()


class Command:
    """
    Interfaz base para un comando del editor.
    Cada comando debe implementar execute() y undo().
    """
    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError