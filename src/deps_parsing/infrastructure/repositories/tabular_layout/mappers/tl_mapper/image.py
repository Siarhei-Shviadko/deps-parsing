from typing import Any

from deps_tabular_layout.models import EntityId, Image, ImageType, Point

from .point import PointMapper

__all__ = ["ImageMapper"]


class ImageMapper:
    @staticmethod
    def to_dict(image: Image) -> dict[str, Any]:
        return {
            "id": image.id(),
            "file_path": image.file_path,
            "type": image.type,
            "position": PointMapper.to_dict(image.position),
            "title": image.title,
            "description": image.description,
        }

    @staticmethod
    def from_dict(raw_data: dict[str, Any]) -> Image:
        return Image(
            id_=EntityId(raw_data["id"]),
            title=raw_data["title"],
            type_=ImageType(raw_data["type"]),
            description=raw_data["description"],
            file_path=raw_data["file_path"],
            position=Point(**raw_data["position"]),
        )
