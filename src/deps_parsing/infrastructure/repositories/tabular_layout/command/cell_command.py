from deps_tabular_layout.models import Cell
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from deps_parsing.domain.interfaces import ICellCommandRepository
from deps_parsing.extras.datasource import Database

from ...tables import cell_table
from ..mappers import CellMapper

__all__ = ["CellCommandRepository"]


class CellCommandRepository(ICellCommandRepository):
    def __init__(self, database: Database) -> None:
        self._db = database

    def save_batch(self, layout_id: str, cells: list[Cell]) -> None:
        raw_cells = [CellMapper.to_dict(layout_id=layout_id, cell=cell) for cell in cells]

        with self._db.connection() as conn:
            query = insert(cell_table).values(raw_cells)
            query = query.on_conflict_do_update(constraint=cell_table.primary_key, set_=dict(query.excluded))

            conn.execute(query)

    def delete(self, layout_id: str) -> None:
        with self._db.connection() as conn:
            query = delete(cell_table).where(cell_table.c.tabular_layout_id == layout_id)

            conn.execute(query)
