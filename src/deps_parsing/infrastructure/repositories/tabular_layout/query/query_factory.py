from itertools import chain

from sqlalchemy import Column, and_, func, select
from sqlalchemy.sql import Select

from deps_parsing.domain.dtos import TabularLayoutFilter

from ...tables import cell_table, tabular_layout_table, tbl_table

__all__ = ["DocumentLayoutQueryFactory"]


class DocumentLayoutQueryFactory:
    def __init__(self) -> None:
        self._cell_schema = cell_table
        self._tl_schema = tabular_layout_table
        self._table_schema = tbl_table

    @property
    def tl_id_column(self) -> Column:
        return self._tl_schema.c.id.label("tabular_layout_id")

    @property
    def tenant_id_column(self) -> Column:
        return self._tl_schema.c.tenant_id

    @property
    def tl_columns(self) -> list[Column]:
        return [
            self.tl_id_column,
            self.tenant_id_column,
            self._tl_schema.c.parsing_type,
            self._tl_schema.c.sheets,
            self._tl_schema.c.extracted_properties,
        ]

    @property
    def table_columns(self) -> list[Column]:
        return [
            self._table_schema.c.id.label("table_id"),
            self._table_schema.c.tabular_layout_id.label("tabular_layout_id"),
            self._table_schema.c.sheet_id.label("sheet_id"),
            self._table_schema.c.column_count.label("column_count"),
            self._table_schema.c.row_count.label("row_count"),
            self._table_schema.c.placement.label("placement"),
        ]

    @property
    def cell_columns(self) -> list[Column]:
        return [
            self._cell_schema.c.id.label("id"),
            self._cell_schema.c.tabular_layout_id.label("tabular_layout_id"),
            self._cell_schema.c.table_id.label("table_id"),
            self._cell_schema.c.content.label("content"),
            self._cell_schema.c.data_type.label("data_type"),
            self._cell_schema.c.relative_position_row.label("relative_position_row"),
            self._cell_schema.c.relative_position_column.label("relative_position_column"),
            self._cell_schema.c.absolute_position_row.label("absolute_position_row"),
            self._cell_schema.c.absolute_position_column.label("absolute_position_column"),
            self._cell_schema.c.merge.label("merge"),
            self._cell_schema.c.style.label("style"),
            self._cell_schema.c.comment.label("comment"),
            self._cell_schema.c.alignment.label("alignment"),
            self._cell_schema.c.borders.label("borders"),
        ]

    @property
    def table_info_columns(self):
        return [
            self._table_schema.c.id.label("table_id"),
            self._table_schema.c.sheet_id.label("sheet_id"),
            self._table_schema.c.column_count.label("column_count"),
            self._table_schema.c.row_count.label("row_count"),
            self._table_schema.c.placement.label("placement"),
        ]

    def select_tabular_layout(self, layout_id: str, tenant_id: str) -> Select:
        return (
            select(
                *self.tl_columns,
                func.json_agg(
                    func.json_build_object(
                        *(chain(*((str(col.name), col) for col in self.table_columns))),
                    ),
                ).label("tables"),
            )
            .select_from(
                self._tl_schema.outerjoin(
                    self._table_schema,
                    self.tl_id_column == self._table_schema.c.tabular_layout_id,
                ),
            )
            .where(and_(self.tl_id_column == layout_id, self.tenant_id_column == tenant_id))
            .group_by(self.tl_id_column, self.tenant_id_column)
        )

    def select_layout_info(self, layout_id: str, tenant_id: str) -> Select:
        return (
            select(
                self.tl_id_column,
                self._tl_schema.c.parsing_type,
                self._tl_schema.c.sheets,
                func.json_agg(
                    func.json_build_object(
                        *(chain(*((str(col.name), col) for col in self.table_info_columns))),
                    ),
                ).label("tables_info"),
            )
            .select_from(
                self._tl_schema.outerjoin(
                    self._table_schema,
                    self.tl_id_column == self._table_schema.c.tabular_layout_id,
                ),
            )
            .where(and_(self.tl_id_column == layout_id, self.tenant_id_column == tenant_id))
            .group_by(self.tl_id_column, self.tenant_id_column)
        )

    def select_tabular_layout_with_cells_by(
        self,
        layout_id: str,
        tenant_id: str,
        filtering: TabularLayoutFilter,
    ) -> Select:
        subquery = self._table_subquery(layout_id=layout_id, filtering=filtering).alias("tables")

        return (
            select(
                *self.tl_columns,
                func.json_agg(
                    func.json_build_object(
                        *(chain(*((str(col.name), col) for col in subquery.c))),
                    ),
                ).label("tables"),
            )
            .select_from(self._tl_schema.outerjoin(subquery, self.tl_id_column == subquery.c.tabular_layout_id))
            .where(and_(self.tl_id_column == layout_id, self.tenant_id_column == tenant_id))
            .group_by(self.tl_id_column, self.tenant_id_column)
        )

    def select_layout_id(self, layout_id: str, tenant_id: str) -> Select:
        return select(self.tl_id_column).where(
            and_(self.tl_id_column == layout_id, self.tenant_id_column == tenant_id),
        )

    def _table_subquery(self, layout_id: str, filtering: TabularLayoutFilter):
        cells_json_agg = func.json_agg(
            func.json_build_object(*(chain(*((col.name, col) for col in self.cell_columns)))),
        ).label("cells")

        subquery = (
            select(*self.table_columns, cells_json_agg)
            .select_from(
                self._table_schema.outerjoin(
                    self._cell_schema,
                    self._table_schema.c.id == self._cell_schema.c.table_id,
                ),
            )
            .where(self._cell_schema.c.tabular_layout_id == layout_id)
            .group_by(self._table_schema.c.id)
        )
        return self._apply_filtering(subquery, filtering)

    def _apply_filtering(
        self,
        query: Select,
        filtering: TabularLayoutFilter,
    ) -> Select:
        if tables := filtering.tables:
            query = query.where(self._table_schema.c.id.in_([tables] if isinstance(tables, str) else tables))
        if row_span := filtering.row_span:
            query = query.where(self._cell_schema.c.relative_position_row.between(*row_span))
        if col_span := filtering.col_span:
            query = query.where(self._cell_schema.c.relative_position_column.between(*col_span))

        return query
