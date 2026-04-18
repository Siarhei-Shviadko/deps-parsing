from typing import cast

from deps_document_layout.model import DocumentLayout, PageBuilder, ParsingType

from deps_parsing.infrastructure import UnifiedDataImage

from .key_value import KeyValuePairsParser
from .paragraph import ParagraphsParser
from .structured_response import StructuredResponse
from .table import TablesParser
from .types import DocAIDocument, DocAIPage

__all__ = ["DocumentAIResponseParser"]


class DocumentAIResponseParser:
    parsing_type = ParsingType.GCP_VISION

    def __init__(self, parsed_document: DocAIDocument, parsed_page: DocAIPage, image: UnifiedDataImage) -> None:
        self.response = StructuredResponse(parsed_document, parsed_page, image)

    def add_page_to(self, document_layout: DocumentLayout) -> DocumentLayout:
        page_builder = self._build_empty_page(document_layout)

        page_builder = self._parse_paragraphs(page_builder)
        page_builder = self._parse_tables(page_builder)
        page_builder = self._parse_key_value_pairs(page_builder)

        page_builder.build()

        return document_layout

    def _build_empty_page(self, document_layout: DocumentLayout) -> PageBuilder:
        builder = (
            document_layout.add_page()
            .with_id(self.response.source_id)
            .with_parsing_type(self.parsing_type)
            .with_page_number(self.response.page_number)
            .with_dimension(
                width=int(self.response.page.dimension.width),
                height=int(self.response.page.dimension.height),
                unit=self.response.page.dimension.unit,
            )
            .with_file_path(self.response.file_path)
            .with_transformations()
            .with_angle(self.response.page_angle)
        )

        for language in self.response.page.detected_languages:
            builder = builder.with_language(language.language_code, language.confidence)

        return builder

    def _parse_paragraphs(self, builder: PageBuilder) -> PageBuilder:
        builder = ParagraphsParser(self.response).add_paragraphs_to(builder)

        return cast(PageBuilder, builder)

    def _parse_tables(self, builder: PageBuilder) -> PageBuilder:
        builder = TablesParser(self.response).add_tables_to(builder)

        return cast(PageBuilder, builder)

    def _parse_key_value_pairs(self, builder: PageBuilder) -> PageBuilder:
        builder = KeyValuePairsParser(self.response).add_key_value_pairs_to(builder)

        return cast(PageBuilder, builder)
