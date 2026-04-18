from typing import Any

from deps_document_layout.model import BaseLineElement, RawBaseLineElement

from .polygon import PolygonMapper

__all__ = ["BaseLineElementMapper"]


class BaseLineElementMapper:
    @classmethod
    def to_dict(cls, element: BaseLineElement) -> RawBaseLineElement:
        return {
            "order": element.order,
            "confidence": element.confidence,
            "polygon": PolygonMapper.to_dict(element.polygon),
        }

    @classmethod
    def from_dict(cls, element: RawBaseLineElement) -> dict[str, Any]:
        return {
            "order": element["order"],
            "confidence": element["confidence"],
            "polygon": PolygonMapper.from_dict(element["polygon"]),
        }
