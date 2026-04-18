from typing import cast

from deps_document_layout.model import PageBuilder
from docx.text.paragraph import Paragraph as DocxParagraph

from .base_element import DOCXElementParser

__all__ = ["DOCXParagraphParser"]


class DOCXParagraphParser(DOCXElementParser):
    def add_paragraph(self, builder: PageBuilder, paragraph: DocxParagraph) -> PageBuilder:
        builder = self._add_paragraph_and_line(
            builder=builder.with_paragraph(),
            content=paragraph.text.strip(),
        )

        words = [word for word in paragraph.runs if word.text.strip()]

        for word_data in words:
            builder = self._add_word_to_line(builder, word_data)

        return cast(PageBuilder, builder)
