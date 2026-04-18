from typing import cast

from deps_document_layout.model import PageBuilder, TableBuilder

from .structured_response import StructuredResponse
from .types import DocAIRow, DocAITable

__all__ = ["TablesParser"]


class TablesParser:
    def __init__(self, response: StructuredResponse) -> None:
        self._response = response

    def add_tables_to(self, builder: PageBuilder) -> PageBuilder:
        for table in self._response.tables:
            # for some reason google can return empty table
            if not table.body_rows and not table.header_rows:
                continue

            builder = (
                builder.with_table()
                .with_confidence(table.layout.confidence)
                .with_polygon(self._response.get_polygon_of(table.layout))
                .with_row_count(len(table.body_rows) + len(table.header_rows))
                .with_column_count(self._count_table_columns(table))
            )

            builder = self._add_table_cells(table, builder)

        return builder

    def _add_table_cells(self, table: DocAITable, builder: TableBuilder) -> PageBuilder:
        row_idx = 0

        for row in table.header_rows:
            builder = self._add_row_cells(row_idx, row, builder)
            row_idx += 1
        for row in table.body_rows[: len(table.body_rows) - 1]:
            builder = self._add_row_cells(row_idx, row, builder)
            row_idx += 1

        return cast(PageBuilder, builder)

    def _add_row_cells(self, row_idx: int, row: DocAIRow, builder: TableBuilder) -> TableBuilder:
        for column_idx, cell in enumerate(row.cells):
            builder = (
                builder.with_cell()
                .with_row_index(row_idx)
                .with_row_span(cell.row_span)
                .with_column_index(column_idx)
                .with_column_span(cell.col_span)
                .with_paragraph_content()
                .with_confidence(cell.layout.confidence)
                .with_polygon(self._response.get_polygon_of(cell.layout))
                .with_content(self._response.get_text_of(cell.layout))
                .with_line()
                .with_confidence(cell.layout.confidence)
                .with_polygon(self._response.get_polygon_of(cell.layout))
                .with_content(self._response.get_text_of(cell.layout))
            )

        return builder

    def _count_table_columns(self, table: DocAITable) -> int:
        """Going through each of rows to find max number of columns"""
        rows = table.body_rows
        rows.extend(table.header_rows)

        return max(len(row.cells) for row in rows if row.cells)
