from typing import cast

from deps_document_layout.model import PageBuilder

from .base_page_element import PageElementParser
from .generic_text import GenericTextDataParser
from .line import LineDataParser
from .signature import SignatureDataParser
from .types import AWSLine, AWSParagraph, AWSSignature

__all__ = ["ParagraphDataParser"]

elements_parser_map = {
    AWSSignature: SignatureDataParser,
    AWSLine: LineDataParser,
}


class ParagraphDataParser(PageElementParser):
    def add_paragraph(self, builder: PageBuilder, paragraph: AWSParagraph) -> PageBuilder:
        if paragraph.is_empty:
            return builder

        builder = (
            builder.with_paragraph()
            .with_confidence(paragraph.confidence)
            .with_content(paragraph.content)
            .with_polygon(paragraph.polygon)
        )

        for child in paragraph.children:
            parser = elements_parser_map.get(type(child), GenericTextDataParser)
            builder = parser(self._response).add_element(builder, child)

        return cast(PageBuilder, builder)
