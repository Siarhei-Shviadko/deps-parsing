from sqlalchemy import select

from deps_parsing.extras.datasource import Database
from deps_parsing.infrastructure.repositories.tables import (
    cell_table,
    tabular_layout_table,
    tbl_table,
)

__all__ = ["TLQueryHelper"]


class TLQueryHelper:
    def __init__(self, database: Database) -> None:
        self.database = database

    def load_all_cells(self) -> list[dict]:
        with self.database.connection() as conn:
            stmt = select(cell_table)
            return conn.execute(stmt).mappings().fetchall()

    def load_all_tables(self) -> list[dict]:
        with self.database.connection() as conn:
            stmt = select(tbl_table)
            return conn.execute(stmt).mappings().fetchall()

    def load_all_tabular_layouts(self) -> list[dict]:
        with self.database.connection() as conn:
            stmt = select(tabular_layout_table)
            return conn.execute(stmt).mappings().fetchall()
