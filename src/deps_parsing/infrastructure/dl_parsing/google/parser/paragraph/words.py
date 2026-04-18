from deps_document_layout.model import LineBuilder, WordBuilder

from ..structured_response import StructuredResponse
from ..types import DocAILine

__all__ = ["WordBuilder"]


class WordParser:
    def __init__(self, response: StructuredResponse) -> None:
        self._response = response

    def add_words_to(self, line: DocAILine, builder: LineBuilder) -> LineBuilder:
        for word in self._response.get_words_of(line):
            builder = (
                builder.with_word()
                .with_content(self._response.get_text_of(word.layout))
                .with_polygon(self._response.get_polygon_of(word.layout))
                .with_confidence(word.layout.confidence)
                .with_style()
            )

        return builder
