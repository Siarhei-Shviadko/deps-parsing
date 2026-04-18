from deps_document_layout.model import LineBuilder, ParagraphBuilder

from ..structured_response import StructuredResponse
from ..types import DocAILine, DocAIParagraph
from .words import WordParser

__all__ = ["LineParser"]


class LineParser:
    def __init__(self, response: StructuredResponse) -> None:
        self._response = response

    def add_lines_to(self, paragraph: DocAIParagraph, builder: ParagraphBuilder) -> LineBuilder:
        for line in self._response.get_lines_of(paragraph):
            builder = (
                builder.with_line()
                .with_content(self._response.get_text_of(line.layout))
                .with_confidence(line.layout.confidence)
                .with_polygon(self._response.get_polygon_of(line.layout))
            )

            builder = self._add_words_for(line, builder)

        return builder

    def _add_words_for(self, line: DocAILine, builder: LineBuilder) -> LineBuilder:
        return WordParser(self._response).add_words_to(line, builder)
