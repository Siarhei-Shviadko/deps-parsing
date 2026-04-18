from typing import Optional

import openpyxl as xl
from deps_tabular_layout.models import PositionInput, TableBuilder

__all__ = ["PositionMapper"]

MergedCellSize = tuple[int, int]


class PositionMapper:
    @staticmethod
    def from_excel(
        cell: xl.cell.cell.Cell,
        sheet: xl.worksheet.worksheet.Worksheet,
        table_builder: TableBuilder,
    ) -> PositionInput:
        return PositionInput(
            absolute_position=(cell.column - 1, cell.row - 1),
            relative_position=_calculate_relative_position(cell, table_builder),
            merge=_merged_info(cell, sheet),
        )


def _calculate_relative_position(
    cell: xl.cell.cell.Cell,
    table: TableBuilder,
) -> tuple[int, int]:
    return cell.column - table.min_column - 1, cell.row - table.min_row - 1


def _merged_info(cell: xl.cell.cell.Cell, sheet: xl.worksheet.worksheet.Worksheet) -> Optional[MergedCellSize]:
    """Calculates the rowsSpan and columnsSpan of a cell if it is merged. Basically a size of the merged cell."""

    if cell.coordinate not in sheet.merged_cells:
        return None

    merged_cell_info = next(
        filter(
            lambda merged_cells_range: cell.coordinate in merged_cells_range,
            sheet.merged_cells,
        ),
    )

    merged_cell_size: dict[str, int] = merged_cell_info.size

    return merged_cell_size["columns"], merged_cell_size["rows"]
