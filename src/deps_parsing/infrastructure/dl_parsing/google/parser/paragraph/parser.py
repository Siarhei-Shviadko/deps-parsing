from deps_document_layout.model import LineBuilder, PageBuilder, ParagraphBuilder

from ..structured_response import StructuredResponse
from ..types import DocAIParagraph
from .lines import LineParser

__all__ = ["ParagraphsParser"]


class ParagraphsParser:
    def __init__(self, response: StructuredResponse) -> None:
        self._response = response

    def add_paragraphs_to(self, builder: PageBuilder) -> LineBuilder:
        for paragraph in self._response.paragraphs:
            builder = (
                builder.with_paragraph()
                .with_content(self._response.get_text_of(paragraph.layout))
                .with_confidence(paragraph.layout.confidence)
                .with_polygon(self._response.get_polygon_of(paragraph.layout))
            )

            builder = self._add_lines_for(paragraph, builder)

        return builder

    def _add_lines_for(
        self,
        paragraph: DocAIParagraph,
        builder: ParagraphBuilder,
    ) -> LineBuilder:
        return LineParser(self._response).add_lines_to(paragraph, builder)
