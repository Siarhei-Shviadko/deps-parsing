from deps_tabular_layout.models import TabularLayout
from sqlalchemy import and_, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection

from deps_parsing.domain.interfaces import ITabularLayoutCommandRepository
from deps_parsing.extras.datasource import Database

from ...tables import tabular_layout_table, tbl_table
from ..mappers import TabularLayoutMapper

__all__ = ["TabularLayoutCommandRepository"]


class TabularLayoutCommandRepository(ITabularLayoutCommandRepository):
    def __init__(self, database: Database) -> None:
        self._db = database

    def save(self, layout: TabularLayout) -> None:
        with self._db.connection() as connection:
            self._save_layout(connection, layout)
            self._replace_layout_tables(connection, layout)

    def delete(self, layout_id: str, tenant_id: str) -> None:
        table_query = delete(tbl_table).where(tbl_table.c.tabular_layout_id == layout_id)

        tabular_layout_query = delete(tabular_layout_table).where(
            and_(
                tabular_layout_table.c.id == layout_id,
                tabular_layout_table.c.tenant_id == tenant_id,
            ),
        )

        with self._db.connection() as connection:
            if (connection.execute(tabular_layout_query)).rowcount > 0:
                connection.execute(table_query)

    def _save_layout(self, connection: Connection, layout: TabularLayout) -> None:
        raw_layout = TabularLayoutMapper.tl_to_dict(layout)

        query = insert(tabular_layout_table).values(**raw_layout)
        query = query.on_conflict_do_update(constraint=tabular_layout_table.primary_key, set_=dict(query.excluded))

        connection.execute(query)

    def _replace_layout_tables(self, connection: Connection, layout: TabularLayout) -> None:
        self._remove_layout_tables(connection, layout)
        self._save_layout_tables(connection, layout)

    def _remove_layout_tables(self, connection: Connection, layout: TabularLayout) -> None:
        query = delete(tbl_table).where(tbl_table.c.tabular_layout_id == layout.id())

        connection.execute(query)

    def _save_layout_tables(self, connection: Connection, layout: TabularLayout) -> None:
        if not (raw_tables := TabularLayoutMapper.tl_to_raw_tables(layout)):
            return

        query = insert(tbl_table).values(raw_tables)
        query = query.on_conflict_do_update(constraint=tbl_table.primary_key, set_=dict(query.excluded))

        connection.execute(query)
