from collections.abc import Sequence

from deps_document_layout.model import PageBuilder, ParagraphBuilder

from .base_page_element import PageElementParser
from .generic_text import GenericTextDataParser
from .line import LineDataParser
from .signature import SignatureDataParser
from .types import AWSLayout, AWSLine, AWSParagraph, AWSSignature, ChildType

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

        return self._add_children(builder, paragraph.children)

    def _add_children(self, builder: ParagraphBuilder, children: Sequence[ChildType]) -> ParagraphBuilder:
        for child in children:
            if isinstance(child, AWSLayout):
                builder = self._add_children(builder, child.children)
            else:
                parser = elements_parser_map.get(type(child), GenericTextDataParser)
                builder = parser(self._response).add_element(builder, child)
        return builder
