from typing import Protocol

from deps_tabular_layout.models import Cell

__all__ = ["ICellCommandRepository"]


class ICellCommandRepository(Protocol):
    def save_batch(self, layout_id: str, cells: list[Cell]) -> None:
        ...

    def delete(self, layout_id: str) -> None:
        ...
