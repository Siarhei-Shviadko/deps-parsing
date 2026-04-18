from typing import Union, cast

from deps_document_layout.model import CellBuilder, PageBuilder, TableBuilder
from docx.oxml.table import CT_Tc as DocxCellElement
from docx.table import Table as DocxTable
from docx.table import _Cell as DocxCell

from .base_element import DOCXElementParser

__all__ = ["DOCXTableCellParser", "DOCXTableParser"]


class DOCXTableParser(DOCXElementParser):
    def add_table(self, builder: Union[PageBuilder, TableBuilder, CellBuilder], table: DocxTable) -> PageBuilder:
        builder = (
            builder.with_table()
            .with_column_count(len(table.columns))
            .with_row_count(len(table.rows))
            .with_polygon(self.POLYGON)
        )
        builder = self._add_cells(table, builder)

        return cast(PageBuilder, builder)

    def _add_cells(self, table: DocxTable, builder: TableBuilder) -> TableBuilder:
        merged_cells: set[DocxCellElement] = set()

        for row_index, row in enumerate(table.rows):
            for column_index, cell in enumerate(row.cells):
                if self._is_cell_merged(cell, merged_cells):
                    continue

                merged_cells.add(cell._tc)

                builder = DOCXTableCellParser().add_cell(builder, cell, row_index, column_index)

        return builder

    @staticmethod
    def _is_cell_merged(cell: DocxCell, merged_cells: set[DocxCellElement]) -> bool:
        return (cell._tc.vMerge or cell._tc.grid_span != 1) and cell._tc in merged_cells


class DOCXTableCellParser(DOCXElementParser):
    def add_cell(
        self,
        builder: Union[TableBuilder, CellBuilder],
        cell: DocxCell,
        row_index: int,
        column_index: int,
    ) -> TableBuilder:
        builder = (
            builder.with_cell()
            .with_column_index(column_index)
            .with_column_span(cell._tc.right - cell._tc.left)
            .with_row_index(row_index)
            .with_row_span(cell._tc.bottom - cell._tc.top)
        )
        builder = self._add_paragraph_and_line(
            builder=builder.with_paragraph_content(),
            content=cell.text.strip(),
        )

        return cast(TableBuilder, builder)
