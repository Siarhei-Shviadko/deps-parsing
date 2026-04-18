from typing import Any, Optional

from deps_document_layout.model import Point, Polygon

from deps_parsing.infrastructure import UnifiedDataImage

from ...image_processing import ParsedImage
from .types import (
    AWSKeyValuePair,
    AWSLayout,
    AWSPage,
    AWSParagraph,
    AWSSignature,
    AWSTable,
    HasLayouts,
)

__all__ = ["StructuredResponse"]


class StructuredResponse:
    def __init__(
        self,
        image: UnifiedDataImage,
        aws_page: AWSPage,
        parsed_page_images: list[ParsedImage],
        language: Optional[str] = None,
    ) -> None:
        self._image = image
        self._aws_page = aws_page
        self._parsed_images = parsed_page_images
        self.language = language

    @property
    def page(self) -> AWSPage:
        return self._aws_page

    @property
    def page_id(self) -> str:
        return self._image.id

    @property
    def page_width(self) -> int:
        return self._image.width

    @property
    def page_height(self) -> int:
        return self._image.height

    @property
    def page_number(self) -> int:
        return self._image.page

    @property
    def file_path(self) -> str:
        return self._image.blob_name

    @property
    def tables(self) -> list[AWSTable]:
        return self.page.tables

    @property
    def key_value_pairs(self) -> list[AWSKeyValuePair]:
        return self.page.key_values

    @property
    def paragraphs(self) -> list[AWSParagraph]:
        return [AWSParagraph(layout) for layout in self.page.layouts if AWSParagraph.layout_is_applicable(layout)]

    @property
    def checkboxes(self) -> list[AWSKeyValuePair]:
        return self.page.checkboxes

    @property
    def signatures(self) -> list[AWSSignature]:
        return self.page.signatures

    @property
    def images(self) -> list[ParsedImage]:
        return self._parsed_images

    @staticmethod
    def polygon_of(aws_object: Any) -> Polygon:
        return (*(Point(x=p["X"], y=p["Y"]) for p in aws_object.raw_object["Geometry"]["Polygon"]),)  # noqa: WPS356

    @staticmethod
    def list_layout_by_type(
        parsed_page: HasLayouts,
        layout_type: str,
        page_number: int | None = None,
    ) -> list[AWSLayout]:
        return [
            layout
            for layout in parsed_page.layouts
            if layout.layout_type == layout_type and (page_number is None or layout.page == page_number)
        ]
