from deps_tabular_layout.models import Point

from .point import PointMapper

__all__ = ["PlacementMapper"]

Placement = tuple[Point, Point]
RawPlacement = tuple[dict[str, int], dict[str, int]]


class PlacementMapper:
    @staticmethod
    def to_dict(placement: Placement) -> RawPlacement:
        return (
            PointMapper.to_dict(placement[0]),
            PointMapper.to_dict(placement[1]),
        )

    @staticmethod
    def from_raw(raw_data: RawPlacement) -> Placement:
        return (
            PointMapper.from_raw(raw_data[0]),
            PointMapper.from_raw(raw_data[1]),
        )
