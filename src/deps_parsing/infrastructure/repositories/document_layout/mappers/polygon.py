from deps_document_layout.model import Point, Polygon

__all__ = ["PointMapper", "PolygonMapper"]


class PolygonMapper:
    @classmethod
    def to_dict(cls, polygon: Polygon) -> list[dict[str, float]]:
        return [PointMapper.to_dict(point) for point in polygon]

    @classmethod
    def from_dict(cls, polygon: list[dict[str, float]]) -> Polygon:
        return tuple(PointMapper.from_dict(point) for point in polygon)


class PointMapper:
    @classmethod
    def to_dict(cls, point: Point) -> dict[str, float]:
        return {
            "x": point.x,
            "y": point.y,
        }

    @classmethod
    def from_dict(cls, point: dict[str, float]) -> Point:
        return Point(x=point["x"], y=point["y"])
