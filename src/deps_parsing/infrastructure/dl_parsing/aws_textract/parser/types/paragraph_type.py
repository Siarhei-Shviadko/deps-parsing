from typing import Union

from deps_document_layout.model import Point, Polygon
from textractor.entities.layout import Layout
from textractor.entities.line import Line
from textractor.entities.signature import Signature

__all__ = ["AWSParagraph"]

ChildType = Union[Line, Signature]


class AWSParagraph:
    LAYOUT_TYPES = {
        "LAYOUT_TEXT",
        "LAYOUT_TITLE",
        "LAYOUT_HEADER",
        "LAYOUT_FOOTER",
        "LAYOUT_SECTION_HEADER",
        "LAYOUT_ENTITY",
        "LAYOUT_TABLE",
        "LAYOUT_LIST",
        "LAYOUT_LIST_ITEM",
        "LAYOUT_PAGE_NUMBER",
        "LAYOUT_KEY_VALUE",
    }

    def __init__(self, layout: Layout) -> None:
        if layout.layout_type not in self.LAYOUT_TYPES:
            raise ValueError(f"Invalid layout type: {layout.layout_type}. Expected one of {self.LAYOUT_TYPES}.")

        self._layout = layout

    @classmethod
    def layout_is_applicable(cls, layout: Layout) -> bool:
        return layout.layout_type in cls.LAYOUT_TYPES

    @property
    def content(self) -> str:
        return self._layout.text

    @property
    def is_empty(self) -> bool:
        return not self.content.strip()

    @property
    def children(self) -> list[ChildType]:
        return self._layout.children

    @property
    def confidence(self) -> float:
        return self._layout.confidence

    @property
    def layout_object(self) -> Layout:
        return self._layout

    @property
    def polygon(self) -> Polygon:
        bbox = self._layout.bbox
        x, y, w, h = bbox.x, bbox.y, bbox.width, bbox.height

        right_x, bottom_y = min(x + w, 1.0), min(y + h, 1.0)

        return (
            Point(x, y),
            Point(right_x, y),
            Point(right_x, bottom_y),
            Point(x, bottom_y),
        )
