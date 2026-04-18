from deps_tabular_layout.models import Point

__all__ = ["PointMapper"]


class PointMapper:
    @staticmethod
    def to_dict(point: Point) -> dict[str, int]:
        return {
            "x": point.x,
            "y": point.y,
        }

    @staticmethod
    def from_raw(raw_data: dict[str, int]) -> Point:
        return Point(
            x=raw_data["x"],
            y=raw_data["y"],
        )
