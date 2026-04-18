from typing import Generator, Sequence

from deps_document_layout.model import Point, Polygon

from deps_parsing.infrastructure.proxies import UnifiedDataImage

from .text_spans import TextSpans
from .types import (
    DocAIDocument,
    DocAIKeyValuePair,
    DocAILayout,
    DocAILine,
    DocAIPage,
    DocAIParagraph,
    DocAITable,
    DocAIWord,
)

__all__ = ["StructuredResponse"]

FIRST_ELEMENT: int = 0

_orientation_to_angle = {
    DocAIDocument.Page.Layout.Orientation.ORIENTATION_UNSPECIFIED: 0.0,
    DocAIDocument.Page.Layout.Orientation.PAGE_UP: 0.0,
    DocAIDocument.Page.Layout.Orientation.PAGE_RIGHT: 90.0,
    DocAIDocument.Page.Layout.Orientation.PAGE_DOWN: 180.0,
    DocAIDocument.Page.Layout.Orientation.PAGE_LEFT: 270.0,
}


class StructuredResponse:
    def __init__(self, response: DocAIDocument, page: DocAIPage, image: UnifiedDataImage) -> None:
        self._response = response
        self._page = page
        self._image = image

    @property
    def has_page_recognition(self) -> bool:
        return bool(self._response.pages)

    @property
    def page(self) -> DocAIDocument.Page:
        return self._page

    @property
    def source_id(self) -> str:
        return self._image.id

    @property
    def page_number(self) -> int:
        return self._image.page

    @property
    def file_path(self) -> str:
        return self._image.blob_name

    @property
    def paragraphs(self) -> Sequence[DocAIParagraph]:
        return self.page.paragraphs

    @property
    def key_value_pairs(self) -> Sequence[DocAIKeyValuePair]:
        original_kvps: Sequence[DocAIKeyValuePair] = self.page.form_fields

        # we have to sort key-value-pairs by their y coordinate to ensure that they are processed in the correct order
        return sorted(
            original_kvps,
            key=lambda kvp: (
                kvp.field_name.bounding_poly.normalized_vertices[FIRST_ELEMENT].y,
                kvp.field_name.bounding_poly.normalized_vertices[FIRST_ELEMENT].x,
            ),
        )

    @property
    def tables(self) -> Sequence[DocAITable]:
        original_tables: Sequence[DocAITable] = self.page.tables

        # we have to sort tables by their y coordinate to ensure that they are processed in the correct order
        return sorted(
            original_tables,
            key=lambda table: table.layout.bounding_poly.normalized_vertices[FIRST_ELEMENT].y,
        )

    @property
    def page_angle(self) -> float:
        first_paragraph = self.page.paragraphs[FIRST_ELEMENT]

        return _orientation_to_angle.get(first_paragraph.layout.orientation, 0.0)

    def get_polygon_of(self, layout: DocAILayout) -> Polygon:
        return tuple([Point(point.x, point.y) for point in layout.bounding_poly.normalized_vertices])

    def get_text_of(self, layout: DocAILayout) -> str:
        return "\n".join(
            [
                self._response.text[text_bounding.start_index : text_bounding.end_index]
                for text_bounding in layout.text_anchor.text_segments
            ],
        )

    def get_lines_of(self, paragraph: DocAIParagraph) -> Generator[DocAILine, None, None]:
        paragraph_spans = TextSpans.for_layout(paragraph.layout)

        for line in self.page.lines:
            if paragraph_spans.lies_below(line.layout):
                continue
            if paragraph_spans.includes(line.layout):
                yield line
                continue

            break

    def get_words_of(self, line: DocAILine) -> Generator[DocAIWord, None, None]:
        line_spans = TextSpans.for_layout(line.layout)

        for word in self.page.tokens:
            if line_spans.lies_below(word.layout):
                continue
            if line_spans.includes(word.layout):
                yield word
                continue

            break
