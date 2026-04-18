from deps_document_layout.model import Cell, Page

from ..markers import SimilarityMarkers
from .abstract_marker import AbstractMarker

__all__ = ["ColumnsAlignmentMarker"]


class ColumnsAlignmentMarker(AbstractMarker):
    """
    This Marker checks column alignment coordinates and widths.
    Algorithm uses last row of first table and first row of next table and check that `x` lines are less than THRESHOLD.
    """

    type = SimilarityMarkers.COLUMNS_ALIGNMENT

    _ALIGNMENT_THRESHOLD = 1

    def is_present(self, first_page: Page, second_page: Page) -> bool:
        first_page_table = self.last_table_of_page(first_page)
        second_page_table = self.first_table_of_page(second_page)

        last_tab_cells: list[Cell] = [
            cell
            for cell in first_page_table.cells
            if cell.row_index == first_page_table.row_count - 1 and cell.row_span == 1
        ]
        first_tab_cells: list[Cell] = [cell for cell in second_page_table.cells if cell.row_index == 0]

        return not any(
            abs(last_coord_cell.x - first_coord_cell.x) > self._ALIGNMENT_THRESHOLD
            for last_table_cell, first_table_cell in zip(last_tab_cells, first_tab_cells)
            for last_coord_cell, first_coord_cell in zip(last_table_cell.polygon, first_table_cell.polygon)
        )
