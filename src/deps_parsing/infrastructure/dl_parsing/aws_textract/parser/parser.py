from typing import Optional

from deps_document_layout.model import DocumentLayout, PageBuilder

from deps_parsing.infrastructure import UnifiedDataImage

from ...image_processing import ParsedImage
from .image import ImageDataParser
from .key_value import KeyValuePairDataParser
from .page import PageDataParser
from .paragraph import ParagraphDataParser
from .structured_response import StructuredResponse
from .table import TableDataParser
from .types import AWSPage

__all__ = ["AwsTextractParser"]


class AwsTextractParser:
    def __init__(
        self,
        aws_page: AWSPage,
        image: UnifiedDataImage,
        parsed_page_images: list[ParsedImage],
        language: Optional[str] = None,
    ) -> None:
        self._response = StructuredResponse(
            image=image,
            aws_page=aws_page,
            language=language,
            parsed_page_images=parsed_page_images,
        )

    def add_page_to(self, document_layout: DocumentLayout) -> DocumentLayout:
        builder = self._add_page(document_layout)
        builder = self._add_tables(builder)
        builder = self._add_key_value_pairs(builder)
        builder = self._add_paragraphs(builder)
        builder = self._add_checkboxes(builder)
        builder = self._add_images(builder)
        builder.build()
        return document_layout

    def _add_page(self, document_layout: DocumentLayout) -> PageBuilder:
        return PageDataParser(self._response).add_page_data(document_layout)

    def _add_images(self, builder: PageBuilder) -> PageBuilder:
        for image in self._response.images:
            builder = ImageDataParser(self._response).add_image(builder, image)
        return builder

    def _add_tables(self, builder: PageBuilder) -> PageBuilder:
        for table in self._response.tables:
            builder = TableDataParser(self._response).add_table_data(builder, table)
        return builder

    def _add_key_value_pairs(self, builder: PageBuilder) -> PageBuilder:
        for kvp in self._response.key_value_pairs:
            builder = KeyValuePairDataParser(self._response).add_key_value_pair(builder, kvp)
        return builder

    def _add_paragraphs(self, builder: PageBuilder) -> PageBuilder:
        for paragraph in self._response.paragraphs:
            builder = ParagraphDataParser(self._response).add_paragraph(builder, paragraph)
        return builder

    def _add_checkboxes(self, builder: PageBuilder) -> PageBuilder:
        for checkbox in self._response.checkboxes:
            builder = KeyValuePairDataParser(self._response).add_key_value_pair(builder, checkbox)
        return builder
