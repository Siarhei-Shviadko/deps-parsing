from dataclasses import dataclass

from deps_tabular_layout.models import Cell, Point

__all__ = ["TableProjection", "TableSchemaProjection"]


@dataclass
class TableSchemaProjection:
    id: str
    sheet_id: str
    column_count: int
    row_count: int
    placement: tuple[Point, Point]


@dataclass
class TableProjection:
    schema: TableSchemaProjection
    data: list[Cell]
