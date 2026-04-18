from typing import cast

from deps_document_layout.model import PageBuilder, ParagraphBuilder

from .base_page_element import PageElementParser
from .types import AWSLine

__all__ = ["LineDataParser"]


class LineDataParser(PageElementParser):
    def add_element(self, builder: ParagraphBuilder, line: AWSLine) -> PageBuilder:
        builder = (
            builder.with_line()
            .with_confidence(line.confidence)
            .with_content(line.text)
            .with_polygon(self._response.polygon_of(line))
        )

        for word in line.get_words_by_type():
            builder = self._add_word_to_line(builder, word)

        return cast(PageBuilder, builder)
