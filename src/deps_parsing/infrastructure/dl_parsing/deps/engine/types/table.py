from dataclasses import dataclass
from typing import Optional

__all__ = ["Table", "Cell", "Row", "Column", "CellCoordinates"]

from .bbox import Bbox
from .source_bbox import SourceBboxCoordinates


@dataclass(frozen=True)
class CellCoordinates:
    column: int
    row: int
    colspan: int
    rowspan: int
    page: int


@dataclass(frozen=True)
class Cell:
    value: Optional[str]
    coordinates: CellCoordinates
    confidence: float
    source_bbox_coordinates: list[SourceBboxCoordinates]

    @classmethod
    def from_dict(cls, **kwargs) -> "Cell":
        source_bbox_coordinates = [
            SourceBboxCoordinates.from_dict(**coord) for coord in kwargs.pop("sourceBboxCoordinates")
        ]
        return cls(
            value=kwargs["value"] if kwargs.get("value") else "",
            coordinates=CellCoordinates(**kwargs["coordinates"]),
            confidence=kwargs["confidence"],
            source_bbox_coordinates=source_bbox_coordinates,
        )


@dataclass(frozen=True)
class Row:
    y: float


@dataclass(frozen=True)
class Column:
    y: float


@dataclass(frozen=True)
class Table:
    columns: list[Column]
    rows: list[Row]
    cells: list[Cell]
    coordinates: Bbox
    source_bbox_coordinates: Optional[SourceBboxCoordinates]

    @classmethod
    def from_dict(cls, **kwargs) -> "Table":
        return cls(
            columns=[Column(col) for col in kwargs["columns"]],
            rows=[Row(row) for row in kwargs["rows"]],
            cells=[Cell.from_dict(**cell) for cell in kwargs["cells"]],
            coordinates=(
                Bbox(
                    x=kwargs["coordinates"]["x"],
                    y=kwargs["coordinates"]["y"],
                    w=kwargs["coordinates"]["w"],
                    h=kwargs["coordinates"]["h"],
                )
                if kwargs.get("coordinates")
                else None
            ),
            source_bbox_coordinates=SourceBboxCoordinates.from_dict(**kwargs["sourceBboxCoordinates"])
            if kwargs.get("sourceBboxCoordinates")
            else None,
        )
