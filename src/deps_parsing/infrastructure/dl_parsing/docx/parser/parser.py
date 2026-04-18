from deps_document_layout.model import DocumentLayout, PageBuilder, ParsingType
from docx import Document as DocxDocument

from .paragraph import DOCXParagraphParser
from .table import DOCXTableParser

__all__ = ["DOCXParser"]


class DOCXParser:
    DEFAULT_PAGE = 1
    DEFAULT_ANGLE = 0.0
    DEFAULT_DIMENSION = (1, 1, "")

    def __init__(self, docx_document: DocxDocument) -> None:
        self._docx_document = docx_document

    def add_page_to(self, document_layout: DocumentLayout) -> DocumentLayout:
        builder = self._add_page(document_layout)
        builder = self._add_paragraphs(builder)
        builder = self._add_tables(builder)
        builder.build()

        return document_layout

    def _add_page(self, document_layout: DocumentLayout) -> PageBuilder:
        builder = (
            document_layout.add_page()
            .with_id(document_layout.id())
            .with_page_number(self.DEFAULT_PAGE)
            .with_parsing_type(ParsingType.DOCX)
            .with_dimension(*self.DEFAULT_DIMENSION)
            .with_file_path(document_layout.id())
            .with_transformations()
            .with_angle(self.DEFAULT_ANGLE)
        )

        return builder

    def _add_tables(self, builder: PageBuilder) -> PageBuilder:
        for table in self._docx_document.tables:
            builder = DOCXTableParser().add_table(builder, table)

        return builder

    def _add_paragraphs(self, builder: PageBuilder) -> PageBuilder:
        for paragraph in self._docx_document.paragraphs:
            builder = DOCXParagraphParser().add_paragraph(builder, paragraph)

        return builder
