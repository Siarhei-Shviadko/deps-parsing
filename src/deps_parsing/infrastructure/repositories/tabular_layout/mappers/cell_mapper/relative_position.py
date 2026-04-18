from typing import Any

from deps_tabular_layout.models import Point

__all__ = ["RelativePositionMapper"]


class RelativePositionMapper:
    @staticmethod
    def from_raw(raw_cell: dict[str, Any]) -> Point:
        return Point(
            x=raw_cell["relative_position_column"],
            y=raw_cell["relative_position_row"],
        )
