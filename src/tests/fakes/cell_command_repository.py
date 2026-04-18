from deps_tabular_layout.models import Cell

from deps_parsing.domain.interfaces import ICellCommandRepository

__all__ = ["FakeCellCommandRepository"]


class FakeCellCommandRepository(ICellCommandRepository):
    def __init__(self) -> None:
        self._db: dict[str, Cell] = {}

    def save_batch(self, layout_id: str, cells: list[Cell]) -> None:
        for cell in cells:
            self._db[cell.id()] = cell

    def local_db(self) -> dict[str, Cell]:
        return self._db
