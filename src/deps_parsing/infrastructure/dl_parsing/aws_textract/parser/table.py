from typing import Union, cast

from deps_document_layout.model import CellBuilder, PageBuilder, TableBuilder

from .base_page_element import PageElementParser
from .structured_response import StructuredResponse
from .types import AWSCell, AWSTable

__all__ = ["TableCellDataParser", "TableDataParser"]


class TableDataParser:
    def __init__(self, response: StructuredResponse):
        self._response = response

    def add_table_data(self, builder: Union[PageBuilder, TableBuilder, CellBuilder], table: AWSTable) -> PageBuilder:
        builder = self._add_table_geometry(builder.with_table(), table)
        builder = self._add_cells(table, builder)
        return cast(PageBuilder, builder)

    def _add_table_geometry(self, builder: TableBuilder, table: AWSTable) -> TableBuilder:
        return (
            builder.with_column_count(table.column_count)
            .with_row_count(table.row_count)
            .with_polygon(self._response.polygon_of(table))
        )

    def _add_cells(self, table: AWSTable, builder: TableBuilder) -> TableBuilder:
        for cell in table.table_cells:
            builder = TableCellDataParser(self._response).add_cell(builder, cell)
        return builder


class TableCellDataParser(PageElementParser):
    def add_cell(self, builder: Union[TableBuilder, CellBuilder], cell: AWSCell) -> TableBuilder:
        builder = self._add_cell_geometry(builder.with_cell(), cell)

        builder = self._add_paragraph_and_line(
            builder.with_paragraph_content(),
            polygon=self._response.polygon_of(cell),
            confidence=cell.confidence,
            content=cell.text,
        )

        for checkbox_or_word in cell.children:
            builder = self._add_word_or_checkbox(builder, checkbox_or_word)
        return cast(TableBuilder, builder)

    @staticmethod
    def _add_cell_geometry(builder: CellBuilder, cell: AWSCell) -> CellBuilder:
        return (
            builder.with_column_index(cell.col_index - 1)
            .with_column_span(cell.col_span)
            .with_row_index(cell.row_index - 1)
            .with_row_span(cell.row_span)
        )
