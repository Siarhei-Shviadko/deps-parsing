from dataclasses import dataclass

__all__ = ["TableReference", "Point"]


@dataclass
class Point:
    row: int
    column: int


@dataclass
class TableReference:
    """
    Represents a table reference with top-left and bottom-right points.
    Indexing starts from 0 ( 0,0 - top left corner of the sheet )
    """

    placement: tuple[Point, Point]

    @property
    def top_left(self) -> tuple[int, int]:
        return self.placement[0].column, self.placement[0].row

    @property
    def bottom_right(self) -> tuple[int, int]:
        return self.placement[1].column, self.placement[1].row

    @property
    def min_row(self) -> int:
        return self.top_left[1]

    @property
    def max_row(self) -> int:
        return self.bottom_right[1]

    @property
    def min_column(self) -> int:
        return self.top_left[0]

    @property
    def max_column(self) -> int:
        return self.bottom_right[0]
