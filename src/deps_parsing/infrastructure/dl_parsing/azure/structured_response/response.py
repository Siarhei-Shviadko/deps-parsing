from functools import cached_property
from typing import Optional

from azure.ai.formrecognizer import (
    AnalyzeResult,
    DocumentLanguage,
    DocumentStyle,
    DocumentWord,
)

from ....exceptions import PageCountMismatchError
from ....proxies import UnifiedDataImage
from ..spans import SpansOf
from .page import StructuredPage

__all__ = ["StructuredResponse"]

FIRST_ELEMENT: int = 0


class StructuredResponse:
    def __init__(
        self,
        parsed_result: AnalyzeResult,
        images: list[UnifiedDataImage],
    ) -> None:
        self._parsed_result = parsed_result

        if (pages_len := len(parsed_result.pages)) != (images_len := len(images)):
            raise PageCountMismatchError(
                f"Mismatch between parsed pages and provided images:  {pages_len} != {images_len}",
            )

        self._initialize_pages(images)

    @property
    def pages(self) -> list[StructuredPage]:
        return list(self._pages.values())

    @cached_property
    def languages(self) -> list[DocumentLanguage]:
        return [] if self._parsed_result.languages is None else self._parsed_result.languages

    @cached_property
    def start_page(self) -> int:
        return min((page.page_number for page in self.pages))

    def style_of(self, word: DocumentWord) -> Optional[DocumentStyle]:
        for style in self._parsed_result.styles:
            if SpansOf(style).include(SpansOf(word)):
                return style

    def _initialize_pages(self, images: list[UnifiedDataImage]) -> None:
        self._pages: dict[int, StructuredPage] = {}

        self._initialize_structured_pages(images)
        self._initialize_parsed_pages()
        self._initialize_paragraphs()
        self._initialize_key_value_pairs()
        self._initialize_tables()

    def _initialize_structured_pages(self, images: list[UnifiedDataImage]) -> None:
        for image in images:
            self._pages[image.page] = StructuredPage(
                source_id=image.id,
                page_number=image.page,
                file_path=image.blob_name,
                languages=self.languages,
            )

    def _initialize_parsed_pages(self) -> None:
        for page in self._parsed_result.pages:
            page_container = self._get_page_container_number(page.page_number)
            self._pages[page_container].add_parsed_page(page)

    def _initialize_tables(self) -> None:
        for table in self._parsed_result.tables or []:
            page_container = self._get_page_container_number(table.bounding_regions[0].page_number)
            self._pages[page_container].add_table(table)

    def _initialize_paragraphs(self) -> None:
        for paragraph in self._parsed_result.paragraphs or []:
            page_container = self._get_page_container_number(paragraph.bounding_regions[0].page_number)
            self._pages[page_container].add_paragraph(paragraph)

    def _initialize_key_value_pairs(self) -> None:
        for kvp in self._parsed_result.key_value_pairs or []:
            page_container = self._get_page_container_number(kvp.key.bounding_regions[0].page_number)
            self._pages[page_container].add_key_value_pair(kvp)

    def _get_page_container_number(self, page_number: int) -> int:
        """
        Maps a given page number from AzureResult (which starts at 1)
        to the corresponding original page number in UnifiedDataImage.
        """
        return page_number + self.start_page - 1
