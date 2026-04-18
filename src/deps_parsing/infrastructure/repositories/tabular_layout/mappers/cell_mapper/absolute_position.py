from typing import Any

from deps_tabular_layout.models import Point

__all__ = ["AbsolutePositionMapper"]


class AbsolutePositionMapper:
    @staticmethod
    def from_raw(raw_cell: dict[str, Any]) -> Point:
        return Point(
            x=raw_cell["absolute_position_column"],
            y=raw_cell["absolute_position_row"],
        )
